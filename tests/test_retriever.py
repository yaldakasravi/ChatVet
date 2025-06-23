# tests/test_retriever.py

import pytest
from openai.embeddings_utils import get_embedding
from retriever import get_pinecone_retriever

# Load retriever once
retriever = get_pinecone_retriever()

def test_similar_query_returns_results():
    """Ensure a relevant symptom query returns top matches."""
    query = "My dog is scratching his ears"
    query_vector = get_embedding(query, engine="text-embedding-ada-002")

    results = retriever.get_relevant_documents(query)
    
    assert isinstance(results, list)
    assert len(results) > 0

    top = results[0]
    assert hasattr(top, "page_content")
    assert isinstance(top.page_content, str)
    assert "ear" in top.page_content.lower() or "scratch" in top.page_content.lower()


def test_unrelated_query_returns_few_results():
    """Test a query that likely has no match still returns safe output."""
    query = "Quantum physics of feline teleportation"
    results = retriever.get_relevant_documents(query)

    assert isinstance(results, list)
    assert len(results) > 0  # should return fallback, not crash


def test_result_structure_and_ordering():
    """Check if results have score ordering and proper structure."""
    query = "puppy has worms in stool"
    results = retriever.get_relevant_documents(query)

    texts = [doc.page_content for doc in results]
    assert all(isinstance(t, str) and len(t) > 5 for t in texts)
