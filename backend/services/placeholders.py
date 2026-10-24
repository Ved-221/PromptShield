from typing import Dict

DEFAULT_PLACEHOLDERS: Dict[str, str] = {
    "EMAIL": "[EMAIL]",
    "PHONE": "[PHONE_NUMBER]",
    "CREDIT_CARD": "[CREDIT_CARD]",
    "OPENAI_KEY": "[OPENAI_API_KEY]",
    "AWS_KEY": "[AWS_ACCESS_KEY]",
    "GITHUB_TOKEN": "[GITHUB_TOKEN]",
    "BEARER_TOKEN": "[BEARER_TOKEN]",
    "JWT_TOKEN": "[JWT_TOKEN]",
    "PRIVATE_KEY": "[PRIVATE_KEY]",
    "DATABASE_URL": "[DATABASE_URL]",
    "PASSWORD_IN_TEXT": "[PASSWORD]",
    "PASSWORD": "[PASSWORD]",
    "SECRET": "[SECRET]",
    "SSN": "[SSN]",
    "AADHAAR": "[AADHAAR_NUMBER]",
    "PAN": "[PAN_NUMBER]",
    "UPI_ID": "[UPI_ID]",
    "IP_ADDRESS": "[IP_ADDRESS]",
    "PERSON": "[PERSON]",
    "ORG": "[ORGANIZATION]",
    "GPE": "[LOCATION]",
    "LOC": "[LOCATION]",
    "LOCATION": "[LOCATION]",
    "DATE": "[DATE]",
    "MONEY": "[FINANCIAL_AMOUNT]",
    "NORP": "[GROUP]",
    "CRYPTO_ADDRESS": "[CRYPTO_ADDRESS]",
    "IBAN": "[IBAN]"
}

def get_placeholder(entity_type: str) -> str:
    if not entity_type:
        return "[REDACTED]"
    clean = entity_type.strip()
    if clean in DEFAULT_PLACEHOLDERS:
        return DEFAULT_PLACEHOLDERS[clean]
    upper = clean.upper()
    if upper in DEFAULT_PLACEHOLDERS:
        return DEFAULT_PLACEHOLDERS[upper]
    return f"[{upper}]"
