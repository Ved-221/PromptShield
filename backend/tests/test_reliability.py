import pytest
from fastapi.testclient import TestClient
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from main import app
from services.rate_limiter import chat_limiter

client = TestClient(app)

def test_input_limits_rejected_over_max():
    # Construct prompt exceeding 20000 chars
    large_prompt = "A" * 20001
    res_analyze = client.post("/analyze", json={"prompt": large_prompt})
    assert res_analyze.status_code == 422

    res_sanitize = client.post("/sanitize", json={"prompt": large_prompt, "findings": []})
    assert res_sanitize.status_code == 422

    res_chat = client.post("/chat", json={"prompt": large_prompt})
    assert res_chat.status_code == 422

def test_chat_rate_limiting(monkeypatch):
    chat_limiter.reset()
    monkeypatch.setenv("PROMPTSHIELD_CHAT_RATE_LIMIT", "5")
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)

    # 5 successful requests
    for i in range(5):
        res = client.post("/chat", json={"prompt": f"Message {i}"})
        assert res.status_code == 200

    # 6th request must trigger HTTP 429
    res_blocked = client.post("/chat", json={"prompt": "Message 6"})
    assert res_blocked.status_code == 429
    assert "Rate limit exceeded" in res_blocked.json()["detail"]
    assert "Retry-After" in res_blocked.headers

    # Reset limiter after test
    chat_limiter.reset()

def test_cors_headers_allowed():
    res = client.options(
        "/analyze",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "POST"
        }
    )
    assert res.headers.get("access-control-allow-origin") == "http://localhost:3000"
    assert res.headers.get("access-control-allow-credentials") == "true"
