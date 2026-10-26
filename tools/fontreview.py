"""fontreview.py: sheets for confirming the font reading of every code the script uses that the matcher was
unsure of (flagged, small margin to the 2nd guess, or a duplicate reading).

    python -X utf8 tools/fontreview.py [--margin 0.15] [--per 60] [--out work/fontreview]

Writes chunkNN.png (each cell: code, zoomed glyph, MS Gothic rendering of the guess and the 2nd guess) and
chunkNN.tsv (code, guess, 2nd guess, three script lines using the code). Reviewers answer per code; the
answers go to tbl/font_fixes.tsv.
"""
import argparse
import csv
import re
import sys
from collections import defaultdict
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fontmatch import FONT_OFF, GLYPH_BYTES, ROM  # noqa: E402
from tbl import Table  # noqa: E402
import textscan  # noqa: E402

_textlike = textscan.textlike
textscan.textlike = lambda s: _textlike(re.sub("‹(.)›", r"\1", s))  # keep lines that use a duplicate reading

ROOT = Path(__file__).resolve().parents[1]


def glyph_img(rom, i, z):
    b = rom[FONT_OFF + i * GLYPH_BYTES:FONT_OFF + (i + 1) * GLYPH_BYTES]
    img = Image.new("L", (12, 12), 255)
    for r in range(12):
        bits = b[r] << 8 | b[12 + r]
        for x in range(12):
            if bits & (0x8000 >> x):
                img.putpixel((x, r), 0)
    return img.resize((12 * z, 12 * z), Image.NEAREST)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--margin", type=float, default=0.15)
    ap.add_argument("--per", type=int, default=60)
    ap.add_argument("--out", default=str(ROOT / "work" / "fontreview"))
    a = ap.parse_args()
    rom = ROM.read_bytes()
    t = Table.load(ROOT / "tbl" / "jp.tbl")
    rows = {r["code"]: r for r in csv.DictReader((ROOT / "work" / "font" / "match.tsv").open(encoding="utf-8"),
                                                  delimiter="\t")}
    # which codes the script uses, with example lines
    ctx = defaultdict(list)
    for pos, n, s in textscan.scan(rom, t, 3):
        for ch in set(re.findall(r"‹.›|[^‹›]", re.sub(r"\{[^}]*\}", "", s))):
            ctx[ch].append(s.replace("{nl}", "/")[:60])
    enc = {v: k.hex().upper() for k, v in t.dec.items()}
    todo = []
    for ch, lines in ctx.items():
        code = enc.get(ch)
        if not code or code not in rows or rows[code]["flag"] == "sheet":
            continue
        r = rows[code]
        unsure = r["flag"] in ("order", "low") or float(r["score"]) - float(r["score2"]) < a.margin
        if unsure or ch.startswith("‹"):
            todo.append((code, ch, r["char2"], lines[:3]))
    todo.sort()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    font = ImageFont.truetype("C:/Windows/Fonts/msgothic.ttc", 24)
    small = ImageFont.truetype("C:/Windows/Fonts/msgothic.ttc", 14)
    z, cw, ch_ = 4, 170, 80
    for c in range(0, len(todo), a.per):
        chunk = todo[c:c + a.per]
        cols = 6
        img = Image.new("L", (cols * cw, ((len(chunk) + cols - 1) // cols) * ch_), 255)
        d = ImageDraw.Draw(img)
        with open(out / f"chunk{c // a.per:02d}.tsv", "w", encoding="utf-8", newline="\n") as f:
            f.write("code\tguess\tsecond\tlines\n")
            for k, (code, guess, second, lines) in enumerate(chunk):
                x, y = (k % cols) * cw, (k // cols) * ch_
                i = int(code, 16) - (0xF15E if len(code) == 4 else 0x50)
                img.paste(glyph_img(rom, i, z), (x + 4, y + 18))
                d.text((x + 4, y + 2), code, font=small, fill=0)
                d.text((x + 60, y + 24), guess.strip("‹›"), font=font, fill=0)
                d.text((x + 100, y + 24), second, font=font, fill=120)
                d.rectangle((x, y, x + cw - 1, y + ch_ - 1), outline=180)
                f.write(f"{code}\t{guess}\t{second}\t{' | '.join(lines)}\n")
        img.save(out / f"chunk{c // a.per:02d}.png")
    print(f"{len(todo)} codes to confirm, {(len(todo) + a.per - 1) // a.per} chunks in {out}")


if __name__ == "__main__":
    main()
