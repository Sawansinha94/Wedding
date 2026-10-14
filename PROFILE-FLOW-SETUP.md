# Wedding Concierge: name matching, question flow and audit

## Setup

1. Keep the existing `.env`. Add `CONCIERGE_SIGNING_SECRET` with a random 32+ character value (for example `python -c 'import secrets;print(secrets.token_urlsafe(48))'`). Never expose this secret in the browser.
2. Set `PINECONE_PRIVATE_INDEX_HOST` to the host containing the **72 records**, and `PINECONE_PRIVATE_NAMESPACE=wedding-private-profiles`. Set `PINECONE_API_KEY` as before. Do not use the legacy `wedding-family` namespace.
3. Configure Neon and execute `observability_schema.sql`; set `OBSERVABILITY_ENABLED=true`, `LOG_SENSITIVE_PAYLOADS=true` if you deliberately want full chat and question-answer logs. Secure Neon access and tell guests about logging.
4. Run `pip install -r requirements.txt` and `uvicorn server:app --reload --port 8000`.
5. On the welcome page, enter `Sailendra Kumar`, open the Concierge, and answer the confirmation prompt. His profile has no question; it uses safe greeting preferences. For `Sandhya`, a question is asked.

## How it works

`POST /api/profile/start` receives the name. Exact matching against the private local master is performed; Pinecone's private namespace is queried to confirm the matching record exists. Pinecone similarity alone never establishes identity. For ambiguous aliases or no match, the visitor continues as a general guest. The backend returns a **signed short-lived confirmation token**, not private profile text.

`POST /api/profile/confirm` asks whether this is the person. If the master has a question with an expected answer, `POST /api/profile/answer` asks it; otherwise it immediately issues a **low-assurance personalization token**. The answer check allows small spelling differences and two attempts. The Concierge then uses only safe greeting and invitation style fields from the master, not private memories or other guest details.

**This is NOT secure identity verification.** A visitor can claim another name and may know trivia answers. No sensitive profile information is released by this flow. For access to complete private biographies or personal memories, implement stronger guest authentication (for example verified email/phone or a one-time invitation link) and authorization first. Do not use a name, confirmation, or trivia question as proof of identity.

## Audit

Events include `profile.start`, `profile.vector.results`, `profile.match.vector_miss`, `profile.confirmation`, `profile.question.answer`, `profile.personalization.ready`, plus existing `chat.user.message`, `chat.assistant.message`, and AI-provider request/response events. Logs are best-effort and depend on Neon availability and logging configuration. Credentials are redacted. The code does not record raw voice audio, but existing voice transcript logs remain available.

## Limitations

- Live Pinecone and Neon connections have **not** been tested here.
- Voice mode uses the existing turn-based service and does not currently drive the confirmation/question workflow; use the text input to complete it first.
- Matching is exact name or alias, rather than fuzzy identity assignment. If multiple people share an alias, matching fails safely.
- The website itself is not gated behind authenticated login. Hosting it publicly would make the non-profile website content accessible.
