import logging
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import analyze, chat

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("PromptShield")

app = FastAPI(
    title="PromptShield — AI Privacy Layer API",
    description="Real-time prompt scanning, PII/Credential redaction, risk scoring, and LLM proxy.",
    version="1.0.0"
)

# Enable CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
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
