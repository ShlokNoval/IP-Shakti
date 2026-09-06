"""
Pydantic schemas for chat request/response models.
Defines the structured output format for all agent responses.
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Literal

class ChatRequest(BaseModel):
    query: str = Field(description="The user's query about Ayurvedic IP or regulation")
    jurisdiction: Literal["india", "international"] = Field(default="india", description="The selected jurisdiction")
    language: str = Field(default="en", description="ISO language code of the query")
    session_id: Optional[str] = Field(default=None, description="Optional session ID for chat history")

class ClassifierOutput(BaseModel):
    category: Literal[
        "CLASSICAL_AYURVEDA",
        "PROPRIETARY_AYURVEDA",
        "PHYTOPHARMACEUTICAL",
        "NEW_DRUG",
        "AYURVEDA_AAHAR",
        "COSMETIC",
        "UNCLEAR"
    ] = Field(description="The assigned category based on the query")
    confidence: float = Field(description="Confidence score between 0.0 and 1.0")
    reasoning: str = Field(description="Brief explanation of why this category was chosen")

class SourceCitation(BaseModel):
    name: str = Field(description="Name of the statute or document (e.g. 'Drugs and Cosmetics Act, 1940')")
    section: str = Field(description="Specific section, rule, or schedule (e.g. 'Rule 122E')")
    link: Optional[str] = Field(default=None, description="Optional URL to the source")

class ComplianceAlert(BaseModel):
    check_name: str = Field(description="Name of the check (e.g., 'Section 3(d)')")
    status: Literal["CLEAR", "REVIEW", "FAIL"] = Field(description="Status of the compliance check")
    reason: str = Field(description="Explanation of the status")

class DomainAgentOutput(BaseModel):
    regulatory_pathway: str = Field(description="Explanation of the regulatory pathway")
    key_requirements: List[str] = Field(description="List of key requirements to fulfill")
    ip_options: List[str] = Field(description="List of available IP protections")
    citations: List[SourceCitation] = Field(description="List of sources cited in the analysis")

class EngineOutput(BaseModel):
    engine: str = Field(description="Name of the compliance engine")
    checks: List[ComplianceAlert] = Field(description="List of compliance checks performed")

class FinalResponse(BaseModel):
    classification: str = Field(description="The final classification category")
    jurisdiction: str = Field(description="The jurisdiction analyzed")
    guidance_text: str = Field(description="The final synthesized markdown advice for the user")
    compliance_alerts: List[ComplianceAlert] = Field(default_factory=list, description="Any red/yellow flags from compliance engines")
    sources: List[SourceCitation] = Field(default_factory=list, description="All accumulated sources")
    overall_confidence: float = Field(description="The final confidence score of the system (0.0 to 1.0)")
