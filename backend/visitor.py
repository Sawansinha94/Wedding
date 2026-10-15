"""Public name recognition; never authentication."""
import json, re, unicodedata
from pathlib import Path
from .llm import model_messages
FAMILY_PATH=Path(__file__).resolve().parent.parent/'data/family/family_profiles.json'
STOP={'guest','unknown','anonymous','test','admin','user','iphone','android','mobile','phone','device','null','none','xyz','abc','name'}

def normalize_person_name(value):
    """Normalize case, accents, punctuation and honorifics for deterministic matching."""
    value=unicodedata.normalize('NFKD',str(value or '')).casefold()
    value=''.join(c for c in value if not unicodedata.combining(c))
    words=re.findall(r"[^\W_]+",value,flags=re.UNICODE)
    honorifics={'mr','mrs','ms','smt','shri','sri','late','dr','ji'}
    return ' '.join(w for w in words if w not in honorifics)

def family_candidates(name):
    key=normalize_person_name(name)
    if len(key)<2:return []
    profiles=json.loads(FAMILY_PATH.read_text(encoding='utf-8'))
    matches=[]
    for profile in profiles:
        if profile.get('approved_for_guests') is not True:continue
        full=normalize_person_name(profile.get('name',''))
        if not full or full.startswith('to be provided'):continue
        aliases=profile.get('aliases') or []
        if not isinstance(aliases,list):continue
        variants={full, *[normalize_person_name(a) for a in aliases if isinstance(a,str)]}
        # A first-name match is allowed, but a surname alone is not an identity match.
        first=full.split()[0]
        if len(first)>=3:variants.add(first)
        if key in variants:
            matches.append({'id':profile['id'],'name':profile['name'],
                            'relation':profile['relation'],'side':profile['side']})
    # Never arbitrarily select the first match if a nickname belongs to two people.
    return matches

def quick_name(name):
    name=' '.join(name.strip().split())[:80]
    if not name or len(name)<2 or len(name)>80:return 'invalid'
    if any(c.isdigit() for c in name) or any(c in name for c in '@/_\\<>:{}') or 'http' in name.lower():return 'invalid'
    words=name.casefold().split()
    if any(w in STOP for w in words):return 'invalid'
    if not all(c.isalpha() or c in " .'-" for c in name):return 'uncertain'
    if len(words)>5:return 'uncertain'
    return 'valid' if len(name)>=4 else 'uncertain'

async def validate_name(name):
    status=quick_name(name)
    if status!='uncertain':return status
    prompt='Classify whether this user-supplied string is a plausible human preferred name. Do not guess identity. Return only JSON {"status":"valid"} or {"status":"invalid"}. Accept international names and initials. Name: '+json.dumps(name[:80])
    try:
        reply=await model_messages([{'role':'system','content':'You are a conservative name-format classifier. Output JSON only.'},{'role':'user','content':prompt}],temperature=0,max_tokens=35)
        data=json.loads(re.search(r'\{.*?\}',reply,re.S).group())
        return 'valid' if data.get('status')=='valid' else 'invalid'
    except Exception:return 'invalid'
