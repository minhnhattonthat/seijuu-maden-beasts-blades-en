"""gfxtext.py: English for the outlined 16 px command-menu words (G6 field, G9 battle, G10 world map;
docs/re/graphics.md).

Each menu is a ROM tilemap record (found with tools/gfxmaps.py): entries of 2 rows x 6 cells, a cell the window
blank $20F7 or a word tile $21xx (VRAM tile $100 + n = tile n of the menu's LZ block, loaded at BG3 tile $100).
menus() draws every entry's English (fonts/menu16.txt, centred in the 48 px row) into the block's word tiles,
reusing identical tiles, and rewrites the records to match. Only tiles that some record entry used, or that were
blank, are redrawn (the rest of a block, e.g. the battle HP gauge, stays).

    python -X utf8 tools/gfxtext.py OUT.png     preview every menu entry (3x zoom)
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FONT = ROOT / "fonts" / "menu16.txt"
BLANK, DY, W, H = 0x20F7, 1, 48, 16  # DY: the skeleton rows move down one, so the outline sits in rows 3-15

# LZ block -> (records {cpu address: entries}, {entry top row as gfxmaps prints it: English})
MENUS = {
    0x0C0000: ({0xC03529: 4, 0xC0358B: 4}, {  # field command menu (A)
        "-- 00 01 02 03 --": "Talk", "08 09 0A 0B 0C 0D": "Search", "-- 04 05 06 07 --": "Party",
        "0E 0F 20 21 22 23": "Status", "24 25 26 27 28 29": "Field"}),
    0x12A94E: ({0xC533F6: 7, 0xC5349F: 6, 0xC53530: 5, 0xC535A9: 4, 0xC5360A: 3, 0xC53653: 3, 0xC5369C: 4,
                0xC536FD: 6, 0xC5378E: 5, 0xC53807: 6, 0xC53898: 5}, {  # dungeon-battle commands
        "-- 00 01 02 03 --": "Move", "-- 20 21 22 23 --": "Attack", "04 05 06 07 08 09": "Item",
        "40 41 42 43 44 45": "Beast", "56 57 58 59 5A 5B": "Focus", "-- 2C 2D 2E 2F --": "Retreat",
        "-- 24 25 26 27 --": "Defend", "0A 0B 0C 0D 0E 0F": "Action", "-- 28 29 2A 2B --": "Wait"}),
    0x0BCEE0: ({0xC0B887: 8, 0xC0B949: 2}, {  # world-map party commands and the move sub-menu
        "-- 26 27 2A 2B --": "Move", "-- 28 29 2A 2B --": "Action", "00 01 02 03 04 05": "Camp",
        "06 07 08 09 0A 0B": "Status", "20 21 22 23 24 25": "Meet", "-- 2C 2D 2E 2F --": "Enter"}),
    0x0BD21F: ({0xC0B97F: 4, 0xC0B9E1: 4}, {
        "-- 00 01 02 03 --": "Confirm", "04 05 06 07 08 09": "Reset", "-- 20 21 22 23 --": "Wait",
        "-- 0A 0B 0C 0D --": "Cancel", "-- 04 05 0E 0F --": "Resume"}),
    0x0BD44D: ({0xC0BA43: 2, 0xC0BA79: 2, 0xC0BAAB: 2}, {  # world-map X menu and map view
        "-- 0A 0B 0C 0D --": "Map", "-- 06 07 08 09 --": "Save", "-- 2C 2D 2E 2F --": "Cities",
        "20 21 22 23 24 25": "Flags Off", "26 27 28 29 2A 2B": "Flags On"}),
}


# Plain words drawn in place (no records to rewrite): 4bpp LZ block -> [(top-left tile, width in tiles, English)];
# a word is tiles t..t+w-1 over t+16..t+16+w-1. Ink colour 1 on 0, no outline.
PLAIN = {
    0x0D3838: [  # status-screen tile set (BG1 at VRAM 0): command list, exchange and party words
        (0xA0, 6, "Dismiss"), (0xA6, 4, "Trade"), (0xAA, 4, "Party"), (0xC0, 6, "Formation"), (0xC6, 6, "Status"),
        (0xCC, 4, "Equip"), (0xE0, 6, "Items"), (0xE6, 4, "Party"), (0xEA, 4, "Assign"),
        # 第N聖獣王 header: 46, the digit pair, 47-49. shortcut: "Holy Beast King No. N" won't fit 48 px (D4 flag)
        (0x46, 1, "№"), (0x47, 3, "King")],
    0x0D4381: [(0x01, 4, "Drop"), (0x06, 4, "Use"), (0x20, 6, "Key Items")],  # item screen commands (VRAM $100+)
}
# Bottom halves drawn alone: the item screen's header puts CD3838 E0-E5 ("Items" top) over CD4381 0A-0F, whose
# row 7 is the header's rule line (kept where the ink isn't).
HALF = {0x0D4381: [(0x0A, 6, "Items")]}
# 第N聖獣王: each army-number pair (1-11) carries 第's tail at the left of its left tile and 聖's head in its right
# tile; beside the narrow "1" (tiles 20/21, bottoms 30/31) they stand alone. (ref tile, columns, tiles): those
# pixels are cleared from every pair, top and bottom.
DIGITS = {0x0D3838: [(0x21, 8, [0x21, 0x23, 0x25, 0x27, 0x29, 0x2B, 0x2D, 0x2F, 0x41, 0x43, 0x45]),
                     (0x20, 3, [0x20, 0x22, 0x24, 0x26, 0x28, 0x2A, 0x2C, 0x2E, 0x40, 0x42, 0x44])]}


# G4 opening poem (LZ CCA415 tiles, 2bpp BG3, DMA'd as 160 tiles: A0+ is the menu font, E4+ the window, 180+ the
# dialogue font, all live beside it; CCAB70 its 32x32 map). Line n sits in map rows 2+2n/3+2n (an HDMA on $212C
# reveals it by scanline); English is one 8 px row per line (the 8x8 menu font, ink 3 white, shadow 1 dark), in the lower row.
POEM_CHR, POEM_MAP, POEM_TILES = 0x0CA415, 0x0CAB70, 0xA0
POEM = ["When eleven holy beasts gather,", "the path of Light is shown;", "when eleven demon beasts gather,",
        "the path of Darkness is shown.", "That is the promised hour:", "the Holy King descends to earth.",
        "That is the hour of judgment.", "Beware the hour of great change."]


def glyph8(font8, table, ch):
    """8 rows of ch from the 8x8 menu font: columns of colour-3 ink, trimmed; a space is 2 blank columns."""
    t = (table.encode(ch)[0] - 0x10) * 16
    rows = [[(font8[t + y * 2] >> (7 - x) & 1) | (font8[t + y * 2 + 1] >> (7 - x) & 1) << 1 for x in range(8)]
            for y in range(8)]
    cols = [x for x in range(8) if any(r[x] == 3 for r in rows)]
    return [[3 if r[x] == 3 else 0 for x in range(cols[0], cols[-1] + 1)] for r in rows] if cols else [[0, 0]] * 8


# G2 title copyright (LZ C7C10D, 4bpp): one 8 px line in tiles 40-4F, ©BPS/ORG/ kept, メディアワークス from x 66 (the / ends at 63).
TITLE_CHR, TITLE_TILE, TITLE_X, TITLE_INK = 0x07C10D, 0x40, 66, 0xF


def title(gfx, font8, table):
    """Redraw メディアワークス as MediaWorks on the title screen (gfx edited in place)."""
    raw = bytearray(gfx[TITLE_CHR])
    px = [sum((untile4(raw, TITLE_TILE + cx)[y] for cx in range(16)), []) for y in range(8)]
    for row in px:
        row[TITLE_X - 1:] = [0] * (128 - TITLE_X + 1)
    x = TITLE_X
    for ch in "MediaWorks":
        g = glyph8(font8, table, ch)
        assert x + len(g[0]) <= 128, "title: MediaWorks too wide"
        for y in range(8):
            for c, v in enumerate(g[y]):
                if v:
                    px[y][x + c] = TITLE_INK
        x += len(g[0]) + 1
    for cx in range(16):
        raw[(TITLE_TILE + cx) * 32:(TITLE_TILE + cx + 1) * 32] = tile4(px, cx, 0)
    gfx[TITLE_CHR] = bytes(raw)


def poem(gfx, font8, table):
    """Draw POEM into the poem's tile block and map (gfx edited in place). font8: the built 8x8 menu font."""
    def glyph(ch):
        return glyph8(font8, table, ch)

    old = gfx[POEM_MAP]
    m = [old[i] | old[i + 1] << 8 for i in range(0, len(old), 2)]
    attr = next(x for x in m if x & 0x3FF) & 0xFC00
    tiles, chr_ = {bytes(16): 0}, bytearray(POEM_TILES * 16)
    for n, s in enumerate(POEM):
        line = [[] for _ in range(8)]
        for ch in s:
            g = glyph(ch)
            for y in range(8):
                line[y] += g[y] + [0]
        w = len(line[0]) - 1
        nt = (w + 8) // 8  # the shadow takes one column past the ink
        assert nt <= 32, f"poem line {n}: {w} px"
        px = [[0] * (nt * 8 + 1) for _ in range(9)]
        for y in range(7):  # the game's glyphs use rows 1-7: move up one, shadow right and below
            for x in range(w):
                if line[y + 1][x]:
                    px[y][x] = 3
        for y in range(8):
            for x in range(w):
                if px[y][x] == 3:
                    for dx, dy in ((1, 0), (0, 1), (1, 1)):
                        if px[y + dy][x + dx] == 0:
                            px[y + dy][x + dx] = 1
        c0 = (32 - nt) // 2
        for r in (2 + 2 * n, 3 + 2 * n):
            m[r * 32:r * 32 + 32] = [attr] * 32
        for cx in range(nt):
            t = tile(px, cx, 0)
            if t not in tiles:
                assert len(tiles) < POEM_TILES, "poem: more than 160 tiles"
                chr_[len(tiles) * 16:len(tiles) * 16 + 16] = t
                tiles[t] = len(tiles)
            m[(3 + 2 * n) * 32 + c0 + cx] = attr | tiles[t]
    gfx[POEM_CHR] = bytes(chr_)
    gfx[POEM_MAP] = b"".join(x.to_bytes(2, "little") for x in m)
    return len(tiles)


def glyphs():
    """{char: (top row, [row strings])}"""
    out = {}
    for n, line in enumerate(FONT.read_text(encoding="utf-8").splitlines(), 1):
        if not line or line.startswith("#"):
            continue
        ch, top, rows = line.split("\t")
        rows = rows.split()
        assert len({len(r) for r in rows}) == 1 and all(set(r) <= {".", "#"} for r in rows), f"menu16.txt:{n}"
        out[" " if ch == "space" else ch] = (int(top), rows)
    return out


def draw(s, g, w=W, plain=False):
    """16 x w colour indices: s centred, fill 1, outline 3, the window's 0/2 checker behind (plain: ink 1 on 0)."""
    ink, x = set(), 0
    for ch in s:
        top, rows = g[ch]
        for r, row in enumerate(rows):
            ink |= {(x + c, top + DY + r) for c, p in enumerate(row) if p == "#"}
        x += len(rows[0]) + 1
    x0 = (w - (x - 1)) // 2
    assert x0 >= (0 if plain else 1), f"{s!r}: {x - 1} px, wider than {w - (0 if plain else 2)}"
    ink = {(px + x0, py - (DY if plain else 0)) for px, py in ink}
    if plain:
        return [[1 if (x, y) in ink else 0 for x in range(w)] for y in range(H)]
    edge = {(px + dx, py + dy) for px, py in ink for dx in (-1, 0, 1) for dy in (-1, 0, 1)} - ink
    return [[1 if (x, y) in ink else 3 if (x, y) in edge else 2 if (x + y) % 2 else 0 for x in range(w)]
            for y in range(H)]


def tile4(px, cx, cy):
    """The 4bpp SNES tile at cell (cx, cy) of a drawn row (planes 0/1 then 2/3)."""
    rows = [px[cy * 8 + y][cx * 8:cx * 8 + 8] for y in range(8)]
    pl = [[sum((v >> p & 1) << (7 - i) for i, v in enumerate(r)) for r in rows] for p in range(4)]
    return bytes(b for y in range(8) for b in (pl[0][y], pl[1][y])) + bytes(b for y in range(8) for b in (pl[2][y], pl[3][y]))


def untile4(raw, t):
    """8x8 colour indices of 4bpp tile t."""
    b = raw[t * 32:t * 32 + 32]
    return [[sum((b[y * 2 + p % 2 + p // 2 * 16] >> (7 - x) & 1) << p for p in range(4)) for x in range(8)]
            for y in range(8)]


def plain(gfx):
    """Draw the PLAIN words into their blocks (in place)."""
    g = glyphs()
    for off, words in PLAIN.items():
        raw = bytearray(gfx[off])
        for ref, cols, ts in DIGITS.get(off, []):
            for dy in (0, 16):
                piece = [r[:cols] + [0] * (8 - cols) for r in untile4(raw, ref + dy)]
                for t in ts:
                    px = untile4(raw, t + dy)
                    px = [[0 if p and p == q else q for p, q in zip(pr, qr)] for pr, qr in zip(piece, px)]
                    raw[(t + dy) * 32:(t + dy) * 32 + 32] = tile4(px, 0, 0)
        for t, w, s in words:
            px = draw(s, g, w * 8, plain=True)
            for cy in (0, 1):
                for cx in range(w):
                    o = (t + cy * 16 + cx) * 32
                    raw[o:o + 32] = tile4(px, cx, cy)
        for t, w, s in HALF.get(off, []):
            px = draw(s, g, w * 8, plain=True)[8:]
            for cx in range(w):
                o = (t + cx) * 32
                rule = [(raw[o + 14 + p % 2 + p // 2 * 16] >> (7 - x) & 1) << p for x in range(8) for p in range(4)]
                rule = [sum(rule[x * 4:x * 4 + 4]) for x in range(8)]  # row 7 colour per pixel
                px[7][cx * 8:cx * 8 + 8] = [v or r for v, r in zip(px[7][cx * 8:cx * 8 + 8], rule)]
            for cx in range(w):
                raw[(t + cx) * 32:(t + cx) * 32 + 32] = tile4(px, cx, 0)
        gfx[off] = bytes(raw)


def tile(px, cx, cy):
    """The 2bpp tile at cell (cx, cy) of a drawn row."""
    b = bytearray()
    for y in range(8):
        row = px[cy * 8 + y][cx * 8:cx * 8 + 8]
        b += bytes([sum((v & 1) << (7 - i) for i, v in enumerate(row)), sum((v >> 1) << (7 - i) for i, v in enumerate(row))])
    return bytes(b)


def key(ws):
    return " ".join("--" if x == BLANK else f"{x & 0xFF:02X}" for x in ws[:6])


def menus(rom, gfx):
    """Redraw each menu block in gfx (decompressed, edited in place); returns the record writes [(offset, bytes)]."""
    g, writes = glyphs(), []
    blank = tile([[2 if (x + y) % 2 else 0 for x in range(8)] for y in range(8)], 0, 0)
    for off, (recs, words) in MENUS.items():
        raw = bytearray(gfx[off])
        n = len(raw) // 16
        ents = []
        for a, k in recs.items():
            o = a & 0x3FFFFF
            for e in range(k):
                ws = [rom[o + e * 24 + i * 2] | rom[o + e * 24 + i * 2 + 1] << 8 for i in range(12)]
                assert all(x == BLANK or x & 0xE300 == 0x2100 for x in ws), f"{a:06X} entry {e}: not a menu entry"
                if key(ws) not in words:
                    raise SystemExit(f"gfxtext: {a:06X} entry {e} ({key(ws)}) has no English")
                ents.append((o + e * 24, ws))
        used = sorted({x & 0xFF for _, ws in ents for x in ws if x != BLANK and x & 0xFF < n})
        spare = [i for i in range(n) if i not in used and raw[i * 16:i * 16 + 16] in (blank, bytes(16))]
        pool = used + spare  # the block's empty tiles only once the words' own tiles run out
        free, made = iter(pool), {}
        for o, ws in ents:
            px, hi = draw(words[key(ws)], g), next(x for x in ws if x != BLANK) & 0xFC00
            out = []
            for cy in (0, 1):
                for cx in range(6):
                    t = tile(px, cx, cy)
                    if t == blank:
                        out.append(BLANK)
                        continue
                    if t not in made:
                        made[t] = next(free, None)
                        if made[t] is None:
                            raise SystemExit(f"gfxtext: block {0xC00000 | off:06X} has {len(pool)} word tiles, "
                                             "not enough for the English")
                        raw[made[t] * 16:made[t] * 16 + 16] = t
                    out.append(hi | 0x100 | made[t])
            writes.append((o, b"".join(x.to_bytes(2, "little") for x in out)))
        for i in free:  # word tiles no entry uses any more
            if i in used:
                raw[i * 16:i * 16 + 16] = blank
        gfx[off] = bytes(raw)
    return writes


def main():
    from PIL import Image
    g = glyphs()
    rows = [w for _, ws in MENUS.values() for w in dict.fromkeys(ws.values())]
    img = Image.new("RGB", (W, H * len(rows)))
    col = [(24, 32, 64), (232, 240, 255), (56, 64, 104), (8, 8, 24)]
    for i, w in enumerate(rows):
        for y, r in enumerate(draw(w, g)):
            for x, v in enumerate(r):
                img.putpixel((x, i * H + y), col[v])
    img.resize((W * 3, H * len(rows) * 3), Image.NEAREST).save(sys.argv[1])


if __name__ == "__main__":
    main()
