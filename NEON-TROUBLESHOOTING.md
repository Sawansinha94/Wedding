# Neon troubleshooting and header fix

## Header
Music control now sits at the far-right of the header. Below 1350px, navigation collapses into a menu instead of wrapping across the logo and music button.

## Neon configuration
The backend only accepts a `DATABASE_URL` beginning with `postgresql://` or `postgres://` and uses psycopg 3. Set it on the **deployed Render service** under Environment. A `.env` on your Mac does not automatically configure Render. After editing Render variables, redeploy/restart the service.

For local development, copy `.env.example` to `.env` and replace the sample URL. Never commit `.env` or paste credentials into chat.

```bash
python -m pip install -r requirements.txt
uvicorn server:app --reload
curl -i http://127.0.0.1:8000/health/db
```

Expected healthy result:
`{"database":"connected","tables":{"rsvps":true,"wishes":true,"replies":true}}`

If `/health/db` returns HTTP 503, check Render logs, that your Neon project is active, the database/user/hostname/port and password, and URL encoding for special characters in passwords. The endpoint never reveals credentials.

**Critical:** `GET /health` only checks whether the website process responds; it does not test Neon. Use `/health/db` to verify database access.

The app creates missing tables on startup when connected. If tables are missing, run the supplied SQL schema against the **same Neon database and branch** as `DATABASE_URL`, then restart.

### Verify inserts in Neon SQL Editor
```sql
SELECT id, guest_name, created_at FROM wedding_rsvps ORDER BY id DESC LIMIT 10;
SELECT id, name, message, created_at FROM public_wedding_wishes ORDER BY id DESC LIMIT 10;
SELECT id, wish_id, name, message FROM wedding_wish_replies ORDER BY id DESC LIMIT 10;
```

The website now displays an error when publishing fails; it no longer silently stores wishes in browser localStorage and calls them published. RSVP and comment forms likewise report errors.

## Deployment reminder
Make sure the public site runs the **FastAPI Render service** rather than a static-only host; `/api/rsvp` and `/api/wishes` require the Python backend.
