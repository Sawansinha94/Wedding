# Voice diagnostics

1. Restart the backend using the Python environment where dependencies are installed.
2. Run `python -m pip install -r requirements.txt` (from the project root).
3. Visit `http://localhost:8000/api/voice/health` and verify `edge_tts_installed: true`.
4. Test: `curl -v -X POST http://localhost:8000/api/voice/speak -H 'Content-Type: application/json' -d '{"language":"hi","text":"नमस्कार, आपका स्वागत है।"}' --output /tmp/wedding-hindi.mp3`
5. If the endpoint returns 503, check backend terminal logs. Microsoft Edge TTS requires external network access and may be blocked or change upstream. This project cannot guarantee synthesis when the external service is unreachable.
6. Hard refresh the browser (Cmd+Shift+R), click Talk with us: the floating panel should appear immediately, before pressing Start conversation.

The browser microphone speech recognition may still be used; speech output uses the backend only.
