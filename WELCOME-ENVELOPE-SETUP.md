# Welcome envelope and Neon name logging

1. Run `NEON-WELCOME-NAME-MIGRATION.sql` in the Neon SQL Editor.
2. Keep `DATABASE_URL` configured in your server environment.
3. Start/redeploy FastAPI.
4. In a private/incognito browser window, open the site. A first-name prompt appears before the invitation.
5. Enter a name; the site sends it to `/api/telemetry/visitor-name` and opens only after Neon confirms the insert.
6. Verify: `SELECT first_name,session_id,created_at FROM wedding_visitor_names ORDER BY id DESC LIMIT 30;`
7. Family matching then runs in the background, whether the name matches Pinecone or not. Matching does not establish identity; the existing verification flow remains required for personal messages.

The prompt appears once per browser tab session. Refreshing or navigating within the tab preserves the name and session ID; a new tab or new browser session asks again. Session storage is used for tab-local continuity, while Neon stores every successful welcome submission. Browsers may restore tabs after reopening; session storage can then survive a browser restart. If Neon is unavailable, the envelope stays open and shows a retry message. Names are personal data; disclose collection in a privacy notice and set a retention policy.
