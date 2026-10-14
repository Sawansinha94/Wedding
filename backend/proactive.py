"""Fast, privacy-aware concierge welcome. A browser does not expose its owner's name."""
import difflib
import re
from fastapi import APIRouter
from pydantic import BaseModel, Field
from .visitor import quick_name, family_candidates, validate_name
from .pinecone_store import family_lookup, family_special_message

router = APIRouter()

class WelcomeRequest(BaseModel):
    name: str = Field(default='', max_length=80)
    source: str = Field(default='', max_length=20)

class ConfirmRequest(BaseModel):
    name: str = Field(max_length=80)
    profile_id: str = Field(max_length=100)
    confirmed: bool = False

def comparable(s):
    return re.sub(r'[^\w]', '', s.casefold(), flags=re.UNICODE)

def likely_name_match(input_name, full_name):
    a = comparable(input_name)
    if len(a) < 3:
        return False
    tokens = [comparable(t) for t in full_name.split() if comparable(t) not in {'mr','mrs','ms','smt','shri','late','kumari'}]
    return any(a == t or (len(a)>=4 and len(t)>=4 and difflib.SequenceMatcher(None,a,t).ratio()>=0.86) for t in tokens)

@router.post('/api/concierge/welcome')
async def welcome(body: WelcomeRequest):
    name = ' '.join(body.name.split())
    # No device fingerprinting or inferred identity. No name means no personalized prompt.
    if body.source not in ('rsvp', 'wish', 'welcome') or await validate_name(name) != 'valid':
        return {'matched': False, 'reason': 'no_reliable_name'}
    candidates = family_candidates(name)
    # Search the family vector index only when a plausible visitor name is available
    # and there was no direct directory match. This is NOT a guest-profile lookup.
    if not candidates and len(name)>=4:
        try:
            for profile in family_lookup(name + ' family member wedding bride groom'):
                if likely_name_match(name, str(profile.get('name',''))):
                    candidates.extend([x for x in family_candidates(profile['name']) if x.get('side')==profile.get('side')])
        except Exception:
            pass  # Welcome must not block or break the website when Pinecone is down.
    # Check the candidate's exact Pinecone record ID, not top-k semantic similarity.
    if len(candidates)==1:
        try:
            from pinecone import Pinecone
            import os
            key=os.getenv('PINECONE_API_KEY','').strip()
            host=os.getenv('PINECONE_INDEX_HOST','').strip()
            if not key or not host:
                candidates=[]
            else:
                index=Pinecone(api_key=key).Index(host=host)
                result=index.fetch(ids=[candidates[0]['id']],namespace=os.getenv('PINECONE_NAMESPACE','wedding-family'))
                vectors=result.get('vectors',{}) if isinstance(result,dict) else getattr(result,'vectors',{})
                record=vectors.get(candidates[0]['id']) if vectors else None
                meta=(record.get('metadata',{}) if isinstance(record,dict) else getattr(record,'metadata',{})) if record else {}
                if meta.get('side')!=candidates[0]['side']:
                    candidates=[]
        except Exception:
            candidates=[]
    if len(candidates)!=1:
        return {'matched':False,'reason':'ambiguous' if candidates else 'no_match'}
    person=candidates[0]
    # Name match is not authentication; request relationship confirmation.
    first = name.split()[0]
    relation = person['relation'].split(';')[0].strip()
    relation = re.sub(r"^Groom's ", "Sawan's ", relation, flags=re.I)
    relation = re.sub(r"^Bride's ", "Pratibha's ", relation, flags=re.I)
    if relation.lower() == 'groom': relation = 'Sawan, the groom'
    elif relation.lower() == 'bride': relation = 'Pratibha, the bride'
    return {'matched':True, 'display_name':first, 'candidate':person,
            'message':f'Namaste, {first} Ji! 🌸 Are you {relation}? Tap to chat with your Wedding Concierge.'}


@router.post('/api/concierge/family-special')
def family_special_deprecated():
    # Old confirmation-only endpoint must not bypass the new knowledge check.
    from fastapi import HTTPException
    raise HTTPException(403, 'Use /api/concierge/verify/start and /answer')
