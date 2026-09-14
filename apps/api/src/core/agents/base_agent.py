"""
Base Agent — Shared logic for all Domain Agents.
"""
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from src.models.chat import DomainAgentOutput
from langchain.output_parsers import PydanticOutputParser
from src.config.settings import settings

class BaseDomainAgent:
    """Base class for all domain-specific IP agents."""
    
    def __init__(self, system_prompt: str):
        self.llm = ChatGroq(
            model=settings.groq_model,
            api_key=settings.groq_api_key,
            temperature=0.1
        )
        self.structured_llm = self.llm.with_structured_output(DomainAgentOutput)
        global_citation_rule = (
            "CITATION RULE: Primarily use the provided 'Retrieved Legal Context' for your citations. "
            "If the context contains the relevant section, cite it exactly. "
            "However, if the retrieved data is very limited but you are absolutely certain (110% sure) "
            "about the relevant statutory citations based on your internal knowledge of Indian/Global IP law, "
            "you may include those important citations. Only do this if you have extremely high confidence."
        )
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt + "\n\n" + global_citation_rule + "\n\nReturn only valid JSON."),
            ("human", "Query: {query}\n\nRetrieved Legal Context:\n{context}")
        ])
        self.chain = self.prompt | self.structured_llm

    def analyze(self, query: str, context: str) -> DomainAgentOutput:
        """Runs the agent with the user's query and the retrieved RAG context."""
        return self.chain.invoke({"query": query, "context": context})
