# ROM map, header, free space

- Dump in `rom.sha1`: 2,621,440 bytes (2.5 MB), no copier header. Header at `$FFC0`: title `ﾋﾞｰｽﾄ ｱﾝﾄﾞﾌﾞﾚｲﾄﾞ`, map mode `$31` (HiROM, FastROM), cart type `$02` (ROM+RAM+battery), ROM size byte `$0C` (declares 4 MB), SRAM `$03` (8 KB), region `$00` (Japan), checksum `$1C37` / complement `$C8E3` (verified: mirrored sum, first 2 MB + 4 x the last 0.5 MB; `tools/bps.py snes_checksum`).
- Banks `$C0-$E7` hold the file (offset = addr & 0x3FFFFF). Code lives in C0-C5 (event VM C0, text engine C3); fonts CA; LZ graphics C4/C7/CB/CC/CD/D2/E1; dialogue + event scripts CE, CF, E3-E7 (docs/re/text.md).

## Free space (verified only where noted)

- **Expansion (planned home of the English text, VWF code and fonts):** grow the file to 4 MB; banks `$E8-$FF` (1.5 MB) are new, 0xFF-filled, reachable in HiROM without a mapper change, and the header already declares 4 MB. Verify in the engine spike: a string placed at `$E80000` and reached through `{call}` prints.
- **Inside the original 2.5 MB:** only small 0xFF/0x00 runs (largest ~3 KB of zeros at `E01EF5`-`E02B00`, many 0x200-0x570-byte 0xFF runs at bank ends: `C2F061`, `D3F292`, `DFF243`...). Candidates only: none has been trap-tested. Hook stubs that must sit in a given bank should use them after a trap test (fill 0xFF -> tour).
- **Freed by relocation:** every dialogue string moved out leaves its old bytes (minus the 6-byte `{call}` stub) free in its own bank; that space is where per-bank code or tables can go.
