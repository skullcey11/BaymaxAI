# backend/assistant/orchestrator.py
"""Core orchestrator for Baymax AI.
It receives a raw user message, detects intent, routes to the appropriate tool,
generates a response via the LLM, runs a safety check, and returns the final reply.
"""
import sys, os
from typing import Dict

# Ensure project root is on PYTHONPATH (backend __init__ already does this)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from backend.assistant.intent import detect_intent, Intent
from backend.tools.health_search import search_health_knowledge
from backend.assistant.safety import apply_safety
from langchain_ollama import ChatOllama

# Initialise the LLM once (shared across requests)
_llm = ChatOllama(model="llama3.2:3b", temperature=0)

async def _llm_generate(context: str, sources: list) -> str:
    """Build a simple prompt, call the LLM, and return the answer.
    The prompt asks the model to answer using ONLY the provided context and to cite sources.
    """
    source_list = "\n".join([f"- {s.get('source', 'unknown')}" for s in sources])
    prompt = f"""
You are Baymax, a friendly health information assistant.
Answer the user's question using ONLY the provided context. If you cannot find an answer, say:
"I could not find the answer in the provided documents."

Context:\n{context}\n\nSources:\n{source_list}\n\nAnswer:
"""
    response = _llm.invoke(prompt)
    # response may be an object with .content attribute
    return getattr(response, "content", str(response))

async def handle_message(message: str) -> str:
    """Public entry point used by the FastAPI chat endpoint.
    Returns a safety‑checked assistant reply.
    """
    intent = detect_intent(message)
    if intent == Intent.HEALTH_QUESTION or intent == Intent.SYMPTOM_INFORMATION:
        rag_result = search_health_knowledge(message)
        raw_reply = await _llm_generate(rag_result["context"], rag_result["sources"])
    elif intent == Intent.REMINDER:
        # Simple placeholder – just acknowledge
        raw_reply = "Sure, I have set the reminder for you."
    elif intent == Intent.WELLNESS_LOG:
        raw_reply = "Your wellness entry has been recorded."
    else:
        # Fallback generic response using the LLM without extra context
        raw_reply = _llm.invoke(message).content

    # Apply safety checks (e.g., emergency warnings)
    safe_reply = apply_safety(raw_reply, intent)
    return safe_reply
