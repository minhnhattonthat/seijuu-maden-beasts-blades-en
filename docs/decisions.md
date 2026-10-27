# Decisions

The user's rulings on scope, style and trade-offs, newest last. Read before asking the user anything; if a later
decision replaces one, mark the old one "replaced by D<n>" instead of deleting it. Binding term spellings live in
`glossary.md`; this file holds the why.

| # | Date | Question | Options offered | Decision and reason |
|---|---|---|---|---|
| D1 | 2026-10-27 | Honorifics and name order | keep (-san), drop; JP or Western order | Keep honorifics; Western order (given name first). Owner's standing answer for one-shot runs. |
| D2 | 2026-10-27 | Romanization source for names | official art, earlier patch, Hepburn | Official English names where they exist (the game's own English: title "Beasts & Blades", intro crawl), else an earlier fan patch, else Hepburn without macrons. |
| D3 | 2026-10-27 | Credits | stay Japanese, translate | English. |
| D4 | 2026-10-27 | Abbreviations | engine work first (default), abbreviate | Default: full names and terms, engine work before abbreviation; abbreviate only as a flagged last resort. |
| D5 | 2026-10-27 | Graphics text left in Japanese | none (default), list | Translate all of it (titles, menus, banners, cards); keep the original Japanese logo only if it has no official English version. The title logo already reads "Beasts & Blades" with small 聖獣魔伝 kanji. |
| D6 | 2026-10-27 | Specs and plans | need approval, pre-approved | Pre-approved: keep going through checkpoints; report at the end. Never `gh release create`, never change repo visibility. |
| D7 | 2026-10-27 | Existing saves / states | provided, none | None provided; build the debug tool. |
| D8 | 2026-10-27 | Member names copied raw into RAM (soldiers 6, others 8 chars) | engine work: member-name printers follow `{call}` stubs; fit the fields | Engine work: hook the member-name drawers to follow stubs (`hooks.md` `mname`/`bbox`). |
