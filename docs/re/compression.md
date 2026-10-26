# Compression (graphics)

**LZSS, decompressor `C3035D`** (verified: `tools/lz.py` decompresses `CCAB70` and `C75BE9` to the tiles seen in VRAM; compress -> decompress roundtrip is exact, `tests/test_text.py::test_lz_roundtrip`).

- Call: `A` = source bank, `Y` = source address, `$7E4BB5` mode (0 = VRAM via `$2118/9`, word address `$7E4BB7`; 1 = CGRAM; 2 = WRAM, 24-bit dest `$7E4BB7-B9`).
- Block: u16 output size, then tokens. Flag byte read MSB-first, 1 = literal, 0 = match. A match is one byte = absolute ring position (256-byte ring at `$1E00`, zero-filled, write position starts at `$EF`) plus a 4-bit length (n+2 = 2-17 bytes); lengths are packed two per byte (first match of a pair reads a new byte after its position byte and uses the high nibble, the next uses the low nibble).
- Text is **not** compressed (dialogue, items, prologue are raw in the ROM).
- `tools/lzblocks.py` lists the blocks the code loads with immediate addresses (54) plus three 16-bit block tables (`C0041E` bank E1, `C25E3F`/`CD0380` bank CD) and walks on through blocks packed back to back (150 found; the chain walk also yields false blocks of non-graphics data). Loaders that take bank and address from registers (`C5037D`, `C50C3B`, `C54094`, `C2405A`, `C2C609`; monster/portrait graphics, guess) are not followed statically.
- Other graphics are raw: e.g. character sprites DMAed from `DBC660`-`DBC8A0` (`C026E0`).
