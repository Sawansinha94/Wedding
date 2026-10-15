# Conditional RAG routing

`backend/concierge.py` uses an LLM planner to determine whether a guest's question requires family-profile retrieval.

- **No Pinecone lookup** for greetings, thanks, wedding dates, venue information, contact details, generic questions, or questions about guests/callers.
- **Pinecone lookup** for approved bride/groom family profiles, personal traits, biographies, and family relationship follow-ups, when the planner explicitly returns `{"search": true, "query": "..."}`.
- The planner receives recent conversation turns to resolve references such as "his" and "her".
- Invalid JSON, unavailable/empty search query, or any value other than boolean `true` **does not trigger retrieval**.
- The reply model always receives verified wedding facts, and only receives retrieved family profiles if retrieval was authorized.
- Response field `searched_family` shows whether retrieval was attempted; `profiles_found` shows how many records passed the family-side filter.

Note: the LLM planner itself is called on each chat turn, even when Pinecone is skipped. Live testing requires configured OpenRouter and Pinecone credentials.
