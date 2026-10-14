# Family profile ingestion — Pinecone

## Recommended source format

Use `data/family/family_profiles.json`, a UTF-8 JSON **array** with one object per person. Each person's stable `id` is used as the Pinecone record ID, so re-running the script updates the same record instead of creating duplicates.

Fields:

| Field | Required | Meaning |
|---|---|---|
| `id` | Yes | Unique stable ID such as `groom-uncle` |
| `name` | Yes | Person's preferred public name |
| `side` | Yes | `groom` or `bride` |
| `relation` | Yes | Explicit relation, e.g. `Groom's uncle; uncle of Sawan` |
| `age` | No | Number or `null` if unknown or not approved |
| `traits` | No | Array of approved personality descriptions |
| `interests` | No | Array of hobbies or interests |
| `bio` | No | Short factual public biography |
| `approved_for_guests` | Yes | Only records with `true` are uploaded |

**Example:**

```json
{
  "id": "groom-uncle",
  "name": "Mr. Ajeet Kumar Sinha",
  "side": "groom",
  "relation": "Groom's uncle; uncle of Sawan",
  "age": null,
  "traits": ["warm and welcoming"],
  "interests": ["gardening"],
  "bio": "He enjoys hosting family gatherings.",
  "approved_for_guests": true
}
```

*The traits, interests and biography in this example are fictional placeholders; do not publish them unless confirmed by the person.* The bundled JSON template contains only previously supplied relationships and leaves personal characteristics empty.

## Pinecone index requirements

Create a **dense index with integrated embedding** in Pinecone. Configure its source text field mapping as `text` (this matches `backend/pinecone_store.py` and `ingest_family.py`). Copy the **index host** from the Pinecone console. Do not use the index name in place of the host. Set namespace `wedding-family`. An index without integrated embeddings will not work with this ingestion/search code without additional embedding logic.

## Run on Mac / Linux

```bash
cd sawan-pratibha-wedding
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # if .env doesn't already exist
```

Add to `.env`:

```env
PINECONE_API_KEY=your_private_key
PINECONE_INDEX_HOST=your_index_host
PINECONE_NAMESPACE=wedding-family
```

Then:

```bash
python ingest_family.py --validate-only
python ingest_family.py --dry-run
python ingest_family.py
```

Test the existing concierge API after ingestion, asking about a family relation and a follow-up. Pinecone may take a short time to make updates searchable.

## Good information to include

Family relationship, preferred name, nickname (only if publicly acceptable), hobbies, personality descriptions the person has approved, how they are connected to the couple, and anecdotes they are comfortable sharing. For accurate relationship questions, spell out connections explicitly rather than relying on vague labels such as "uncle".

## Do not include

Phone numbers, private addresses, birth dates, medical or financial information, private family disputes, identification documents, or unverified personal traits. Age is optional and should only be published with consent. Pinecone records here are guest-facing retrieval data, **not a private personnel database**.

## Maintenance

Re-running `ingest_family.py` overwrites matching record IDs. Removing a person from JSON **does not delete** their previously uploaded record from Pinecone; delete that record separately from the index when needed. Keep your `.env` private and never expose Pinecone credentials in browser JavaScript.


## Strict scope
Only ingest bride, groom, and family member profiles with permission. Never ingest guest/caller/visitor profiles, RSVP records, chat transcripts, or wedding wishes into this Pinecone namespace. The concierge does not identify visitors or answer personal questions about guests.
