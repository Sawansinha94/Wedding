# Neon table mapping — supplied Tables.rtf

The supplied nine tables are **not dropped or renamed**. Existing RSVP/Wish routes still write to their legacy tables for backward compatibility. The application also logs normalized records where appropriate.

| Existing table | Website usage |
| --- | --- |
| `public_wedding_wishes` | Primary public wish feed and submission |
| `wedding_wish_replies` | Public comments linked to wishes |
| `wedding_rsvps` | Existing RSVP form storage |
| `rsvp_responses` | Additional event-linked RSVP rows (two for Both events) |
| `wedding_events` | Four published ceremony records, synchronized on startup |
| `wedding_wishes` | Additional wish record; `is_approved=false` for the existing moderation workflow |
| `ai_chat_history` | Successful Concierge LLM question and response, grouped by page-session UUID |
| `website_visits` | Page opens (anonymous UUID, device category, referrer and path) |
| `guests` | Not populated: the current form does not collect the phone, email or invitation code required by `guests_contact_check`. We intentionally do not fabricate identifiers or change your forms. Existing guest records remain untouched. |
| **NEW** `wedding_site_activity` | Calendar clicks, optional music/voice actions, family prompt actions, AI wish generation/rephrasing, and contact clicks; never typed text. |

**Important:** The website already maintains chat history only until refresh for conversation context. With this logging requirement, successful chat exchanges are also retained in Neon `ai_chat_history` for administrative records. A refresh resets the active conversation, not those database records. Consider adding a privacy notice, access controls, retention/deletion policy, and rate limiting before launch.

**No live Neon connection was attempted**. Run `NEON-LOGGING-MIGRATION.sql` on your database (or let startup create the new activity table) and ensure the nine original tables exist. `DATABASE_URL` must point to the exact database/branch that holds your existing tables.

To verify:
```sql
SELECT event_key,event_name,starts_at AT TIME ZONE 'Asia/Kolkata' AS local_start
FROM wedding_events ORDER BY starts_at;
SELECT count(*) FROM website_visits;
SELECT count(*) FROM wedding_site_activity;
SELECT count(*) FROM ai_chat_history;
SELECT count(*) FROM rsvp_responses;
SELECT count(*) FROM wedding_wishes;
```
