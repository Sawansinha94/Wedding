# OpenRouter -> Bedrock OpenAI-compatible fallback

Set `OPENROUTER_API_KEY` and `OPENROUTER_MODEL` first. Configure `BEDROCK_BASE_URL` (the actual OpenAI-compatible `/v1` base URL supplied by your Bedrock provider), `BEDROCK_API_KEY`, and `BEDROCK_MODEL_ID=openai.gpt-oss-120b` in `.env`. The application appends `/chat/completions` unless the base URL already ends with it. The key is never exposed to the browser. Restart `python server.py`.

**Important:** This path uses bearer-key OpenAI-compatible API authentication. AWS IAM/SigV4 Bedrock endpoints are different and require a different client; do not use a standard AWS console URL here.

OpenRouter is tried on every request. On any OpenRouter error, the same messages are sent to Bedrock. If both fail, the caller gets the existing controlled provider error. `stream=False` is intentional: the website's existing routes expect a complete text response. The streaming sample provided by the user is not wired to the HTTP chat UI.

Profile personalization is intentionally limited to fields approved for guests; the name-and-familiarity challenge is not secure authentication. For biographical fields to be supplied, the profile must have `approved_for_guests: true`, `visibility_policy.public_summary_approved: true`, and `review_status: approved`. Owner-only private notes are never sent to the LLM.

Static UI translations are in `assets/js/29-static-catalog.js`. To rebuild after changing website copy, run `python build_static_translations.py` with working provider credentials and review the generated translations. Dynamic generated text uses the selected language in the Concierge prompt.
