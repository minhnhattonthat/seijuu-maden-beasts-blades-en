# Engine hooks (tools/asm/text.asm)

One row per patched site. Bank E8 `$0000-$3FFF` belongs to the asm (code at `E80000`, font at `E81000`); relocated
text starts at `E84000` (`build.py` `ASM_SPACE`). Disassemble every hook after a change (`dis65816.py --map hirom`).

| Site | Was | Now | Why |
|---|---|---|---|
| `C3193B`, `C325D6` | `CMP #$50` (typed / bulk dispatch) | `CMP #$80` | codes 10-7F take the half-width path: 6 px English glyphs |
| `C3194E` | half-width: `SBC #$10; JSR $1B74` | `JMP $1B74` -> `typed_half` | |
| `C325E9` | half-width: `SBC #$10; JSR $275D` | `JMP $275D` -> `bulk_half` | |
| `C31B74` (`typed_half`, was the half-width loader) | | `JSL compose; JSR $19BE; JSR ($133B,x); JMP $1933` | two English glyphs composed into one 12 px cell, then the game's full-width shift/shadow/draw |
| `C3275D` (`bulk_half`) | | same with `JSR ($1343,x); JMP $2587` | bulk engine (scrolls, choice lists) |
| `C32CA4` | line width for centred lines | `JML measure` (`E8`) | follows `{call}` stubs; an English pair counts as one full-width cell |
| `C557A3` | battle weapon/item list: `LDA [$C2],y; BEQ $57B1` (name bytes -> tiles, code - $10) | `JSL bname` (`E8`) | follows a `0F FF lo hi bank` stub (C6 names relocated), keeps X (tilemap index), sets C for the caller's `SBC #$10` |
| `C254AA` | member name cells (`C254A9`, status/formation/exchange NAME:, `[$BF]` -> RAM member name, X cells): `REP #$30; LDY #0` | `JSL mname; NOP` (`E8`) | a name copied from a stubbed C6 field is `0F FF lo hi bank` in RAM: `bf_follow` points `$BF-$C1` at the called string, keeps X |
| `C5329A` | dungeon-battle name box: `LDY #0; LDA [$BF],y` (bytes -> tiles until 00) | `JSL bbox; NOP` (`E8`) | same, M8 X16, returns the first byte for the caller's `SEC; SBC #$10` |
| `C31B69`, `C31D1E` | auto-wrap after a cell (`C31B58` full-width / `C31D13`: column `$4770` past `$4768` and `LDA [$32]; AND #$FF; BEQ` -> `JSR $1E2B` new line) | `JSL wrapchk; BEQ; NOP` (`E8`) | no auto-wrap when the next code (past `{delay}`/`{sfx}`) is `00`, `{c0B}`, `{c0C}` or `{nl}`: a line that fills the row exactly (35 or 36 English chars = 18 cells) plus its `{nl}` left a blank line (2026-10-28; asar 1.91 encoded `beq $C31D28` wrong, so the targets are labels) |

Member-name readers found by watching reads of the hero's RAM name (`$6052`) in `status_hero`, `status_formation`,
`world_status`, `status_items`, `status_beast`, the exchange screen, `battle_t10/_t13/_fort` (+ victory), `world_map`,
`world_cmd`, `field_menu`: only these two (`C32AEA` there is a 16-bit read of the level at `$6051`). Not watched: grid
field battles, army info outside these scenes. `[$BF]` is a general pointer (150+ readers), so a static sweep can't
tell name drawers apart: a new screen with a garbled member name is a third drawer to hook.

Font: `fonts/en6.txt` -> `build/en6.bin` (`tools/font.py`), 16 bytes per code 10-7F, 5 px glyphs + the game's 1 px
shadow. A lone English glyph before a control code or kanji gets a blank right half (6 px gap).

## Text relocation (tools/build.py, no asm)

- A line longer than its slot becomes `0F FF lo hi bank 00` (`{call}{end}`, 6 bytes) to the expansion. Allocated
  addresses never contain a `00` byte (code that skips strings by scanning for `00` must not stop in a stub).
- Slots under 6 bytes: the stub goes into a freed tail (old bytes after an in-place stub) in the same bank, and
  every 16-bit pointer to the line moves there: event `0A`/`0C` ops (`extract.event_sites`), `PTRS` tables,
  `RUN_TABLES` / `RUN_PTRS` in build.py.
- C6 name fields (8x8 menu printer `C32912`: `00`-terminated, codes < $10 via table `C328F2`; its code `0F FF lo hi
  bank` is a call, `C32A1D`): a long name becomes a stub too, the rest of the field zero-filled.
- Menu records (`extract.MENUS`) that grow move to a freed tail in bank C1; the menu-script op `10 lo hi` is moved.
- SEQ runs (prologue, intro, endings, credits; `extract.SEQ`) are read line after line (`C160DE`: measure, draw,
  `INC $32`): the whole run is rewritten in place as one stub per line, and the ending table `C17044` is moved.
