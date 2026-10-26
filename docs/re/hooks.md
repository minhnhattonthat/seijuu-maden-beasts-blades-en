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

Font: `fonts/en6.txt` -> `build/en6.bin` (`tools/font.py`), 16 bytes per code 10-7F, 5 px glyphs + the game's 1 px
shadow. A lone English glyph before a control code or kanji gets a blank right half (6 px gap).

## Text relocation (tools/build.py, no asm)

- A line longer than its slot becomes `0F FF lo hi bank 00` (`{call}{end}`, 6 bytes) to the expansion. Allocated
  addresses never contain a `00` byte (code that skips strings by scanning for `00` must not stop in a stub).
- Slots under 6 bytes: the stub goes into a freed tail (old bytes after an in-place stub) in the same bank, and
  every 16-bit pointer to the line moves there: event `0A`/`0C` ops (`extract.event_sites`), `PTRS` tables,
  `RUN_TABLES` / `RUN_PTRS` in build.py.
- SEQ runs (prologue, intro, endings, credits; `extract.SEQ`) are read line after line (`C160DE`: measure, draw,
  `INC $32`): the whole run is rewritten in place as one stub per line, and the ending table `C17044` is moved.
