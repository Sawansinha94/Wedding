# New features and Neon database

1. Configure `DATABASE_URL` in `.env` with your Neon PostgreSQL URL. The backend now refuses to start without PostgreSQL, preventing accidental local SQLite storage.
2. Install dependencies with `pip install -r requirements.txt` and run `uvicorn server:app --reload`. On startup the `public_wedding_wishes`, `wedding_wish_replies`, and `wedding_rsvps` tables are created automatically.
3. In Wedding Wishes, name is required. Each Latest Wish supports comments/replies with required responder name and comment. Replies are saved to Neon.
4. Music starts OFF. Click the musical note at the start of the header to toggle it. Activating microphone or Read replies aloud stops music. Speech uses the browser's installed voices; voice quality and available accents vary by device.
5. Keep `DATABASE_URL` and all API keys on the server, never in frontend code. Add moderation, rate limits and spam prevention before public launch.
