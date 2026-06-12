"""
Image classification using Ollama vision models (moondream / llava / minicpm-v).

Sends images to the local Ollama instance with a vision model.
Asks category-specific questions and parses the response for detection.
"""

import base64
import os
import tempfile
from typing import Dict, Optional

# ── Category Definitions ──────────────────────────────────────────

CATEGORIES = [
    "Road Maintenance",
    "Electricity",
    "Water Supply",
    "Waste Management",
    "Public Transportation",
]

DEPARTMENT_MAP = {c: c for c in CATEGORIES}

# ── Detection prompts per category ────────────────────────────────

DETECT_PROMPTS = {
    "Road Maintenance": (
        "Look at this image. Is there a pothole, cracked road, damaged sidewalk, "
        "broken street light, road debris, or any road/pavement damage? "
        "Answer YES or NO and briefly describe what you see."
    ),
    "Electricity": (
        "Look at this image. Is there a downed power line, broken street lamp, "
        "damaged transformer, exposed wire, fallen utility pole, or any electrical hazard? "
        "Answer YES or NO and briefly describe what you see."
    ),
    "Water Supply": (
        "Look at this image. Is there a water leak, burst pipe, flooding, "
        "broken hydrant, waterlogging, or any water infrastructure damage? "
        "Answer YES or NO and briefly describe what you see."
    ),
    "Waste Management": (
        "Look at this image. Is there a garbage pile, overflowing trash bin, "
        "illegal dumping, scattered litter, or any waste management issue? "
        "Answer YES or NO and briefly describe what you see."
    ),
    "Public Transportation": (
        "Look at this image. Is there a damaged bus stop, broken bus shelter, "
        "damaged metro station, broken ticket machine, or any transit infrastructure damage? "
        "Answer YES or NO and briefly describe what you see."
    ),
}

# ── Lazy-loaded client ───────────────────────────────────────────

_client = None


def _get_client():
    global _client
    if _client is not None:
        return _client

    try:
        import ollama

        base_url = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")
        _client = ollama.Client(host=base_url)
        print(f"------ [ INFO ] ------ Ollama vision client initialized ({base_url})")
        return _client
    except Exception as e:
        print(f"------ [ ERROR ] ------ Failed to init Ollama client: {e}")
        return None


def _get_vision_model() -> str:
    return os.getenv("OLLAMA_VISION_MODEL", "gemma4:31b-cloud")


def _image_to_base64(image_path: str) -> str:
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def _ask_vision_model(image_path: str, prompt: str) -> str:
    """Send an image + prompt to Ollama vision model and return the response text."""
    client = _get_client()
    if client is None:
        return ""

    model = _get_vision_model()
    img_b64 = _image_to_base64(image_path)

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
        return response["message"]["content"].strip()
    except Exception as e:
        print(f"------ [ WARN ] ------ Ollama vision chat failed: {e}")
        return ""


def _parse_yes_no(response: str) -> bool:
    """Check if the model's response indicates a YES detection."""
    upper = response.upper().strip()
    # Check first word or first line
    first_word = upper.split()[0] if upper.split() else ""
    return first_word in ("YES", "YES," "YES.")


def classify_image(
    image_path: str,
    confidence_threshold: Optional[float] = None,
    **kwargs,
) -> Dict:
    """
    Classify an image using Ollama vision model.

    For each category, sends the image with a detection prompt.
    If the model says YES, that category is considered detected.

    Returns:
        Dict with keys: category, confidence, detections, suggested_department,
                       category_scores
    """
    if confidence_threshold is None:
        confidence_threshold = float(os.getenv("OLLAMA_VISION_CONFIDENCE", "0.3"))

    results = {}
    all_detections = []

    for category, prompt in DETECT_PROMPTS.items():
        response = _ask_vision_model(image_path, prompt)

        if not response:
            continue

        is_detected = _parse_yes_no(response)

        if is_detected:
            # Use a fixed confidence for Ollama vision (it doesn't give probabilities)
            confidence = 0.75
            results[category] = confidence
            all_detections.append({
                "category": category,
                "confidence": confidence,
                "description": response[:200],
            })

    if not results:
        return {
            "category": "Unspecified",
            "confidence": 0.0,
            "detections": [],
            "suggested_department": None,
            "category_scores": {},
        }

    best_cat = max(results, key=lambda k: results[k])

    return {
        "category": best_cat,
        "confidence": round(results[best_cat], 3),
        "detections": all_detections,
        "suggested_department": DEPARTMENT_MAP.get(best_cat),
        "category_scores": {k: round(v, 4) for k, v in results.items()},
    }


def classify_image_from_bytes(
    image_bytes: bytes,
    filename: str = "image.jpg",
    confidence_threshold: Optional[float] = None,
    **kwargs,
) -> Dict:
    """Classify an image from raw bytes (e.g., uploaded file)."""
    suffix = os.path.splitext(filename)[1] or ".jpg"
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        tmp.write(image_bytes)
        tmp_path = tmp.name

    try:
        return classify_image(tmp_path, confidence_threshold)
    finally:
        os.unlink(tmp_path)
