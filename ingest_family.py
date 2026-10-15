"""Validate and ingest approved family JSON profiles into a Pinecone integrated-embedding index.
Usage: python ingest_family.py --validate-only
       python ingest_family.py --dry-run
       python ingest_family.py
"""
import argparse
import json
import os
import re
from pathlib import Path
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent
DEFAULT_FILE = ROOT / 'data' / 'family' / 'family_profiles.json'
ALLOWED_SIDES = {'groom', 'bride'}

def build_records(path):
    data = json.loads(Path(path).read_text(encoding='utf-8'))
    if not isinstance(data, list):
        raise ValueError('Root JSON must be an array of family profiles')
    records, seen = [], set()
    for n, profile in enumerate(data, 1):
        if not isinstance(profile, dict):
            raise ValueError(f'Profile {n} must be an object')
        pid = str(profile.get('id', '')).strip()
        name = str(profile.get('name', '')).strip()
        side = str(profile.get('side', '')).strip().lower()
        relation = str(profile.get('relation', '')).strip()
        if not re.fullmatch(r'[a-z0-9][a-z0-9_-]{2,99}', pid):
            raise ValueError(f'Profile {n}: id must be 3-100 lowercase letters, digits, _ or -')
        if pid in seen:
            raise ValueError(f'Duplicate id: {pid}')
        seen.add(pid)
        if not name or side not in ALLOWED_SIDES or not relation:
            raise ValueError(f'Profile {n}: name, side (groom/bride), relation are required')
        if profile.get('approved_for_guests') is not True:
            print(f'SKIP {pid}: not approved for guest-facing search')
            continue
        traits = profile.get('traits') or []
        if not isinstance(traits, list) or any(not isinstance(t, str) for t in traits):
            raise ValueError(f'{pid}: traits must be a list of strings')
        age = profile.get('age')
        if age is not None and (type(age) is not int or not 0 <= age <= 120):
            raise ValueError(f'{pid}: age must be a whole number from 0 to 120 or null')
        bio = str(profile.get('bio') or '').strip()
        special_message = str(profile.get('special_message') or '').strip()
        if len(special_message) > 800: raise ValueError(f'{pid}: special_message must be 800 characters or less')
        interests = profile.get('interests') or []
        if not isinstance(interests, list) or any(not isinstance(t, str) for t in interests):
            raise ValueError(f'{pid}: interests must be a list of strings')
        if name.startswith('TO BE PROVIDED'):
            print(f'SKIP {pid}: placeholder name')
            continue
        aliases = profile.get('aliases') or []
        if not isinstance(aliases,list) or any(not isinstance(v,str) for v in aliases):
            raise ValueError(f'{pid}: aliases must be strings')
        aliases=[v.strip() for v in aliases if v.strip()]
        if any(len(v)>80 for v in aliases) or len(aliases)>20:
            raise ValueError(f'{pid}: maximum 20 aliases, 80 characters each')
        lines = [f'Name: {name}', f'Family side: {side}', f'Relationship: {relation}']
        if aliases: lines.append('Also known as: ' + ', '.join(aliases))
        if age is not None: lines.append(f'Age: {age}')
        if traits: lines.append('Traits: ' + ', '.join(traits))
        if interests: lines.append('Interests: ' + ', '.join(interests))
        if bio: lines.append('About: ' + bio)
        # Conversational context is held as a compact JSON metadata field.
        # Do not put private verification answers here or in the searchable text.
        context_keys = ('preferred_address','preferred_language','relationship_context',
                        'shared_memories','habits','likes','dislikes','conversation_style',
                        'conversation_starters','wedding_encouragement','topics_to_avoid','notes_for_host')
        context = {k:profile.get(k) for k in context_keys if profile.get(k)}
        context_json = json.dumps(context,ensure_ascii=False)
        if len(context_json.encode('utf-8')) > 12000:
            raise ValueError(f'{pid}: conversational context exceeds 12 KB')
        records.append({'_id': pid, 'name': name, 'side': side, 'relation': relation,
                         'aliases': ', '.join(aliases), 'conversation_context': context_json,
                        'age': str(age) if age is not None else '',
                        'traits': ', '.join(traits), 'bio': bio, 'special_message': special_message, 'text': '\n'.join(lines)})
    return records

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--file', default=str(DEFAULT_FILE))
    parser.add_argument('--validate-only', action='store_true')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    records = build_records(args.file)
    print(f'Validated {len(records)} approved family profiles')
    if args.validate_only: return
    if args.dry_run:
        print(json.dumps(records, ensure_ascii=False, indent=2))
        return
    load_dotenv(ROOT / '.env')
    api_key = os.getenv('PINECONE_API_KEY')
    host = os.getenv('PINECONE_INDEX_HOST')
    namespace = os.getenv('PINECONE_NAMESPACE', 'wedding-family')
    if not api_key or not host:
        raise SystemExit('Set PINECONE_API_KEY and PINECONE_INDEX_HOST in .env')
    if not records:
        print('No approved profiles to ingest')
        return
    from pinecone import Pinecone
    pc = Pinecone(api_key=api_key)
    index = pc.Index(host=host)
    for start in range(0, len(records), 50):
        batch = records[start:start+50]
        index.upsert_records(namespace=namespace, records=batch)
        print(f'Upserted {min(start+len(batch),len(records))}/{len(records)}')
    print(f'Done. Namespace: {namespace}. Search may take a short time to reflect updates.')

if __name__ == '__main__':
    main()
