"""List ROM tilemap records of the outlined 16 px command menus (G6/G9/G10, docs/re/graphics.md): runs of map words
that are the window blank $20F7 or a word tile $21xx (VRAM tiles $100-$1FF, priority, any palette).

    python -X utf8 tools/gfxmaps.py [--min 12] [--only C53] [--render X.vram.bin OUT.png]
    -> one line per run: address, words (tile number low byte, pN = palette N)
"""
import argparse

from build import ROM

BLANK = 0x20F7


def runs(rom, least=12):
    """(cpu address, [word, ...]) for each run of at least `least` menu words, every word aligned on its own."""
    w = [rom[i] | rom[i + 1] << 8 for i in range(len(rom) - 1)]
    ok = [x == BLANK or x & 0xE300 == 0x2100 for x in w]  # any palette: greyed-out entries use another one
    out, i = [], 0
    while i < len(w):
        n = 0
        while i + 2 * n < len(w) and ok[i + 2 * n]:
            n += 1
        if n >= least and any(x != BLANK for x in w[i:i + 2 * n:2]):
            out.append((0xC00000 | i, w[i:i + 2 * n:2]))
            i += 2 * n
        else:
            i += 1
    return out


def render(recs, vram, out, chr_at=0x8000):
    """Each record as rows of 6 cells drawn from a VRAM dump (BG3 2bpp tiles at chr_at), stacked, 3x zoom, grey."""
    from PIL import Image
    h = sum((len(ws) + 5) // 6 for _, ws in recs) + len(recs)
    img = Image.new("L", (6 * 8, h * 8), 40)
    y = 0
    for _, ws in recs:
        for i, x in enumerate(ws):
            t = vram[chr_at + (x & 0x3FF) * 16:chr_at + (x & 0x3FF) * 16 + 16]
            for py in range(8):
                for px in range(8):
                    v = (t[py * 2] >> (7 - px) & 1) | (t[py * 2 + 1] >> (7 - px) & 1) << 1
                    img.putpixel((i % 6 * 8 + px, (y + i // 6) * 8 + py), (0, 120, 255, 180)[v])
        y += (len(ws) + 5) // 6 + 1
    img.resize((img.width * 3, img.height * 3), Image.NEAREST).save(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--min", type=int, default=12)
    ap.add_argument("--render", nargs=2, metavar=("VRAM", "OUT"), help="draw the records from a VRAM dump")
    ap.add_argument("--only", default="", help="address prefix of the records to keep (e.g. C53)")
    a = ap.parse_args()
    recs = [r for r in runs(ROM.read_bytes(), a.min) if f"{r[0]:06X}".startswith(a.only.upper())]
    if a.render:
        render(recs, open(a.render[0], "rb").read(), a.render[1])
    for addr, ws in recs:
        print(f"{addr:06X} {len(ws):3d} " + " ".join(
            "--" if x == BLANK else f"{x & 0xFF:02X}" + ("" if x >> 10 & 7 == 0 else f"p{x >> 10 & 7}") for x in ws))


if __name__ == "__main__":
    main()
