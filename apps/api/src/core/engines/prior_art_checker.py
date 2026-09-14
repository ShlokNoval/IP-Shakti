"""
Prior Art Checker Engine

A specialized compliance engine that checks if the formulation
is likely already known in Traditional Knowledge Digital Library (TKDL)
or common Ayurvedic practice.
"""
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from src.models.chat import EngineOutput
from src.config.settings import settings
from langchain.output_parsers import PydanticOutputParser

class PriorArtChecker:
    def __init__(self):
        self.llm = ChatGroq(
            model=settings.groq_model,
            api_key=settings.groq_api_key,
            temperature=0.0
        )
        self.structured_llm = self.llm.with_structured_output(EngineOutput)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a Prior Art Evaluation Engine for Ayurvedic IP.
Check the user's formulation against common traditional knowledge (e.g., Turmeric for wound healing, Neem for skin).
Flag potential TKDL (Traditional Knowledge Digital Library) conflicts.
If ingredients are used for their well-known traditional purposes, return a REVIEW or FAIL status.
Return a list of compliance checks. Return only valid JSON."""),
            ("human", "Query: {query}\n\nContext:\n{context}")
        ])
        
        self.chain = self.prompt | self.structured_llm

    def evaluate(self, query: str, context: str) -> EngineOutput:
        return self.chain.invoke({"query": query, "context": context})

# Singleton instance
prior_art_checker = PriorArtChecker()
