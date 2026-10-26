# Event scripts (dialogue pointers)

- **Interpreter** `C03BE6` (verified: watch probe on `E771BC-E771C2` while the opening cutscene runs). Script pointer 24-bit at DP `$69-$6B`. Opcode byte read at `C03C39`; `FF` ends, `FE` special; else `TAX` + `JSR ($3B31,x)`: **opcodes are even bytes**, handler table `C03B31` (word per even opcode, 64 entries seen).
- **Message opcodes `0A` and `0C`** (both -> handler `C03E60`): `0A ff lo hi`. `ff` = flags (bit 1 -> `$4B94` wait mode, bit 0 -> `$4984`, bits 3-7 kept), then `lo hi` = string address **in the script's bank** (`$6B`), copied to the text pointer `$32`. Verified on `E771BE: 0A 03 D3 78` -> `E778D3`.
- Scripts and their text share a bank (E7: scripts around `E77160`, text from `E778D3`). `E77160` starts a 16-bit table of script entry points in that bank (guess).
- Not yet done (phase 4): the length of every opcode, so the extractor can walk scripts and find every `0A`/`0C` exactly instead of pattern-matching `0A xx lo hi`.

## Text relocation options (for phase 5)

1. Keep the 16-bit pointers and move strings within their bank: only works while English fits the bank's free space (it won't: English runs ~2x the bytes of kana/kanji).
2. Replace each original string in place by `{call:XXXXXX}{end}` (6 bytes) pointing into expanded banks E8-FF; strings shorter than 6 bytes stay in place or share a neighbour's slot. No interpreter change.
3. Hook handler `C03E60` to read a 24-bit pointer from a side table indexed by script address.
Option 2 is the default plan (docs/re/text.md §Control codes).
