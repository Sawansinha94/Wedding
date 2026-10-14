# Special family greetings — strict trigger rules

1. No name can be recovered from device model, IP address, or user agent. On initial page load, a notification is eligible **only** when this browser previously saved a name from a successful RSVP or published Wish. A new anonymous visitor sees nothing.
2. After a successful RSVP or published Wish, the saved name is validated and matched against approved family names, including first names. The notification is a small bottom-right floating prompt, shown at most 20 seconds.
3. Clicking scrolls to Your Wedding Concierge, asks the relationship confirmation, and waits for the visitor's Yes. Only then is `special_message` read from Pinecone and shown in chat. No special message is included in the notification.
4. Open `data/family/family_profiles.json` and fill in `special_message` for each approved family member. Keep messages public-safe; self-reported confirmation is NOT authentication. Run `python ingest_family.py --validate-only` then `python ingest_family.py` to upload new records to Pinecone. Blank messages are not displayed.
5. Pinecone is used for approved family matching when the local directory lacks a match, and for the special message only after confirmation. General wedding questions still use conditional RAG.
6. A browser cannot tell whether an RSVP name is actually the person holding the device. Shared devices may have a previous visitor's name; ask confirmation and never disclose private details.

The browser remembers name + source using localStorage. Conversation history resets on refresh. Only a successful server submission should set a name source; an offline Wish is not eligible.
