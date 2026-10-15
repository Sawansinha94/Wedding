"""Structured, non-blocking Neon audit events. Sensitive payload capture is opt-in.

Initialize schema first with observability_schema.sql. Never expose this module to guests.
"""
import contextvars
import datetime as dt
import functools
import hashlib
import inspect
import json
import logging
import os
import queue
import re
import threading
import time
import traceback
import uuid

log = logging.getLogger('wedding.observability')
_ctx = contextvars.ContextVar('wedding_trace', default={})
_q = queue.Queue(maxsize=5000)
_started = False
_lock = threading.Lock()
_drop_count = 0

_SECRET = re.compile(r'(?i)(authorization|api[_-]?key|token|password|secret|cookie|set-cookie|aws_access_key_id|aws_secret_access_key|credential|bearer)')
_TOKEN = re.compile(r'(?i)\b(sk-or-[A-Za-z0-9_-]+|AKIA[A-Z0-9]{16}|Bearer\s+[^\s]+)\b')


def _clean(value, depth=0):
    if depth > 6:
        return '[max-depth]'
    if isinstance(value, dict):
        return {str(k)[:100]: ('[REDACTED]' if _SECRET.search(str(k)) else _clean(v, depth + 1)) for k, v in list(value.items())[:300]}
    if isinstance(value, (list, tuple)):
        return [_clean(v, depth + 1) for v in value[:300]]
    if isinstance(value, str):
        return _TOKEN.sub('[REDACTED]', value[:int(os.getenv('LOG_MAX_FIELD_CHARS', '60000'))])
    if isinstance(value, (int, float, bool)) or value is None:
        return value
    return _clean(str(value), depth + 1)


def _payload(value):
    if not os.getenv('LOG_SENSITIVE_PAYLOADS', 'false').lower() == 'true':
        return {'omitted': True, 'reason': 'LOG_SENSITIVE_PAYLOADS=false'}
    return _clean(value)


def bind(**values):
    return _ctx.set({**_ctx.get(), **values})


def reset(token):
    _ctx.reset(token)


def emit(event_type, *, level='INFO', service=None, operation=None, status='ok', duration_ms=None,
         input_data=None, output_data=None, details=None, exception=None, caller_depth=1):
    """Best effort: never block or fail a website request because logging is unavailable."""
    if os.getenv('OBSERVABILITY_ENABLED', 'true').lower() != 'true':
        return
    frame = inspect.currentframe()
    try:
        for _ in range(caller_depth):
            frame = frame.f_back if frame else None
        context = _ctx.get()
        error = None
        if exception is not None:
            error = {'type': type(exception).__name__, 'message': _clean(str(exception)),
                     'traceback': _clean(''.join(traceback.format_exception(type(exception), exception, exception.__traceback__))[-8000:])}
        item = {
            'event_id': str(uuid.uuid4()), 'timestamp': dt.datetime.now(dt.timezone.utc).isoformat(),
            'trace_id': context.get('trace_id'), 'request_id': context.get('request_id'),
            'session_id': context.get('session_id'), 'actor_id': context.get('actor_id'),
            'ip_hash': context.get('ip_hash'), 'http_method': context.get('http_method'),
            'http_path': context.get('http_path'), 'event_type': event_type, 'level': level,
            'service': service, 'operation': operation, 'status': status,
            'duration_ms': duration_ms, 'source_file': os.path.basename(frame.f_code.co_filename) if frame else None,
            'function_name': frame.f_code.co_name if frame else None,
            'line_number': frame.f_lineno if frame else None,
            'input_data': _payload(input_data), 'output_data': _payload(output_data),
            'details': _clean(details or {}), 'error': error,
        }
        try:
            _q.put_nowait(item)
        except queue.Full:
            global _drop_count
            _drop_count += 1
            log.warning('Observability queue full; dropped event (total %s)', _drop_count)
    finally:
        del frame


def _worker():
    while True:
        batch = [_q.get()]
        try:
            while len(batch) < 40:
                batch.append(_q.get_nowait())
        except queue.Empty:
            pass
        try:
            import psycopg
            from psycopg.types.json import Jsonb
            db_url = os.getenv('DATABASE_URL', '')
            if not db_url:
                raise RuntimeError('DATABASE_URL missing')
            # Matches the existing Neon schema created in the SQL editor.
            with psycopg.connect(db_url, connect_timeout=8) as conn:
                with conn.cursor() as cur:
                    cur.executemany('''INSERT INTO public.wedding_system_logs (
                        timestamp, trace_id, request_id, session_id, user_id, ip_hash,
                        http_method, endpoint, event_type, level, service, operation, status,
                        duration_ms, source_file, function_name, line_number, input_data,
                        output_data, details, error, stack_trace)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''', [
                        (e['timestamp'],e['trace_id'],e['request_id'],e['session_id'],
                         e['actor_id'],e['ip_hash'],e['http_method'],e['http_path'],
                         e['event_type'],e['level'],e['service'],e['operation'],e['status'],
                         e['duration_ms'],e['source_file'],e['function_name'],e['line_number'],
                         Jsonb(e['input_data']),Jsonb(e['output_data']),Jsonb(e['details']),
                         json.dumps(e['error'],ensure_ascii=False) if e['error'] else None,
                         e['error'].get('traceback') if e['error'] else None) for e in batch])
        except Exception as exc:
            log.exception('Log write failed; %d events not persisted: %s', len(batch), exc)
            # Local fallback, for diagnosing database failures without losing the event.
            try:
                with open(os.getenv('LOG_FAILURE_FILE', 'wedding_log_failures.jsonl'), 'a', encoding='utf-8') as fh:
                    for event in batch:
                        fh.write(json.dumps({'failure':str(exc),'event':event},ensure_ascii=False,default=str)+'\n')
            except OSError:
                log.exception('Local log fallback also failed')
        finally:
            for _ in batch:
                _q.task_done()


def start():
    global _started
    with _lock:
        if not _started and os.getenv('OBSERVABILITY_ENABLED', 'true').lower() == 'true':
            threading.Thread(target=_worker, daemon=True, name='wedding-db-logger').start()
            _started = True


def traced(event_type, service=None):
    """Decorator for synchronous and asynchronous business functions."""
    def decorate(fn):
        if inspect.iscoroutinefunction(fn):
            @functools.wraps(fn)
            async def async_wrapper(*args, **kwargs):
                t = time.perf_counter()
                try:
                    result = await fn(*args, **kwargs)
                    emit(event_type, service=service, operation=fn.__name__,
                         duration_ms=round((time.perf_counter()-t)*1000, 2),
                         input_data={'args':args,'kwargs':kwargs},output_data=result)
                    return result
                except Exception as exc:
                    emit(event_type, level='ERROR', service=service, operation=fn.__name__,status='error',
                         duration_ms=round((time.perf_counter()-t)*1000,2), exception=exc)
                    raise
            return async_wrapper
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            t = time.perf_counter()
            try:
                result = fn(*args, **kwargs)
                emit(event_type,service=service,operation=fn.__name__,duration_ms=round((time.perf_counter()-t)*1000,2),
                     input_data={'args':args,'kwargs':kwargs},output_data=result)
                return result
            except Exception as exc:
                emit(event_type,level='ERROR',service=service,operation=fn.__name__,status='error',
                     duration_ms=round((time.perf_counter()-t)*1000,2),exception=exc)
                raise
        return wrapper
    return decorate


async def http_audit_middleware(request, call_next):
    """Request metadata, status and latency; never log raw IP or untrusted X-Forwarded-For."""
    from fastapi.responses import JSONResponse
    start()
    trace_id = str(uuid.uuid4())
    # A keyed digest permits limited incident correlation without storing IP addresses.
    raw_ip = request.client.host if request.client else ''
    salt = os.getenv('LOG_IP_HASH_SECRET', '')
    ip_hash = hashlib.sha256((salt + raw_ip).encode()).hexdigest() if salt and raw_ip else None
    token = bind(trace_id=trace_id, request_id=trace_id, ip_hash=ip_hash,
                 http_method=request.method, http_path=request.url.path)
    started = time.perf_counter()
    # Capture JSON and textual input before downstream processing. Never store credentials.
    # Starlette caches request.body() so downstream request handlers can still read it.
    if os.getenv('LOG_SENSITIVE_PAYLOADS', 'false').lower() == 'true' and request.method in ('POST','PUT','PATCH'):
        ctype = request.headers.get('content-type', '').lower()
        if 'application/json' in ctype or 'text/plain' in ctype:
            try:
                body = await request.body()
                cap = int(os.getenv('LOG_MAX_HTTP_BODY_BYTES', '131072'))
                if len(body) <= cap:
                    try:
                        parsed = json.loads(body)
                    except (ValueError, UnicodeError):
                        parsed = body.decode('utf-8', errors='replace')
                    emit('http.request.body', service='fastapi', operation=request.url.path,
                         input_data=parsed, details={'bytes': len(body), 'content_type': ctype})
                else:
                    emit('http.request.body.skipped', service='fastapi', operation=request.url.path,
                         details={'bytes': len(body), 'reason': 'size_limit'})
            except Exception as exc:
                emit('http.request.body.error', service='fastapi', operation=request.url.path,
                     level='WARNING', status='error', exception=exc)
    try:
        response = await call_next(request)
        emit('http.request', service='fastapi',operation=request.url.path,
             status='ok' if response.status_code < 400 else 'http_error',
             level='INFO' if response.status_code < 400 else 'WARNING',
             duration_ms=round((time.perf_counter()-started)*1000,2),
             details={'status_code':response.status_code,'query_keys':list(request.query_params.keys()),
                      'user_agent':_clean(request.headers.get('user-agent',''))[:200]})
        response.headers['X-Trace-ID'] = trace_id
        return response
    except Exception as exc:
        emit('http.exception',service='fastapi',operation=request.url.path,status='error',level='ERROR',
             duration_ms=round((time.perf_counter()-started)*1000,2),exception=exc)
        raise
    finally:
        reset(token)
