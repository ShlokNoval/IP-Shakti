"""
ABS (Access and Benefit Sharing) Compliance Engine

Evaluates whether the biological resources used trigger the 
Biological Diversity Act, 2002 requirements (e.g. NBA approval).
"""
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from src.models.chat import EngineOutput
from src.config.settings import settings
from langchain.output_parsers import PydanticOutputParser

class ABSComplianceEngine:
    def __init__(self):
        self.llm = ChatGroq(
            model=settings.groq_model,
            api_key=settings.groq_api_key,
            temperature=0.0
        )
        self.structured_llm = self.llm.with_structured_output(EngineOutput)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an ABS Compliance Engine for Indian IP Law.
Evaluate the user's formulation to determine if it uses Indian biological resources.
If it does, flag that National Biodiversity Authority (NBA) approval and Access and Benefit Sharing (ABS) may be required under the Biological Diversity Act, 2002.
If the user mentions 'value added products' or 'highly processed extracts', evaluate if they fall under the exemption.
Return a list of compliance checks with STATUS (CLEAR, REVIEW, FAIL) and reason. Return only valid JSON."""),
            ("human", "Query: {query}\n\nContext:\n{context}")
        ])
        
        self.chain = self.prompt | self.structured_llm

    def evaluate(self, query: str, context: str) -> EngineOutput:
        return self.chain.invoke({"query": query, "context": context})

# Singleton instance
abs_compliance_engine = ABSComplianceEngine()
