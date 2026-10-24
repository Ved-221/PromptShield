import pytest
from fastapi.testclient import TestClient
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from main import app

client = TestClient(app)

def test_chat_blocks_critical_finding_in_block_mode(monkeypatch):
    monkeypatch.setenv("PROMPTSHIELD_CHAT_MODE", "block")
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)

    secret = "sk-proj-1234567890abcdef1234567890abcdef"
    prompt = f"Please debug my code with API key: {secret}"

    res = client.post("/chat", json={"prompt": prompt})
    assert res.status_code == 422
    data = res.json()
    assert "Prompt blocked" in data["detail"]
    assert "OPENAI_KEY" in data["detail"]
    # Ensure raw secret is NEVER leaked in error message
    assert secret not in data["detail"]

def test_chat_auto_redacts_in_redact_mode(monkeypatch):
    monkeypatch.setenv("PROMPTSHIELD_CHAT_MODE", "redact")
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)

    secret = "sk-proj-1234567890abcdef1234567890abcdef"
    prompt = f"Please debug with key {secret} now."

    res = client.post("/chat", json={"prompt": prompt})
    assert res.status_code == 200
    data = res.json()
    assert data["sanitized"] is True
    # The simulated sandbox response should NOT contain raw secret
    assert secret not in data["response"]

def test_chat_clean_prompt_succeeds(monkeypatch):
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)

    res = client.post("/chat", json={"prompt": "How to sort a list in Python?"})
    assert res.status_code == 200
    data = res.json()
    assert data["sanitized"] is True
    assert "Simulated Sandbox" in data["model_used"]

def test_chat_sandbox_fallback_is_neutral_and_simulated(monkeypatch):
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)

    res = client.post("/chat", json={"prompt": "Write a poem about privacy."})
    assert res.status_code == 200
    resp_text = res.json()["response"]
    assert "Simulated AI Response — Sandbox Mode" in resp_text
    # Must NOT claim false privacy guarantee
    assert "All personal identifiers, credentials, and sensitive tokens were safely masked" not in resp_text
