# backend/assistant/intent.py
"""Simple rule‑based intent detection for Baymax.
We look for keywords to map a user message to an Intent enum.
This is deliberately lightweight for the 2‑day prototype.
"""
import re
from enum import Enum

class Intent(Enum):
    HEALTH_QUESTION = "health_question"
    SYMPTOM_INFORMATION = "symptom_information"
    DOCUMENT_QUESTION = "document_question"
    DOCUMENT_SUMMARY = "document_summary"
    WELLNESS_LOG = "wellness_log"
    WELLNESS_SUMMARY = "wellness_summary"
    REMINDER = "reminder"
    GENERAL_CONVERSATION = "general_conversation"
    EMERGENCY_CONCERN = "emergency_concern"
    UNKNOWN = "unknown"

# Keyword groups – can be expanded later
_HEALTH_Q = [r"what is", r"explain", r"definition", r"describe"]
_SYMPTOM = [r"symptom", r"feel", r"pain", r"headache", r"tired"]
_REMINDER = [r"remind", r"reminder", r"notify", r"alert"]
_WELLNESS = [r"log", r"track", r"record", r"sleep", r"water", r"exercise"]
_EMERGENCY = [r"chest pain", r"shortness of breath", r"severe", r"unconscious", r"bleeding", r"stroke", r"allergic reaction"]

def detect_intent(message: str) -> Intent:
    lowered = message.lower()
    # Emergency takes priority
    for pattern in _EMERGENCY:
        if re.search(pattern, lowered):
            return Intent.EMERGENCY_CONCERN
    if any(re.search(p, lowered) for p in _REMINDER):
        return Intent.REMINDER
    if any(re.search(p, lowered) for p in _WELLNESS):
        return Intent.WELLNESS_LOG
    if any(re.search(p, lowered) for p in _SYMPTOM):
        return Intent.SYMPTOM_INFORMATION
    if any(re.search(p, lowered) for p in _HEALTH_Q):
        return Intent.HEALTH_QUESTION
    # Fallback to general conversation
    return Intent.GENERAL_CONVERSATION
