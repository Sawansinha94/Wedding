from .observability import traced
import os
@traced('vector.search', service='pinecone')
def family_lookup(query: str) -> list[dict]:
    api_key = os.getenv("PINECONE_API_KEY", "").strip()
    index_host = os.getenv("PINECONE_INDEX_HOST", "").strip()
    if not api_key or not index_host:
        return []
    from pinecone import Pinecone
    pc = Pinecone(api_key=api_key)
    index = pc.Index(host=index_host)
    namespace = os.getenv("PINECONE_NAMESPACE", "wedding-family")
    # Pinecone integrated-embedding index (field configured as 'text').
    result = index.search(namespace=namespace, query={"inputs":{"text":query}, "top_k":5}, fields=["name","side","relation","age","traits","bio","text"])
    hits = result.get("result", {}).get("hits", []) if isinstance(result,dict) else result.result.hits
    records=[]
    for hit in hits:
        h=hit if isinstance(hit,dict) else hit.to_dict()
        fields=h.get("fields",{})
        if fields.get("side") not in ("groom", "bride"):
            continue
        records.append({k:str(v)[:500] for k,v in fields.items() if k in ("name","side","relation","age","traits","bio","text")})
    return records



@traced('vector.fetch', service='pinecone')
def family_special_message(profile_id: str) -> str:
    """Fetch the confirmed member's public special message by exact Pinecone ID.

    Semantic search is unsuitable here: the correct record might not be in top-k.
    """
    import re, json
    from .visitor import FAMILY_PATH
    if not re.fullmatch(r"[a-z0-9_-]{3,100}", profile_id):
        return ""
    key = os.getenv("PINECONE_API_KEY", "").strip()
    host = os.getenv("PINECONE_INDEX_HOST", "").strip()
    if not key or not host:
        return ""
    profiles = json.loads(FAMILY_PATH.read_text(encoding="utf-8"))
    approved = next((p for p in profiles if p.get("id") == profile_id
                     and p.get("approved_for_guests") is True
                     and p.get("side") in ("groom", "bride")), None)
    if not approved:
        return ""
    from pinecone import Pinecone
    index = Pinecone(api_key=key).Index(host=host)
    namespace = os.getenv("PINECONE_NAMESPACE", "wedding-family")
    response = index.fetch(ids=[profile_id], namespace=namespace)
    records = response.get("vectors", {}) if isinstance(response, dict) else getattr(response, "vectors", {})
    record = records.get(profile_id) if records else None
    if not record:
        return ""
    metadata = record.get("metadata", {}) if isinstance(record, dict) else getattr(record, "metadata", {})
    if not metadata or metadata.get("side") != approved["side"]:
        return ""
    return str(metadata.get("special_message") or "").strip()[:800]


@traced('vector.fetch', service='pinecone')
def family_verified_context(profile_id: str) -> dict:
    """Exact-ID lookup after a valid server-issued verification token."""
    import json
    from pinecone import Pinecone
    if not __import__('re').fullmatch(r'[a-z0-9_-]{3,100}', profile_id):
        return {}
    index = Pinecone(api_key=os.environ['PINECONE_API_KEY']).Index(host=os.environ['PINECONE_INDEX_HOST'])
    result = index.fetch(ids=[profile_id], namespace=os.getenv('PINECONE_NAMESPACE','wedding-family'))
    vectors = result.get('vectors', {}) if isinstance(result,dict) else getattr(result,'vectors',{})
    record = vectors.get(profile_id)
    if not record: return {}
    metadata = record.get('metadata',{}) if isinstance(record,dict) else getattr(record,'metadata',{})
    if not metadata: return {}
    return {'name':metadata.get('name',''), 'relation':metadata.get('relation',''),
            'special_message':metadata.get('special_message',''),
            'conversation_context':json.loads(metadata.get('conversation_context') or '{}')}


def private_profile_record(profile_id: str) -> dict:
    """Fetch exact complete source profile by ID, never semantic reconstruction.

    Source-of-truth is the private master JSON. Pinecone integrated-embedding
    search stores text, but fetch() on a record index is not guaranteed to
    return its fields as vector metadata. This function deliberately uses the
    same authoritative master that the ingestion script reads.
    """
    from .profile_flow import profiles
    if not __import__('re').fullmatch(r'[a-z0-9_-]{3,100}', profile_id or ''):
        return {}
    return dict(profiles().get(profile_id) or {})
