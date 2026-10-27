# Glossary - Seijuu Maden: Beasts & Blades

Binding for every translator and reviewer. Agents propose additions in reports; only the controller edits this file.

## Rulings (asked of the user once; options and reasons in docs/decisions.md)
- Honorifics: kept, hyphenated (Johannes-san). Name order: Western (D1).
- Romanisation source: the game's own English (title, intro crawl, credits), else an earlier fan patch (none found), else Hepburn without macrons (D2).
- Credits: English (D3; the staff names are already English in the ROM).
- Register / flavour: <e.g. keep light JP flavour>. Sound effects: <*Slam!*>.
- Abbreviations: <default: full names and terms everywhere, prefer engine changes over shortening>.

## Style rules
- Punctuation map: 「」 -> "...", 『』 -> '...', ・・・ -> ..., ！？ -> !?, <more>.
- <voice notes per character, or point to docs/style-reference.md>

## Characters
| JP | EN | max | notes | Avoid |
|---|---|---|---|---|

## Places
| JP | EN | max | notes | Avoid |
|---|---|---|---|---|

## Items / skills / terms
| JP | EN | max | notes | Avoid |
|---|---|---|---|---|
| ちから | Strength | 8 | status stat (labels in tools/build.py `STATS`) | Str |
| たいりょく | Stamina | 8 | | |
| すばやさ | Agility | 8 | | Speed |
| ちせい | Wisdom | 8 | | Int |
| やせい | Instinct | 8 | beasts' stat in place of Wisdom | |
| じゅうりょう | Weight | 7 | | |
| こうげき | Attack | 7 | | |
| ぼうぎょ | Defense | 7 | | |
| きどうりょく | Move | 7 | movement range on the battle grid | Mobility (too long) |
| ぶき / ぼうぐ | Weapon / Armor | 7 | equip rows "Armor 1".."Armor 3" | |
| ぶきレベル | LV | 2 | weapon level, "LV:" | |
| りんせつ / かいふく / えんぽう / とくべつ | Melee / Heal / Ranged / Special | 7 | beast skill ranges | |
| どく | Poison | 7 | | |

## Decisions from earlier batches
- <batch> <JP> -> <EN> (reason)
