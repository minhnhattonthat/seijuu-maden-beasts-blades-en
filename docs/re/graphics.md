# Graphics text survey

Static sweep: every LZ block `tools/lzblocks.py --render work/gfx` finds (docs/re/compression.md), rendered 2bpp and 4bpp and read by eye. Tour: boot, title, name entry, opening cutscenes, hero's house, field command menu (states in `work/states/orig_*.mss`, regenerate from the routes in docs/status.md).

## Japanese drawn as tiles

| # | Screen | Source | Format | State | Plan |
|---|---|---|---|---|---|
| G1 | Title logo: small 聖獣魔伝 and ビースト&ブレイド over the English "Beasts & Blades" | LZ `C75BE9` (with the logo), loaded `C1011D`/`C15F00` | 4bpp BG | seen on title + in block | D5: the logo already has its English name; replace the katakana reading, keep or romanise 聖獣魔伝 (decide at the graphics phase, note in decisions.md) |
| G2 | Title: ©BPS/ORG/メディアワークス | LZ `C7C10D` (also holds PUSH START and the English intro crawl) | 2bpp | seen | redraw as ©BPS/ORG/MediaWorks |
| G3 | Intro crawl: Japanese subtitle lines under the English verses | LZ `C7AF0D` (16 px glyphs, 2 tile rows) | 2bpp | seen in block and on boot | redraw in English or drop (the English verse above already says it; decide with the intro) |
| G4 | Opening cutscene: poem 十と一つの聖獣を... over the room | LZ `CCA415` chr (2560 B -> `$7F0000` -> VRAM `$8000`, BG3) + `CCAB70` (2 KB, map) loaded at `C05438`/`C0544E` | 2bpp BG3 | seen (`orig_poem.mss`, ~f300) | redraw |
| G5 | Title/file menu labels (16 px) | LZ `CBCEE0`, `CBD21F`, `CBD44D`, `CBD6C7` (loaded `C06139`-`C06165`, title code) | 4bpp | in block only | confirm on the title menu (needs a save), redraw |
| G6 | Field command menu: 話す 調べる 仲間 ... (outlined 16 px, opened with A) | not yet matched (vramfind); candidates `CD3838`/`CD4381` style | 2bpp? | seen (`orig_home_free.mss` + A) | find source, redraw |
| G7 | Party/battle UI labels: フォーメーション アイテム パーティ 第N聖獣王 引ける 捨てる 使う 貴重品 陣形 前... | LZ `CD3838`, `CD4381` (`C25828`/`C25839`) | 2bpp, 16 px in 2 tile rows | in block only | redraw |
| G8 | Unknown text-like strips | LZ `D2A94E`, `D2AD77` (`C52B83`/`C52B95`) | 4bpp | in block only | identify on the tour |

Not Japanese (no work): PUSH START, the English intro verses, PAUSE sprite, battle UI `CD51CD` (STATUS ACTION HEART), status UI `CD498F` (NAME LV EXP HP MALE FEMALE STATUS EQUIP ITEM NEXT SEX).

## Fonts (text work, not graphics text)

- 12 px dialogue font `CA027C` and 6 px half-width font `CA0000`: raw 1bpp in ROM (docs/re/text.md).
- **8x8 menu font** in LZ `CBC255` (2bpp, loaded from 7 sites): 0-9 A-Z ! ? … 、 。 ・ : + - × / = ( ) LV kcal, hiragana and katakana in the 12 px font's code order, window frame tiles. Uppercase only: English menus need lowercase cells (phase 5).
- Name entry grid: kana drawn as text (assumed; confirm in the marker build).

## Not covered yet (tour with the debug tool, phases 2 and 5)

Battle screens, monster/beast names, shop/inn/church, save/load screen, world map and place names, chapter or "第N聖獣王" cards, game over, ending, credits. LZ loaders that take bank/address from registers (`C5037D`, `C50C3B`, `C54094`, `C2405A`, `C2C609`) are not swept statically; raw (uncompressed) graphics banks are not swept either (only the sprite bank `DB` was seen).
