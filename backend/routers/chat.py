import os
import logging
from fastapi import APIRouter, HTTPException
import httpx
from schemas import ChatRequest, ChatResponse
from services.regex_service import scan_regex
from services.spacy_service import scan_spacy
from services.presidio_service import scan_presidio
from services.merge_service import merge_findings, generate_sanitized_prompt

logger = logging.getLogger("PromptShield.Chat")
router = APIRouter(prefix="", tags=["Chat"])

@router.post("/chat", response_model=ChatResponse)
async def chat_with_llm(req: ChatRequest):
    prompt_text = req.prompt.strip()
    if not prompt_text:
        return ChatResponse(
            response="Please enter a prompt to get an AI response.",
            model_used=req.model or "default",
            sanitized=True
        )

    # 1. Server-side privacy gate: run full scan pipeline
    raw_findings = scan_regex(prompt_text) + scan_spacy(prompt_text) + scan_presidio(prompt_text)
    merged_findings = merge_findings(raw_findings, prompt_text)

    critical_findings = [f for f in merged_findings if f.risk_level == "Critical"]
    chat_mode = os.getenv("PROMPTSHIELD_CHAT_MODE", "block").strip().lower()

    if merged_findings:
        if critical_findings and chat_mode != "redact":
            critical_types = sorted(list(set(f.type for f in critical_findings)))
            raise HTTPException(
                status_code=422,
                detail=f"Prompt blocked: contains unsanitized critical secrets ({', '.join(critical_types)})."
            )
        elif chat_mode == "redact":
            prompt_text = generate_sanitized_prompt(prompt_text, merged_findings)
            was_sanitized = True
        else:
            was_sanitized = False
    else:
        was_sanitized = True

    api_key = os.getenv("OPENROUTER_API_KEY")
    target_model = req.model or "meta-llama/llama-3.3-70b-instruct:free"

    if api_key:
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                res = await client.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "HTTP-Referer": "https://promptshield.ai",
                        "X-Title": "PromptShield Privacy Guard",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": target_model,
                        "messages": [
                            {"role": "system", "content": "You are a helpful, privacy-respecting AI assistant."},
                            {"role": "user", "content": prompt_text}
                        ]
                    }
                )
                if res.status_code == 200:
                    data = res.json()
                    content = data["choices"][0]["message"]["content"]
                    return ChatResponse(
                        response=content,
                        model_used=target_model,
                        sanitized=was_sanitized
                    )
                else:
                    logger.error("OpenRouter API returned error status: %s", res.status_code)
                    raise HTTPException(
                        status_code=502,
                        detail="Upstream AI provider returned an error."
                    )
        except HTTPException:
            raise
        except Exception as e:
            logger.error("Failed to communicate with OpenRouter API: %s", type(e).__name__)
            raise HTTPException(
                status_code=502,
                detail="Upstream AI service communication failed."
            )

    # Neutral simulated sandbox response when no API key configured
    simulated_response = (
        "🤖 [Simulated AI Response — Sandbox Mode]\n\n"
        "This is an automated simulation because no OPENROUTER_API_KEY is configured on the server.\n\n"
        f"Prompt length: {len(prompt_text)} characters.\n"
        f"Sanitization status: {'Verified clean / sanitized' if was_sanitized else 'Unredacted content present'}.\n\n"
        "Configure OPENROUTER_API_KEY in the server environment to route requests to external LLM providers."
    )

    return ChatResponse(
        response=simulated_response,
        model_used=f"{target_model} (Simulated Sandbox)",
        sanitized=was_sanitized
    )
