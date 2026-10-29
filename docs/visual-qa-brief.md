# Visual-QA reviewer brief - Seijuu Maden: Beasts & Blades

You review contact sheets from a translated build's QA tour and give each one a verdict. Read-only on everything
except your one verdict file: no edits to the repo, no git, no subagents.

## Inputs (in your dispatch)
- A chunk file: one `id<TAB>path` line per sheet. Read every sheet in it; none may be skipped.
- Your verdict file: `work/qa/verdicts/<chunk>.tsv`.
- Optional: the original ROM's sheets (`work/qa/tour_jp/`, same ids) and `glossary.md`.

## How to look
- Read each sheet whole first. Where text is small, zoom into it with
  `python -X utf8 $SKILL/scripts/sheet.py SHEET.png --crop x,y,w,h --zoom 3 --out <scratch>.png` and read that.
- When something looks wrong, open the same id from `tour_jp/` (`sheet.py EN.png --compare JP.png`). If the
  original shows the same thing, it is the game's own behaviour: `ok`, with a note.

## Judge
An `issue` is any of:
- Japanese still visible;
- text overflowing a box, clipped by a frame, or running off screen;
- garbage tiles, wrong or missing glyphs, a strike or stray pixels across letters;
- broken line breaks: a word split mid-line, a page ending mid-sentence, a one-word last line;
- an empty box where text belongs;
- a name that differs from `glossary.md`.

Standing non-bugs, `ok` (the controller adds the game's own below):
- text still typing out, a box mid-fade or mid-scroll, a cursor caught mid-blink;
- a map or scene still loading after a warp;
- anything identical in the original's sheet.
- English is a 6 px fixed font, two letters per 12 px cell; menus use an 8x8 font. Tight letter pairs are by design.

Known open work: still an `issue`, but start the note with the tag so the controller can sort it from new finds:
- `known-gfx:` Japanese drawn as graphics, not text: title logo, the poem screen, outlined 16 px command menus
  (world map, camp, battle) and the status-screen command list with its 第1聖獣王 header.
- Shop buy lists wrap a long name onto the entry's blank lower row ("Bronze / Dagger"): by design, `ok`.
- `shop_6c_pack`: its beasts show ペガサス, poked test data with Japanese name bytes: `ok`.
- `known-width:` only the 4 beast names of 14-15 letters (Thunder Dragon, Platinum Dragon..) and 3 enemy names
  cut at 13 on status/formation screens. Every other list was widened (2026-10-29): any other cut or overlap
  (`LV:`, `×N`, a frame) is a new issue.
- Each scene also has `final` (its last frame at full size): read menu spelling there, the sheets are half size.

## Verdicts
Write your verdict file once you have read every sheet, one line per id in the chunk:
`id<TAB>ok|issue<TAB>what and where` (for an issue: which tile, which text, what is wrong).
Then return a short summary: counts, and the issues one per line.
