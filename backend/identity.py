"""Optional, low-assurance knowledge check; not strong authentication."""
import os, json, time, hmac, hashlib, base64, secrets, unicodedata
from pathlib import Path
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field
from .visitor import family_candidates
from .pinecone_store import family_verified_context
router=APIRouter()
ROOT=Path(__file__).resolve().parent.parent
PRIVATE=ROOT/'data/private/identity_questions.json'

def normalize(s):
    return ' '.join(unicodedata.normalize('NFKC',s).casefold().split())

def secret():
    value=os.getenv('CONCIERGE_SIGNING_SECRET','')
    if len(value)<32: raise HTTPException(503,'Verification is not configured')
    return value.encode()

def sign(data):
    raw=base64.urlsafe_b64encode(json.dumps(data,separators=(',',':')).encode()).decode().rstrip('=')
    mac=hmac.new(secret(),raw.encode(),hashlib.sha256).hexdigest()
    return raw+'.'+mac

def verify(token):
    try:
        raw,mac=token.rsplit('.',1)
        if not hmac.compare_digest(hmac.new(secret(),raw.encode(),hashlib.sha256).hexdigest(),mac):raise ValueError()
        data=json.loads(base64.urlsafe_b64decode(raw+'='*(-len(raw)%4)))
        if time.time()>data['exp']:raise ValueError()
        return data
    except (ValueError,KeyError,TypeError):raise HTTPException(403,'Verification expired or invalid')

def questions(pid):
    if not PRIVATE.exists():return []
    records=json.loads(PRIVATE.read_text())
    return records.get(pid,[])[:3]

class Start(BaseModel):
    name:str=Field(max_length=80)
    profile_id:str=Field(max_length=100)
    confirmed:bool
class Answer(BaseModel):
    token:str=Field(max_length=2000)
    answer:str=Field(max_length=300)

@router.post('/api/concierge/verify/start')
def start(body:Start):
    raise HTTPException(403,'Private profile access requires a verified invitation; knowledge questions are disabled')
    if not body.confirmed or body.profile_id not in [p['id'] for p in family_candidates(body.name)]:
        raise HTTPException(403,'No matching confirmed relationship')
    qs=questions(body.profile_id)
    if len(qs)<2 or any(not q.get('question') or not q.get('answer_sha256') for q in qs):
        return {'status':'unavailable','message':'A private verification check has not been configured for this profile. You can still ask me about the wedding.'}
    token=sign({'pid':body.profile_id,'name':normalize(body.name),'i':0,'score':0,'exp':int(time.time())+300})
    return {'status':'question','question':qs[0]['question'],'token':token,'step':1,'total':len(qs)}

@router.post('/api/concierge/verify/answer')
def answer(body:Answer):
    state=verify(body.token);qs=questions(state['pid']);i=state['i']
    if i>=len(qs) or i>=3:raise HTTPException(403,'No more questions')
    # SHA256 answers are not resistant to dictionary attacks; private file must never be public.
    digest=hashlib.sha256(normalize(body.answer).encode()).hexdigest()
    correct=hmac.compare_digest(digest,qs[i]['answer_sha256'])
    score=state['score']+(2 if correct and qs[i].get('strong',False) else 1 if correct else 0)
    if score>=2:
        token=sign({'pid':state['pid'],'verified':True,'exp':int(time.time())+1800})
        try:profile=family_verified_context(state['pid'])
        except Exception:profile={}
        return {'status':'verified','verified_token':token,'special_message':profile.get('special_message',''),
                'greeting': 'Wonderful to have you here! How have you been? 🌸'}
    next_i=i+1
    if next_i>=len(qs) or next_i>=3:
        return {'status':'not_verified','message':'Thank you for trying. We can still chat about the celebrations!'}
    token=sign({'pid':state['pid'],'name':state['name'],'i':next_i,'score':score,'exp':state['exp']})
    return {'status':'question','question':qs[next_i]['question'],'token':token,'step':next_i+1,'total':len(qs)}

def verified_profile(token):
    if not token:return ''
    try:
        data=verify(token)
        return data.get('pid','') if data.get('verified') is True else ''
    except HTTPException:return ''
