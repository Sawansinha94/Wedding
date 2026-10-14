# Guest profile and translation patch

## Changes
- `backend/profile_flow.py`: the low-assurance guest flow now provides the full **allowlisted public-approved** profile (`id`, `name`, `aliases`, `side`, `relation`, `traits`, `bio`, `conversation_style`, `wedding_encouragement`) to the LLM context, but only when `approved_for_guests=true`, `visibility_policy.public_summary_approved=true`, and `review_status=approved`. Other fields, including `private_notes` and verification answers, are never sent.
- `backend/concierge.py`: consumes the authorized context and answers profile-grounded questions; remains proactive; avoids logging the full prompt.
- `backend/pinecone_store.py`: adds `private_profile_record(profile_id)` to retrieve the exact authoritative complete JSON by ID from the local master. Pinecone's integrated-embedding records are not reliably available via `Index.fetch(...).metadata`; the existing ingestion script indexes a text copy for search.
- `assets/js/28-multilingual.js`: translates select option labels and dynamically added text nodes; maintains numbers and existing exclusion rules.
- `assets/js/29-static-catalog.js`: adds offline Hindi/Odia translations for common UI labels and headings, removing network wait for these phrases.

## Access security
Name confirmation and guessable knowledge questions are NOT strong authentication. To reveal owner-only notes, implement actual guest authentication and a distinct authorized endpoint first. Do not simply pass raw profile JSON to a public chat endpoint.

## Important data observation
The bundled `data/private/profiles_master.json` currently has 72 records; the Vamsee record is NOT approved (`approved_for_guests=false`, `public_summary_approved=false`, `review_status=pending_owner_review`). Until the owner approves those flags, only his safe greeting preferences can be used.

## Run
Keep the current `.env` on the server; never commit secrets. Deploy the updated ZIP and restart. To refresh the Pinecone private search index after editing the master, run `python ingest_private_profiles.py --validate-only`, then `python ingest_private_profiles.py --confirm-private-upload` with your private Pinecone environment configured. No re-ingestion is necessary for the local authoritative-profile retrieval change alone.

## Limits
This is a targeted patch, not a complete human-reviewed translation of every paragraph. The existing `/api/site/translate` fallback still handles untranslated copy.
