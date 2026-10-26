# Event scripts, scenarios, story state

## Interpreter (verified)

- **VM** `C03BE6`, script pointer 24-bit at DP `$69-$6B`. Opcode byte read at `C03C37`; `FF` ends, `FE` yields;
  else `JSR ($3B31,x)`: opcodes are even bytes `00`-`A8` (85 handlers, table `C03B31`). The loop first honours
  wait bits in `$A10C` (bit 0 message, 1 `1C` wait, 2 `1E` delay, 5, 6); **`$A10C` bit 7 = a script is running**
  (set by every script start: `$69/$6B` = entry, `$A10C |= $80`). `$A0C5` >= `FE` leaves the VM: `14` sets
  `FFFF` (back to the town menu), `16` sets `FFFE` (to the world map).
- **Lengths of every opcode: `tools/evdis.py`** (`ARGS`; verified: walking every event of all 98 scenarios by
  control flow gives no bad opcode except the dummy scenario and one dead call in scenario 4 ev 0 into
  `CE757D`, a message followed by plain text). Conditionals: `02 a op lo hi type [arg]` (if not (value(type)
  `op` a) goto lo hi; type 00 = last result `$6D`, 02 = nibble var, 04 = flag, 06-10 = item/party checks
  `C33489`, 12 = leader, 14 = party member word, +1 byte), `04 lo hi type [arg]` (goto unless true).
  `00 lo hi` goto, `06 lo hi` call, `08` return (stack `$A0EA`, depth `$A10A`). All targets in the script's bank.
- **Message opcodes `0A` and `0C`** (handler `C03E60`): `0A ff lo hi`. `ff` = flags (bit 1 -> `$4B94` wait mode,
  bit 0 -> `$4984`), then `lo hi` = string address **in the script's bank** (`$6B`), copied to the text pointer
  `$32`. Verified on `E771BE: 0A 03 D3 78` -> `E778D3`. Scripts and their text share a bank.

## Opcodes the debug tool uses (verified by warps, `tools/debug/`)

| Op | Bytes | Meaning |
|---|---|---|
| `0E` | `map x y dir a b c` | change map in this scenario (x/y pixels, `a`*2 = transition, `c` != 0 plays sfx 0D) |
| `10` | `sub scn map x y dir a b c ev` | change scenario: writes the word `$5059` = sub, scn (so `$505A` = scn), reloads the scenario tables, `0E` body, then jumps to event `ev` of the new scenario (`FF` = none: the `FF` is then read as "end") |
| `14` / `16` | - | leave the VM to the town menu / the world map |
| `30` / `32` / `1A` | `var val` / `var` / `var` | set / increment / decrement nibble var |
| `34` / `36` | `flag` | set / clear scenario flag (`$505C` bits) |
| `5E` | `type b c d e` | battle; type 00 = fight on the current isometric map (dungeon battle); table `C0493C` by type |
| `60`-`76` | lists / price | building menus (shops `60`/`62`/`6A`/`6C` take item lists, `64` byte list, `66 lo hi` inn price); each runs a built-in script at `C04D96` and C1 menu code (`$72` = C1 routine) |
| `78` | - | rest (bed), heals |
| `80` | - | the poem screen (G4: LZ `CCA415` + `CCAB70`) |
| `A2` | `n` | ending sequence `n` (C169F1; text pointer table `C17044`) |
| `A6` | - | sky/scroll effect before the war (scenario 58 event 1) |

Other lengths are in `tools/evdis.py`; meanings beyond the table are unverified.

## Scenarios (verified by warps)

- `$505A` = scenario (0-97), `$505B` = map in it, `$5059` = sub byte. Table `CE0002` + 3*scenario -> header in
  the scenario's bank: `+0` entry list (`FFFF` = none; else `var map event` triples picked by nibble var, e.g.
  scenario 35 `FF 00 00` = var FF == 0 -> map 0, event 0, the opening), `+2` ?, `+4` event table (16-bit
  pointers), `+6..` map headers until `FF 00`. Scenario start `C00030` (clears the scenario flags `$505C-$509B`,
  sets `$505B = FF` until the first map loads). Unused entries point at the dummy `CE3467`.
- New game: `C08341` sets `$505A = 35` (opening, Gaias's castle) and calls `C00030` at `C08344`.
- Map header: room graphics id, then object records of 11 bytes (position, facing, event number); exits are
  objects whose event runs `14`/`16` or `0E`.
- Names: location name list at `C60C08` (`ダミー`, ルーナス城, 山賊砦, ダスカー城, ...; index = scenario for the first entries, e.g. 6 = メイシルヴァ城; not every scenario matches its name entry: the opening scenario 35 is the hero's hometown events, whose town menu shows ラヴィウス).
- Towns are a 3x3 building menu (town menu, `14`), not a walkable map; buildings are maps of the scenario.

## Story state (verified where the debug tool writes it)

- **Nibble vars** `$4F69-$4FE8` (256 x 4 bits; `C30139` read, `C3015D` write). **Var `FF` (high nibble of
  `$4FE8`) = main progress**: 0 new game, 1 after the opening (scenario 35), 2 after the sky event (scenario 58
  event 1, `A6`), 3-5 and 10 in Melshiva Castle (scenario 6 event 6), 6-8 (scenario 6 event 47), 9 (scenario 60
  event 7). The new-game code tests `$4FE8 < $10`.
- Scenario flags `$505C-$507B` (`C30185` test, `C301B0` set, `C301C8` clear), cleared at every scenario start.
- Party: records from `$601A` (`$2F` bytes each), hero first; gold 24-bit `$600C`; hero HP `$6065`, max `$6066`
  (cheat list, confirmed by GOD in warp.lua). Position `$94CE`/`$94D0` (pixels), facing `$94C4`.

## Text relocation options (for phase 5)

1. Keep the 16-bit pointers and move strings within their bank: only works while English fits the bank's free space (it won't: English runs ~2x the bytes of kana/kanji).
2. Replace each original string in place by `{call:XXXXXX}{end}` (6 bytes) pointing into expanded banks E8-FF; strings shorter than 6 bytes stay in place or share a neighbour's slot. No interpreter change.
3. Hook handler `C03E60` to read a 24-bit pointer from a side table indexed by script address.
Option 2 is the default plan (docs/re/text.md §Control codes). `tools/evdis.py` now walks every script exactly,
so the extractor can take each `0A`/`0C` string address from the walk instead of pattern matching.
Ending and credits text (`C1704E`-`C17Dxx`) is a separate list of `{end}`-terminated lines read by C1 code
(`C16C43` loads the credits at `C17C03`), not event scripts.
