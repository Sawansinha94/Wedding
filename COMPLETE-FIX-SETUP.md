# Wedding Concierge — complete website bundle and fixes

## Included
- Full existing website assets, pages, images, backend and data, not just a patch.
- Latest 72-profile master including Pranam preferences.
- Corrected Pinecone diagnostic parsing (`_id`, `_score`).
- Server-side deterministic profile name/alias lookup, restricted to owner token.
- Immediate bundled translations for strings already translated; untranslated strings are fetched and cached on first use.
- One-time translation builder to precompute every static HTML string (`python build_static_translations.py`).

## Start
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Set OPENROUTER_API_KEY, DATABASE_URL, PINECONE_API_KEY, PINECONE_PRIVATE_INDEX_HOST, PINECONE_PRIVATE_NAMESPACE
python test_local_fixes.py
python diagnose_private_search.py 'Sailendra Kumar'
python build_static_translations.py
uvicorn server:app --reload --port 8000
```

## Secure profile matching
Add `WEDDING_OWNER_TOKEN` (32+ random characters) to `.env`. Only an authorized owner can call `GET /api/owner/profiles/lookup?name=Sailendra%20Kumar` with header `X-Owner-Token`. Never put the token into website JavaScript or a public page. This lookup uses the exact private master JSON and does not depend on semantic similarity; Pinecone is still available for diagnostics. Public guest chat does not expose private profile data. A separate real guest authentication mechanism is required for personalized access. Name matching alone is not authentication.

## Language switching
The HTML localization bundle is applied synchronously. Build the complete offline catalog once using your OpenRouter key. Any newly inserted/untranslated dynamic text uses `/api/site/translate` asynchronously, then caches translations. This is not a guarantee that every dynamic phrase is translated immediately; chat replies are requested in the selected language. Review Odia/Hindi/Telugu translations before publishing.

## Voice
The bundled Talk With Us retains browser fallback and turn-based backend speech. It is not guaranteed to work on every browser or support Odia speech recognition; use Chrome on localhost/HTTPS and check microphone permissions. No realtime ChatGPT voice parity is claimed.

## Privacy
Pinecone has 72 private vectors and 19 older family vectors in the user's account, based on user-run diagnostics. This package does not upload or delete vectors. All credentials remain local. Do not expose owner token or raw profile JSON via static routes. The website itself is not yet access-gated, so it should not be published if every page must be private.
