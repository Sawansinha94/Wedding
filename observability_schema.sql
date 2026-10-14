-- Execute once in Neon SQL editor. Do not grant SELECT on this table to guest-facing DB roles.
CREATE TABLE IF NOT EXISTS wedding_system_logs (
    event_id UUID PRIMARY KEY,
    timestamp TIMESTAMPTZ NOT NULL DEFAULT now(),
    trace_id UUID,
    request_id UUID,
    session_id TEXT,
    actor_id TEXT,
    ip_hash TEXT,
    http_method TEXT,
    http_path TEXT,
    event_type TEXT NOT NULL,
    level TEXT NOT NULL,
    service TEXT,
    operation TEXT,
    status TEXT,
    duration_ms NUMERIC(12,2),
    source_file TEXT,
    function_name TEXT,
    line_number INTEGER,
    input_data JSONB,
    output_data JSONB,
    details JSONB,
    error JSONB
);
CREATE INDEX IF NOT EXISTS idx_wedding_logs_time ON wedding_system_logs(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_wedding_logs_trace ON wedding_system_logs(trace_id, timestamp);
CREATE INDEX IF NOT EXISTS idx_wedding_logs_error ON wedding_system_logs(timestamp DESC) WHERE level='ERROR';
CREATE INDEX IF NOT EXISTS idx_wedding_logs_service ON wedding_system_logs(service, timestamp DESC);
-- Example retention: schedule via Neon-compatible cron or external job after review:
-- DELETE FROM wedding_system_logs WHERE timestamp < now() - interval '30 days';
