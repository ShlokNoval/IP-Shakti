"""
Hybrid Retriever — Combines vector search + keyword search for legal documents.
"""

from typing import List, Dict, Any

class HybridRetriever:
    def __init__(self):
        # In the future, Subordinate 3 will initialize Supabase here
        pass

    def retrieve(self, query: str, jurisdiction: str) -> List[Dict[str, Any]]:
        # STUB: Returns mock legal context so the Orchestrator can function
        return [
            {
                "content": "Rule 122E of the Drugs and Cosmetics Rules defines a Phytopharmaceutical as a purified and standardized fraction with defined minimum four bio-active or phytochemical compounds.",
                "metadata": {"source": "D&C Act, 1940", "section": "Rule 122E"}
            },
            {
                "content": "Section 3(p) of the Patents Act states that an invention which in effect, is traditional knowledge or which is an aggregation or duplication of known properties of traditionally known component or components is not patentable.",
                "metadata": {"source": "Patents Act, 1970", "section": "Section 3(p)"}
            }
        ]

# Singleton instance
hybrid_retriever = HybridRetriever()
