# Wedding Concierge: diagnostic build

This build is based on the prior 72-profile website package, preserving its layout and static assets.

## Confirmed code problems repaired
1. **Neon logger schema mismatch:** previous writer tried to INSERT columns `event_id`, `actor_id`, `http_path` and a JSON error object into columns that do not exist in the SQL schema you created. New writer targets `user_id`, `endpoint`, `error TEXT`, `stack_trace`. This explains silent missing logs.
2. **Concierge KeyError:** `personalized_context()` does not return an `id`, but chat attempted `private_profile["id"]`. Now uses `name`.
3. **Double LLM calls:** the unused retrieval planner invoked an LLM before every guest response, then hard-disabled search. Removed the redundant call.
4. **Bedrock success audit:** undefined `data` variable replaced with `response`.
5. **Performance:** cached master roster and Pinecone name candidate results within the Python process. Restart to refresh profiles.

## Setup
- Copy your newly rotated secrets into `.env` (never include it in ZIP).
- `pip install -r requirements.txt`
- `OBSERVABILITY_ENABLED=true` and `LOG_SENSITIVE_PAYLOADS=true` in `.env` to capture full chat prompts.
- `uvicorn server:app --reload --port 8000 --log-level debug`
- In another terminal: `python debug_verify.py` to verify DB logging writes.
- Open website and enter `Sailendra Kumar`, then check the Concierge prompt.
- Use Chrome DevTools > Network > Fetch/XHR to inspect `/api/profile/start`, `/api/profile/confirm`, `/api/profile/answer`, `/api/concierge`.
- OpenRouter actual request/response is logged as `ai.request` and `ai.response`; assembled prompt as `chat.context.ready`.

## Neon SQL
```sql
SELECT timestamp,trace_id,event_type,service,operation,duration_ms,input_data,output_data,error
FROM public.wedding_system_logs ORDER BY timestamp DESC LIMIT 100;
```

## Limitations
- Live Pinecone/Neon/OpenRouter tests were NOT run here.
- Existing profiles are private; confirmation/trivia does not prove identity. Only safe conversational context is sent to the LLM.
- The logger remains asynchronous and best-effort; on DB write failure it writes `wedding_log_failures.jsonl` locally.
- The frontend's speech service is unchanged.
- Cache is per-process and reset on restart.
