from typing import List, Dict, Optional
from pydantic import BaseModel, Field

class Finding(BaseModel):
    id: str
    text: str
    type: str  # e.g., EMAIL, PHONE, API_KEY, PERSON, ORG, CREDIT_CARD, PASSWORD, SECRET, IP_ADDRESS
    category: str  # PII, Financial, Authentication, Organization, Healthcare, Technical, Legal
    start: int
    end: int
    confidence: float = Field(ge=0.0, le=1.0)
    risk_level: str  # Critical, High, Medium, Low
    reason: str
    recommendation: str
    placeholder: str
    source: str = "Engine"

class AnalyzeRequest(BaseModel):
    prompt: str

class SanitizeRequest(BaseModel):
    prompt: str
    findings: List[Finding]
    actions: Optional[Dict[str, str]] = Field(default_factory=dict)  # finding_id -> "replace" | "remove" | "keep"

class StatsSummary(BaseModel):
    total_findings: int
    critical_count: int
    high_count: int
    medium_count: int
    low_count: int
    by_category: Dict[str, int]

class AnalyzeResponse(BaseModel):
    prompt: str
    findings: List[Finding]
    sanitized_prompt: str
    privacy_score: int  # 0 to 100 (100 = safe)
    risk_level: str     # Safe, Low, Medium, High, Critical
    stats: StatsSummary

class ChatRequest(BaseModel):
    prompt: str
    model: Optional[str] = "meta-llama/llama-3.3-70b-instruct:free"

class ChatResponse(BaseModel):
    response: str
    model_used: str
    sanitized: bool
