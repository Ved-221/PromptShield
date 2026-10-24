import pytest
from services.risk_service import compute_risk_score
from schemas import Finding

def test_risk_score_clean():
    score, risk_level, stats = compute_risk_score([])
    assert score == 100
    assert risk_level == "Safe"
    assert stats.total_findings == 0

def test_risk_score_critical_penalty():
    findings = [
        Finding(
            id="f1",
            text="sk-proj-1234567890abcdef1234567890abcdef",
            type="OPENAI_KEY",
            category="Authentication",
            start=0,
            end=40,
            confidence=1.0,
            risk_level="Critical",
            reason="API key",
            recommendation="Redact",
            placeholder="[OPENAI_API_KEY]",
            source="Regex"
        )
    ]
    score, risk_level, stats = compute_risk_score(findings)
    assert score == 75  # 100 - 25
    assert risk_level == "Medium"
    assert stats.critical_count == 1
    assert stats.by_category["Authentication"] == 1

def test_risk_score_multiple_findings():
    findings = [
        Finding(
            id="f1",
            text="a@b.com",
            type="EMAIL",
            category="PII",
            start=0,
            end=7,
            confidence=0.98,
            risk_level="High",
            reason="Email",
            recommendation="Redact",
            placeholder="[EMAIL]",
            source="Regex"
        ),
        Finding(
            id="f2",
            text="secret",
            type="PASSWORD",
            category="Authentication",
            start=10,
            end=16,
            confidence=0.95,
            risk_level="Critical",
            reason="Password",
            recommendation="Redact",
            placeholder="[PASSWORD]",
            source="Regex"
        ),
        Finding(
            id="f3",
            text="John",
            type="PERSON",
            category="PII",
            start=20,
            end=24,
            confidence=0.85,
            risk_level="Medium",
            reason="Name",
            recommendation="Redact",
            placeholder="[PERSON]",
            source="spaCy"
        )
    ]
    # Penalties: Critical=25, High=15, Medium=8 -> total 48. Score = 52
    score, risk_level, stats = compute_risk_score(findings)
    assert score == 52
    assert risk_level == "High"
    assert stats.total_findings == 3
    assert stats.critical_count == 1
    assert stats.high_count == 1
    assert stats.medium_count == 1
    assert stats.by_category["PII"] == 2
    assert stats.by_category["Authentication"] == 1
