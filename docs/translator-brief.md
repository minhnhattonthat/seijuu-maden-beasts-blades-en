# Translator brief - Seijuu Maden: Beasts & Blades (SNES, 1995)

You translate part of the Japanese script of Seijuu Maden: Beasts & Blades into English for a fan patch. A fantasy
war/strategy RPG: the player is one of 11 Holy Beast Kings of the Light, fighting the Dark's Demon Beast Kings with
an army and tamed beasts in a war the gods started. Earnest hero, lots of comic townsfolk, a darker turn at the end.
Work only on the batches named in your dispatch, one at a time in the order given, each to a passing check before
the next. Do all translation yourself; do not dispatch subagents.

## Read first
1. `docs/style-reference.md` - layout rules, character voices and approved example pairs. Match this voice.
2. `build/terms_<batch>.txt` - binding glossary rows for this batch (full table in `glossary.md` if you need more:
   read its Rulings and Style rules once). Item, weapon, beast, enemy and skill names in dialogue use the game's
   own English from its "Data names" section: hiragana-only names aren't in the terms file, so grep `glossary.md`
   for any item-like word (`grep -n "| きのや |" glossary.md`).
3. `docs/synopsis.md` - plot, who is who and the late reveals. Don't give a reveal away early.

## Input: `work/tl/<batch>.tsv`
`id<TAB>speaker<TAB>form<TAB>limit<TAB>Japanese` - speaker is empty (the name is the first line of the JP text).
form: dlg (dialogue box, 35 cells per line, wrapped for you) | narration (one scroll line, 40 max) | name | menu.
` / ` shows where the JP breaks lines. limit is the hard cap per line in characters for narration/name/menu.
Lines are in ROM order, which is mostly story order within a scenario: use neighbours for context. `{...}` are
control codes (`{var:02}` = hero's name, `{icall:..}`/`{num:..}` = a name/number drawn there, `{delay:N}` pause,
`{c0C}` new page, `{choice:0201}` a choice list follows, `{sfx:N}` sound).

## Output: `work/tl/<batch>.out.tsv`, written with your file-write tool (not a shell heredoc)
`id<TAB>English`, every input id exactly once, same order. Plain ASCII: straight quotes, `...`, `--`; no tabs inside
the English, no Japanese or fullwidth characters, no `\uXXXX`.
- dlg: don't copy the JP line breaks. Write `Speaker / "the whole page as one run"`; ` / ` only after the speaker
  name, before a choice list and between choice options (`Go in? / {choice:0201} Yes /  No`), or where a break is
  meaningful (a poem, a list). The tool word-wraps the rest. Keep every `{c0C}` (pages) at the matching point.
- narration/name/menu: ` / ` = a line break wherever the JP has one; each line within the limit.
- Copy every control code except `{nl}`/`{c0C}` exactly as often as the JP has it, in the matching place.
- Entries that are names (form name): the glossary spelling if listed; else a natural English rendering
  (European names as the European name, monsters by their usual English name: スライム Slime, ケルベロス Cerberus).

## Validate
`python -X utf8 tools/batches.py check <batch>` from the repo root; fix every reported id until it prints OK.
`python -X utf8 tools/batches.py fit "text" --file event_E4` shows how a dialogue page wraps.

## Style
- Faithful: keep the information and order of ideas; adapt idiom, not meaning. Don't add details the Japanese
  doesn't state; don't summarise or skip. Adapt wordplay so the joke still lands (no translator notes).
- Names and terms exactly as in the glossary. Never abbreviate or squeeze to fit (no "Brz.Dagger", no CamelCase
  "FireDagger", no dropped words): write the full, natural English name ("Bronze Dagger"). The check reports
  over-limit names/menus as `LONG` warnings, not errors; those screens get widened by engine work (D4).
  Dialogue lines are word-wrapped, so they never need squeezing.
- Honorifics on a variable are fine ("{var:00}-san"); the no-suffix rule is about ordinals.
- Honorifics kept, hyphenated (Lang-sama, Elma-san, Zona-dono); 王よ -> "my king"; 姫 -> Princess.
- Placeholders: no suffix glued to a variable ("Holy Beast King No. {num:..}", never "{num}th"); no a/an right
  before a name variable; sentences must read whatever name the player typed.
- Voices: see style-reference and the glossary's Style rules (foreign merchant's broken English, monsters' broken
  katakana speech, Kansai -> folksy).
- The same JP line often appears several times (shops, repeated NPC lines): translate it the same way each time.

## Consistency
Never edit `glossary.md`. For a recurring name or term not in it, pick a form, use it consistently, and report it.

## Report (reply with only this)
Files written and entry count; then any lines: `NEW TERM: jp -> en`, `UNSURE: id - note`, `LONG: id - note`.
