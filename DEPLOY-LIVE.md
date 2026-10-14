# Live deployment (Render + Neon + Pinecone + OpenRouter)

## Prerequisites
Python 3.12, Git/GitHub, Render account, Neon database, Pinecone integrated-embedding index, OpenRouter key. Do not commit `.env` or share API keys.

## 1. Run locally
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```
Fill `.env` with `DATABASE_URL`, `OPENROUTER_API_KEY`, `PINECONE_API_KEY`, `PINECONE_INDEX_HOST`, and `PINECONE_NAMESPACE=wedding-family`. Neon URL should use TLS (`sslmode=require`).

## 2. Set up Pinecone
Create an integrated-embedding index, text field `text`, and use its HOST (not its name). Review `data/family/family_profiles.json`, keep only approved-for-guests profiles.
```bash
python ingest_family.py --validate-only
python ingest_family.py --dry-run
python ingest_family.py
```

## 3. Test locally
```bash
uvicorn server:app --reload
```
Visit http://127.0.0.1:8000 and http://127.0.0.1:8000/health. Submit a test RSVP and Wish, then test the Concierge with a wedding-date question and a family-profile question.

## 4. Push code to a PRIVATE GitHub repository
```bash
git init
git add .
git commit -m "Wedding website production deployment"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-PRIVATE-REPO.git
git push -u origin main
```

## 5. Deploy on Render
Dashboard > New > Blueprint, connect the repository, select `render.yaml`. Use a paid persistent web instance for reliability. Enter all secret environment values in Render (not in Git). Render builds with `pip install -r requirements.txt` and starts with `uvicorn server:app --host 0.0.0.0 --port $PORT --proxy-headers`. Note: health check verifies HTTP service only, not the LLM/DB/Pinecone integration.

## 6. Verify production
Open `https://YOUR-SERVICE.onrender.com/health` and `/`. Submit an RSVP and Wish and confirm rows exist in Neon. Test family and non-family questions; `searched_family` should be false for dates and greetings. Test on mobile, microphone permissions (HTTPS), and browser audio playback restrictions. Attach custom domain in Render and set DNS per Render instructions.

## Security / privacy checklist
- No keys or passwords in browser JS, screenshots, or repository.
- Visitor names are self-declared, never proof of identity. Family relationship confirmations do not grant access.
- No visitor or guest profiles in Pinecone.
- Browser localStorage retains the name; chat history resets on page reload.
- Public wishes require moderation/rate limits before sharing broadly. Add CAPTCHA/rate limiting to public write endpoints before inviting many guests.
- Keep PostgreSQL backups and review spending quotas for OpenRouter/Pinecone/Render.
- Existing app uses SQLite as fallback when DATABASE_URL is unset: NEVER rely on SQLite on ephemeral hosting.
