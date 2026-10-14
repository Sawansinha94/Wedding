# Wedding website fixes

- Full JSON for a personalized guest is sent to the LLM on every request if the owner sets `approved_for_guests=true` and `visibility_policy.share_with_subject_after_verified_login=true`. There is no field allowlist for those approved records.
- Name confirmation or a familiarity question is **not secure authentication**; approval flags remain necessary to protect other guests.
- No runtime LLM translation calls: all available UI translations are bundled in `assets/js/29-static-catalog.js` and `assets/js/28-multilingual.js`.
- **Not yet 100% translated**: run `python build_static_translations.py` and review `TRANSLATION-AUDIT.json`. Dynamic text is generated in the selected language.
- Do not put live credentials in the website ZIP or commit a `.env`.
