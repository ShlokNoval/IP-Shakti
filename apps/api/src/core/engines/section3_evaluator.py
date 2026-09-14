"""
Section 3(p) Evaluator Engine

Evaluates whether the formulation falls under Section 3(p) of the Patents Act, 1970,
which excludes "an invention which in effect, is traditional knowledge or which is 
an aggregation or duplication of known properties of traditionally known component or components."
"""
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from src.models.chat import EngineOutput
from src.config.settings import settings
from langchain.output_parsers import PydanticOutputParser

class Section3Evaluator:
    def __init__(self):
        self.llm = ChatGroq(
            model=settings.groq_model,
            api_key=settings.groq_api_key,
            temperature=0.0
        )
        self.structured_llm = self.llm.with_structured_output(EngineOutput)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a Section 3(p) Evaluator for the Indian Patents Act, 1970.
Read the user's formulation. If it is merely an aggregation of known Ayurvedic ingredients (e.g., turmeric + neem + aloe), flag it as a FAIL under Section 3(p).
To clear Section 3(p), there must be a 'synergistic effect' demonstrated (the combination works better than the sum of its parts).
Advise the user if they need to provide clinical or lab data showing synergy.
Return a list of compliance checks. Return only valid JSON."""),
            ("human", "Query: {query}\n\nContext:\n{context}")
        ])
        
        self.chain = self.prompt | self.structured_llm

    def evaluate(self, query: str, context: str) -> EngineOutput:
        return self.chain.invoke({"query": query, "context": context})

# Singleton instance
section3_evaluator = Section3Evaluator()
