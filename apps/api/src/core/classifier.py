"""
Agent 1: IP Type Classifier

Uses Gemini Flash-Lite with few-shot prompting to classify an Ayurvedic product
into one of 6 regulatory categories. Returns category + confidence + reasoning.

Categories:
  1. Classical/Generic Medicine (Schedule I texts)
  2. Proprietary Medicine
  3. New Drug (Schedule Y)
  4. Phytopharmaceutical (Rule 122E)
  5. Ayurveda-Aahar / Nutraceutical (FSSAI)
  6. Cosmetic (D&C Act Ch III-A)

If confidence < 60%, the system asks the user clarifying questions.
"""

# TODO: Implement classifier with structured output (Pydantic model)
# Model: Gemini Flash-Lite (fast, cheap, sufficient for classification)
