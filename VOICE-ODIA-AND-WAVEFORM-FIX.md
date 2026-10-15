# Voice repair

- Linked previously unlinked `assets/css/29-concierge-voice.css` in index.html.
- Voice panel is fixed on screen when Talk with us is opened; waveform bars animate during voice sessions.
- Odia TTS tries Subhasini, then Sukant, with one retry each.
- No browser speech synthesis fallback.
- The Edge consumer endpoint is unofficial and may refuse Odia voices; official Azure Speech is the reliable alternative.

## Verify

1. Restart backend and hard-refresh browser (Cmd+Shift+R).
2. Click Talk with us; floating panel must appear before microphone starts.
3. Test Odia directly with: `python -m edge_tts --voice or-IN-SukantNeural --text "ନମସ୍କାର, ଆପଣଙ୍କୁ ସ୍ୱାଗତ।" --write-media odia.mp3`
4. If both Odia voices return NoAudioReceived, configure an authenticated provider; no code can guarantee an unofficial endpoint works.
