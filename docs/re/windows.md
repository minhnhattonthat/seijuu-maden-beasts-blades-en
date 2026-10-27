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
| Battle messages (`battle` C57CD8 table, printer C57C00) and battle results (`battle_result` C34B9D..) | **35 chars per line, 3 lines** (same box as dialogue: wraps after char 36, 4th line scrolls) | `--qa C34BD0=` / `C57D3C=` ruler, `battle_t10` state + `tools/lua/battle_end.lua` (BATTLE_END=1 victory, 2 defeat) | measured (`work/qa/bruler`, `blose`) |
| Battle weapon/item list (C6 names via C557A3, hooked to follow stubs) | **8 chars** (the `×--` count is drawn over col 9+; longer names wrap into the next row) | `--qa C6253D=1234567890ABCDEF`, `battle_t10` state, `down a` | measured (`work/qa/batk_r`) |
| Equip screen names (status menu → 装備) | **10 chars** (cols 16-25 after the English re-layout, `build.STATUS_CODE`; same as the shop budget). Beast skill names on the same rows: 10 too. The selected row's highlight still ends at col 20 (cosmetic, not traced) | `--qa C611B0=1234567890{end} --qa C61D3F=ABCDEFGHIJ{end}`, `status_menu` state, `down down a a` | measured (`work/qa/g12/qa_equip3.png`) |
| Status screen labels (`status_map` in build.py; overrides `C26940`-`C26BC4` in `party_menu.json`) | fixed: stat labels 8 left / 7 right, equip labels 7; an override must be padded to the label it covers (`C26BA0` "  Wisdom", `C26948` 7 per line); `C26BC0` (poison) 7, drawn over the HP value from col 15 | `status_menu` state, `down down a a` | measured (`work/qa/g12/en_final3.png`); beast overrides not seen yet (no beast in the warp party) |
| Item screen list (status screen → アイテム → 使う; weapons/armor/food/items/items2 names, two columns) | **7 chars** (the `×N` count, or `LV:n` for a weapon, is drawn from col 8 of the column over the name's tail). Tightest of all C6 name budgets (shop/equip 10, battle 8): engine work (one column, or count moved) before abbreviating, per D4 | `--qa C60FFB=1234567890ABCDEF` (same for C6247D C61CE5 C6253D C62BFD), warp `status_items` (poked inventory) | measured (`work/qa/item/mk_qa.png`) |
| Item screen prompt (`C25342` and the other 17-byte `party_menu` prompts, top line from col 8) | **16 chars** (the FRONT/REAR legend sprites start at col 24) | `--qa C25342=1234...`, warp `status_items` | measured (`work/qa/item/prompt.png`) |
| Item type label over the list (`item_types` C6301E..) | **14 chars** (cols 17-30) | `--qa C6301E=1234...`, warp `status_items` | measured (`work/qa/item/mk_qa.png`) |
| Formation name (`C2C8EB`.. in `party_menu`, `name{nl}{nl}フォーメーション`, right-aligned by leading spaces) | **8 chars per line**, 2 lines (cols 23-30; a 9th char lands on col 31, the screen edge: "Formation" doesn't fit, the screen title already says it) | `--qa "C2C8EB=1234567890ABCDEF{nl}{nl}abcdefghijklmnop"`, warp `status_formation` | measured (`work/qa/item/form_qa.png`) |
| Shouts (C57DCB..), battle idle lines | not reached yet | | guess |

Glyph torture: `--qa 'E7792E=abcdefghijklmnopqrstuvwxyz  ABCDEFGHIJ{nl}KLMNOPQRSTUVWXYZ 0123456789 !?.,;:...'`:
every printable glyph renders; 「 and 」 are drawn at the cell edges (Japanese style), so `「」` shows a gap.
