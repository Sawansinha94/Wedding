# Private profile ingestion — 72 profiles

This package contains the latest 72-profile master with the 11 respectful **Pranam** greetings. The incorrect “Manish Shankar” alias for **Mani Shankar** has been removed.

## Privacy and boundaries

- All 72 records are **private and pending owner review**. This uploader does **not** set `approved_for_guests=true`.
- Create a **new, dedicated Pinecone index**, separate from your public wedding index. Choose an index supporting **integrated embeddings** with field map `text`. The script uses `upsert_records`; it will not work with an ordinary bring-your-own-vectors index.
- The private index should be accessed **only from the backend with a secret API key**. Pinecone namespaces are not an authentication mechanism; index isolation and server authorization matter.
- Do **not** connect this private index to `family_lookup`, `family_verified_context`, or any public API route. The existing conversational trivia challenge is not strong authentication.
- The upload sends readable personal profile content to Pinecone for embedding. It is **not end-to-end encrypted**. Review consent, vendor terms, data residency, retention, and deletion requirements before upload. Verification question/answer candidates are excluded from the vector records, but remain in the local private JSON.
- Anyone with your Pinecone API key and index access may be able to retrieve these records. Keep keys out of git, browser JavaScript, logs, and screenshots. Rotate any exposed key.
- Profile lookup for a verified guest needs an additional authorization layer (for example, owner-issued one-time invitations bound to a specific profile, authenticated sessions, rate limits, and exact-ID access). This package deliberately does not expose the private index to guests.

## Setup (Mac)

```bash
cd sawan-pratibha-wedding
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # only if .env does not already exist
```

Set in `.env`:

```dotenv
PINECONE_API_KEY=your_actual_key
PINECONE_INDEX_HOST=existing_public_index_host
PINECONE_NAMESPACE=wedding-family
PINECONE_PRIVATE_INDEX_HOST=new_dedicated_private_index_host
PINECONE_PRIVATE_NAMESPACE=wedding-private-profiles
```

Use a distinct private index host. If `PINECONE_PRIVATE_INDEX_HOST` matches `PINECONE_INDEX_HOST`, the uploader refuses to run.

## Run

```bash
python ingest_private_profiles.py --validate-only
python ingest_private_profiles.py --dry-run
python ingest_private_profiles.py --confirm-private-upload
```

The dry run prints only profile IDs and names. Actual upload needs explicit confirmation. A rerun upserts the same IDs. **Removed IDs are not automatically deleted** from Pinecone; reconcile deletions separately.

## Important: website behavior

This upload stores the profiles privately. It **does not yet enable guest-specific private personalization**. Do not change the existing `PINECONE_INDEX_HOST` to the private index host. Public wedding facts and guest-approved summaries can continue to use the existing public index.

## Verify upload

Review record count and namespace in the Pinecone console for the **private index**. Do not copy the personal vector contents into a public chat or support ticket.

## Old records

Do not delete the existing 19 approved family records until you review their public visibility and confirm they are no longer needed. The old public namespace is not changed by this uploader.
