from .observability import traced
"""Server-side owner-authorized profile matching. Never call from public visitor endpoints."""
import json,os,re,unicodedata,hmac
from pathlib import Path
from fastapi import APIRouter,Header,HTTPException
from .private_invites import profiles
router=APIRouter()
def norm(s):
 s=unicodedata.normalize('NFKC',str(s or '')).casefold()
 return ' '.join(re.findall(r'[^\W_]+',s,flags=re.UNICODE))
@traced('profile.match', service='private-profile-lookup')
def match_profiles(name):
 key=norm(name)
 if len(key)<2:return []
 found=[]
 for p in profiles():
  aliases=p.get('aliases') or []
  if isinstance(aliases,str):aliases=[aliases]
  variants={norm(p.get('name','')),*[norm(a) for a in aliases if isinstance(a,str)]}
  if key in variants:found.append(p)
 return found
@router.get('/api/owner/profiles/lookup')
def lookup(name:str,x_owner_token:str|None=Header(default=None)):
 secret=os.getenv('WEDDING_OWNER_TOKEN','')
 if len(secret)<32 or not x_owner_token or not hmac.compare_digest(secret,x_owner_token):
  raise HTTPException(403,'Owner authorization required')
 matches=match_profiles(name)
 return {'matches':[{'id':p['id'],'name':p['name'],'aliases':p.get('aliases',[]),'relation':p.get('relation','')} for p in matches], 'ambiguous':len(matches)>1}
