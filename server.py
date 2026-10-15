"""Wedding website application entry point: uvicorn server:app --reload."""
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import logging
import psycopg
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
BASE=Path(__file__).resolve().parent
load_dotenv(BASE/'.env')
from backend.database import init_wishes
from backend.rsvp import init_rsvps
from backend import profile_flow,concierge,generation,wishes,rsvp,proactive,rephrase,telemetry,identity,site_translation,realtime_voice
from backend.private_profile_search import router as owner_profile_router
from backend.event_registry import sync_events
from backend.telemetry import init_telemetry
from backend.observability import http_audit_middleware, start as start_observability, emit as audit_emit
app=FastAPI(title='Sawan & Pratibha Wedding')
app.middleware("http")(http_audit_middleware)
app.include_router(owner_profile_router)
app.mount('/images',StaticFiles(directory=BASE/'images'),name='images')
app.mount('/assets',StaticFiles(directory=BASE/'assets'),name='assets')
for module in (profile_flow,concierge,generation,wishes,rsvp,proactive,rephrase,telemetry,identity,site_translation,realtime_voice):
    app.include_router(module.router)
logger=logging.getLogger('wedding.database')

@app.on_event('startup')
def initialize_database():
    start_observability()
    audit_emit('application.startup', service='fastapi', operation='initialize_database')
    try:
        init_wishes()
        init_rsvps()
        sync_events()
        init_telemetry()
        logger.info('Neon PostgreSQL tables are ready.')
    except Exception as exc:
        # Keep the website accessible so /health/db can report an outage.
        logger.error('Neon initialization failed: %s', type(exc).__name__)

@app.exception_handler(psycopg.Error)
async def postgres_error(request: Request, exc: psycopg.Error):
    logger.error('Database operation failed at %s: %s', request.url.path, type(exc).__name__)
    return JSONResponse(status_code=503,content={'detail':'Database unavailable. Your submission was NOT saved. Please retry later.'})

@app.exception_handler(RuntimeError)
async def configuration_error(request: Request, exc: RuntimeError):
    if 'DATABASE_URL' in str(exc):
        logger.error('DATABASE_URL missing or invalid for %s',request.url.path)
        return JSONResponse(status_code=503,content={'detail':'Neon database is not configured. Your submission was NOT saved.'})
    raise exc

@app.get('/health')
def health():
    return {'status':'ok'}

@app.get('/health/db')
def database_health():
    from backend.database import wishes_db
    try:
        with wishes_db() as (db, _):
            db.execute('SELECT 1').fetchone()
            tables=db.execute("SELECT to_regclass('public.wedding_rsvps'), to_regclass('public.public_wedding_wishes'), to_regclass('public.wedding_wish_replies')").fetchone()
        with wishes_db() as (db, _):
            mapped=db.execute("""SELECT to_regclass('public.ai_chat_history'),to_regclass('public.guests'),
                to_regclass('public.rsvp_responses'),to_regclass('public.website_visits'),
                to_regclass('public.wedding_events'),to_regclass('public.wedding_wishes'),
                to_regclass('public.wedding_site_activity')""").fetchone()
        return {'database':'connected','tables':{'rsvps':bool(tables[0]),'wishes':bool(tables[1]),'replies':bool(tables[2]),
            'ai_chat_history':bool(mapped[0]),'guests':bool(mapped[1]),'rsvp_responses':bool(mapped[2]),
            'website_visits':bool(mapped[3]),'wedding_events':bool(mapped[4]),'wedding_wishes':bool(mapped[5]),
            'wedding_site_activity':bool(mapped[6])}}
    except Exception as exc:
        logger.error('Neon health check failed: %s',type(exc).__name__)
        return JSONResponse(status_code=503,content={'database':'unavailable','message':'Check DATABASE_URL, Neon network access, and Render logs. No credentials are exposed.'})

@app.get('/')
def home():
    return FileResponse(BASE/'index.html')
