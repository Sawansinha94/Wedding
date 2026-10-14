# Wedding Concierge — text and voice modes

- Header shortcut opens the concierge section.
- Text chat remains available; voice is opt-in through Talk with us -> Start conversation.
- Speech recognition and speech synthesis use browser Web Speech APIs, and reuse the existing `/api/concierge` endpoint and selected language.
- Supported language requests: English (en-IN), Hindi (hi-IN), Odia (or-IN), Telugu (te-IN). Actual recognition accuracy and available spoken voices depend on device/browser.
- Indian male voice is preferred when an appropriate installed browser voice exists; **not guaranteed**.
- This is a turn-taking voice mode, **not ChatGPT Realtime voice**. For consistent natural Indian male voices, low-latency streaming, interruption/barge-in, and high-quality Odia/Telugu speech, integrate a dedicated streaming STT/LLM/TTS or realtime speech service on the backend.
- Requires HTTPS for microphone on deployed sites and explicit microphone permission.
- Privacy: browser speech recognition may use third-party speech services depending on the browser. Obtain consent and review privacy policies before deployment.
- Live browser/device QA not performed; test Chrome desktop/Android and Safari iOS, especially Odia/Telugu.
