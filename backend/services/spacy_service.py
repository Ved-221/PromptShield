import spacy
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

nlp = None

def get_spacy_model():
    global nlp
    if nlp is not None:
        return nlp
    
    try:
        nlp = spacy.load("en_core_web_sm")
    except Exception as e:
        logger.warning(f"Could not load spacy en_core_web_sm model: {e}. Attempting download or fallback...")
        try:
            # pyrefly: ignore [missing-import]
            from spacy.cli import download
            download("en_core_web_sm")
            nlp = spacy.load("en_core_web_sm")
        except Exception as ex:
            logger.error(f"Failed to download en_core_web_sm: {ex}")
            nlp = None
    return nlp

ENTITY_CATEGORY_MAP = {
    "PERSON": ("PII", "Medium", "Name of an individual.", "Replace with [PERSON] placeholder."),
    "ORG": ("Organization", "Medium", "Name of a company, institution, or organization.", "Replace with [ORGANIZATION] placeholder."),
    "GPE": ("PII", "Low", "Geographical location (city, state, country).", "Replace with [LOCATION] placeholder."),
    "LOC": ("PII", "Low", "Location or landmark.", "Replace with [LOCATION] placeholder."),
    "DATE": ("PII", "Low", "Specific date or time period.", "Replace with [DATE] placeholder."),
    "MONEY": ("Financial", "Medium", "Financial amount or currency.", "Replace with [AMOUNT] placeholder."),
    "NORP": ("PII", "Low", "Nationalities, religious or political groups.", "Replace with [GROUP] placeholder.")
}

PLACEHOLDER_MAP = {
    "PERSON": "[PERSON]",
    "ORG": "[ORGANIZATION]",
    "GPE": "[LOCATION]",
    "LOC": "[LOCATION]",
    "DATE": "[DATE]",
    "MONEY": "[FINANCIAL_AMOUNT]",
    "NORP": "[GROUP]"
}

COMMON_TECH_TERMS = {
    "python", "java", "c++", "c#", "javascript", "typescript", "html", "css", "sql",
    "react", "vue", "angular", "node", "nodejs", "git", "docker", "kubernetes",
    "linux", "macos", "windows", "aws", "azure", "gcp", "bash", "zsh", "fastapi",
    "flask", "django", "postgres", "postgresql", "mysql", "mongodb", "redis"
}

def scan_spacy(text: str) -> List[Dict[str, Any]]:
    model = get_spacy_model()
    if not model:
        return []

    doc = model(text)
    findings = []
    idx = 0

    for ent in doc.ents:
        if ent.label_ in ENTITY_CATEGORY_MAP:
            category, risk_level, reason, recommendation = ENTITY_CATEGORY_MAP[ent.label_]
            placeholder = PLACEHOLDER_MAP.get(ent.label_, f"[{ent.label_}]")

            # Avoid tagging tiny single-word stop words or common tech terms as PERSON/ORG/LOCATION
            if len(ent.text.strip()) <= 1 or ent.text.strip().lower() in COMMON_TECH_TERMS:
                continue

            findings.append({
                "id": f"spacy_{idx}",
                "text": ent.text,
                "type": ent.label_,
                "category": category,
                "start": ent.start_char,
                "end": ent.end_char,
                "confidence": 0.85,
                "risk_level": risk_level,
                "reason": reason,
                "recommendation": recommendation,
                "placeholder": placeholder,
                "source": "spaCy NER"
            })
            idx += 1

    return findings
