# Four-language offline catalog review

The existing bundled catalog contains 346 entries, each with Hindi, Odia and Telugu values. This revision normalizes all localized numerals to ASCII digits and adds explicit place/family/name mappings.

All translations are local files; the visitor greeting currently retains the visitor-entered name unchanged, rather than transliterating it. Runtime transliteration is **not implemented**.

Important: the source excludes live chat and visitor-generated wishes from static localization, and its static audit does not verify all dynamically inserted text. Manual browser QA remains required.
