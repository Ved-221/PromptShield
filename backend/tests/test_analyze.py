import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add backend directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import app

client = TestClient(app)

def test_analyze_clean_prompt():
    response = client.post("/analyze", json={"prompt": "How do I reverse a binary tree in Python?"})
    assert response.status_code == 200
    data = response.json()
    assert data["privacy_score"] == 100
    assert data["risk_level"] == "Safe"
    assert len(data["findings"]) == 0
    assert data["sanitized_prompt"] == "How do I reverse a binary tree in Python?"

def test_analyze_sensitive_prompt():
    sensitive_prompt = (
        "Hi my name is John Doe, email john.doe@example.com and phone +1-555-0199. "
        "My OpenAI key is sk-proj-1234567890abcdef1234567890abcdef. "
        "DB URL postgresql://admin:secret123@db.internal:5432/prod"
    )
    response = client.post("/analyze", json={"prompt": sensitive_prompt})
    assert response.status_code == 200
    data = response.json()
    assert data["privacy_score"] < 60
    assert data["risk_level"] in ["High", "Critical"]
    assert len(data["findings"]) >= 3

    types = [f["type"] for f in data["findings"]]
    assert "EMAIL" in types
    assert "OPENAI_KEY" in types
    assert "[EMAIL]" in data["sanitized_prompt"]
    assert "[OPENAI_API_KEY]" in data["sanitized_prompt"]

def test_sanitize_override():
    sensitive_prompt = "Contact me at alice@company.com"
    resp_analyze = client.post("/analyze", json={"prompt": sensitive_prompt})
    data = resp_analyze.json()
    finding_id = data["findings"][0]["id"]

    # Test "keep" override
    resp_keep = client.post("/sanitize", json={
        "prompt": sensitive_prompt,
        "findings": data["findings"],
        "actions": {finding_id: "keep"}
    })
    assert resp_keep.json()["sanitized_prompt"] == sensitive_prompt

    # Test "remove" override
    resp_remove = client.post("/sanitize", json={
        "prompt": sensitive_prompt,
        "findings": data["findings"],
        "actions": {finding_id: "remove"}
    })
    assert "alice@company.com" not in resp_remove.json()["sanitized_prompt"]

def test_chat_endpoint():
    response = client.post("/chat", json={"prompt": "Hello AI!"})
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert data["sanitized"] is True
