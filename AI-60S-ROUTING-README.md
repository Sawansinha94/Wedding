# AI 60-second timeout and busy-provider routing

- Browser `/api/concierge` and other `requestAI` calls wait up to 60 seconds.
- Backend `AI_TOTAL_TIMEOUT=58` caps the combined OpenRouter and Bedrock attempt.
- OpenRouter has a 45-second ceiling, with time reserved for Bedrock.
- When another request is **currently running** on OpenRouter, new requests immediately use Bedrock.
- A non-blocking OS file lock (`OPENROUTER_BUSY_LOCK_FILE`, default `/tmp/sawan-wedding-openrouter.lock`) detects in-flight calls across workers on the same host. It is automatically released after the request or worker exit.
- Audit events `ai.routing` with `reason=openrouter_busy` document routing decisions. Historical logs are not a reliable indicator of whether a request is still running.
- This file lock does not coordinate multiple independent servers/containers. For distributed deployments, use Redis or a shared coordination service.
- Both providers must be configured for fallback. An AI timeout can still occur because of upstream networking or browser cancellations.
- Restart the Python server and hard-refresh the browser after installing this update.
