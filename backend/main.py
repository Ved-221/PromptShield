import os
import logging
from contextlib import asynccontextmanager
import uvicorn
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import analyze, chat
from services.spacy_service import preload_spacy_model
from services.presidio_service import preload_presidio_analyzer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("PromptShield")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up PromptShield backend...")
    spacy_ok = preload_spacy_model()
    if not spacy_ok:
        logger.error("CRITICAL: spaCy model preload failed; NER scanning will be non-functional.")

    presidio_ok = preload_presidio_analyzer()
    if not presidio_ok:
        logger.error("CRITICAL: Presidio AnalyzerEngine preload failed; PII scanning will be non-functional.")

    yield
    logger.info("PromptShield backend shutting down.")

app = FastAPI(
    title="PromptShield — AI Privacy Layer API",
    description="Real-time prompt scanning, PII/Credential redaction, risk scoring, and LLM proxy.",
    version="1.0.0",
    lifespan=lifespan
)

# Parse allowed origins from environment
allowed_origins_env = os.getenv("PROMPTSHIELD_ALLOWED_ORIGINS", "http://localhost:3000")
allowed_origins = [o.strip() for o in allowed_origins_env.split(",") if o.strip()]

# Enable CORS safely without combining wildcard with credentials
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analyze.router)
app.include_router(chat.router)

@app.get("/")
async def root():
    return {
        "status": "online",
        "app": "PromptShield AI Privacy Layer API",
        "version": "1.0.0",
        "endpoints": ["/analyze", "/sanitize", "/chat"]
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
