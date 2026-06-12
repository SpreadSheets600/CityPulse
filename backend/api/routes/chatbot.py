import os
from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import User, Issue


FAQ = {
    "how to report": {
        "question": "How do I report an issue?",
        "answer": "To report an issue, click on 'Report Issue' in the navigation menu. Fill in the title, description, and upload at least one image. You can also add your location to help us respond faster."
    },
    "report issue": {
        "question": "How do I report an issue?",
        "answer": "To report an issue, click on 'Report Issue' in the navigation menu. Fill in the title, description, and upload at least one image. You can also add your location to help us respond faster."
    },
    "track issue": {
        "question": "How do I track my issue?",
        "answer": "You can track your issues by going to 'My Issues' in the navigation menu. Each issue shows its current status: Pending, In Progress, Resolved, or Rejected."
    },
    "track status": {
        "question": "How do I track my issue?",
        "answer": "You can track your issues by going to 'My Issues' in the navigation menu. Each issue shows its current status: Pending, In Progress, Resolved, or Rejected."
    },
    "status": {
        "question": "What do the status labels mean?",
        "answer": "Pending: Your issue has been received. In Progress: An admin is working on it. Resolved: The issue has been fixed. Rejected: The issue could not be verified."
    },
    "upvote": {
        "question": "What is upvoting?",
        "answer": "Upvoting lets you show support for an issue. Click the upvote button on any issue to increase its priority. Issues with more upvotes get attention first."
    },
    "comment": {
        "question": "Can I add comments to an issue?",
        "answer": "Yes! You can add comments to any issue to provide additional information or updates. Scroll down to the comments section on the issue page."
    },
    "contact": {
        "question": "How do I contact support?",
        "answer": "You can start a chat with our support team by clicking the chat button in the bottom right corner. Admins typically respond within a few hours during business hours."
    },
    "help": {
        "question": "What can you help me with?",
        "answer": "I can help you with: reporting issues, tracking your reports, understanding issue statuses, upvoting issues, and contacting support. Just ask!"
    },
    "hello": {
        "question": "Hello!",
        "answer": "Hello! I'm the CityPulse assistant. I can help you report issues, track your reports, or answer questions about the platform. How can I help you today?"
    },
    "hi": {
        "question": "Hello!",
        "answer": "Hello! I'm the CityPulse assistant. I can help you report issues, track your reports, or answer questions about the platform. How can I help you today?"
    }
}


def _faq_response(message: str) -> str:
    """Fallback FAQ-based keyword matching."""
    best_match = None
    best_score = 0

    for key, entry in FAQ.items():
        if key in message or message in key:
            score = len(key) / max(len(message), 1)
            if score > best_score:
                best_score = score
                best_match = entry

    if not best_match:
        words = set(message.split())
        for key, entry in FAQ.items():
            key_words = set(key.split())
            overlap = len(words & key_words)
            if overlap > 0:
                score = overlap / max(len(key_words), 1)
                if score > best_score:
                    best_score = score
                    best_match = entry

    if best_match and best_score > 0.2:
        return best_match["answer"]

    return (
        "I'm not sure I understand. I can help you with:\n"
        "- How to report an issue\n"
        "- Tracking your issues\n"
        "- Understanding status labels\n"
        "- Upvoting issues\n"
        "- Contacting support\n\n"
        "Try asking something like 'How do I report an issue?'"
    )


class Chatbot(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        message = data.get("message", "").strip()

        if not message:
            return {"response": "Please type a message and I'll do my best to help!"}

        # Try Ollama AI if enabled
        ai_enabled = os.getenv("AI_TEXT_ENABLED", "false").lower() in ("true", "1", "yes")
        if ai_enabled:
            try:
                from ..utils.ai_client import chat
                response = chat(message)
                return {"response": response}
            except Exception as e:
                print(f"------ [ WARN ] ------ Ollama chat failed, falling back to FAQ: {e}")

        # Fallback to FAQ keyword matching
        return {"response": _faq_response(message.lower())}
