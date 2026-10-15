# Personal Wedding Concierge — setup

1. Edit `data/family/family_profiles.json`. Add only truthful, approved information to `aliases`, `relationship_context`, `shared_memories`, `habits`, `likes`, `dislikes`, `conversation_style`, `conversation_starters`, `wedding_encouragement`, and `topics_to_avoid`. Existing messages are preserved.
2. Check duplicate `groom-brother` / `groom-elder-brother` (Aswini Sinha). The former is disabled to prevent two matches. Verify whether `bride-younger-brother`'s message addressing **Karthik** is intended for **Pradyun Patel**. Grandparent placeholders are disabled.
3. Set `CONCIERGE_SIGNING_SECRET` to a random value of at least 32 characters in `.env` and on your deployment host (`python -c "import secrets; print(secrets.token_urlsafe(48))"`).
4. Run `python make_identity_questions.py`. Add 2–3 approved questions for each person you want to recognize. The answers stay in `data/private/identity_questions.json`, NOT Pinecone. Deploy this file to a server-private location, never to a static/public folder, and never commit it. This simple challenge is low assurance: a shared secret or OTP is stronger.
5. Run `python ingest_family.py --validate-only`, then `--dry-run`, then `python ingest_family.py` using the same integrated-embedding Pinecone index with `text` field and namespace `wedding-family`.
6. Restart FastAPI. Test: enter a known name → confirm relationship → answer challenge → exact Pinecone profile message → conversational follow-ups. An incorrect answer progresses through up to three questions. Missing challenges do not grant personalization.
7. Ordinary wedding questions continue without family retrieval unless the LLM planner needs it. Personalized context is loaded only after verification.

## Privacy and limitations
- Only store profile details the individual would be comfortable having the concierge use. Avoid private, embarrassing, medical, financial, or other sensitive details.
- Names and relationship confirmations are NOT identity verification. Private knowledge questions are also not strong authentication; avoid confidential messages. Stronger option: invite-code or verified OTP.
- This lightweight implementation uses signed challenge tokens; for production-grade abuse resistance add Redis or Neon-backed per-session/IP attempt counters, CAPTCHA, and short-term lockouts. The signed token alone does not stop repeated fresh challenge starts.
- If using integrated-embedding Pinecone, the model's embedding dimension is determined by the index model; you do not increase dimensions by adding JSON fields. Keep conversational context in metadata and index only discovery-friendly facts.
- Pinecone records deleted from the JSON are not automatically removed; delete stale IDs explicitly.
