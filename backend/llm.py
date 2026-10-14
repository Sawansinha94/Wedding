from fastapi import HTTPException
from backend.ai_fallback import generate, AIProviderError

async def llm(system: str, user: str) -> str:
    try:
        return await generate([{'role': 'system', 'content': system}, {'role': 'user', 'content': user}], temperature=0.6, max_tokens=350)
    except AIProviderError as exc:
        raise HTTPException(502, 'AI providers temporarily unavailable') from exc

async def model_messages(messages, *, temperature=0.25, max_tokens=500):
    try:
        return await generate(messages, temperature=temperature, max_tokens=max_tokens)
    except AIProviderError as exc:
        raise HTTPException(502, 'AI providers temporarily unavailable') from exc
