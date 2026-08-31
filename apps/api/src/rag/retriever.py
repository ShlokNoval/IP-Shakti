"""
Hybrid Retriever — Combines vector search + keyword search for legal documents.

Vector search (pgvector): Good for semantic similarity
Keyword search (PostgreSQL full-text): Good for exact statute/section references
Combined via Reciprocal Rank Fusion for best of both worlds.
"""

# TODO: Implement hybrid retrieval with RRF merging
