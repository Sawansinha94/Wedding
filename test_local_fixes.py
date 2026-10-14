import json
from pathlib import Path
from backend.private_profile_search import match_profiles
root=Path(__file__).resolve().parent
profiles=json.loads((root/'data/private/profiles_master.json').read_text())
assert len(profiles)==72
assert len({p['id'] for p in profiles})==72
assert any(p['name']=='Sailendra Kumar' for p in match_profiles('Sailendra Kumar'))
assert any(p['name']=='Sailendra Kumar' for p in match_profiles('Shailendar')) if any('Shailendar' in str(p.get('aliases')) for p in profiles if p['name']=='Sailendra Kumar') else True
assert not match_profiles('unknown person 999')
print('PASS: 72 unique profiles; exact-name matching; unknown-name fallback')
