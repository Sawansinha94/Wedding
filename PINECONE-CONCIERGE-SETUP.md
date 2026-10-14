# Your Wedding Concierge — Setup

## Environment
Copy `.env.example` to `.env`. Set `OPENROUTER_API_KEY`, `OPENROUTER_MODEL`, `PINECONE_API_KEY`, `PINECONE_INDEX_HOST`, `PINECONE_NAMESPACE=wedding-family`. Never put API keys in HTML or browser JavaScript.

## Pinecone
Create a **separate integrated-embedding index** (text field `text`) in Pinecone. Set `PINECONE_INDEX_HOST` to the index host, not its console URL. The agent queries the index only when its planning step determines family retrieval is needed. Pinecone and OpenRouter must both be configured for the full agent.

Upload one record per person, with a unique ID and text plus metadata fields `name`, `side` (groom/bride), `relation`, `age` (optional), `traits` (optional), `bio` (optional). Use the script `seed_family.py` as a starter and edit the JSON before uploading. Do not publish sensitive or unconsented biographical data; guests can ask questions about indexed records.

## Conversation and speech
The frontend sends the most recent 12 conversation turns for context. History is kept in JavaScript memory only: refreshing clears it. Speech recognition uses the browser's Web Speech API and may not be available on all browsers or languages. Text-to-speech uses installed browser voices. Microphone access generally requires HTTPS or localhost and user permission; playback may require user interaction.

## Running
`pip install -r requirements.txt` then `uvicorn server:app --reload`. Test `POST /api/concierge` with `question`, `language`, `history`. The website continues to offer limited static answers when the agent service is unavailable. No changes to the existing RSVP and public wishes tables are required.
