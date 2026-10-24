import pytest
from services.validators import luhn_ok, verhoeff_ok

# ==================== Luhn Checksum Tests ====================

def test_luhn_valid_cards():
    # Standard 16-digit Visa test card
    assert luhn_ok("4111 1111 1111 1111") is True
    assert luhn_ok("4111111111111111") is True
    # Valid 16-digit card
    assert luhn_ok("4532 0150 1234 5671") is True
    assert luhn_ok("4532-0150-1234-5671") is True

def test_luhn_invalid_cards():
    # One digit altered
    assert luhn_ok("4111 1111 1111 1112") is False
    assert luhn_ok("4532 0150 1234 5674") is False
    # Non-digit / too short
    assert luhn_ok("123456") is False
    assert luhn_ok("") is False
    assert luhn_ok("not_a_number") is False

# ==================== Verhoeff Checksum Tests ====================

def test_verhoeff_valid_aadhaar():
    # Valid 12-digit Aadhaar number with correct Verhoeff check digit (4)
    assert verhoeff_ok("2345 6789 0124") is True
    assert verhoeff_ok("234567890124") is True
    assert verhoeff_ok("2345-6789-0124") is True

def test_verhoeff_invalid_aadhaar():
    # Altered check digit (3 instead of 4)
    assert verhoeff_ok("2345 6789 0123") is False
    # Starts with 0 or 1 (not allowed for Indian Aadhaar)
    assert verhoeff_ok("0345 6789 0124") is False
    assert verhoeff_ok("1345 6789 0124") is False
    # Wrong length
    assert verhoeff_ok("2345 6789") is False
    assert verhoeff_ok("") is False
    assert verhoeff_ok("abcdefghijkl") is False
