"""Translate website UI strings using the already configured OpenRouter model.
Only static site text should be sent. Never send visitor messages, private profiles or form data.
"""
import json, os, re
from functools import lru_cache
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from .llm import model_messages
router=APIRouter()
LANGS={'hi':'Hindi','or':'Odia','te':'Telugu'}
class TranslationRequest(BaseModel):
    language:str
    texts:list[str]=Field(min_length=1,max_length=32)
@lru_cache(maxsize=4096)
def cached_translation(language, source):
    return None
@router.post('/api/site/translate')
async def translate(req:TranslationRequest):
    if req.language not in LANGS:raise HTTPException(400,'Unsupported language')
    if any(len(x)>900 for x in req.texts):raise HTTPException(400,'Text too long')
    # Short UI strings only; no names, user submissions, or personal profile content.
    prompt=('Translate this JSON array of wedding website UI strings into '+LANGS[req.language]+'. '
            'Return ONLY a JSON array of exactly the same length. Preserve proper names Sawan, Pratibha, '
            'addresses, numbers, dates, brand names and symbols accurately. Use natural culturally appropriate wording. '
            'Do not add facts.\n'+json.dumps(req.texts,ensure_ascii=False))
    raw=await model_messages([{'role':'system','content':'You are a professional wedding website localizer. Respond in JSON only.'},
                              {'role':'user','content':prompt}],temperature=0,max_tokens=2200)
    raw=re.sub(r'^```(?:json)?\s*|\s*```$','',raw.strip())
    try:
        data=json.loads(raw)
        if not isinstance(data,list) or len(data)!=len(req.texts) or not all(isinstance(x,str) for x in data):raise ValueError()
    except ValueError:raise HTTPException(502,'Invalid translation response')
    return {'translations':data}
