# Integrated Sawan & Pratibha Wedding Website

## Services
- FastAPI serves the website and API.
- OpenRouter runs chat and response generation (`OPENROUTER_API_KEY`).
- Neon Postgres stores RSVP, wishes, and other existing application data (`DATABASE_URL`).
- Pinecone holds vector records for **approved** family facts (`PINECONE_API_KEY`, `PINECONE_INDEX_HOST`).
- Voice: local CPU faster-whisper transcription + OpenRouter chat + Edge neural TTS. This is a **turn-based voice experience**, not native WebRTC streaming or ChatGPT Voice parity. Edge TTS needs internet access and has no service-level guarantee. Odia voice and transcription must be tested: Whisper's Odia support and installed voices may be insufficient. Indian male voice is not guaranteed for Odia.

## Setup (macOS / Linux)
1. Install Python 3.11+ and FFmpeg (`brew install ffmpeg` on macOS).
2. `python3 -m venv .venv && source .venv/bin/activate`
3. `pip install -r requirements.txt`
4. `cp .env.example .env` and enter OpenRouter, Neon and Pinecone credentials; set a random `CONCIERGE_SIGNING_SECRET`.
5. Run Neon SQL migration(s) in project root as appropriate for your existing schema, reviewing first. Never reset your production database.
6. `uvicorn server:app --host 127.0.0.1 --port 8000 --reload`
7. Visit http://127.0.0.1:8000 and test text, RSVP, multilingual UI and Talk With Us.
8. Deploy with HTTPS and enable rate limiting and quotas before exposing voice endpoints publicly.

## Profiles and indexing
`data/private/profiles_master.json` contains 72 profiles and should remain owner-only. These are NOT approved for guest visibility. Do not upload this raw master to public Pinecone namespaces. Review each record, redact sensitive fields and explicitly approve guest-safe fields before indexing. Existing `ingest_family.py` is preserved but must not be run on unreviewed private profiles. Knowledge questions are NOT authentication.

## Tests and limits
`python -m compileall -q server.py backend` checks Python syntax. A live integration test requires your real keys and service access. Turn-based voice records approximately 4.5-second clips; this is not fluid interruptible streaming. Realtime speech would require a supported streaming STT/TTS provider. Existing website routes and frontend assets are retained. Database migrations have not been applied to your live Neon instance and Pinecone has not been modified.
