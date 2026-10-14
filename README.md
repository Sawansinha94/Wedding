# Sawan & Pratibha — Wedding website with AI

## Run on MacBook

```bash
cd sawan-pratibha-wedding-ai
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add your own NEW OpenRouter key (optional)
uvicorn server:app --reload
```
Open http://127.0.0.1:8000

## What works without an API key?
The concierge uses built-in verified wedding facts in English, Hindi and Odia; the wishes generator uses built-in multilingual templates. With a valid OpenRouter API key in `.env`, both use a real AI model. No secrets are exposed to browser JavaScript.

## Deploy
Deploy this Python/FastAPI project on a hosting service that supports Python processes. Set `OPENROUTER_API_KEY` as a server-side environment variable. Static-only hosting will use the offline fallback, not live AI.

## Notes
- Phone call buttons use `tel:` and work on supported devices.
- RSVP currently opens an email draft; edit `RSVP_EMAIL` in `index.html` before publishing. No RSVP database storage is implemented.
- This site includes 3 photos bundled from your uploaded files. Replace images/photo1.jpg etc if desired.
- Avoid pasting any token into HTML, screenshots, or public repositories. Revoke previously exposed WhatsApp tokens and App Secret.
- Do not use an unrestricted AI endpoint without rate limits for public production hosting.


## Screenshot-inspired additions
Ceremony cards, two embedded venue maps, journey route link, arranged-marriage timeline, interactive petal shower, and original synthesized wedding-style melody are included. The story panels use decorative graphics, not the screenshot's stock photographs; replace with your own licensed photos if desired. Embedded Google maps require internet access. The music is an original generated tune, not a recorded wedding song. RSVP remains email-based.


Family Tree update: The Photo Gallery has been replaced by Our Families with relationship-only cards for both families. Portrait placeholders are intentional. Family contact Call buttons remain intact.


## New homepage artwork
The homepage uses `images/wedding-homepage-theme.png` as a responsive full-width invitation image. The image already contains the couple’s names and wedding dates, so the former hero heading is removed to avoid duplication. Buttons below the image link to Events and RSVP.


## Editable homepage
The homepage is native HTML/CSS with individual groom and bride photos in `images/groom-portrait.webp` and `images/bride-portrait.webp`. The soft mandap illustration is `images/mandap-decoration.svg` and is decorative only. Wedding copy and dates can be edited directly in `index.html`. All paths are relative and work under FastAPI static serving.

## Wedding logo
The supplied S&P logo is added to the navigation header, footer and browser favicon. Its optimized files are in images/wedding-monogram.webp and images/wedding-favicon.png.

Watermark: The SP logo is applied with a low-opacity CSS pseudo-element to all sections except the first homepage hero. Adjust opacity in the final CSS style block in index.html.

## Couple story photograph
The seated couple portrait is shown as a featured image in the Arranged Marriage Story section (`images/couple-sitting.webp`).

## Engagement photo update
The standing couple photo is placed next to the June 21 engagement story, replacing the decorative heart. The seated couple photo remains above the timeline.

## Scroll animations
Sections, ceremony cards, family tree panels, story elements and contact cards reveal gently on scroll. Implemented using IntersectionObserver with one-time animation, staggered timing and reduced-motion accessibility support. No additional dependencies.


## Background wedding audio
The supplied MP3 loops in the background without a visible music control. Browsers that block audible autoplay will begin playback on the first visitor interaction.


## Wedding wishes wall

A new public wishes wall shows the latest 40 messages and refreshes every 12 seconds. Visitors can create/edit wishes and publish them. The concierge is the final page section. Public-facing AI wording has been removed.

For local development, wishes persist in `wedding_wishes.sqlite3`. For deployment across instances, set `DATABASE_URL` to your Neon PostgreSQL connection string; the `public_wedding_wishes` table is created automatically. Do not expose the database URL or OpenRouter API key to the browser.

Before sharing publicly, add rate limiting, spam filtering/moderation, and a way to remove inappropriate comments. Guest submissions are public.

## New background
Golden mandala and rose-petal artwork is applied exclusively to the Wedding Wishes & Blessings section; homepage remains unchanged. Image: images/golden-petals-background.webp.


## Mobile responsive update
Responsive grids, fluid images, compact typography, mobile collapsible navigation, touch-friendly forms, tablet layout, and small-phone overflow fixes. No backend routes changed.
# Wedding
