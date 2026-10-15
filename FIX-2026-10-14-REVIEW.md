# Fixes and diagnosis

- Added bundled Hindi/Odia/Telugu translations for 17 prominent missing story and ceremony strings. These load without a translation API. Translation coverage remains incomplete: see TRANSLATION-AUDIT.json.
- Replaced misleading generic concierge answer on AI API errors with an explicit connection failure message for profile queries.
- Added `profile_blocked_by_guest_policy` to concierge diagnostics.
- Pratibha profile is `approved_for_guests: false` and `share_with_subject_after_verified_login: false`; her full JSON is therefore intentionally not exposed to anonymous chat. Approve access only after choosing an appropriate authentication/consent mechanism. A nickname knowledge question is not strong identity verification.
- No live OpenRouter, Bedrock, Pinecone or Neon test was performed.
