from .observability import emit as audit_emit
"""OpenRouter text AI + local faster-whisper STT + Edge neural TTS. Turn based, not native realtime."""
import os, asyncio, tempfile
from pathlib import Path
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import Response
from .llm import model_messages
router=APIRouter()
LANG={'en':'English','hi':'Hindi','or':'Odia','te':'Telugu'}
VOICES={'en':'en-IN-PrabhatNeural','hi':'hi-IN-MadhurNeural','or':'or-IN-SubhasiniNeural','te':'te-IN-MohanNeural'}
_model=None
@router.post('/api/voice/turn')
async def voice_turn(audio: UploadFile=File(...), language: str=Form('en'), history: str=Form('[]')):
    global _model
    if language not in LANG:raise HTTPException(400,'Unsupported language')
    raw=await audio.read(5_000_001)
    if len(raw)>5_000_000:raise HTTPException(413,'Audio exceeds 5MB')
    if not raw:raise HTTPException(400,'Empty audio')
    import hashlib
    audit_emit('voice.audio.received',service='voice',operation='voice_turn',details={'audio_bytes':len(raw),'audio_sha256':hashlib.sha256(raw).hexdigest(),'language':language,'audio_type':audio.content_type})
    try:
        from faster_whisper import WhisperModel
        if _model is None:_model=WhisperModel(os.getenv('WHISPER_MODEL','small'),device='cpu',compute_type='int8')
        with tempfile.NamedTemporaryFile(suffix='.webm') as tmp:
            tmp.write(raw);tmp.flush()
            segments,_=_model.transcribe(tmp.name,language={'en':'en','hi':'hi','or':None,'te':'te'}[language],beam_size=3)
            transcript=' '.join(x.text.strip() for x in segments).strip()
    except Exception as exc:
        raise HTTPException(503,'Speech recognition unavailable; install faster-whisper and FFmpeg') from exc
    if not transcript:raise HTTPException(422,'No speech detected')
    audit_emit('voice.transcript',service='voice',operation='transcribe',output_data={'transcript':transcript,'language':language})
    try:
        import json
        prev=json.loads(history)
        if not isinstance(prev,list):prev=[]
        prev=[{'role':x['role'],'content':str(x['content'])[:1000]} for x in prev[-8:] if isinstance(x,dict) and x.get('role') in ('user','assistant')]
    except Exception:prev=[]
    prompt=('You are the friendly, respectful Sawan and Pratibha Wedding Concierge. Reply briefly and naturally ONLY in '+LANG[language]+'. '
       'Warm, gentle Indian male hosting style. Wedding 24 November 2026 7 PM, Swastik Foundation, Ranchi Ring Road, Ranchi. '
       'Reception 27 November 2026 1 PM, residence, Baghmara, Talcher, Odisha. '
       'Do not claim to know guest identity, and never disclose private profile details. Do not invent facts. '
       'For respected elders, greet with Pranam when appropriate. You are an AI assistant.')
    reply=await model_messages([{'role':'system','content':prompt},*prev,{'role':'user','content':transcript}],temperature=0.5,max_tokens=220)
    audit_emit('voice.reply',service='voice',operation='voice_turn',input_data={'transcript':transcript,'language':language,'history':prev},output_data={'reply':reply})
    return {'transcript':transcript,'reply':reply}
@router.post('/api/voice/speak')
async def voice_speak(payload: dict):
    lang=payload.get('language','en');txt=str(payload.get('text',''))[:1200]
    if lang not in LANG or not txt:raise HTTPException(400,'Invalid speech request')
    import logging
    logger=logging.getLogger(__name__)
    try:
        import edge_tts
    except ImportError as exc:
        raise HTTPException(503,'edge-tts not installed in active Python environment') from exc
    # Odia can intermittently return no audio on the unofficial Edge endpoint.
    # Retry once with the other Odia neural voice; never switch to browser TTS.
    candidates=[VOICES[lang]]
    if lang=='or': candidates.append('or-IN-SukantNeural')
    errors=[]
    for voice in candidates:
        for attempt in range(2 if lang=='or' else 1):
            try:
                stream=edge_tts.Communicate(txt,voice,rate='-4%',pitch='+0Hz')
                chunks=[]
                async for msg in stream.stream():
                    if msg['type']=='audio': chunks.append(msg['data'])
                if not chunks: raise RuntimeError('NoAudioReceived')
                audio_bytes=b''.join(chunks)
                audit_emit('voice.tts',service='voice',operation='voice_speak',input_data={'language':lang,'voice':voice},details={'output_audio_bytes':len(audio_bytes)})
                return Response(audio_bytes,media_type='audio/mpeg',headers={'X-Voice-Used':voice,'Cache-Control':'no-store'})
            except Exception as exc:
                errors.append(f'{voice}: {type(exc).__name__}')
                logger.warning('Voice synthesis failed voice=%s attempt=%s error=%r',voice,attempt+1,exc)
                if attempt==0 and lang=='or': await asyncio.sleep(.35)
    raise HTTPException(503,'Neural speech unavailable for '+LANG[lang]+'. Tried '+', '.join(candidates)+'. Errors: '+', '.join(errors)+'. See backend logs; consider official Azure Speech if Odia remains unavailable.')
@router.post('/api/realtime/session')
async def unsupported_native_realtime():
    raise HTTPException(501,'Native WebRTC realtime requires a supported realtime provider; use /api/voice/turn')

@router.get('/api/voice/health')
async def voice_health():
    try:
        import edge_tts
        return {'edge_tts_installed':True,'voices':VOICES,'note':'Installed does not guarantee network connectivity. POST /api/voice/speak to test synthesis.'}
    except ImportError:
        return {'edge_tts_installed':False,'fix':'python -m pip install -r requirements.txt'}
