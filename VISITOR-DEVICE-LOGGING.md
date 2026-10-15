# Visitor device and approximate location logging

Run `NEON-VISITOR-DEVICE-MIGRATION.sql` once in the Neon SQL Editor, then deploy this package. The application also attempts to add missing columns on startup.

Each page load calls `POST /api/telemetry/visit` and inserts one row in `website_visits` with a fresh session UUID, timestamp, page/referrer, browser and OS (best effort), device type, screen/viewport dimensions, language and time zone. The user-agent is collected by the server from the request.

## Location
- Browsers do not disclose personal device names or GPS coordinates by default. The `device_model` field stays null rather than guessing.
- Location is **not guaranteed**. Time zone and language are not proof of location.
- To log approximate country via Cloudflare, set `TRUST_CLOUDFLARE_GEO=true` only when the site is actually behind trusted Cloudflare infrastructure and the header cannot be spoofed by clients.
- For approximate city/region/country, install `geoip2` and supply a **locally hosted** licensed GeoLite2 City `.mmdb` at `GEOLITE2_CITY_DB`. If you also enable `LOG_VISITOR_IP=true`, the server can use the connecting IP for the lookup. Configure a trusted proxy and verify `request.client` is the actual visitor address. Accuracy varies and VPNs affect results. No third-party location lookup is performed.
- IP logging is **disabled by default**. Set `LOG_VISITOR_IP=true` only after adding an appropriate privacy notice and retention policy. Avoid storing precise coordinates unless guests explicitly opt in.

## Inspect records
```sql
SELECT visit_id,visited_at,device_type,browser_name,operating_system,
       screen_width,screen_height,language,timezone,country_code,region_name,city_name
FROM website_visits ORDER BY visited_at DESC LIMIT 100;
```

## Privacy and operational notes
Disclose analytics collection, restrict database access, and set a retention/deletion schedule. The website does not collect passwords, personal device names, keystrokes, GPS, or a persistent cross-visit fingerprint. Session IDs are generated per page load. The server records only visits reaching the API; ad blockers, network failures, and JavaScript-disabled browsers can prevent a record.
