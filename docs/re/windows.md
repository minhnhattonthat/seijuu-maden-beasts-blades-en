# Window budgets (width gate)

English text: 6 px per character (fonts/en6.txt, two per 12 px cell) in the 12 px engine; 8 px per character in
8x8 menus. Measured on `build.py --marker --qa ID=text` builds, shots in `work/qa/` (regenerate with the commands).

| Variant | Budget | How measured | State |
|---|---|---|---|
| Dialogue box (event messages, shops, inn) | **35 chars per line, 3 lines per page** (a speaker name line counts as one) | `--qa 'E7792E=1234...'`, warp `opening`: the engine wraps by itself after char 36; a 36-char line followed by `{nl}` leaves a blank line, so 35. A 4th line waits for a button (scroll). Torture line: all glyphs drawn, descenders ok | measured (`work/qa/ruler1.png`, `torture1.png`, `lines1.png`) |
| Centred scroll lines (prologue, intro, endings, credits) | **40 chars** | `--qa C16304=` 40 digits fit with margin, 42 fill the screen edge to edge, 44 are not drawn at all | measured (`work/qa/scroll1.png`) |
| Menu records (shop/inn command windows, `script/menus.json`) | row length sets the window width; keep <= 8 chars (window sits at the left edge, nothing to its right) | marker build: `[C14C63]` (8 cells) draws fine | measured (`work/qa/menus1.png`) |
| Choice lists (`{choice}`), battle messages, name fields (C6, 8x8), location title box | not yet | | guess |

Glyph torture: `--qa 'E7792E=abcdefghijklmnopqrstuvwxyz  ABCDEFGHIJ{nl}KLMNOPQRSTUVWXYZ 0123456789 !?.,;:...'`:
every printable glyph renders; 「 and 」 are drawn at the cell edges (Japanese style), so `「」` shows a gap.
