"""Low-assurance, consent-based wedding greeting flow. Not an authentication system."""
import os, json, re, time, hmac, hashlib, base64, unicodedata, difflib, functools
from pathlib import Path
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from .observability import emit

router=APIRouter()
MASTER=Path(__file__).resolve().parent.parent/'data/private/profiles_master.json'

@functools.lru_cache(maxsize=1)
def profiles():
    data=json.loads(MASTER.read_text(encoding='utf-8'))
    return {p['id']:p for p in data}

def norm(s):
    return ' '.join(re.sub(r'[^\w\s]',' ',unicodedata.normalize('NFKC',str(s)).casefold()).split())

def secret():
    s=os.getenv('CONCIERGE_SIGNING_SECRET','')
    if len(s)<32:raise HTTPException(503,'Configure CONCIERGE_SIGNING_SECRET (32+ characters)')
    return s.encode()

def sign(payload):
    raw=base64.urlsafe_b64encode(json.dumps(payload,separators=(',',':')).encode()).decode().rstrip('=')
    return raw+'.'+hmac.new(secret(),raw.encode(),hashlib.sha256).hexdigest()

def read_token(token):
    try:
        raw,mac=token.rsplit('.',1)
        if not hmac.compare_digest(hmac.new(secret(),raw.encode(),hashlib.sha256).hexdigest(),mac):raise ValueError()
        p=json.loads(base64.urlsafe_b64decode(raw+'='*(-len(raw)%4)))
        if p['exp']<time.time():raise ValueError()
        return p
    except (ValueError,KeyError,TypeError):raise HTTPException(403,'Session expired; please start again')

# The vector search is a candidate generator only. Exact local name/alias validation prevents
# semantically similar people (e.g. Saurav vs Saurabh) from being incorrectly selected.
@functools.lru_cache(maxsize=256)
def vector_candidates(name):
    import pinecone
    started=time.perf_counter()
    key=os.getenv('PINECONE_API_KEY','')
    host=os.getenv('PINECONE_PRIVATE_INDEX_HOST','')
    if not key or not host:
        emit('profile.vector.unavailable',service='pinecone',operation='candidate_search',status='error')
        return []
    idx=pinecone.Pinecone(api_key=key).Index(host=host)
    namespace=os.getenv('PINECONE_PRIVATE_NAMESPACE','wedding-private-profiles')
    result=idx.search(namespace=namespace,query={'inputs':{'text':name},'top_k':12},fields=['name','aliases'])
    data=result.to_dict() if hasattr(result,'to_dict') else result
    if not isinstance(data,dict):data={}
    hits=data.get('result',{}).get('hits',[])
    found=[]
    for h in hits:
        if not isinstance(h,dict):h=h.to_dict()
        found.append({'id':h.get('_id') or h.get('id'),'name':(h.get('fields') or {}).get('name'), 'score':h.get('_score',h.get('score'))})
    emit('profile.vector.results',service='pinecone',operation='candidate_search',input_data={'name':name},output_data={'hits':found,'namespace':namespace},duration_ms=round((time.perf_counter()-started)*1000,2))
    return found

def name_candidates(name):
    """Fast in-memory first-name/alias lookup. Similar names need confirmation."""
    entered=norm(name)
    if not entered:return []
    ranked=[]
    for profile in profiles().values():
        names=[profile['name']]+[a for a in profile.get('aliases',[]) if isinstance(a,str)]
        scores=[]
        for value in names:
            canonical=norm(value)
            parts=canonical.split()
            if entered==canonical:scores.append(1.0)
            elif entered in parts:scores.append(.94 if entered==parts[0] else .86)
            elif len(entered)>=3:
                # Tolerate modest misspellings, but never use similarity as identity proof.
                scores.append(.82*difflib.SequenceMatcher(None,entered,canonical).ratio())
                if parts:scores.append(.91*difflib.SequenceMatcher(None,entered,parts[0]).ratio())
        score=max(scores or [0])
        if score>=.72:ranked.append((score,profile))
    ranked.sort(key=lambda x:(-x[0],x[1]['name']))
    return ranked[:6]

def matched(name):
    candidates=name_candidates(name)
    emit('profile.match.candidates',service='concierge',operation='match',
         input_data={'name':name},output_data={'candidates':[{'id':p['id'],'score':round(score,3)} for score,p in candidates]})
    if not candidates:return None
    # Disambiguate near-equal names rather than choosing the wrong person.
    if len(candidates)>1 and candidates[0][0]-candidates[1][0]<.035:return None
    return candidates[0][1]

def questions(p):
    return [q for q in p.get('verification_question_candidates',[]) if isinstance(q,dict) and q.get('question') and q.get('expected_answer')]

def answer_matches(actual,expected):
    """Friendly phonetic/fuzzy answer check, not authentication for private information."""
    def phonetic(value):
        value = norm(value).replace(' ', '')
        # Common English renderings of Indic names/places (Raani/Rani, Laad/Lada).
        value = re.sub(r'(.)\1+', r'\1', value)
        value = re.sub(r'aa|ee|ii|oo|uu', lambda m: m.group()[0], value)
        value = value.replace('w', 'v').replace('ph', 'f')
        return value
    a = norm(actual)
    if not a:
        return False
    options = [norm(x) for x in re.split(r'\s+or\s+|\s*/\s*|\s*;\s*', str(expected), flags=re.I)]
    for option in options:
        if not option:
            continue
        if a == option or phonetic(a) == phonetic(option):
            return True
        aa, bb = phonetic(a), phonetic(option)
        # Only accept near spellings of substantial answers; avoid matching short guesses.
        if min(len(aa), len(bb)) >= 4:
            ratio = difflib.SequenceMatcher(None, aa, bb).ratio()
            if ratio >= 0.78 and abs(len(aa) - len(bb)) <= 3:
                return True
            if len(aa) >= 5 and len(bb) >= 5 and (aa in bb or bb in aa):
                return True
        elif min(len(aa), len(bb)) >= 3 and abs(len(aa)-len(bb)) <= 1:
            if difflib.SequenceMatcher(None, aa, bb).ratio() >= 0.85:
                return True
    return False

class Start(BaseModel):
    name:str=Field(min_length=1,max_length=80)
class Confirm(BaseModel):
    token:str=Field(max_length=3000)
    yes:bool
class Answer(BaseModel):
    token:str=Field(max_length=3000)
    answer:str=Field(max_length=300)

@router.post('/api/profile/start')
def start(body:Start):
    p=matched(body.name)
    emit('profile.start',service='concierge',operation='start',input_data={'name':body.name},details={'matched':bool(p)})
    if not p:
        candidates=name_candidates(body.name)
        if candidates:
            # Return names only; never expose private profile metadata.
            return {'status':'ambiguous','message':'I found a few similar names. Which one should I welcome?',
                    'candidates':[{'name':x['name']} for _,x in candidates[:4]]}
        return {'status':'unmatched','message':'Welcome! We are delighted you are here. Will you join us for the celebrations?'}
    return {'status':'confirm','message':f'Are you {p["name"]}?','name':p['name'],
            'token':sign({'pid':p['id'],'step':'confirm','exp':int(time.time())+600})}

@router.post('/api/profile/confirm')
def confirm(body:Confirm):
    state=read_token(body.token)
    if state.get('step')!='confirm':raise HTTPException(400,'Invalid flow step')
    p=profiles().get(state['pid'])
    if not p:raise HTTPException(404,'Profile unavailable')
    emit('profile.confirmation',service='concierge',operation='confirm',input_data={'profile_id':p['id'],'yes':body.yes})
    if not body.yes:return {'status':'declined','message':'Thank you! You can still ask me anything about the wedding.'}
    qs=questions(p)
    if qs:
        return {'status':'question','question':qs[0]['question'],'token':sign({'pid':p['id'],'step':'question','attempts':0,'exp':int(time.time())+300})}
    return complete(p,'self_confirmed')

def complete(p,assurance):
    # This is a conversational personalization token, NOT proof of identity.
    token=sign({'pid':p['id'],'step':'personalized','assurance':assurance,'exp':int(time.time())+3600})
    emit('profile.personalization.ready',service='concierge',operation='complete',details={'profile_id':p['id'],'assurance':assurance})
    greeting='Pranam' if 'pranam' in json.dumps(p,ensure_ascii=False).lower() else 'Welcome'
    return {'status':'ready','token':token,'message':f'{greeting}, {p["name"]} Ji! 🌸 Sawan and Pratibha would be delighted to celebrate with you. How have you been, and do you think you can join us for the wedding?'}

@router.post('/api/profile/answer')
def answer(body:Answer):
    state=read_token(body.token)
    if state.get('step')!='question':raise HTTPException(400,'Invalid flow step')
    p=profiles().get(state['pid'])
    if not p or not questions(p):raise HTTPException(404,'Question unavailable')
    q=questions(p)[0]
    correct=answer_matches(body.answer,q['expected_answer'])
    emit('profile.question.answer',service='concierge',operation='answer',input_data={'profile_id':p['id'],'question':q['question'],'answer':body.answer},details={'correct':correct})
    if correct:return complete(p,'knowledge_check')
    attempts=state.get('attempts',0)+1
    if attempts>=2:return {'status':'failed','message':'Thanks for trying. We can still chat about the wedding.'}
    return {'status':'question','question':'That does not quite match. Please try once more: '+q['question'],
            'token':sign({'pid':p['id'],'step':'question','attempts':attempts,'exp':state['exp']})}

def guest_visible_profile(profile):
    """Send the complete JSON of a guest-access-approved profile, without a field allowlist.

    Conversational name matching is not identity authentication. The owner must
    explicitly enable guest access to the record; otherwise do not disclose it.
    """
    policy = profile.get('visibility_policy') or {}
    if not (profile.get('approved_for_guests') is True
            and policy.get('share_with_subject_after_verified_login') is True):
        return {}
    # The entire JSON is passed verbatim, including future custom keys.
    return json.loads(json.dumps(profile, ensure_ascii=False))


def personalized_context(token):
    if not token:return {}
    try:state=read_token(token)
    except HTTPException:return {}
    if state.get('step')!='personalized':return {}
    p=profiles().get(state.get('pid'))
    if not p:return {}
    # The owner must opt the profile into guest access; name matching alone is insufficient.
    result={'name':p['name'], 'conversation_style':p.get('conversation_style',''),
            'wedding_encouragement':p.get('wedding_encouragement',''),
            'preferred_greeting':'Pranam' if 'pranam' in json.dumps(p,ensure_ascii=False).lower() else '',
            'assurance':'low; not identity authentication'}
    visible=guest_visible_profile(p)
    if visible:
        result['guest_approved_profile']=visible
    return result
