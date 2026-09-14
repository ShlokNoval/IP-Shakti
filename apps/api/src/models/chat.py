"""
Pydantic schemas for chat request/response models.
Defines the structured output format for all agent responses.
"""
from pydantic import AliasChoices, BaseModel, Field, field_validator, model_validator
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
    text: Optional[str] = Field(default=None, description="Quoted text or explanation")
    link: Optional[str] = Field(default=None, description="Optional URL to the source")

class ComplianceAlert(BaseModel):
    check_name: str = Field(
        description="Name of the check (e.g., 'Section 3(d)')",
        validation_alias=AliasChoices("check_name", "checkName", "check", "name"),
    )
    status: Literal["CLEAR", "REVIEW", "FAIL"] = Field(
        description="Status of the compliance check",
        validation_alias=AliasChoices("status", "result"),
    )
    reason: str = Field(
        default="No additional explanation was returned.",
        description="Explanation of the status",
        validation_alias=AliasChoices("reason", "comment", "description"),
    )

    @field_validator("status", mode="before")
    @classmethod
    def normalize_status(cls, value: str) -> str:
        """Map common model status variants to the UI's three supported states."""
        normalized = str(value).upper()
        if normalized in {"PENDING", "WARNING", "CAUTION", "REQUIRED", "RECOMMENDED", "YES", "POTENTIAL"}:
            return "REVIEW"
        if normalized in {"OPTIONAL", "NO"}:
            return "CLEAR"
        return normalized

class DomainAgentOutput(BaseModel):
    regulatory_pathway: str = Field(description="Explanation of the regulatory pathway")
    key_requirements: list[str] = Field(description="List of key requirements", json_schema_extra={"items": {"type": "string"}})
    ip_options: list[str] = Field(description="List of available IP protections", json_schema_extra={"items": {"type": "string"}})
    citations: list[SourceCitation] = Field(description="List of sources cited", json_schema_extra={"items": {"type": "object"}})

class EngineOutput(BaseModel):
    engine: str = Field(default="Compliance engine", description="Name of the compliance engine")
    checks: list[ComplianceAlert] = Field(
        description="List of compliance checks",
        validation_alias=AliasChoices("checks", "compliance_checks"),
        json_schema_extra={"items": {"type": "object"}},
    )

    @model_validator(mode="before")
    @classmethod
    def normalize_engine_response(cls, value):
        """Accept concise model summaries when a detailed checks array is absent."""
        if not isinstance(value, dict):
            return value
        normalized = dict(value)
        if "checks" not in normalized and "compliance_checks" not in normalized:
            assessment = normalized.get("evaluation") or normalized.get("notes")
            recommendation = normalized.get("recommendation")
            if assessment or recommendation:
                normalized["checks"] = [{
                    "check_name": normalized.get("section", "Compliance assessment"),
                    "status": normalized.get("status", "REVIEW"),
                    "reason": " ".join(part for part in (assessment, recommendation) if part),
                }]
        return normalized

class FinalResponse(BaseModel):
    classification: str = Field(description="The final classification category")
    jurisdiction: str = Field(description="The jurisdiction analyzed")
    guidance_text: str = Field(description="The final synthesized markdown advice for the user")
    compliance_alerts: list[ComplianceAlert] = Field(default_factory=list, description="Any red/yellow flags", json_schema_extra={"items": {"type": "object"}})
    sources: list[SourceCitation] = Field(default_factory=list, description="All accumulated sources", json_schema_extra={"items": {"type": "object"}})
    overall_confidence: float = Field(description="The final confidence score of the system (0.0 to 1.0)")
