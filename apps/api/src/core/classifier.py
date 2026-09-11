"""
Agent 1: IP Type Classifier

Uses Gemini Flash-Lite with few-shot prompting to classify an Ayurvedic product
into one of 6 regulatory categories. Returns category + confidence + reasoning.
"""

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from src.models.chat import ClassifierOutput
from src.config.settings import settings

class ClassifierAgent:
    def __init__(self):
        # We use gemini-2.5-flash since gemini-2.0-flash-lite might not be available everywhere
        # For SIH we assume a fast flash model. 
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash", 
            google_api_key=settings.google_api_key,
            temperature=0.0
        )
        # Force the output to match our Pydantic schema
        self.structured_llm = self.llm.with_structured_output(ClassifierOutput)

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert Ayurvedic regulatory classifier. 
Your job is to read a product description and classify it into exactly one of the following categories:
- CLASSICAL_AYURVEDA: Mentioned in Schedule I of the Drugs and Cosmetics Act (e.g. Chyawanprash, Triphala).
- PROPRIETARY_AYURVEDA: A new combination of known Ayurvedic ingredients not in classical texts.
- PHYTOPHARMACEUTICAL: A purified, standardized extract of a plant (Rule 122E).
- NEW_DRUG: A completely novel synthetic or highly modified Ayurvedic formulation requiring clinical trials.
- AYURVEDA_AAHAR: Food products/nutraceuticals based on Ayurveda (FSSAI).
- COSMETIC: For applying to the human body for cleansing/beautifying (Chapter III-A).
- UNCLEAR: If the description is too vague to classify.

Give a confidence score (0.0 to 1.0) and a brief 1-sentence reasoning. Be conservative. If you are not sure, give a lower confidence score."""),
            ("human", "Classify this product description: {query}")
        ])

    def classify(self, query: str) -> ClassifierOutput:
        chain = self.prompt | self.structured_llm
        result = chain.invoke({"query": query})
        return result

# Singleton instance
classifier_agent = ClassifierAgent()
