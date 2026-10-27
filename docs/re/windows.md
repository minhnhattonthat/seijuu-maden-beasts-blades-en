# Window budgets (width gate)

English text: 6 px per character (fonts/en6.txt, two per 12 px cell) in the 12 px engine; 8 px per character in
8x8 menus. Measured on `build.py --marker --qa ID=text` builds, shots in `work/qa/` (regenerate with the commands).

| Variant | Budget | How measured | State |
|---|---|---|---|
| Dialogue box (event messages, shops, inn) | **35 chars per line, 3 lines per page** (a speaker name line counts as one) | `--qa 'E7792E=1234...'`, warp `opening`: the engine wraps by itself after char 36; a 36-char line followed by `{nl}` leaves a blank line, so 35. A 4th line waits for a button (scroll). Torture line: all glyphs drawn, descenders ok | measured (`work/qa/ruler1.png`, `torture1.png`, `lines1.png`) |
| Centred scroll lines (prologue, intro, endings, credits) | **40 chars** | `--qa C16304=` 40 digits fit with margin, 42 fill the screen edge to edge, 44 are not drawn at all | measured (`work/qa/scroll1.png`) |
| Menu records (shop/inn command windows, `script/menus.json`) | row length sets the window width; keep <= 8 chars (window sits at the left edge, nothing to its right) | marker build: `[C14C63]` (8 cells) draws fine | measured (`work/qa/menus1.png`) |
| Weapon names in the shop buy list (C6 fields via the 8x8 printer `C32912`) | **10 chars** (an 11th wraps to the next row) | marker `[C60FFB] T` + wrap, warp `shop_buy` | measured (`work/qa/fields1.png`) |
| Choice lists (`{choice}` in a dialogue message, options as ` text{nl}` lines) | **34 chars per option** (after the leading space; the cursor takes the first cell), 3 lines per box | `--qa 'E7792E={choice:0201} 1234...{nl} No{end}'`, warp `opening`: 34 drawn, the 35th wraps and is lost | measured (`work/qa/choice1.png`) |
| Yes/no record `C0C30D` (`script/menus.json`) | **4 chars per row** (box grows rightwards from x~184; at 5 the right border is off screen) | `--qa 'C0C30D=1234{nl}No'`, warp `shop_6e` | measured (`work/qa/yn1.png`) |
| Town building name box (`town_lists` strings, e.g. `CE3419` さかば) | **8 chars** (fixed box, the rest is cut) | `--qa CE3419=1234567890123456`, warp `town_enter` | measured (`work/qa/townname1.png`) |
| World-map info box `C0BAF7` | its 114-byte slot (no free space in bank C0 to grow) | build error when larger | known limit |
| Battle messages, names in status/equip/battle/item screens | not yet: no warp reaches a battle message or an item screen | | guess |

Glyph torture: `--qa 'E7792E=abcdefghijklmnopqrstuvwxyz  ABCDEFGHIJ{nl}KLMNOPQRSTUVWXYZ 0123456789 !?.,;:...'`:
every printable glyph renders; 「 and 」 are drawn at the cell edges (Japanese style), so `「」` shows a gap.
