"""
Base Agent — Shared logic for all Domain Agents.
"""
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from ...models.chat import DomainAgentOutput
from ...config.settings import settings

class BaseDomainAgent:
    """Base class for all domain-specific IP agents."""
    
    def __init__(self, system_prompt: str):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash", 
            google_api_key=settings.google_api_key,
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
