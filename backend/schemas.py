import os
from typing import List, Dict, Optional
from pydantic import BaseModel, Field

def get_max_prompt_chars() -> int:
    try:
        return int(os.getenv("PROMPTSHIELD_MAX_PROMPT_CHARS", "20000"))
    except ValueError:
        return 20000

MAX_PROMPT_CHARS = get_max_prompt_chars()

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
    prompt: str = Field(min_length=0, max_length=MAX_PROMPT_CHARS)

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
    prompt: str = Field(min_length=0, max_length=MAX_PROMPT_CHARS)
    model: Optional[str] = "meta-llama/llama-3.3-70b-instruct:free"

class ChatResponse(BaseModel):
    response: str
    model_used: str
    sanitized: bool
