# Dedicated realtime voice service — Sawan & Pratibha

Uses OpenAI Realtime speech-to-speech over WebRTC. The FastAPI backend brokers the SDP exchange and keeps the API key server-side.

## Setup

1. Add `OPENAI_API_KEY` to `.env` (requires API billing and realtime model access).
2. Install existing requirements: `pip install -r requirements.txt`.
3. Run `uvicorn server:app --reload`. Open on `https://` or `http://localhost:8000`.
4. Choose language (English/Hindi/Odia/Telugu), open Concierge > Talk with us > Start conversation, allow microphone.
5. Talk naturally; the session uses semantic turn detection and can be interrupted. Switch to Text Chat to end.

## Important limitations

- **Not tested with a live API key**; voice quality, Odia/Telugu understanding, and latency must be tested on real devices. A male Indian accent is requested in instructions but cannot be guaranteed with a built-in voice.
- **Private Pinecone/guest profiles are not connected to realtime voice.** The voice model knows only public wedding basics. Do not deploy private profiles to the browser or expose them without permission.
- **Production security is unfinished**: add per-guest quotas, authentication/CAPTCHA, rate limiting, request size controls and spend alerts before exposing the SDP endpoint publicly. A public endpoint could incur charges.
- Voice mode and existing text mode have **separate conversational contexts**. They are not yet synchronized.
- The service requires paid API access; it does not use a ChatGPT subscription.
- Model and voice availability can change. See https://developers.openai.com/api/docs/guides/voice-webrtc.
- AI voice disclosure appears in the voice panel.
