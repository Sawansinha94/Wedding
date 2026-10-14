# Wedding Concierge patch and debugging

## Install
1. Extract this project; copy your private `.env` locally (never upload or commit it).
2. `pip install -r requirements.txt`
3. `python debug_verify.py` to check Neon logging inserts.
4. `uvicorn server:app --reload --port 8000 --log-level debug`
5. Enter **Sailendra Kumar** on the entry page. A floating panel should show the confirmation immediately, with Yes and Not me buttons. The chat panel retains the same state.

## Diagnose
- In browser Developer Tools > Network, inspect `POST /api/profile/start` (expect `status: confirm`).
- Tap Yes; inspect `POST /api/profile/confirm` (expect `ready` or `question`).
- In Neon, run: `SELECT timestamp,trace_id,event_type,service,error FROM wedding_system_logs ORDER BY timestamp DESC LIMIT 50;`
- If no logs, check `python debug_verify.py` and `wedding_log_failures.jsonl`.
- The browser's floating panel listens for `wedding:profile-stage`; it does not use the older `/api/concierge/welcome` endpoint.

## Translation
The bundled `28-multilingual.js` immediately translates strings found in its built-in dictionary and offline catalog; other strings still use `/api/site/translate` and a persistent browser cache. Complete first-load offline translations for every section require generating and reviewing the full catalog; this package does **not** claim full translation coverage. Numbers are preserved where static translations retain ASCII digits. Keep numeric values unchanged when reviewing new translations.

## Security
Name confirmation and personal trivia are conversational checks, not secure authentication. Do not reveal unapproved private profiles. Keep `.env`, logs, and profile master out of public static assets. The full master remains server-side under `data/private`.
