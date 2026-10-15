# OpenRouter primary / Amazon Bedrock fallback

All backend `llm()` and `model_messages()` requests now try OpenRouter first. On any request/response failure (including HTTP 402, timeouts and invalid responses), the backend tries Bedrock Converse. The static translation builder uses the same provider chain. Existing translations are saved after each successful batch.

## Setup

```bash
pip install -r requirements.txt
```

In `.env`:

```dotenv
OPENROUTER_API_KEY=your_key
OPENROUTER_MODEL=google/gemini-2.5-flash
OPENROUTER_TIMEOUT=25
AWS_REGION=ap-south-1
BEDROCK_MODEL_ID=your_enabled_bedrock_converse_model_id
```

Bedrock supports standard AWS credential chains (AWS profile, IAM role, environment credentials). For Bedrock API keys, use `AWS_BEARER_TOKEN_BEDROCK=your_bedrock_api_key` with a current boto3/botocore version that supports Bedrock bearer credentials. Do not put secrets into frontend JS or commit `.env`.

**Prerequisites:** The selected Bedrock model must support the Converse API, be enabled/available in the selected region, and the credentials must have `bedrock:InvokeModel` permission. Some models require inference profile IDs rather than direct model IDs. Charges and quotas are separate for both providers.

## Run

```bash
python build_static_translations.py
uvicorn server:app --reload --port 8000
```

For a fallback test, temporarily set `OPENROUTER_MODEL=invalid/model-id` in a **local** environment and run a single chat request. The backend should use Bedrock if configured correctly. Restore the original model afterwards. Do not use a deliberately invalid model in production.

## Limits

This fallback covers backend LLM text generation and the static translation builder. It does **not** replace Whisper, Edge TTS, microphone or voice services. Translation batches may still fail when models truncate JSON; inspect and retry. The project has not been live-tested against your AWS account.
