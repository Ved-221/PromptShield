from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)
logging.getLogger("presidio-analyzer").setLevel(logging.ERROR)

analyzer = None

def get_presidio_analyzer():
    global analyzer
    if analyzer is not None:
        return analyzer
    try:
        from presidio_analyzer import AnalyzerEngine
        from presidio_analyzer.nlp_engine import NlpEngineProvider

        nlp_config = {
            "nlp_engine_name": "spacy",
            "models": [{"lang_code": "en", "model_name": "en_core_web_sm"}]
        }
        provider = NlpEngineProvider(nlp_configuration=nlp_config)
        nlp_engine = provider.create_engine()
        analyzer = AnalyzerEngine(nlp_engine=nlp_engine)
    except Exception as e:
        logger.warning(f"Presidio AnalyzerEngine initialization failed or presidio not installed: {e}")
        try:
            from presidio_analyzer import AnalyzerEngine
            analyzer = AnalyzerEngine()
        except Exception as ex:
            logger.error(f"Fallback Presidio initialization failed: {ex}")
            analyzer = None
    return analyzer

PRESIDIO_MAP = {
    "EMAIL_ADDRESS": ("EMAIL", "PII", "High", "[EMAIL]", "Detected email address via Presidio."),
    "PHONE_NUMBER": ("PHONE", "PII", "High", "[PHONE_NUMBER]", "Detected phone number via Presidio."),
    "PERSON": ("PERSON", "PII", "Medium", "[PERSON]", "Detected personal name via Presidio."),
    "CREDIT_CARD": ("CREDIT_CARD", "Financial", "Critical", "[CREDIT_CARD]", "Detected credit card number via Presidio."),
    "CRYPTO": ("CRYPTO_ADDRESS", "Financial", "High", "[CRYPTO_ADDRESS]", "Detected crypto wallet address."),
    "IBAN_CODE": ("IBAN", "Financial", "High", "[IBAN]", "Detected International Bank Account Number."),
    "IP_ADDRESS": ("IP_ADDRESS", "Technical", "Medium", "[IP_ADDRESS]", "Detected IP address."),
    "US_SSN": ("SSN", "PII", "Critical", "[SSN]", "Detected US Social Security Number."),
    "LOCATION": ("LOCATION", "PII", "Low", "[LOCATION]", "Detected location description.")
}

COMMON_TECH_TERMS = {
    "python", "java", "c++", "c#", "javascript", "typescript", "html", "css", "sql",
    "react", "vue", "angular", "node", "nodejs", "git", "docker", "kubernetes",
    "linux", "macos", "windows", "aws", "azure", "gcp", "bash", "zsh", "fastapi",
    "flask", "django", "postgres", "postgresql", "mysql", "mongodb", "redis"
}

def scan_presidio(text: str) -> List[Dict[str, Any]]:
    engine = get_presidio_analyzer()
    if not engine:
        return []

    try:
        results = engine.analyze(text=text, language="en")
        findings = []
        idx = 0
        for res in results:
            entity_type = res.entity_type
            matched_text = text[res.start:res.end]
            if matched_text.strip().lower() in COMMON_TECH_TERMS:
                continue

            if entity_type in PRESIDIO_MAP:
                t_type, category, risk, placeholder, reason = PRESIDIO_MAP[entity_type]
            else:
                t_type = entity_type
                category = "PII"
                risk = "Medium"
                placeholder = f"[{entity_type}]"
                reason = f"Detected {entity_type} entity."

            findings.append({
                "id": f"presidio_{idx}",
                "text": matched_text,
                "type": t_type,
                "category": category,
                "start": res.start,
                "end": res.end,
                "confidence": round(float(res.score), 2),
                "risk_level": risk,
                "reason": reason,
                "recommendation": f"Replace {t_type} with placeholder {placeholder}.",
                "placeholder": placeholder,
                "source": "Microsoft Presidio"
            })
            idx += 1
        return findings
    except Exception as ex:
        logger.error(f"Error during Presidio scan: {ex}")
        return []
