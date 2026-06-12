"""
Ollama AI client for text-based tasks.

Uses a local Ollama instance for:
- Text classification (replaces keyword-based classifier)
- Priority scoring (replaces heuristic scorer)
- Chatbot responses (replaces FAQ matcher)
"""

import os
from typing import Dict, Optional

_client = None


def _get_client():
    """Get or create cached Ollama client."""
    global _client
    if _client is not None:
        return _client

    try:
        import ollama

        base_url = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")
        _client = ollama.Client(host=base_url)
        print(f"------ [ INFO ] ------ Ollama client initialized ({base_url})")
        return _client
    except Exception as e:
        print(f"------ [ WARN ] ------ Ollama client init failed: {e}")
        return None


def _get_model() -> str:
    return os.getenv("OLLAMA_MODEL", "llama3.2")


def is_available() -> bool:
    """Check if Ollama is reachable and has the required model."""
    client = _get_client()
    if client is None:
        return False
    try:
        client.list()
        return True
    except Exception:
        return False


def classify_issue_text(title: str, description: str) -> Dict:
    """
    Classify an issue using Ollama LLM.

    Returns:
        Dict with keys: category, confidence, department, reasoning
    """
    client = _get_client()
    if client is None:
        return {"category": None, "confidence": 0.0, "department": None, "reasoning": "Ollama unavailable"}

    prompt = f"""You are a civic issue classifier. Classify the following issue into exactly ONE category.

Categories: Road Maintenance, Electricity, Water Supply, Waste Management, Public Transportation

Issue Title: {title}
Issue Description: {description}

Reply with ONLY a JSON object (no markdown, no explanation):
{{"category": "<category>", "confidence": <0.0-1.0>, "department": "<department>", "reasoning": "<one line>"}}

Department mapping:
- Road Maintenance -> Road Maintenance
- Electricity -> Electricity
- Water Supply -> Water Supply
- Waste Management -> Waste Management
- Public Transportation -> Public Transportation"""

    try:
        response = client.chat(
            model=_get_model(),
            messages=[{"role": "user", "content": prompt}],
            options={"temperature": 0.1},
        )
        text = response["message"]["content"].strip()

        # Parse JSON from response
        import json
        # Handle markdown code blocks
        if "```" in text:
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
            text = text.strip()

        result = json.loads(text)
        return {
            "category": result.get("category", "Unspecified"),
            "confidence": float(result.get("confidence", 0.5)),
            "department": result.get("department"),
            "reasoning": result.get("reasoning", ""),
        }

    except Exception as e:
        print(f"------ [ WARN ] ------ Ollama classification failed: {e}")
        return {"category": None, "confidence": 0.0, "department": None, "reasoning": str(e)}


def assess_priority(title: str, description: str, issue_type: str, upvote_count: int = 0) -> Dict:
    """
    Assess issue priority using Ollama LLM.

    Returns:
        Dict with keys: level, score, reasoning
    """
    client = _get_client()
    if client is None:
        return {"level": "medium", "score": 50, "reasoning": "Ollama unavailable"}

    prompt = f"""You are a civic issue priority assessor. Rate the urgency of this issue.

Issue Type: {issue_type}
Title: {title}
Description: {description}
Community Upvotes: {upvote_count}

Consider: safety risk, number of people affected, time-sensitivity, and community support.

Reply with ONLY a JSON object (no markdown):
{{"level": "<critical|high|medium|low>", "score": <0-100>, "reasoning": "<one line>"}}"""

    try:
        response = client.chat(
            model=_get_model(),
            messages=[{"role": "user", "content": prompt}],
            options={"temperature": 0.1},
        )
        text = response["message"]["content"].strip()

        import json
        if "```" in text:
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
            text = text.strip()

        result = json.loads(text)
        level = result.get("level", "medium")
        if level not in ("critical", "high", "medium", "low"):
            level = "medium"

        return {
            "level": level,
            "score": int(result.get("score", 50)),
            "reasoning": result.get("reasoning", ""),
        }

    except Exception as e:
        print(f"------ [ WARN ] ------ Ollama priority assessment failed: {e}")
        return {"level": "medium", "score": 50, "reasoning": str(e)}


def chat(user_message: str, context: str = "") -> str:
    """
    Generate a chatbot response using Ollama.

    Args:
        user_message: The user's message.
        context: Optional context about the platform.

    Returns:
        Response string.
    """
    client = _get_client()
    if client is None:
        return "AI assistant is currently unavailable. Please try again later."

    system_prompt = """You are CityPulse assistant, a helpful chatbot for a civic issue reporting platform.
You help citizens:
- Report civic issues (potholes, water leaks, garbage, power outages, transit problems)
- Track the status of their reported issues
- Understand how the platform works
- Contact support

Be concise, friendly, and helpful. If you don't know something specific about the platform, say so honestly.
Keep responses under 3 sentences unless more detail is needed."""

    messages = [{"role": "system", "content": system_prompt}]
    if context:
        messages.append({"role": "system", "content": f"Platform context: {context}"})
    messages.append({"role": "user", "content": user_message})

    try:
        response = client.chat(
            model=_get_model(),
            messages=messages,
            options={"temperature": 0.7},
        )
        return response["message"]["content"].strip()

    except Exception as e:
        print(f"------ [ WARN ] ------ Ollama chat failed: {e}")
        return "I'm having trouble connecting to my AI brain right now. Please try again in a moment."
