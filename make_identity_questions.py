"""Build private verification question file. Never commit or ingest it into Pinecone."""
import json,hashlib,unicodedata
from pathlib import Path
root=Path(__file__).parent
def norm(s):return ' '.join(unicodedata.normalize('NFKC',s).casefold().split())
print('Create at least 2 questions per person. Avoid public facts, birthdays and simple guesses.')
profiles=json.loads((root/'data/family/family_profiles.json').read_text())
ids={p['id'] for p in profiles if p.get('approved_for_guests')}
result={}
while True:
    pid=input('Profile ID (blank to finish): ').strip()
    if not pid:break
    if pid not in ids:print('Unknown or unapproved profile');continue
    questions=[]
    for n in range(3):
        q=input(f'Question {n+1} (blank to finish): ').strip()
        if not q:break
        a=input('Private expected answer: ').strip()
        if not a:break
        strong=input('Hard-to-guess private answer? (y/N): ').strip().lower()=='y'
        questions.append({'question':q,'answer_sha256':hashlib.sha256(norm(a).encode()).hexdigest(),'strong':strong})
    if len(questions)>=2:result[pid]=questions
    else:print('Need at least 2 questions; skipping')
path=root/'data/private/identity_questions.json';path.parent.mkdir(parents=True,exist_ok=True)
path.write_text(json.dumps(result,indent=2))
try:path.chmod(0o600)
except OSError:pass
print('Wrote',len(result),'profile challenges to',path)
