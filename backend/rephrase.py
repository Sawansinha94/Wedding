"""Rephrase an existing guest-written wish without changing its meaning."""
from fastapi import APIRouter, Request
from pydantic import BaseModel, Field
from .llm import model_messages
from .knowledge import LANG

router = APIRouter()

class RephraseRequest(BaseModel):
    text: str = Field(min_length=2, max_length=2000)
    language: str = 'en'
    tone: str = 'heartfelt'

@router.post('/api/wish/rephrase')
async def rephrase(payload: RephraseRequest, request: Request):
    language=LANG.get(payload.language,'English')
    tone=payload.tone if payload.tone in ('heartfelt','traditional','poetic','funny') else 'heartfelt'
    result=await model_messages([
        {'role':'system','content':f'You are a wedding writing assistant. Rewrite the guest-written text as a polished, warm and grammatically correct wedding wish in {language}, in a {tone} tone. Preserve the guest original meaning, people, names and facts. Do not invent personal details. Return ONLY the rewritten wish; no preface or quotation marks. Maximum 900 characters.'},
        {'role':'user','content':payload.text}
    ],temperature=.35,max_tokens=360)
    from .telemetry import log_activity
    log_activity(request.headers.get('X-Wedding-Session'),'wish_rephrased',payload.language)
    return {'text':result.strip()[:1200]}
