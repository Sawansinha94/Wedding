# Concierge repair patch

- Removed invitation-code UI and text-mode button. **Private-profile personalization is intentionally not enabled without authenticated guest access.** Name matching is not authentication.
- Talk With Us now prefers browser speech recognition and browser speech synthesis, falling back to existing server recording mode where unavailable. This is a functional fallback, **not ChatGPT-style realtime voice**; Odia and Telugu browser voices vary by OS and browser. Requires microphone permission and HTTPS/localhost.
- Website language switching no longer waits for live API translation. Existing core strings change immediately. To precompile the rest of the website's static copy, run `python build_static_translations.py` once with an OpenRouter key, review the generated `data/static-translations.json`, then deploy the bundled `assets/js/29-static-catalog.js`. Dynamic AI chat replies use the selected language.
- Pinecone private records are not queried by the guest-facing Concierge: this is deliberate until secure authentication is in place. Run `python diagnose_private_pinecone.py "Sailendra Kumar"` to confirm private-index ingestion, namespace and search independently.
- Nothing was uploaded to Pinecone or deployed. Keep all profiles private and do not expose the diagnostic script via HTTP.
