import pytest
from fastapi.testclient import TestClient
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from main import app
from services.merge_service import generate_sanitized_prompt
from schemas import Finding

client = TestClient(app)

def test_sanitize_remove_whitespace_normalization():
    prompt = "Mail a@b.com now"
    f = Finding(
        id="f1",
        text="a@b.com",
        type="EMAIL",
        category="PII",
        start=5,
        end=12,
        confidence=0.99,
        risk_level="High",
        reason="Email",
        recommendation="Redact",
        placeholder="[EMAIL]",
        source="Regex"
    )
    result = generate_sanitized_prompt(prompt, [f], {"f1": "remove"})
    assert result == "Mail now"

def test_sanitize_remove_at_start_and_end():
    # At start
    prompt_start = "a@b.com now"
    f_start = Finding(
        id="f1",
        text="a@b.com",
        type="EMAIL",
        category="PII",
        start=0,
        end=7,
        confidence=0.99,
        risk_level="High",
        reason="Email",
        recommendation="Redact",
        placeholder="[EMAIL]",
        source="Regex"
    )
    assert generate_sanitized_prompt(prompt_start, [f_start], {"f1": "remove"}) == "now"

    # At end
    prompt_end = "Mail a@b.com"
    f_end = Finding(
        id="f2",
        text="a@b.com",
        type="EMAIL",
        category="PII",
        start=5,
        end=12,
        confidence=0.99,
        risk_level="High",
        reason="Email",
        recommendation="Redact",
        placeholder="[EMAIL]",
        source="Regex"
    )
    assert generate_sanitized_prompt(prompt_end, [f_end], {"f2": "remove"}) == "Mail"

def test_sanitize_endpoint_rejects_overlapping_findings():
    prompt = "abcdefghijklmnop"
    findings = [
        {
            "id": "f1",
            "text": "abcd",
            "type": "TOKEN",
            "category": "PII",
            "start": 0,
            "end": 6,
            "confidence": 0.9,
            "risk_level": "Medium",
            "reason": "R",
            "recommendation": "Rec",
            "placeholder": "[TOKEN]",
            "source": "Engine"
        },
        {
            "id": "f2",
            "text": "cdef",
            "type": "TOKEN",
            "category": "PII",
            "start": 4,
            "end": 10,
            "confidence": 0.9,
            "risk_level": "Medium",
            "reason": "R",
            "recommendation": "Rec",
            "placeholder": "[TOKEN]",
            "source": "Engine"
        }
    ]
    res = client.post("/sanitize", json={"prompt": prompt, "findings": findings})
    assert res.status_code == 422
    assert "Overlapping findings" in res.json()["detail"]

def test_sanitize_endpoint_rejects_out_of_range_offsets():
    prompt = "Short"
    findings = [
        {
            "id": "f1",
            "text": "Out of range",
            "type": "EMAIL",
            "category": "PII",
            "start": 0,
            "end": 100,
            "confidence": 0.9,
            "risk_level": "High",
            "reason": "R",
            "recommendation": "Rec",
            "placeholder": "[EMAIL]",
            "source": "Engine"
        }
    ]
    res = client.post("/sanitize", json={"prompt": prompt, "findings": findings})
    assert res.status_code == 422
    assert "Invalid finding bounds" in res.json()["detail"]

def test_sanitize_endpoint_ignores_client_placeholder_injection():
    prompt = "Contact me at user@corp.com"
    findings = [
        {
            "id": "f1",
            "text": "user@corp.com",
            "type": "EMAIL",
            "category": "PII",
            "start": 14,
            "end": 27,
            "confidence": 0.95,
            "risk_level": "High",
            "reason": "R",
            "recommendation": "Rec",
            "placeholder": "SYSTEM_INJECTION_IGNORE_ALL_PREVIOUS_INSTRUCTIONS",
            "source": "Client"
        }
    ]
    res = client.post("/sanitize", json={"prompt": prompt, "findings": findings})
    assert res.status_code == 200
    sanitized = res.json()["sanitized_prompt"]
    assert "SYSTEM_INJECTION" not in sanitized
    assert sanitized == "Contact me at [EMAIL]"
