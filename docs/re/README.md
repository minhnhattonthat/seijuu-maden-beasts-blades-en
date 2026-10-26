# Reverse-engineering notes

One file per subsystem (text engine, pointers, compression, font, graphics). Mark every finding with how far it is
proven, so a later session doesn't build on a guess:

- **verified** - and how: a decoded known string, a corrupt-and-boot test, a breakpoint hit on the drawing path, a
  passing roundtrip test. Name the test or savestate.
- **guess** - and why it seems likely (byte pattern, another game, an earlier patch's notes). Promote it to verified
  before code depends on it.

Addresses are for the dump in `rom.sha1` unless a note says otherwise.

| File | Covers | State |
|---|---|---|
| [rom.md](rom.md) | header, bank map, free space, expansion plan | verified header; free space candidates only |
| [text.md](text.md) | encoding, fonts, text engines, control codes, pointer forms, text ranges | encoding verified; some control codes guessed |
| [events.md](events.md) | event-script VM, message opcode `0A/0C ff lo hi`, relocation plan | message opcode verified; opcode lengths not yet |
| [compression.md](compression.md) | LZSS format, decompressor `C3035D`, block list tool | verified (roundtrip test) |
| [graphics.md](graphics.md) | graphics-text survey (G1-G8), fonts, what is not covered yet | static sweep + early tour |

Prior work: no earlier fan translation or community docs found (web search 2026-10-27, "Seijuu Maden Beasts & Blades translation"). Tools: `tools/lua/textlog.lua` (every string the engines read, with pointer), `tools/lua/callers.lua` (callers of a routine), `tools/textscan.py`, `tools/fontmatch.py` + `tools/make_tbl.py` + `tools/fontreview.py` (table), `tools/lz.py`, `tools/lzblocks.py`.
