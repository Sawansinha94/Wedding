# Wedding Concierge — Neon System Observability

## 1. Database setup

Run `observability_schema.sql` in Neon SQL Editor before starting the app. Use a dedicated database role with INSERT for application logging; keep SELECT restricted to the owner/admin. The existing application DATABASE_URL needs INSERT on `wedding_system_logs`.

## 2. Environment

Append to your `.env`:

```dotenv
OBSERVABILITY_ENABLED=true
LOG_SENSITIVE_PAYLOADS=false
LOG_IP_HASH_SECRET=generate_a_long_random_secret
```

**Do not turn `LOG_SENSITIVE_PAYLOADS=true` on for guest traffic without appropriate consent, access controls, retention and redaction review.** It records prompts and outputs and could include profile information. Even with this option enabled, automatic redaction is not perfect. Never store API keys, passwords, cookies, authorization headers or raw voice recordings in logs.

`LOG_IP_HASH_SECRET` is used to create a pseudonymous IP hash. No raw IP is saved. Reverse proxies should be configured separately; do not trust arbitrary X-Forwarded-For headers.

## 3. Install and start

```bash
pip install -r requirements.txt
uvicorn server:app --reload --port 8000
```

In a second terminal:

```bash
curl -i http://127.0.0.1:8000/health
```

A `X-Trace-ID` response header identifies the request in logs. The logger writes in batches in a background thread. It will never block a visitor request, but logging is best-effort and queued events may be lost on sudden shutdown or database failure.

## 4. Query Neon logs

```sql
-- Latest errors
SELECT timestamp, trace_id, service, operation, source_file, function_name,
       line_number, details, error
FROM wedding_system_logs
WHERE level = 'ERROR'
ORDER BY timestamp DESC LIMIT 50;

-- Trace a request end-to-end
SELECT timestamp, event_type, service, operation, status, duration_ms, details
FROM wedding_system_logs
WHERE trace_id = 'PASTE-X-TRACE-ID-HERE'::uuid
ORDER BY timestamp;

-- Slow endpoints
SELECT http_path, count(*) AS requests, round(avg(duration_ms),2) AS avg_ms,
       round(max(duration_ms),2) AS max_ms
FROM wedding_system_logs
WHERE event_type='http.request' AND timestamp > now()-interval '24 hours'
GROUP BY http_path ORDER BY avg_ms DESC;

-- Provider fallbacks
SELECT timestamp, trace_id, service, details, error
FROM wedding_system_logs
WHERE event_type='ai.fallback'
ORDER BY timestamp DESC LIMIT 30;

-- Vector events
SELECT timestamp, trace_id, operation, status, duration_ms
FROM wedding_system_logs
WHERE event_type LIKE 'vector.%'
ORDER BY timestamp DESC LIMIT 30;
```

## 5. Instrument additional functions and scripts

```python
from backend.observability import start, emit, traced
start()

@traced('rsvp.validate', service='rsvp')
def validate_rsvp(payload):
    return {'valid': True}

emit('script.start', service='ingestion', operation='ingest_private_profiles',
     details={'record_count':72})
```

For standalone scripts, run `start()` before emitting. Because writes are asynchronous, a script that exits immediately may not flush its logs. For important one-off ingestion jobs, add an explicit synchronous flush or use direct database logging; do not assume a queued event is persisted when the script exits.

## 6. Security and limitations

- Database access to logs must be admin-only. Never expose an unauthenticated log-reading endpoint.
- Source filename, function name, and line number are captured at the **logging call site**, not necessarily the deepest point of failure; exceptions also store stack traces.
- No request body or response body is captured by HTTP middleware. Function-level capture is opt-in and defaults to omitted.
- The vector integration records operations, latency and exceptions, but not full Pinecone HTTP payloads by default.
- HTTP calls in unrelated modules are not automatically traced; instrument their service functions with `@traced` or `emit`.
- Raw IPs are not stored. IP hash is available only if `LOG_IP_HASH_SECRET` is configured.
- The queue drops events when full; DB failures also lose affected batches. For guaranteed audit trails, use a durable queue and monitoring/alerting.
- Apply retention, e.g. delete events older than 30 days with a scheduled admin task. Rotate credentials and limit production DB access.
