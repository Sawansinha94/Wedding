"""Owner-operated upload of all private profiles to an isolated Pinecone namespace.

Requires a Pinecone index with integrated embeddings mapped to the `text` field.
Does NOT expose private namespace to any website API route.
"""
import argparse
import json
import os
import re
from pathlib import Path
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'data/private/profiles_master.json'
RECORDS = ROOT / 'data/private'


def records_from_master(path):
    data = json.loads(Path(path).read_text(encoding='utf-8'))
    if not isinstance(data, list):
        raise ValueError('Master must be a JSON array')
    records, seen = [], set()
    for n, profile in enumerate(data, 1):
        if not isinstance(profile, dict):
            raise ValueError(f'Profile {n} must be an object')
        pid = profile.get('id')
        if not isinstance(pid, str) or not re.fullmatch(r'[a-z0-9][a-z0-9_-]{2,99}', pid):
            raise ValueError(f'Invalid profile id at {n}: {pid!r}')
        if pid in seen:
            raise ValueError(f'Duplicate profile id: {pid}')
        seen.add(pid)
        name, side = profile.get('name'), profile.get('side')
        if not isinstance(name, str) or not name.strip() or side not in ('groom','bride'):
            raise ValueError(f'Invalid name or side at {pid}')
        # Do not upload knowledge-check answers, secrets, or access-control metadata
        # as embedded/searchable content. All conversational fields remain.
        excluded = {'verification_question_candidates', 'visibility_policy',
                    'approved_for_guests', 'review_status', 'source_type',
                    'verification_questions', 'verification_answers'}
        details = {k: v for k, v in profile.items() if k not in excluded}
        text = json.dumps(details, ensure_ascii=False, separators=(',', ':'))
        if len(text.encode('utf-8')) > 30000:
            raise ValueError(f'Profile {pid} exceeds 30KB; review/chunk manually')
        records.append({'_id':pid, 'text':text, 'name':name.strip(),
                        'side':side, 'private':'true', 'dataset':'wedding-private-v1'})
    return records


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--file', default=str(SOURCE))
    parser.add_argument('--validate-only', action='store_true')
    parser.add_argument('--dry-run', action='store_true', help='Print IDs/names only; not private content')
    parser.add_argument('--confirm-private-upload', action='store_true',
                        help='Acknowledge sending personal profile content to Pinecone')
    args = parser.parse_args()
    records = records_from_master(args.file)
    print(f'Validated {len(records)} private profiles (not guest-approved)')
    if args.dry_run:
        for r in records: print(f"{r['_id']}  {r['name']}")
    if args.validate_only or args.dry_run:
        return
    if not args.confirm_private_upload:
        parser.error('Upload requires --confirm-private-upload')
    load_dotenv(ROOT / '.env')
    api_key = os.getenv('PINECONE_API_KEY','').strip()
    host = os.getenv('PINECONE_PRIVATE_INDEX_HOST','').strip()
    namespace = os.getenv('PINECONE_PRIVATE_NAMESPACE','wedding-private-profiles').strip()
    public_host = os.getenv('PINECONE_INDEX_HOST','').strip()
    public_namespace = os.getenv('PINECONE_NAMESPACE','wedding-family').strip()
    if not api_key or not host:
        raise SystemExit('Configure PINECONE_API_KEY and PINECONE_PRIVATE_INDEX_HOST in .env')
    if not namespace or namespace == public_namespace:
        raise SystemExit('REFUSING: private namespace must differ from public namespace')
    # Stronger boundary: require a DIFFERENT index host, not just a namespace.
    if public_host and host.rstrip('/') == public_host.rstrip('/'):
        raise SystemExit('REFUSING: use a dedicated PRIVATE Pinecone index, not the public index')
    from pinecone import Pinecone
    index = Pinecone(api_key=api_key).Index(host=host)
    for offset in range(0,len(records),25):
        batch=records[offset:offset+25]
        index.upsert_records(namespace=namespace,records=batch)
        print(f'Uploaded {min(offset+len(batch),len(records))}/{len(records)} private profiles')
    print(f'Upload complete: {len(records)} records in PRIVATE index, namespace {namespace}.')
    print('No guest-facing route has been granted access to these records.')

if __name__ == '__main__':
    main()
