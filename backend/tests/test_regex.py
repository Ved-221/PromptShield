import pytest
from services.regex_service import scan_regex
from services.merge_service import generate_sanitized_prompt, merge_findings

# ==================== Key-Value Secrets Tests ====================

def test_key_value_secrets_positive():
    prompt = "Configure DB_PASSWORD=Sup3rS3cret in settings and api_key = 'sk_live_99887766'."
    findings = scan_regex(prompt)
    types = [f["type"] for f in findings]
    assert "PASSWORD_IN_TEXT" in types

    pw_findings = [f for f in findings if f["type"] == "PASSWORD_IN_TEXT"]
    texts = [f["text"] for f in pw_findings]
    assert "Sup3rS3cret" in texts
    assert "sk_live_99887766" in texts

    # Verify that only the value is matched, keeping key name visible
    merged = merge_findings(findings, prompt)
    sanitized = generate_sanitized_prompt(prompt, merged)
    assert "DB_PASSWORD=[PASSWORD]" in sanitized
    assert "api_key = '[PASSWORD]'" in sanitized
    assert "Sup3rS3cret" not in sanitized
    assert "sk_live_99887766" not in sanitized

def test_key_value_secrets_negative():
    # Ordinary prose containing the word password without key-value assignment
    prompt = "Please follow the password policy when creating your account."
    findings = scan_regex(prompt)
    pw_findings = [f for f in findings if f["type"] == "PASSWORD_IN_TEXT"]
    assert len(pw_findings) == 0

# ==================== Bearer Token Tests ====================

def test_bearer_token_positive():
    token = "ya29.a0AfH6SMD_secret1234567890"
    prompt = f"curl -H 'Authorization: Bearer {token}' https://api.internal"
    findings = scan_regex(prompt)
    types = [f["type"] for f in findings]
    assert "BEARER_TOKEN" in types

    bearer_f = [f for f in findings if f["type"] == "BEARER_TOKEN"][0]
    assert bearer_f["text"] == token

    merged = merge_findings(findings, prompt)
    sanitized = generate_sanitized_prompt(prompt, merged)
    assert "Bearer [BEARER_TOKEN]" in sanitized
    assert token not in sanitized

def test_bearer_token_negative():
    # Short token string (< 16 chars)
    prompt = "Authorization: Bearer short123"
    findings = scan_regex(prompt)
    bearer_f = [f for f in findings if f["type"] == "BEARER_TOKEN"]
    assert len(bearer_f) == 0

# ==================== Credit Card Validator Integration ====================

def test_credit_card_luhn_filtered():
    # Valid Visa card passes
    valid_prompt = "Payment card: 4111 1111 1111 1111"
    valid_findings = scan_regex(valid_prompt)
    assert any(f["type"] == "CREDIT_CARD" for f in valid_findings)

    # Invalid Luhn card filtered out
    invalid_prompt = "Fake card: 4111 1111 1111 1112"
    invalid_findings = scan_regex(invalid_prompt)
    assert not any(f["type"] == "CREDIT_CARD" for f in invalid_findings)

# ==================== Aadhaar Verhoeff Integration ====================

def test_aadhaar_verhoeff_filtered():
    # Valid Aadhaar passes
    valid_prompt = "Aadhaar number 2345 6789 0124"
    valid_findings = scan_regex(valid_prompt)
    assert any(f["type"] == "AADHAAR" for f in valid_findings)

    # Invalid Aadhaar filtered out
    invalid_prompt = "Random number 2345 6789 0123"
    invalid_findings = scan_regex(invalid_prompt)
    assert not any(f["type"] == "AADHAAR" for f in invalid_findings)
