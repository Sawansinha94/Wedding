# Localization and proactive concierge update

The personalized concierge now has a relationship-specific master prompt in `backend/concierge_personality.py`. After the guest greeting flow, the browser requests an LLM-generated proactive opener through the existing concierge API. The OpenRouter-first, Bedrock-fallback setup is unchanged.

## Completing the 4-language static catalog

The supplied archive retains all existing translated strings. **Not all remaining text has been translated yet**: without a live provider request, it would be misleading to claim otherwise. Run this ONE TIME on your development machine with a working OpenRouter or Bedrock key:

```bash
python build_complete_translations.py
```

This extracts HTML text, attributes and candidate JavaScript interface messages, translates them in batches, caches every completed batch in `assets/js/29-static-catalog.js`, and writes `FULL-TRANSLATION-AUDIT.json`. Review translations and the extracted candidates (JS heuristic may include non-UI phrases) before publishing. No translation model calls happen when a visitor changes language. Refresh the page after generating the catalog.

This is a legacy DOM translation implementation, not a complete migration to explicit `t(key)` calls. Text that is generated inside excluded chat/wish regions, template interpolation, or backend errors may still require explicit localization at their source. Do not treat a catalog count as a full end-to-end browser coverage guarantee.

## Test

Check Pratibha's September 11–12 visit question, Shailendra Kumar's fatherly welcome, Vamsee's mentorship, and multiple consecutive follow-up questions. Test all four languages on every page and dynamic form state. Never publish credentials in the ZIP or browser JavaScript.
