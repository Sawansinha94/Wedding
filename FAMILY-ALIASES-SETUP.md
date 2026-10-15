# Alternative names and nicknames — Wedding Concierge

Edit `data/family/family_profiles.json`. Every approved person can have an `aliases` array:

```json
{
  "id": "groom-younger-brother",
  "name": "Abhishek Sinha",
  "aliases": ["Lalu"],
  "side": "groom"
}
```

The snippet shows only relevant fields; keep all other existing fields in the profile. **Lalu is suggested from the existing special-message wording; confirm this nickname before publishing.** No aliases have been invented or automatically populated.

Aliases may include nicknames, common short names, alternate spellings, and preferred family names. Matching is case-insensitive and punctuation/accents are normalized. A person's first name also matches. Ambiguous names (e.g., two people sharing the same nickname) are **not** automatically resolved: the Concierge should ask which person the visitor means. An alias match is not proof of identity; the existing relationship confirmation and private knowledge check still apply.

Ingestion includes aliases in Pinecone's searchable `text` and in metadata. The welcome-name lookup uses the local JSON for fast deterministic candidate matching, then checks that the exact profile ID exists in Pinecone. This avoids choosing an unrelated vector similarity hit.

Commands:

```bash
python ingest_family.py --validate-only
python ingest_family.py --dry-run
python ingest_family.py
```

Restart the FastAPI application after changing JSON because the running service must load the updated file. No index dimension or SQL schema changes are needed. Use the same `PINECONE_NAMESPACE=wedding-family`.

Do not store private identity-question answers in aliases, searchable text, or metadata.
