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
| `C557A3` | battle weapon/item list: `LDA [$C2],y; BEQ $57B1` (name bytes -> tiles, code - $10) | `JSL bname` (`E8`) | follows a `0F FF lo hi bank` stub (C6 names relocated), keeps X (tilemap index), sets C for the caller's `SBC #$10`; space (10) -> tile E7 (tile 0 is a dark block there) |
| `C52F60` `C52F9D` `C52F8A` `C52FD2` `C5300F` `C5305A` `C52E88` `C52EAF` | battle list window (frame col `$264D`, BG frame+text `$AF`, BG save/restore, text origin, shared menu cursor C52E6A) | `bwin` `bwinc` `bframe` `bsave` `btext` `bcur` `bcur2` | window 11 -> 23 cells (2026-10-29; widths `C52F73` `C52FB0` `C53051`, text rows `$2E` apart: `C5574F`.., count col 20 `C5307D`); moved 12 cells left (`boff`) when `$12B2` is in the right half (frame cols 6-30; left side cols 1-25). Cursor shift only while flag 7F:66FE = `$4C57` (set at open, cleared at close). BG save (25 x 5 cells, `$FA` bytes) moved 7F:6442 -> 7F:6600-66F9 (C53D68 uses 64C4-6505). Empty list `C5597F` = "No items" (raw tiles) |
| `C254AA` | member name cells (`C254A9`, status/formation/exchange NAME:, `[$BF]` -> RAM member name, X cells): `REP #$30; LDY #0` | `JSL mname; NOP` (`E8`) | a name copied from a stubbed C6 field is `0F FF lo hi bank` in RAM: `bf_follow` points `$BF-$C1` at the called string, keeps X |
| `C5329A` | dungeon-battle name box: `LDY #0; LDA [$BF],y` (bytes -> tiles until 00) | `JSL bbox; NOP` (`E8`) | same, M8 X16, returns the first byte for the caller's `SEC; SBC #$10`. Box widened 14 -> 23 cells (2026-10-29): template `bbox_t` (`E8`, was `C5336F`, loop `C53291`), HP digits col 10 -> 19 (`C532D6`), right box (`$12AE` set) 9 more cells left (`C53256`, col 17 -> 8), its clears (`C50280` width at `C52CCA`, `C55B1D`) 23. The HP gauge on the top edge still spans its original cells |
| `C31B69`, `C31D1E` | auto-wrap after a cell (`C31B58` full-width / `C31D13`: column `$4770` past `$4768` and `LDA [$32]; AND #$FF; BEQ` -> `JSR $1E2B` new line) | `JSL wrapchk; BEQ; NOP` (`E8`) | no auto-wrap when the next code (past `{delay}`/`{sfx}`) is `00`, `{c0B}`, `{c0C}` or `{nl}`: a line that fills the row exactly (35 or 36 English chars = 18 cells) plus its `{nl}` left a blank line (2026-10-28; asar 1.91 encoded `beq $C31D28` wrong, so the targets are labels) |
| `C0FAE9`, `C0FB29` | shop buy list, weapon / armor handler of the menu-script VM (table `C0FAC9`): `JSL $C32912` on the C6 name | `JSL wrapname` (`E8`) | a name over 10 chars breaks at its last space within 10; the rest goes one tile row down, indented 1, 9 cells (entries are 16 px apart, that row is blank). A line over its cells starts that much further left (`Demon Blade`, `Breastplate`: 11). Both lines blank-padded. Keeps `$4F-$51` (the shop sets the bank once per list: a changed `$51` broke the next name) |
| `C0E88E`, `C0E892`, `C0E8B3` | beast buy list (event op `6C`, drawer `C0E845`: entries id/LV at `$A164`, two 14-cell columns in a 28-cell buffer `$4BA1`, highlight table `C0C243` offset/width pairs): name `JSL $C32912`, then `LV:` at X+9, next column X+5 | `JSL beastname` (`wrapname` with W=13), `JSL beastlv` (X+9, one row down), `JSL beastnx` (row back up, X+5) | names up to 13 on the entry row, longer break at the last space onto the blank lower row; `LV:` always on the lower row at X+9 (over the padding). Stride and highlight unchanged. Shop beasts reach 15 (Platinum Dragon). Shot `work/qa/beast13/crop.png` |
| `C26C9F` | `C26C9E` (blank, then print a name via a RAM `0F FF` call): `LDA #9; JSR $6CE0; SEP #$20` | `JSL eqcount; JSR $6CE0; NOP` | blank by place: weapon row 46 from col 9 = 18 cells (LV from col 27), other rows to col 30 (armor 22 cells, beast skills cols 16-30), item list buffer (`$4BA4` >= `$AE00`) 10 as before. With `build.STATUS_CODE`: icons col 8, names col 9, empty-slot blanks, the 1-cell blank after a name `JSR $6CE0` -> `BIT $6CE0`. Labels `C26BAB` (ぶき/ぼうぐ1-3) are `{end}`: drawn after the names, they would wipe them; the beast labels `C26948` are 8 wide to cover col 15. The status rows are HDMA-squeezed (9 px), so no second line there |

| `C26140` (bag list entry), `C2B3F9..B57E` / `C2A654..A7A4` (cursor, use/discard/valuables and equip-page bag), `C2B76B` / `C2ABD8` (row highlight) | two columns of 12 cells: entry `$4BA4` = base + (slot odd ? $18) + slot/2 * $80; cursor ±2 rows, ±1 columns | one column: row = slot, count/LV col 28 (`C2620C`/`C262AB`/`C26457`), highlight 24 cells, down/up ±1, left/right off, ▽ bound `B990`; `JSR $B798` at `C26167` blanks the row and zeroes its lower half (`text.asm`) | item names up to 19 chars (D4). Buffer 7F:AE10, $80 per entry: 2 tile rows, HDMA squeezes each to 12 px but the lower row's top shows, so stale tiles there must go. 32 rows reach 7F:BE10: the exchange screen's second list moved 7F:B6D0 -> BED0 (`C2612D`, `C2D150`, `C2D7C3/C8`, `C2D5EB`) |

Bag-list layout (`C26140`, `C260BB` list 1 = unit `E12B`, `C2610F` list 2 = unit `E12D`, exchange screen only):
cursor `E11F` index, `E121` row, `E123` row in the 5-row window, `E125` (list 2 `E127`) scroll = buffer address
of the top row; `C2B7C6` DMAs 10 tile rows from it to VRAM `5888`. Exchange-screen item trade (`C2D114`, list in
`E11E`, X = list) has its own twin cursor (`C2D217..D37E`) and highlight (`C2D593`): patched the same way (2026-10-28),
checked with `tools/lua/exchange_items.lua` (`work/qa/exitems*/`). Equip-page bag (`C2A5B0`) checked from the
exchange equip page (`exchange_equip.lua` + a poked bag, `work/qa/equipbag*/`). Discard leaves an empty row in
place; the original does the same.

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
