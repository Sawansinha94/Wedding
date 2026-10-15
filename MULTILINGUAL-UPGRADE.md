# Wedding website: welcome screen and four-language UI

The original website features, forms, visitor-name logging, and 20-second optional-name entry remain intact.

## Features
- Premium invitation entrance using existing `images/wedding-monogram.webp` and the Sawan ♥ Pratibha title.
- Four language choices at entrance: English (default), Hindi, Odia and Telugu.
- Persistent header globe language selector; preference stored locally in browser.
- Built-in immediate translations for important entry text, navigation and actions.
- Additional page text and static labels are translated in batches via `/api/site/translate` using the site's existing `OPENROUTER_API_KEY` and `OPENROUTER_MODEL` configuration. Without that key or when the provider is unavailable, non-dictionary content stays English. Therefore complete translation requires a configured and available AI provider.
- AI concierge language, wish generator language, and voice recognition/synthesis preferences follow the global language choice. Browser voice support varies.
- Guest-generated wishes, chat, visitor names and form contents are excluded from automatic UI translation.

## Notes
- AI translation is generated dynamically; review translated content in all three languages before launch. It can be slow or imperfect.
- Dynamic UI strings and server responses may still contain English in error/fallback states. The client does not translate the text of guests' submissions.
- No third-party API key is embedded in the frontend.
- For full offline coverage, replace dynamic translations with reviewed locale catalogs for every visible UI string.
- To test, run the FastAPI app per DEPLOY-LIVE.md and select a language on the welcome page. Change it from the globe control in the header.
