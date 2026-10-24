import pytest
from services.merge_service import merge_findings

def test_merge_contained_span():
    prompt = "The customer email is john.doe@example.com."
    raw = [
        {
            "id": "det1",
            "text": "john.doe@example.com",
            "type": "EMAIL",
            "category": "PII",
            "start": 22,
            "end": 42,
            "confidence": 0.95,
            "risk_level": "High",
            "reason": "Email address",
            "recommendation": "Redact",
            "placeholder": "[EMAIL]",
            "source": "Regex Engine"
        },
        {
            "id": "det2",
            "text": "doe",
            "type": "PERSON",
            "category": "PII",
            "start": 27,
            "end": 30,
            "confidence": 0.85,
            "risk_level": "Medium",
            "reason": "Person name",
            "recommendation": "Redact",
            "placeholder": "[PERSON]",
            "source": "spaCy NER"
        }
    ]
    merged = merge_findings(raw, prompt)
    assert len(merged) == 1
    f = merged[0]
    assert f.start == 22
    assert f.end == 42
    assert f.text == "john.doe@example.com"
    assert f.risk_level == "High"
    assert f.type == "EMAIL"
    assert "Regex Engine" in f.source
    assert "spaCy NER" in f.source

def test_merge_partial_overlap():
    prompt = "abcdefghijklmnopqrstuvwxyz0123456789"
    # Finding 1: High at [0, 20)
    # Finding 2: Critical at [15, 40)
    raw = [
        {
            "id": "f1",
            "text": prompt[0:20],
            "type": "TOKEN",
            "category": "Authentication",
            "start": 0,
            "end": 20,
            "confidence": 0.90,
            "risk_level": "High",
            "reason": "Token substring",
            "recommendation": "Redact",
            "placeholder": "[TOKEN]",
            "source": "Regex Engine"
        },
        {
            "id": "f2",
            "text": prompt[15:35],
            "type": "OPENAI_KEY",
            "category": "Authentication",
            "start": 15,
            "end": 35,
            "confidence": 0.99,
            "risk_level": "Critical",
            "reason": "OpenAI Secret Key",
            "recommendation": "Remove immediately",
            "placeholder": "[OPENAI_API_KEY]",
            "source": "Presidio Engine"
        }
    ]
    merged = merge_findings(raw, prompt)
    assert len(merged) == 1
    f = merged[0]
    assert f.start == 0
    assert f.end == 35
    assert f.text == prompt[0:35]
    assert f.risk_level == "Critical"
    assert f.type == "OPENAI_KEY"
    assert f.source == "Regex Engine + Presidio Engine"

def test_merge_chain_of_three():
    prompt = "0123456789012345678901234567890123456789"
    raw = [
        {
            "id": "a",
            "text": prompt[0:10],
            "type": "TYPE_A",
            "category": "PII",
            "start": 0,
            "end": 10,
            "confidence": 0.8,
            "risk_level": "Low",
            "reason": "Reason A",
            "recommendation": "Rec A",
            "placeholder": "[TYPE_A]",
            "source": "Detector A"
        },
        {
            "id": "b",
            "text": prompt[8:20],
            "type": "TYPE_B",
            "category": "PII",
            "start": 8,
            "end": 20,
            "confidence": 0.85,
            "risk_level": "Medium",
            "reason": "Reason B",
            "recommendation": "Rec B",
            "placeholder": "[TYPE_B]",
            "source": "Detector B"
        },
        {
            "id": "c",
            "text": prompt[18:30],
            "type": "TYPE_C",
            "category": "PII",
            "start": 18,
            "end": 30,
            "confidence": 0.95,
            "risk_level": "High",
            "reason": "Reason C",
            "recommendation": "Rec C",
            "placeholder": "[TYPE_C]",
            "source": "Detector C"
        }
    ]
    merged = merge_findings(raw, prompt)
    assert len(merged) == 1
    f = merged[0]
    assert f.start == 0
    assert f.end == 30
    assert f.text == prompt[0:30]
    assert f.risk_level == "High"
    assert f.type == "TYPE_C"
    assert f.source == "Detector A + Detector B + Detector C"

def test_merge_identical_duplicates_across_different_positions():
    prompt = "Email me at user@test.com or copy user@test.com and user@test.com."
    raw = [
        {
            "id": "e1",
            "text": "user@test.com",
            "type": "EMAIL",
            "category": "PII",
            "start": 12,
            "end": 25,
            "confidence": 0.98,
            "risk_level": "High",
            "reason": "Email",
            "recommendation": "Redact",
            "placeholder": "[EMAIL]",
            "source": "Regex"
        },
        {
            "id": "e2",
            "text": "user@test.com",
            "type": "EMAIL",
            "category": "PII",
            "start": 34,
            "end": 47,
            "confidence": 0.98,
            "risk_level": "High",
            "reason": "Email",
            "recommendation": "Redact",
            "placeholder": "[EMAIL]",
            "source": "Regex"
        },
        {
            "id": "e3",
            "text": "user@test.com",
            "type": "EMAIL",
            "category": "PII",
            "start": 52,
            "end": 65,
            "confidence": 0.98,
            "risk_level": "High",
            "reason": "Email",
            "recommendation": "Redact",
            "placeholder": "[EMAIL]",
            "source": "Regex"
        }
    ]
    merged = merge_findings(raw, prompt)
    assert len(merged) == 3
    assert merged[0].start == 12 and merged[0].end == 25
    assert merged[1].start == 34 and merged[1].end == 47
    assert merged[2].start == 52 and merged[2].end == 65

def test_merge_same_position_duplicate_collapses_with_joined_sources():
    prompt = "Contact: user@test.com"
    raw = [
        {
            "id": "r1",
            "text": "user@test.com",
            "type": "EMAIL",
            "category": "PII",
            "start": 9,
            "end": 22,
            "confidence": 0.95,
            "risk_level": "High",
            "reason": "Regex Email",
            "recommendation": "Redact",
            "placeholder": "[EMAIL]",
            "source": "Regex Engine"
        },
        {
            "id": "r2",
            "text": "user@test.com",
            "type": "EMAIL",
            "category": "PII",
            "start": 9,
            "end": 22,
            "confidence": 0.97,
            "risk_level": "High",
            "reason": "Presidio Email",
            "recommendation": "Redact",
            "placeholder": "[EMAIL]",
            "source": "Microsoft Presidio"
        }
    ]
    merged = merge_findings(raw, prompt)
    assert len(merged) == 1
    assert merged[0].confidence == 0.97
    assert merged[0].source == "Regex Engine + Microsoft Presidio"

def test_merge_non_overlapping_untouched():
    prompt = "Alpha 1234 Beta 5678"
    raw = [
        {
            "id": "a",
            "text": "1234",
            "type": "PIN",
            "category": "Auth",
            "start": 6,
            "end": 10,
            "confidence": 0.9,
            "risk_level": "Medium",
            "reason": "PIN",
            "recommendation": "Redact",
            "placeholder": "[PIN]",
            "source": "Engine"
        },
        {
            "id": "b",
            "text": "5678",
            "type": "PIN",
            "category": "Auth",
            "start": 16,
            "end": 20,
            "confidence": 0.9,
            "risk_level": "Medium",
            "reason": "PIN",
            "recommendation": "Redact",
            "placeholder": "[PIN]",
            "source": "Engine"
        }
    ]
    merged = merge_findings(raw, prompt)
    assert len(merged) == 2
    assert merged[0].start == 6 and merged[0].end == 10
    assert merged[1].start == 16 and merged[1].end == 20

def test_sanitization_whitespace_normalization():
    from services.merge_service import generate_sanitized_prompt
    from schemas import Finding

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

def test_sanitization_remove_at_start_and_end():
    from services.merge_service import generate_sanitized_prompt
    from schemas import Finding

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

