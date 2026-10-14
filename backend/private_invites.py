"""Private invite tokens, never exposed through static files. Owner distributes out-of-band."""
import os,json,time,hmac,hashlib,base64
from pathlib import Path
from fastapi import APIRouter,HTTPException
from pydantic import BaseModel,Field
router=APIRouter()
MASTER=Path(__file__).resolve().parent.parent/'data/private/profiles_master.json'
def profiles():
    return json.loads(MASTER.read_text(encoding='utf-8'))
def secret():
    value=os.getenv('CONCIERGE_SIGNING_SECRET','')
    if len(value)<32:raise HTTPException(503,'Invitation service is not configured')
    return value.encode()
def issue(pid,days=45):
    payload={'pid':pid,'exp':int(time.time())+days*86400,'v':1}
    raw=base64.urlsafe_b64encode(json.dumps(payload,separators=(',',':')).encode()).decode().rstrip('=')
    sig=hmac.new(secret(),raw.encode(),hashlib.sha256).hexdigest()
    return raw+'.'+sig
def resolve(token):
    try:
        raw,sig=token.rsplit('.',1)
        if not hmac.compare_digest(sig,hmac.new(secret(),raw.encode(),hashlib.sha256).hexdigest()):return None
        data=json.loads(base64.urlsafe_b64decode(raw+'='*(-len(raw)%4)))
        if data.get('exp',0)<time.time() or data.get('v')!=1:return None
        return next((p for p in profiles() if p['id']==data['pid']),None)
    except (ValueError,TypeError,KeyError,UnicodeError):return None
class Claim(BaseModel):
    code:str=Field(min_length=20,max_length=2000)
@router.post('/api/concierge/invite/claim')
def claim(body:Claim):
    profile=resolve(body.code)
    if not profile:raise HTTPException(403,'Invitation code invalid or expired')
    return {'ok':True,'name':profile['name'],'profile_id':profile['id']}
