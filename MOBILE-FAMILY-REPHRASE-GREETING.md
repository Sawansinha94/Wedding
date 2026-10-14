# Latest improvements

- Family tree photos are 95px (25% larger than the original 76px), with centered equal-width responsive rows. At very narrow widths photos scale to fit.
- `With Love & Blessings` panels now fill their backgrounds with `cover`. The supplied groom photo is installed at `images/groom-portrait-new.webp`.
- RSVP and Wedding Wishes have **Rephrase with Wedding Assistant** actions. The backend `/api/wish/rephrase` requires an OpenRouter API key. It only rephrases existing text, and never submits automatically.
- After a visitor confirms a proposed family relationship in the Concierge, `/api/concierge/family-special` retrieves the `special_message` for that record from Pinecone. A negative reply clears the pending match. A self-reported relationship is not identity verification; do not store confidential messages.
- To update special greetings, edit `data/family/family_profiles.json` and run `python ingest_family.py` with Pinecone configured.
- Verify on iPhone and Android after deployment.
