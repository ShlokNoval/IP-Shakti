"""
ABS Compliance Agent — Checks for Access and Benefit Sharing obligations.
"""
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from src.models.chat import EngineOutput
from src.config.settings import settings

class ABSComplianceEngine:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash", 
            google_api_key=settings.google_api_key,
            temperature=0.1
        )
        self.structured_llm = self.llm.with_structured_output(EngineOutput)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a compliance officer for the National Biodiversity Authority (NBA).
Your job is to check if the product uses Indian biological resources and triggers Access and Benefit Sharing (ABS) obligations under the Biological Diversity Act, 2002.
Evaluate for:
- Prior Informed Consent (PIC) requirements.
- Mutually Agreed Terms (MAT) requirements.
- Exemptions (e.g., normally traded commodities).

Return your engine name as "ABS Compliance Engine" and provide specific checks.
"""),
            ("human", "Query: {query}\n\nContext:\n{context}")
        ])
        self.chain = self.prompt | self.structured_llm

    def evaluate(self, query: str, context: str) -> EngineOutput:
        return self.chain.invoke({"query": query, "context": context})

abs_compliance = ABSComplianceEngine()
