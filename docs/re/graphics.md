# Graphics text survey

Static sweep: every LZ block `tools/lzblocks.py --render work/gfx` finds (docs/re/compression.md), rendered 2bpp and 4bpp and read by eye. Tour: boot, title, name entry, opening cutscenes, hero's house, field command menu (states in `work/states/orig_*.mss`, regenerate from the routes in docs/status.md).

## Japanese drawn as tiles

| # | Screen | Source | Format | State | Plan |
|---|---|---|---|---|---|
| G1 | Title logo: small 聖獣魔伝 and ビースト&ブレイド over the English "Beasts & Blades" | LZ `C75BE9` (with the logo), loaded `C1011D`/`C15F00` | 4bpp BG | seen on title + in block | D5: the logo already has its English name; replace the katakana reading, keep or romanise 聖獣魔伝 (decide at the graphics phase, note in decisions.md) |
| G2 | Title: ©BPS/ORG/メディアワークス | LZ `C7C10D` (also holds PUSH START and the English intro crawl) | 2bpp | seen | redraw as ©BPS/ORG/MediaWorks |
| G3 | Intro crawl: Japanese subtitle lines under the English verses | LZ `C7AF0D` (16 px glyphs, 2 tile rows) | 2bpp | seen in block and on boot | redraw in English or drop (the English verse above already says it; decide with the intro) |
| G4 | Opening cutscene: poem 十と一つの聖獣を... over the room | LZ `CCA415` chr (2560 B -> `$7F0000` -> VRAM `$8000`, BG3) + `CCAB70` (2 KB, map) loaded at `C05438`/`C0544E` | 2bpp BG3 | seen (`orig_poem.mss`, ~f300) | redraw |
| G5 | was "title/file menu labels": these are the G10 world-map menu words | LZ `CBCEE0`, `CBD21F`, `CBD44D` (`CBD6C7` is art) | 2bpp | done (G10) | - |
| G6 | Field command menu: 話す 調べる 仲間 フィールド ステータス (outlined 16 px, opened with A) | LZ `CC0000` (BG3 tiles $100+), records `C03529`/`C0358B` | 2bpp | **done** (`tools/gfxtext.py`): Talk Search Party Field Status, `work/qa/gfxtxt/z_both.png` | - |
| G7 | Party/battle UI labels: フォーメーション アイテム パーティ 第N聖獣王 引ける 捨てる 使う 貴重品 陣形 前... | LZ `CD3838`, `CD4381` (`C25828`/`C25839`) | 2bpp, 16 px in 2 tile rows | in block only | redraw |
| G8 | `D2A94E` = G9's words + the HP gauge art; `D2AD77` (loaded `C52B95`) holds 6x2-tile strips, partly loaded at BG3 tile $157 (part of 集中's old cells): not identified | LZ `D2AD77` | 2bpp | in block only | identify on the tour |
| G9 | Battle command menu: 移動 攻撃 アイテム ビースト 集中 退却 防御 アクション 待機 | LZ `D2A94E`, records `C533F6`..`C53898` (11) | 2bpp | **done**: Move Attack Item Beast Focus Retreat Defend Action Wait (seen: first 4) | - |
| G10 | World-map party commands 移動/行動 キャンプ ステータス ランデブー; 移動 sub-menu 移動/入る; X menu マップ/セーブ; 確認 再設定 待機 中止 再開; 都市 旗オフ/旗オン | LZ `CBCEE0` (records `C0B887`, `C0B949`), `CBD21F` (`C0B97F`, `C0B9E1`), `CBD44D` (`C0BA43`, `C0BA79`, `C0BAAB`) | 2bpp | **done**: Move/Action Camp Status Meet, Move/Enter, Map/Save seen; Confirm.. and Cities/Flags not seen (block assignment of those records inferred from tile use) | find their screens |

Menu records (`tools/gfxmaps.py` lists them): entries of 2 rows x 6 BG3 map words, `$20F7` = window blank, `$21nn`
= tile n of the block loaded at BG3 tile $100. `C30F90` copies a record (long pointer `$4C`) to VRAM; some menus are
first copied to WRAM (`$7E498C`). The JP shares tiles between words (移動/行動 share 動, 再設定/再開 share 再), so
`gfxtext.menus` re-lays every entry out (English centred in 48 px, identical tiles shared) and rewrites the records.
Font `fonts/menu16.txt` (1 px skeletons, fill 1 + outline 3 on the window's 0/2 checker, like the kanji).
Probes: `tools/lua/winsrc.lua`, `vramval.lua` (who writes a tile number to VRAM). "Meet" for ランデブー: "Rendezvous"
is 52 px, the row 48; dialogue still says "rendezvous".
| G11 | Location title box on entering a map (山賊砦, どうぐや) | text engine or tiles: check in the marker build | ? | seen (warp `battle_fort`) | marker build decides |
| G12 | Status/equip screen labels as 8x8-font tilemaps (tile = code - $10): ちから じゅうりょう たいりょく こうげき すばやさ ぼうぎょ ちせい きどうりょく ぶきレベル ぼうぐ, アイテム rows | LZ `CD51CD` (hi byte 00), `CD5812` (hi 20, long forms そうびじゅうりょう こうげきりょく ぼうぎょりょく) | tilemap over the 8x8 font | seen garbled in the marker build (`status_menu` + `down down a a`): the font's kana tiles 40-6A are lowercase now | rewrite the maps like `build.name_grid`; lay out with the equip names (7 chars now, `windows.md`) |

Not Japanese (no work): town menu "OK?" bubble and EXIT sign, save screen NO DATA, battle REMAIN/MAXIMUM/HP gauges,
world-map POINT/FOOD/USE box, staff credits (English names in the text engine, C17C03).
Not Japanese (no work, earlier list): PUSH START, the English intro verses, PAUSE sprite, battle UI `CD51CD` (STATUS ACTION HEART; its kana labels are G12), status UI `CD498F` (NAME LV EXP HP MALE FEMALE STATUS EQUIP ITEM NEXT SEX).

### G12 details (status/equip tilemaps)

- Loader `C25914`: `$7EE0FB` = 0 -> `CD51CD`, else `CD5812`; both decompress to `$7F:A000`, 32 x 128 cells,
  cell (row, col) = `$7FA000 + (row*32 + col)*2`. `CD51CD` = own status/equip screen (warp `status_menu`, logged).
  `CD5812` = `E0FB` 1 (set at `C29B30`) or 3 (`C5DE2D`..): long labels, right values at col 28 (code
  `C2A4xx-C2B0xx`). **Not** the formation screen's ステータス -> member view: that one (warp `status_beast`, then
  `a`, pick a member) reuses `CD51CD` already in RAM (the formation screen loads it, no LZ on the way).
  `CD5812` is the **army-exchange screen** (two armies meet on the world map: A on another army, `C0A0CB` ->
  `C0A19D`; 交換/仲間/アイテム) and its equip page. Reach it with `tools/lua/exchange_equip.lua` (header has the
  route). Checked on screen: same look as the own view. The loader's branch test is `C2590E` (`C25914` is the
  `E0FB`=0 branch only).
- C2 dispatcher `JSL C28000` (A = index, `JSR ($8018,x)`): 1 `C293C5` exchange screen (E0FB=1), 3 `C2B209`,
  4 `C2A302` "whose equipment?", 8 `C2A361` equip page, 9 `C2A5B0`, C/D/E = `C9BA`/`CA56`/`D114` (exchange
  commands, `E13B`+$0C), F `C28040`. Equip-row highlight: `C2A459` -> `C25485` (palette over Y cells from X;
  row starts in `C2A47A`), count at `C2A471`, now 18 (`build.STATUS_CODE`). Item-list highlight (11 cells)
  at `C2AC2F`, not checked.
- Party RAM: units of `$301` bytes from `$601A` (unit 0 = the hero's), member records `$2F` bytes from unit+`$33`
  (record +0 kind, +1 unit, +5 name). Op `38 id 06` builds unit `id` and increments `$6010` (unit count).
  `status_beast` puts unit 1's beast record (JP-coded name) into the hero's second slot `$607C`.
- BEAST/MASTER row of that screen: template `C29F7C` (8x8 printer, called from `C29F6E`; name, LV and the じゅうぞく
  bar drawn over it), missed by the coverage check (code bank C2), now a `party_menu` string.
- `CD51CD` cells: stats rows 36/38/40/42: left label ends col 12, `:` col 13, value cols 14-15; right label ends col
  22, `:` 23, value 24-26. Equip rows 46/48/50/52: label cols 8-11, `:` 12, icon col 13 (tile $1xx), name from col 14
  (7 placeholder cells `1234567`), row 46 ぶきレベル: cols 24-29, value col 30. Rows 56-121: item list placeholders.
- Value/name positions are immediates (`LDA #$cell`, then `STA $4BA4`) in C2 (found by scanning C2 for
  `A9/A0/A2 lo hi` of every cell; a hit can be a false match, check the disassembly): left values `C26C4F` A91C, `C26C5A`, `C26C65`, `C26C70`; right values
  `C26B58` A930 (weight), `C26C7D` A9B0, `C26C88`, `C26C93`; icons `C268AA`/`C26962` AB9A, `C269FD` AC1A, `C26A70`
  AC9A, `C26AE3` AD1A; names `C26995` AB9C, `C26A32` AC1C, `C26AA5` AC9C, `C26B18` AD1C; weapon level `C269DF` ABBC;
  blank 7 cells (`LDA #7; JSR C26CE0`) at `C268E3`, `C26912` (row 46 col 24 = ABB0, also `C269F1`, `C26B95`).
  Writers: values `C32B82` (number printer), icons `C263F0`, names `C329C3` (8x8 printer), `C26D31` (code->tile
  string printer).
- Beast overrides drawn over the labels by `C26D31` (already text units): `C26940` `---` over the weight value
  (`C26903`, A930), `C26944` やせい over ちせい (`C26922`, r42 c10), `C26948` りんせつ/かいふく/えんぽう/とくべつ over the
  equip labels (`C26935`/`C26B7E`/`C2A488`, r46 c8, one line per 2 rows). An override shorter than the label it covers
  leaves the label's tail: English overrides must be padded to the label width.
- **Done for `CD51CD`** (2026-10-27): `build.status_map` rewrites rows 36-52 (English labels, values/icons moved)
  and `build.STATUS_CODE` moves the C2 operands to match (each checked against the original word). Missed
  text found on the way: `C26BA0`-`C26BC9` (human labels drawn back after a beast: ちせい, ぶきレベル:, the equip
  labels; どく at `A7A6`; `-----`), now a `party_menu` run; their `LDA #lo` operands are in `build.RUN_PTRS`.
  Measured on the English build: `work/qa/g12/en_final3.png`.
- `CD5812` value cells (party view): `C2AC37`.. clear 3 cells at col 27 (A936, A9B6, AA36, AAB6; also `C2AE4F`..),
  values at col 28 (`C2AD45` A938, `C2AD94` A9B8, `C2ADD1` AA38, `C2AE0E` AAB8); equip labels at col 8 from `C2AF5A`
  AC10, `C2AFCF` AC90, `C2B04E` AD10. Not traced at run time.

## Fonts (text work, not graphics text)

- 12 px dialogue font `CA027C` and 6 px half-width font `CA0000`: raw 1bpp in ROM (docs/re/text.md).
- **8x8 menu font** in LZ `CBC255` (2bpp, loaded from 7 sites): 0-9 A-Z ! ? … 、 。 ・ : + - × / = ( ) LV kcal, hiragana and katakana in the 12 px font's code order, window frame tiles. Uppercase only: English menus need lowercase cells (phase 5).
- Name entry grid: kana drawn as text (assumed; confirm in the marker build).

## Not covered yet (tour with the debug tool, phases 2 and 5)

Seen through warps in phase 2 (`tools/debug/scenes.lua`): battles, shops/inn, save screen, world map, town menu,
endings and credits (ending text is the 12 px text engine over a picture). Still to check in the marker build:
beast/monster name plates, the 第N聖獣王 banner on the world map (C60xxx list is text: likely the text engine),
grid field battles (world-map encounters; no warp yet). LZ loaders that take bank/address from registers (`C5037D`, `C50C3B`, `C54094`, `C2405A`, `C2C609`) are not swept statically; raw (uncompressed) graphics banks are not swept either (only the sprite bank `DB` was seen).
