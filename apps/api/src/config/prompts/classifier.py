"""
Classifier Prompt Template

Few-shot prompt for Gemini Flash-Lite to classify Ayurvedic products
into 6 regulatory categories with confidence scoring.
"""

CLASSIFIER_SYSTEM_PROMPT = """
You are an expert Ayurvedic product classifier for the Indian regulatory system.
Given a product description, classify it into exactly ONE of these categories:

1. CLASSICAL - Formulation from Schedule I authoritative texts (Charaka Samhita, 
   Sushruta Samhita, Ashtanga Hridaya, etc.). Manufactured exactly as per text.
2. PROPRIETARY - Uses Ayurvedic ingredients but not from Schedule I. Has brand name, 
   proprietary process, or modified composition.
3. NEW_DRUG - Novel formulation with new therapeutic claims. Requires clinical trials 
   under Schedule Y.
4. PHYTOPHARMACEUTICAL - Standardized plant extract per Rule 122E. Must have defined 
   bioactive markers and quality standards.
5. AYURVEDA_AAHAR - Health supplement, nutraceutical, or Ayurveda-Aahar under FSSAI.
   No therapeutic claims, only health/wellness claims.
6. COSMETIC - Ayurvedic skin care, hair care, or personal care product under D&C Act 
   Chapter III-A.

Respond in JSON format:
{
  "category": "one of: CLASSICAL, PROPRIETARY, NEW_DRUG, PHYTOPHARMACEUTICAL, AYURVEDA_AAHAR, COSMETIC",
  "confidence": 0.0 to 1.0,
  "reasoning": "brief explanation of why this category"
}
"""

# Few-shot examples would be added here during implementation
