# Full conversation and service logging

1. Run `observability_schema.sql` in Neon SQL Editor if not already applied.
2. Merge `.env.logging.example` settings into your `.env`.
3. Start `uvicorn server:app --reload --port 8000`.
4. Test text chat and voice; inspect `wedding_system_logs`.

This mode stores chat messages, prompts and AI outputs (including system prompts) and voice transcripts. It records model requests, provider responses, fallback events, HTTP JSON/text request bodies, request metadata, Pinecone instrumented operations, and exceptions. Binary microphone recordings are **not** persisted: their size and SHA-256 fingerprint are logged. It does not automatically capture every Python function or all third-party network calls; add `@traced` where needed. HTTP response bodies not explicitly emitted by handlers are not captured. Logs redact API keys, passwords, authorization headers and bearer tokens even with full payload logging enabled.

The existing asynchronous database writer can drop events on process crash or DB outage. This is diagnostic logging, not a guaranteed audit trail. Avoid exposing log table to guests. Protect and restrict DB access, choose retention, and disclose recording/transcript logging to guests. Do not use these logs to store authentication secrets.

Example queries:

```sql
SELECT timestamp, trace_id, event_type, service, operation, input_data, output_data, details, error
FROM wedding_system_logs ORDER BY timestamp DESC LIMIT 100;
```

```sql
SELECT timestamp, event_type, input_data, output_data
FROM wedding_system_logs
WHERE event_type IN ('chat.user.message','chat.assistant.message','voice.transcript','voice.reply','ai.request','ai.response')
ORDER BY timestamp DESC LIMIT 100;
```
