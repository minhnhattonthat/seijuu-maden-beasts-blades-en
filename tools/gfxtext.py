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


def draw(s, g):
    """16 x 48 colour indices: s centred, fill 1, outline 3, the window's 0/2 checker behind."""
    ink, x = set(), 0
    for ch in s:
        top, rows = g[ch]
        for r, row in enumerate(rows):
            ink |= {(x + c, top + DY + r) for c, p in enumerate(row) if p == "#"}
        x += len(rows[0]) + 1
    x0 = (W - (x - 1)) // 2
    assert x0 >= 1, f"{s!r}: {x - 1} px, wider than {W - 2}"
    ink = {(px + x0, py) for px, py in ink}
    edge = {(px + dx, py + dy) for px, py in ink for dx in (-1, 0, 1) for dy in (-1, 0, 1)} - ink
    return [[1 if (x, y) in ink else 3 if (x, y) in edge else 2 if (x + y) % 2 else 0 for x in range(W)]
            for y in range(H)]


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
