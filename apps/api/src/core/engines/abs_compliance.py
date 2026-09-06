"""
ABS Compliance Agent — Checks for Access and Benefit Sharing obligations.
"""
from langchain_google_vertexai import ChatVertexAI
from langchain_core.prompts import ChatPromptTemplate
from ...models.chat import EngineOutput
from ...config.settings import settings

class ABSComplianceEngine:
    def __init__(self):
        self.llm = ChatVertexAI(
            model_name="gemini-2.5-flash", 
            project=settings.google_cloud_project,
            location=settings.google_cloud_location,
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
