"""
Base Agent — Shared logic for all Domain Agents.
"""
from langchain_google_vertexai import ChatVertexAI
from langchain_core.prompts import ChatPromptTemplate
from ...models.chat import DomainAgentOutput
from ...config.settings import settings

class BaseDomainAgent:
    """Base class for all domain-specific IP agents."""
    
    def __init__(self, system_prompt: str):
        self.llm = ChatVertexAI(
            model_name="gemini-2.5-flash", 
            project=settings.google_cloud_project,
            location=settings.google_cloud_location,
            temperature=0.1
        )
        self.structured_llm = self.llm.with_structured_output(DomainAgentOutput)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "Query: {query}\n\nRetrieved Legal Context:\n{context}")
        ])
        self.chain = self.prompt | self.structured_llm

    def analyze(self, query: str, context: str) -> DomainAgentOutput:
        """Runs the agent with the user's query and the retrieved RAG context."""
        return self.chain.invoke({
            "query": query,
            "context": context
        })
