"""
Section 3 Evaluator — Checks against Indian Patents Act Section 3 exclusions.
"""
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from ...models.chat import EngineOutput
from ...config.settings import settings

class Section3Evaluator:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash", 
            google_api_key=settings.google_api_key,
            temperature=0.1
        )
        self.structured_llm = self.llm.with_structured_output(EngineOutput)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert Patent Examiner in India.
Your job is to evaluate if a product violates Section 3 of the Patents Act, 1970.
Evaluate specifically for:
- 3(d): Is it just a new form of a known substance without enhanced efficacy?
- 3(e): Is it a mere admixture resulting only in the aggregation of properties?
- 3(p): Is it an invention which in effect is traditional knowledge?

Return your engine name as "Section 3 Evaluator" and provide specific checks.
"""),
            ("human", "Query: {query}\n\nContext:\n{context}")
        ])
        self.chain = self.prompt | self.structured_llm

    def evaluate(self, query: str, context: str) -> EngineOutput:
        return self.chain.invoke({"query": query, "context": context})

section3_evaluator = Section3Evaluator()
