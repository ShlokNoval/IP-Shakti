"""
Prior Art Checker — Cross-references formulations against TK references.
"""
from langchain_google_vertexai import ChatVertexAI
from langchain_core.prompts import ChatPromptTemplate
from ...models.chat import EngineOutput
from ...config.settings import settings

class PriorArtChecker:
    def __init__(self):
        self.llm = ChatVertexAI(
            model_name="gemini-2.5-flash", 
            project=settings.google_cloud_project,
            location=settings.google_cloud_location,
            temperature=0.1
        )
        self.structured_llm = self.llm.with_structured_output(EngineOutput)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a prior art search specialist for Indian IP.
Your job is to check if the formulation described by the user likely exists in traditional knowledge (TK) repositories like the Ayurvedic Pharmacopoeia or TKDL (Traditional Knowledge Digital Library).

Check for:
- Known formulations containing these exact ingredients.
- Historical usage for the claimed therapeutic purpose.

Return your engine name as "Prior Art Checker" and provide specific checks.
"""),
            ("human", "Query: {query}\n\nContext:\n{context}")
        ])
        self.chain = self.prompt | self.structured_llm

    def evaluate(self, query: str, context: str) -> EngineOutput:
        return self.chain.invoke({"query": query, "context": context})

prior_art_checker = PriorArtChecker()
