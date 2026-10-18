# backend/assistant/safety.py
"""Safety layer for Baymax responses.
- If the detected intent is EMERGENCY_CONCERN, prepend an urgent notice.
- Optionally scan the generated reply for emergency keywords as a fallback.
"""
from typing import List
from .intent import Intent

EMERGENCY_NOTICE = (
    "**IMPORTANT:** If you are experiencing a medical emergency, please seek immediate professional "
    "medical attention or call emergency services (e.g., 112 or 911)."
)

def apply_safety(response: str, intent: Intent) -> str:
    """Apply safety checks based on intent and content.
    Args:
        response: The raw LLM answer.
        intent: Detected Intent.
    Returns:
        A possibly modified response that includes safety warnings.
    """
    if intent == Intent.EMERGENCY_CONCERN:
        return f"{EMERGENCY_NOTICE}\n\n{response}"
    # Simple keyword scan as a backup (could be expanded)
    emergency_keywords = [
        "chest pain",
        "shortness of breath",
        "unconscious",
        "severe bleeding",
        "stroke",
        "allergic reaction",
    ]
    lowered = response.lower()
    if any(word in lowered for word in emergency_keywords):
        return f"{EMERGENCY_NOTICE}\n\n{response}"
    return response
