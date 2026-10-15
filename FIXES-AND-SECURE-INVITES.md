# Wedding Concierge — fixes and secure personalization

## Applied
- Removed the visible 20-second countdown message; automatic behavior is unchanged.
- Welcome screen now stores the visitor's preferred name locally and opens even when Neon visitor-name logging is unavailable. The failed telemetry request does not block entry. Names are not proof of identity.
- Personalized homepage greeting updates after the visitor enters their name, whether or not the name appears in the profile master.
- Replaced the Talcher residence map embed with the provided Sinha Prasad Family Google Maps embed; corrected reception start time to 1 PM on the page and the offline English/Hindi/Odia responses.
- Polished the Text chat and Talk with us controls, improved voice error display, and corrected a recording-stop issue.
- Added fast local translations for common Concierge controls and browser-local caching for AI-translated static strings. **Full instant translation is not guaranteed:** uncached strings still depend on OpenRouter availability and latency, and user-generated text is excluded. Audit the site in all four languages before publishing.
- Disabled old family-directory matching and trivia-based 'verification' for private profiles. Private personalization now requires a signed, expiring invitation code tied to one exact master-profile ID.
- Private profiles are read server-side from `data/private/profiles_master.json`; no guest-facing Pinecone search is performed. The master file is not served by FastAPI static mounts. The old Pinecone ingestion script remains separate and should not be run to a public namespace.

## Setup
1. Extract the package; run `pip install -r requirements.txt` and configure `.env`.
2. Set `CONCIERGE_SIGNING_SECRET` to a random 32+ character value (e.g. `python -c 'import secrets;print(secrets.token_urlsafe(48))'`). Do not expose it or commit `.env`.
3. Generate one invitation code for a particular profile (owner only):
   `python create_invitation_codes.py --profile-id relation-sailendra-kumar --days 45`
   If the ID differs, inspect `data/private/profiles_master.json` to get the exact ID.
4. Give each guest only their own code via a private channel. They can enter it under Wedding Concierge -> Personal invitation code. They can then receive their own profile-specific personalized replies.
5. Start with `uvicorn server:app --host 127.0.0.1 --port 8000 --reload`.

## Security limitations / deployment requirements
- Signed codes are **bearer credentials**: anyone who obtains a code can use that profile until expiration. Use HTTPS, short expiry, avoid URL query parameters, and consider OTP login for higher assurance.
- The code is submitted in request JSON, so avoid logging request bodies; do not use public analytics to capture the code. Add rate limiting and revocation support before public deployment.
- This release does **not** make the website private: public HTML, contact details, RSVP and wishes endpoints remain reachable. If nothing should be publicly accessible, add site-wide authentication at the reverse proxy or backend before deployment.
- No actual Pinecone or Neon account was modified. No live voice test was possible here.
- Voice remains **turn-based**, not full duplex ChatGPT Voice. It needs faster-whisper, FFmpeg, Edge TTS network access, microphone permissions, and localhost/HTTPS. Odia voice availability is unverified. It is not a native OpenRouter realtime speech service.
- The signed invitation token is stored in browser JS memory only; refreshing requires entering the code again.
- For production, require authenticated sessions, per-profile access control, rate limiting, a revocation table, and security testing.
