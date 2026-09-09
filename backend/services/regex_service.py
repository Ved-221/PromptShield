import re
from typing import List, Dict, Any

REGEX_PATTERNS: List[Dict[str, Any]] = [
    {
        "type": "EMAIL",
        "category": "PII",
        "pattern": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
        "risk_level": "High",
        "confidence": 0.98,
        "reason": "Contains an email address which exposes personal contact details.",
        "recommendation": "Replace with generic placeholder or remove.",
        "placeholder": "[EMAIL]"
    },
    {
        "type": "PHONE",
        "category": "PII",
        "pattern": r"(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b",
        "risk_level": "High",
        "confidence": 0.95,
        "reason": "Contains a phone number.",
        "recommendation": "Replace with generic phone placeholder.",
        "placeholder": "[PHONE_NUMBER]"
    },
    {
        "type": "CREDIT_CARD",
        "category": "Financial",
        "pattern": r"\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|6(?:011|5[0-9][0-9])[0-9]{12}|3[47][0-9]{13}|3(?:0[0-5]|[68][0-9])[0-9]{11}|(?:2131|1800|35\d{3})\d{11})\b",
        "risk_level": "Critical",
        "confidence": 0.99,
        "reason": "Detected credit or debit card number string.",
        "recommendation": "Never share card numbers with AI services. Remove immediately.",
        "placeholder": "[CREDIT_CARD]"
    },
    {
        "type": "OPENAI_KEY",
        "category": "Authentication",
        "pattern": r"\bsk-(?:proj-)?[a-zA-Z0-9_-]{32,64}\b",
        "risk_level": "Critical",
        "confidence": 1.0,
        "reason": "Detected OpenAI API Secret Key.",
        "recommendation": "Remove key immediately before sending to prevent key compromise.",
        "placeholder": "[OPENAI_API_KEY]"
    },
    {
        "type": "AWS_KEY",
        "category": "Authentication",
        "pattern": r"\b(AKIA|ASIA)[0-9A-Z]{16}\b",
        "risk_level": "Critical",
        "confidence": 1.0,
        "reason": "Detected AWS Access Key ID.",
        "recommendation": "Remove credential to avoid unauthorized cloud resource usage.",
        "placeholder": "[AWS_ACCESS_KEY]"
    },
    {
        "type": "GITHUB_TOKEN",
        "category": "Authentication",
        "pattern": r"\b(?:ghp_[a-zA-Z0-9]{36}|github_pat_[a-zA-Z0-9]{22}_[a-zA-Z0-9]{59})\b",
        "risk_level": "Critical",
        "confidence": 1.0,
        "reason": "Detected GitHub Personal Access Token.",
        "recommendation": "Remove token to protect code repositories.",
        "placeholder": "[GITHUB_TOKEN]"
    },
    {
        "type": "JWT_TOKEN",
        "category": "Authentication",
        "pattern": r"\beyJ[a-zA-Z0-9_-]{10,}\.eyJ[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9_-]{10,}\b",
        "risk_level": "Critical",
        "confidence": 0.99,
        "reason": "Detected JSON Web Token (JWT) bearer token.",
        "recommendation": "Sanitize auth tokens from prompts.",
        "placeholder": "[JWT_TOKEN]"
    },
    {
        "type": "PRIVATE_KEY",
        "category": "Authentication",
        "pattern": r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----[\s\S]*?-----END (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
        "risk_level": "Critical",
        "confidence": 1.0,
        "reason": "Detected Private Cryptographic Key block.",
        "recommendation": "Remove private key data completely.",
        "placeholder": "[PRIVATE_KEY]"
    },
    {
        "type": "DATABASE_URL",
        "category": "Technical",
        "pattern": r"\b(?:postgres|postgresql|mysql|mongodb|redis|oracle|mssql):\/\/[a-zA-Z0-9_.-]+:[^@\s]+@[a-zA-Z0-9_.-]+:[0-9]+\/[a-zA-Z0-9_.-]+\b",
        "risk_level": "Critical",
        "confidence": 0.98,
        "reason": "Detected Database Connection URL containing username and password.",
        "recommendation": "Redact database connection strings.",
        "placeholder": "[DATABASE_URL]"
    },
    {
        "type": "PASSWORD_IN_TEXT",
        "category": "Authentication",
        "pattern": r"(?i)\b(?:password|passwd|pwd|secret_key|api_secret)\s*[:=]\s*['\"]?([^\s'\"]{4,})['\"]?",
        "risk_level": "Critical",
        "confidence": 0.92,
        "reason": "Detected password or secret assignment in key-value format.",
        "recommendation": "Remove plain-text passwords.",
        "placeholder": "[PASSWORD]"
    },
    {
        "type": "SSN",
        "category": "PII",
        "pattern": r"\b\d{3}-\d{2}-\d{4}\b",
        "risk_level": "Critical",
        "confidence": 0.95,
        "reason": "Detected US Social Security Number.",
        "recommendation": "Remove SSN to preserve identity privacy.",
        "placeholder": "[SSN]"
    },
    {
        "type": "AADHAAR",
        "category": "PII",
        "pattern": r"\b[2-9]{1}\d{3}\s?\d{4}\s?\d{4}\b",
        "risk_level": "Critical",
        "confidence": 0.90,
        "reason": "Detected 12-digit Indian Aadhaar number format.",
        "recommendation": "Redact government identification numbers.",
        "placeholder": "[AADHAAR_NUMBER]"
    },
    {
        "type": "PAN",
        "category": "PII",
        "pattern": r"\b[A-Z]{5}[0-9]{4}[A-Z]{1}\b",
        "risk_level": "High",
        "confidence": 0.95,
        "reason": "Detected Indian PAN Card number format.",
        "recommendation": "Replace PAN identifier with placeholder.",
        "placeholder": "[PAN_NUMBER]"
    },
    {
        "type": "UPI_ID",
        "category": "Financial",
        "pattern": r"\b[a-zA-Z0-9.\-_]{2,256}@(?:upi|ybl|axl|icici|paytm|okaxis|okicici|oksbi|sbi|hdfcbank|ibl)\b",
        "risk_level": "High",
        "confidence": 0.95,
        "reason": "Detected Indian UPI Payment ID.",
        "recommendation": "Redact financial payment address.",
        "placeholder": "[UPI_ID]"
    },
    {
        "type": "IP_ADDRESS",
        "category": "Technical",
        "pattern": r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b",
        "risk_level": "Medium",
        "confidence": 0.90,
        "reason": "Detected IPv4 address string.",
        "recommendation": "Replace host IP addresses with placeholders.",
        "placeholder": "[IP_ADDRESS]"
    }
]

def scan_regex(text: str) -> List[Dict[str, Any]]:
    findings = []
    idx = 0
    for rule in REGEX_PATTERNS:
        matches = re.finditer(rule["pattern"], text)
        for m in matches:
            # Handle full match or capture group if password assignment match
            matched_text = m.group(0)
            start_pos = m.start()
            end_pos = m.end()

            # Skip common local IP if needed, or keep
            if rule["type"] == "IP_ADDRESS" and matched_text in ("127.0.0.1", "0.0.0.0"):
                continue

            findings.append({
                "id": f"regex_{idx}",
                "text": matched_text,
                "type": rule["type"],
                "category": rule["category"],
                "start": start_pos,
                "end": end_pos,
                "confidence": rule["confidence"],
                "risk_level": rule["risk_level"],
                "reason": rule["reason"],
                "recommendation": rule["recommendation"],
                "placeholder": rule["placeholder"],
                "source": "Regex Engine"
            })
            idx += 1
    return findings
