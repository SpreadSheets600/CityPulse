"""
Image verification using Ollama Gemma 4 Cloud model.

Verifies that uploaded images actually match the described civic issue.
Detects fake/misleading images and flags users accordingly.
"""

import base64
import json
import os
import tempfile
from typing import Dict


_client = None


def _get_client():
    global _client
    if _client is not None:
        return _client

    try:
        import ollama
        base_url = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")
        _client = ollama.Client(host=base_url)
        return _client
    except Exception as e:
        print(f"------ [ ERROR ] ------ Failed to init Ollama client: {e}")
        return None


def _get_model() -> str:
    return os.getenv("OLLAMA_VISION_MODEL", "gemma4:31b-cloud")


def _image_to_base64(image_path: str) -> str:
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def verify_image_matches_issue(
    image_path: str,
    issue_title: str,
    issue_description: str,
    issue_type: str,
) -> Dict:
    """
    Verify that an image actually shows the described civic issue.

    Returns:
        Dict with keys: is_valid, confidence, reasoning, detected_objects, mismatch_flags
    """
    client = _get_client()
    if client is None:
        return {
            "is_valid": True,
            "confidence": 0.0,
            "reasoning": "AI verification unavailable",
            "detected_objects": [],
            "mismatch_flags": [],
        }

    model = _get_model()
    img_b64 = _image_to_base64(image_path)

    prompt = f"""You are a civic issue verification expert. Analyze this image and determine if it actually shows the reported issue.

REPORTED ISSUE:
- Type: {issue_type}
- Title: {issue_title}
- Description: {issue_description}

TASK:
1. What do you actually see in this image? List all visible objects/scenes.
2. Does this image show a {issue_type} issue?
3. Is the image consistent with the title and description?
4. Are there any red flags (e.g., stock photo, unrelated image, manipulated image)?

RESPOND WITH ONLY A JSON OBJECT (no markdown, no explanation):
{{
    "is_valid": true/false,
    "confidence": 0.0-1.0,
    "reasoning": "one line explanation",
    "detected_objects": ["object1", "object2", ...],
    "mismatch_flags": ["flag1", "flag2", ...] or []
}}

EXAMPLES OF MISMATCH FLAGS:
- "Image shows indoor scene, not outdoor infrastructure"
- "No visible road/pavement damage detected"
- "Image appears to be a stock photo"
- "Image quality too low to verify"
- "Image shows different location type than described"
- "No evidence of water leak or damage"
- "Image appears manipulated or edited"
"""

    try:
        response = client.chat(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                    "images": [img_b64],
                }
            ],
            options={"temperature": 0.1},
        )
        text = response["message"]["content"].strip()

        if "```" in text:
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
            text = text.strip()

        result = json.loads(text)

        return {
            "is_valid": bool(result.get("is_valid", True)),
            "confidence": float(result.get("confidence", 0.5)),
            "reasoning": str(result.get("reasoning", "")),
            "detected_objects": list(result.get("detected_objects", [])),
            "mismatch_flags": list(result.get("mismatch_flags", [])),
        }

    except Exception as e:
        print(f"------ [ WARN ] ------ Image verification failed: {e}")
        return {
            "is_valid": True,
            "confidence": 0.0,
            "reasoning": f"Verification error: {str(e)}",
            "detected_objects": [],
            "mismatch_flags": [],
        }


def verify_image_from_bytes(
    image_bytes: bytes,
    filename: str = "image.jpg",
    issue_title: str = "",
    issue_description: str = "",
    issue_type: str = "",
) -> Dict:
    """Verify an image from raw bytes."""
    suffix = os.path.splitext(filename)[1] or ".jpg"
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        tmp.write(image_bytes)
        tmp_path = tmp.name

    try:
        return verify_image_matches_issue(
            tmp_path, issue_title, issue_description, issue_type
        )
    finally:
        os.unlink(tmp_path)


def should_flag_user(verification_result: Dict) -> bool:
    """
    Determine if a user should be flagged based on verification result.

    Flags user if:
    - AI confidence > 0.7 that image doesn't match
    - Multiple mismatch flags detected
    """
    if verification_result["is_valid"]:
        return False

    confidence = verification_result["confidence"]
    mismatch_count = len(verification_result["mismatch_flags"])

    return confidence >= 0.7 or mismatch_count >= 2
