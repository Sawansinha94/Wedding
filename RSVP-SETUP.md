# RSVP database setup

1. Set `DATABASE_URL` in a `.env` file to your Neon PostgreSQL connection string. Never put it in index.html.
2. Optionally run `database-rsvp.sql` in Neon SQL Editor. The server also creates `wedding_rsvps` automatically when started.
3. Run `pip install -r requirements.txt` then `uvicorn server:app --reload` inside the website folder.
4. Open `http://127.0.0.1:8000` (not `file://.../index.html`). Submit an RSVP and check Neon table `wedding_rsvps`.
5. No emails are sent. The envelope animation is a visual confirmation after the database commits the record.

For production, use HTTPS and consider rate limiting/CAPTCHA to prevent spam. Database credentials stay server-side.
