# Proactive Wedding Concierge — background welcome

On first page load, `assets/js/09-proactive-concierge.js` reads the browser's **previously saved preferred name** from `wedding-visitor-preferred-name-v1` and calls `POST /api/concierge/welcome` in the background. It does not delay the page, and aborts after 4.5 seconds. The notification is displayed only for a single plausible family-name match; tapping it scrolls to the existing concierge chat. Visitors can dismiss it.

The same check is repeated when the visitor saves a name through the existing RSVP or Wish frontend flows. It does not extract names from device information: standard browsers do not reveal the device owner's name. There is no fingerprinting, device-identity inference, or guest-profile search.

## Matching

1. Validate name format locally; reject placeholders, device names, and usernames.
2. Match first/full names and approved aliases against `data/family/family_profiles.json` immediately.
3. If there is no direct match, optionally search the approved family Pinecone index. Compare the returned *family member name* with the visitor's supplied name, requiring a strong token similarity before showing a notification.
4. If no unique match exists, show nothing. This is a **potential** match, not verified identity. The notification asks whether the relationship applies.
5. The normal Concierge remains conditional-RAG; a background welcome lookup is a separate, name-triggered family matching operation.

## Configuration

No new environment variables are required. Pinecone is optional for the initial name-match check; the local family directory works without it. `PINECONE_API_KEY`, `PINECONE_INDEX_HOST`, and `PINECONE_NAMESPACE` enable the vector fallback.

## Privacy and limitations

Do not treat matching or a guest's verbal confirmation as authentication. Never grant private access based on the match. A shared device may have a previous visitor's preferred name; users should be offered a way to change or clear that name. Only public, approved family records belong in Pinecone. An empty browser name yields no personalized notification.

## Compact floating prompt
The family-match prompt appears as a compact floating bubble at the **bottom-right** of the visible screen, including on mobile. It disappears automatically after **20 seconds**. Clicking the bubble before it disappears scrolls to the Concierge and focuses its input. Visitors can dismiss it earlier with ×. No notification appears when no reliable saved name or family match exists.
