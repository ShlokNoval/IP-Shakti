"""
Agent 8: Section 3 Patentability Evaluator

Checks whether a product/process passes the patentability bars under
Section 3 of the Indian Patents Act, 1970.

Sub-section checks:
  § 3(d) — Known substance (does modified process add novelty?)
  § 3(e) — Mere admixture (is there synergistic effect?)
  § 3(f) — Mere arrangement of known devices
  § 3(p) — Traditional knowledge (TKDL cross-check)

Output per sub-section: CLEAR ✅ / REVIEW ⚠️ / BLOCKED ❌ with reasoning.

Called when: Orchestrator detects a patent-related query.
Model: Gemini 2.0 Flash + deterministic rule checks
"""

# TODO: Implement with sub-section analysis + structured output
