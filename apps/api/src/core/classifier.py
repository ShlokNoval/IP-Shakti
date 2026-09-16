import json
from groq import Groq
from src.models.chat import ClassifierOutput
from src.config.settings import settings

class ClassifierAgent:
    def __init__(self):
        self.client = Groq(api_key=settings.groq_api_key)

    def classify(self, query: str) -> ClassifierOutput:
        query_upper = query.upper()
        # Fast path for Innovation Disclosure Profiles
        if "INNOVATION DISCLOSURE PROFILE" in query_upper:
            if "CLASSICAL" in query_upper:
                return ClassifierOutput(category="CLASSICAL_AYURVEDA", confidence=0.98, reasoning="Derived from structured Innovation Disclosure Profile (Schedule I Classical Ayurveda).")
            elif "PHYTOPHARMACEUTICAL" in query_upper:
                return ClassifierOutput(category="PHYTOPHARMACEUTICAL", confidence=0.98, reasoning="Derived from structured Innovation Disclosure Profile (Rule 122E Phytopharmaceutical).")
            elif "AYURVEDA-AAHAR" in query_upper or "AAHAR" in query_upper:
                return ClassifierOutput(category="AYURVEDA_AAHAR", confidence=0.98, reasoning="Derived from structured Innovation Disclosure Profile (FSSAI Ayurveda-Aahar).")
            elif "COSMETIC" in query_upper:
                return ClassifierOutput(category="COSMETIC", confidence=0.98, reasoning="Derived from structured Innovation Disclosure Profile (Ayurvedic Cosmetic Chapter III-A).")
            elif "NEW DRUG" in query_upper or "NEW_DRUG" in query_upper:
                return ClassifierOutput(category="NEW_DRUG", confidence=0.98, reasoning="Derived from structured Innovation Disclosure Profile (Novel Botanical New Drug).")
            elif "PROPRIETARY" in query_upper:
                return ClassifierOutput(category="PROPRIETARY_AYURVEDA", confidence=0.98, reasoning="Derived from structured Innovation Disclosure Profile (Proprietary Ayurveda).")

        try:
            chat = self.client.chat.completions.create(
                model=settings.groq_model,
                messages=[
                    {"role": "system", "content": """You are an expert Ayurvedic regulatory classifier.
Classify the product into exactly one category: CLASSICAL_AYURVEDA, PROPRIETARY_AYURVEDA, PHYTOPHARMACEUTICAL, NEW_DRUG, AYURVEDA_AAHAR, COSMETIC, or UNCLEAR.
Return valid JSON with keys: "category" (string), "confidence" (float 0.0 to 1.0), "reasoning" (string)."""},
                    {"role": "user", "content": f"Classify this product description: {query}"}
                ],
                response_format={"type": "json_object"},
                temperature=0.0
            )
            data = json.loads(chat.choices[0].message.content)
            category = data.get("category", "UNCLEAR").upper()
            valid_cats = {"CLASSICAL_AYURVEDA", "PROPRIETARY_AYURVEDA", "PHYTOPHARMACEUTICAL", "NEW_DRUG", "AYURVEDA_AAHAR", "COSMETIC", "UNCLEAR"}
            if category not in valid_cats:
                category = "UNCLEAR"
            return ClassifierOutput(
                category=category,
                confidence=float(data.get("confidence", 0.85)),
                reasoning=data.get("reasoning", "Classified via regulatory knowledge base.")
            )
        except Exception as e:
            print(f"Classifier fallback: {e}")
            return ClassifierOutput(
                category="PROPRIETARY_AYURVEDA",
                confidence=0.70,
                reasoning="Defaulted to proprietary formulation for comprehensive regulatory assessment."
            )

# Singleton instance
classifier_agent = ClassifierAgent()
