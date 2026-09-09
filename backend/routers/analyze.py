from fastapi import APIRouter, HTTPException
from schemas import AnalyzeRequest, AnalyzeResponse, SanitizeRequest
from services.regex_service import scan_regex
from services.spacy_service import scan_spacy
from services.presidio_service import scan_presidio
from services.merge_service import merge_findings, generate_sanitized_prompt
from services.risk_service import compute_risk_score

router = APIRouter(prefix="", tags=["Analyze"])

@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_prompt(req: AnalyzeRequest):
    prompt_text = req.prompt.strip()
    if not prompt_text:
        return AnalyzeResponse(
            prompt="",
            findings=[],
            sanitized_prompt="",
            privacy_score=100,
            risk_level="Safe",
            stats={
                "total_findings": 0,
                "critical_count": 0,
                "high_count": 0,
                "medium_count": 0,
                "low_count": 0,
                "by_category": {}
            }
        )

    # 1. Layer 1: Regex
    regex_results = scan_regex(prompt_text)

    # 2. Layer 2: spaCy NER
    spacy_results = scan_spacy(prompt_text)

    # 3. Layer 3: Presidio PII
    presidio_results = scan_presidio(prompt_text)

    # Combine all raw findings
    all_raw = regex_results + spacy_results + presidio_results

    # 4. Merge overlaps & resolve conflicts
    merged_findings = merge_findings(all_raw)

    # 5. Compute default sanitized prompt
    sanitized = generate_sanitized_prompt(prompt_text, merged_findings)

    # 6. Compute risk score & stats
    score, risk_level, stats = compute_risk_score(merged_findings)

    return AnalyzeResponse(
        prompt=prompt_text,
        findings=merged_findings,
        sanitized_prompt=sanitized,
        privacy_score=score,
        risk_level=risk_level,
        stats=stats
    )

@router.post("/sanitize")
async def sanitize_prompt(req: SanitizeRequest):
    sanitized = generate_sanitized_prompt(req.prompt, req.findings, req.actions)
    return {"sanitized_prompt": sanitized}
