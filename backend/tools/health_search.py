# backend/tools/health_search.py
"""Health knowledge search tool – wraps the existing RAG pipeline.
It returns a dict with:
    "context" – concatenated top‑k passages (string)
    "sources" – list of source identifiers (placeholder for now)
"""
import sys, os
from typing import List, Dict

# Ensure project root on PYTHONPATH (backend __init__ already does this)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

# Import existing retrieval utilities
from query.hybrid_search import hybrid_search
from query.reranker import rerank

TOP_K = 3

def search_health_knowledge(query: str) -> Dict[str, object]:
    """Run hybrid search + reranking and return a structured result.
    Args:
        query: User question.
    Returns:
        dict with keys ``context`` (str) and ``sources`` (list).
    """
    # First obtain raw hybrid results (list of strings)
    hybrid_results = hybrid_search(query, k=TOP_K)
    # Re‑run reranker to get scored docs – it expects a query and uses hybrid_search internally
    reranked = rerank(query, top_k=TOP_K)
    # Build context from reranked docs (doc is the string content)
    context_parts: List[str] = [doc for doc, _score in reranked]
    context = "\n\n".join(context_parts)
    # Sources are placeholders – original code does not keep filenames; we can attach index numbers.
    sources = [{"source": f"doc_{i+1}"} for i in range(len(context_parts))]
    return {"context": context, "sources": sources}
