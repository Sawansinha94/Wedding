"""OpenRouter first, Amazon Bedrock Converse second. No client-side credentials."""
import asyncio
import logging
import os
import httpx
import time
import fcntl
from pathlib import Path

log = logging.getLogger(__name__)
from .observability import emit as audit_emit

class AIProviderError(RuntimeError):
    pass


def _content(value):
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return '\n'.join(str(part.get('text', '')) for part in value if isinstance(part, dict) and part.get('type') == 'text')
    return str(value or '')


async def _openrouter(messages, temperature, max_tokens):
    key = os.getenv('OPENROUTER_API_KEY', '').strip()
    if not key:
        raise AIProviderError('OpenRouter API key missing')
    url = os.getenv('OPENROUTER_BASE_URL', 'https://openrouter.ai/api/v1/chat/completions')
    payload = {'model': os.getenv('OPENROUTER_MODEL', 'google/gemini-2.5-flash'),
               'messages': messages, 'temperature': temperature, 'max_tokens': max_tokens}
    audit_emit('ai.request',service='openrouter',operation='chat.completions',input_data=payload,details={'model':payload['model']})
    async with httpx.AsyncClient(timeout=float(os.getenv('OPENROUTER_TIMEOUT', '50'))) as client:
        response = await client.post(url, headers={'Authorization': f'Bearer {key}'}, json=payload)
        if response.status_code >= 400:
            audit_emit('ai.failure', service='openrouter',operation='chat.completions',status='error',level='ERROR',
                       input_data=payload,output_data={'http_status':response.status_code,'response_body':response.text},details={'http_status':response.status_code,'model':payload['model']})
            raise AIProviderError(f'OpenRouter HTTP {response.status_code}: {response.text[:300]}')
        data = response.json()
        answer = data['choices'][0]['message']['content'].strip()
        audit_emit('ai.response', service='openrouter', operation='chat.completions',
                   input_data={'messages': messages, 'model':payload['model']},output_data={'answer':answer,'provider_response':data},
                   details={'http_status':response.status_code,'model':payload['model'],'usage':data.get('usage')})
        return answer


async def _bedrock_openai(messages, temperature, max_tokens):
    """Bedrock OpenAI-compatible endpoint, not boto3 Converse.

    BEDROCK_BASE_URL may be a base ending /v1 or a complete /chat/completions URL.
    """
    key = os.getenv('BEDROCK_API_KEY', '').strip()
    base = os.getenv('BEDROCK_BASE_URL', '').strip().rstrip('/')
    model = os.getenv('BEDROCK_MODEL_ID', 'openai.gpt-oss-120b').strip()
    if not key or not base:
        raise AIProviderError('BEDROCK_API_KEY and BEDROCK_BASE_URL must be configured')
    url = base if base.endswith('/chat/completions') else base + '/chat/completions'
    payload = {'model': model, 'messages': messages, 'temperature': temperature,
               'max_tokens': max_tokens, 'stream': False}
    audit_emit('ai.request', service='bedrock', operation='chat.completions',
               details={'model':model, 'message_count':len(messages)})
    async with httpx.AsyncClient(timeout=float(os.getenv('BEDROCK_TIMEOUT','55'))) as client:
        response = await client.post(url, headers={'Authorization':f'Bearer {key}',
            'Content-Type':'application/json'}, json=payload)
        if response.status_code >= 400:
            log.warning('Bedrock chat completion failed with HTTP %s', response.status_code)
            raise AIProviderError(f'Bedrock HTTP {response.status_code}')
        data = response.json()
        answer = _content(data['choices'][0]['message'].get('content')).strip()
        if not answer:
            raise AIProviderError('Bedrock returned empty content')
        audit_emit('ai.response', service='bedrock', operation='chat.completions',
                   details={'model':model, 'usage':data.get('usage',{})})
        return answer


# An advisory, non-blocking OS file lock tracks in-flight OpenRouter calls.
# Unlike checking historical logs, this reflects whether a request is ACTIVE.
# It works across worker processes on the same host; separate hosts need Redis.
_OPENROUTER_LOCK_PATH = Path(os.getenv('OPENROUTER_BUSY_LOCK_FILE', '/tmp/sawan-wedding-openrouter.lock'))


def _acquire_openrouter_slot():
    _OPENROUTER_LOCK_PATH.parent.mkdir(parents=True, exist_ok=True)
    handle = open(_OPENROUTER_LOCK_PATH, 'a+')
    try:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        handle.close()
        return None
    return handle


def _release_openrouter_slot(handle):
    if handle is not None:
        fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
        handle.close()


async def generate(messages, *, temperature=0.25, max_tokens=500):
    """60s browser budget; keep server work under 58s, route busy OpenRouter to Bedrock.

    A log event is emitted for each routing decision. Logs alone cannot reliably
    identify in-flight requests, so the live OS lock is authoritative here.
    """
    budget = max(1.0, min(float(os.getenv('AI_TOTAL_TIMEOUT', '58')), 59.0))
    deadline = time.monotonic() + budget
    slot = _acquire_openrouter_slot()
    if slot is None:
        log.info('OpenRouter already processing a request; routing this request to Bedrock')
        audit_emit('ai.routing', service='ai-router', operation='generate',
                   details={'reason': 'openrouter_busy', 'selected': 'bedrock'})
    else:
        try:
            # Reserve some time for Bedrock if OpenRouter fails or times out.
            remaining = deadline - time.monotonic()
            openrouter_limit = min(float(os.getenv('OPENROUTER_TIMEOUT', '45')), max(1.0, remaining - 12.0))
            try:
                return await asyncio.wait_for(
                    _openrouter(messages, temperature, max_tokens), timeout=openrouter_limit)
            except asyncio.CancelledError:
                raise
            except Exception as exc:
                log.warning('OpenRouter failed; trying Bedrock: %s', type(exc).__name__)
                audit_emit('ai.fallback', service='ai-router', operation='generate',
                           status='fallback', level='WARNING', exception=exc)
        finally:
            _release_openrouter_slot(slot)

    remaining = deadline - time.monotonic()
    if remaining <= 0:
        raise AIProviderError('AI response timed out')
    try:
        return await asyncio.wait_for(
            _bedrock_openai(messages, temperature, max_tokens), timeout=remaining)
    except asyncio.CancelledError:
        raise
    except Exception as exc:
        log.error('Bedrock fallback failed: %s', type(exc).__name__)
        audit_emit('ai.failure', service='bedrock', operation='generate',
                   status='error', level='ERROR', exception=exc)
        raise AIProviderError('Both AI providers unavailable or timed out') from exc
