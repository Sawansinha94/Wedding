# Modular wedding website

## Frontend
- `index.html`: HTML structure and wedding sections only.
- `assets/css/`: stylesheets extracted in original order; edit the relevant numbered file.
- `assets/js/`: JavaScript features extracted in original execution order.
- `images/`: independent bride, groom, family and story image placeholders.

## Backend
- `server.py`: application bootstrap, static files and route registration.
- `backend/knowledge.py`: confirmed wedding facts and supported languages.
- `backend/schemas.py`: request validation models.
- `backend/database.py`: Neon PostgreSQL / SQLite connections and shared wishes table.
- `backend/rsvp.py`: RSVP persistence and validation.
- `backend/wishes.py`: public wishes feed and publishing.
- `backend/llm.py`: OpenRouter calls.
- `backend/pinecone_store.py`: Pinecone family profile search.
- `backend/concierge.py`: agentic retrieval decisions and chat.
- `backend/generation.py`: wedding wish generation and legacy chat endpoint.

Run `pip install -r requirements.txt` then `uvicorn server:app --reload`. Configure `.env` using `.env.example`.
