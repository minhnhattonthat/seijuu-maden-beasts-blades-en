"""fontmatch.py: first-guess reading of the game's 12x12 font by template matching against MS Gothic 12px bitmaps.

    python -X utf8 tools/fontmatch.py [--out work/font/match.tsv]

Writes one row per glyph index: index, code, best char, score, 2nd char, 2nd score, flag. A guess, not a table:
the kanji run is in JIS order, so a best match that breaks the order is flagged and re-picked from the
candidates between its neighbours (only when the raw score is weak). Indices 0-162 (kana, ー, ■) come from
KANA below, not from matching. Reviewers confirm flagged rows on zoomed sheets (docs/re/text.md).
"""
import argparse
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ROM = ROOT / "rom" / "Seijuu Maden Beasts & Blades (Japan).sfc"
FONT_OFF, GLYPH_BYTES, N_GLYPHS = 0x0A027C, 24, 2690
# Font cells 0-162 read off the font sheet (work/font/v0.png): the game's kana don't match MS Gothic's shapes.
KANA = ("をぁぃぅぇぉゃゅょっあいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわん"
        "がぎぐげござじずぜぞだぢづでどばびぶべぼぱぴぷぺぽ"
        "ヲァィゥェォャュョッアイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワン"
        "ガギグゲゴザジズゼゾダヂヅデドバビブベボパピプペポヴー■")
assert len(KANA) == 163


def code_of(i):
    """Text code for font index i: $50-$F1 one byte, then $F2xx-$FFxx (index + $F15E)."""
    return f"{i + 0x50:02X}" if i < 0xA2 else f"{i + 0xF15E:04X}"


def game_glyph(rom, i):
    b = rom[FONT_OFF + i * GLYPH_BYTES:FONT_OFF + (i + 1) * GLYPH_BYTES]
    a = np.zeros((12, 12), np.float32)
    for r in range(12):
        bits = b[r] << 8 | b[12 + r]
        for x in range(12):
            a[r, x] = 1.0 if bits & (0x8000 >> x) else 0.0
    return a


def jis_chars():
    out = []
    for hi in range(0x21, 0x75):
        for lo in range(0x21, 0x7F):
            try:
                c = bytes([hi | 0x80, lo | 0x80]).decode("euc_jp")
            except UnicodeDecodeError:
                continue
            if len(c) == 1:
                out.append((hi << 8 | lo, c))
    return out


def render(font, c):
    img = Image.new("L", (12, 12), 0)
    ImageDraw.Draw(img).text((0, 0), c, font=font, fill=255)
    return (np.asarray(img) > 127).astype(np.float32)


def shifts(a):
    """The 9 one-pixel shifts of a 12x12 bitmap, flattened."""
    p = np.pad(a, 1)
    return np.stack([p[1 + dy:13 + dy, 1 + dx:13 + dx].ravel() for dy in (-1, 0, 1) for dx in (-1, 0, 1)])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ROOT / "work" / "font" / "match.tsv"))
    a = ap.parse_args()
    rom = ROM.read_bytes()
    font = ImageFont.truetype("C:/Windows/Fonts/msgothic.ttc", 12)
    cands = jis_chars()
    T = np.stack([render(font, c).ravel() for _, c in cands])            # (C, 144)
    G = np.stack([game_glyph(rom, i) for i in range(N_GLYPHS)])           # (N, 12, 12)
    GS = np.stack([shifts(g) for g in G])                                 # (N, 9, 144)
    tn = T.sum(1)
    best = np.full((N_GLYPHS, len(cands)), -1e9, np.float32)
    for s in range(9):
        g = GS[:, s, :]
        inter = g @ T.T                                                   # overlap
        union = g.sum(1)[:, None] + tn[None, :] - inter
        best = np.maximum(best, inter / np.maximum(union, 1))             # IoU
    order = np.argsort(-best, 1)[:, :2]
    jis = np.array([j for j, _ in cands])
    rows = []
    for i in range(N_GLYPHS):
        if i < len(KANA):
            rows.append([i, code_of(i), KANA[i], 1.0, "", 0.0, "sheet"])
            continue
        if G[i].sum() == 0:
            rows.append([i, code_of(i), "", 0.0, "", 0.0, "blank"])
            continue
        k1, k2 = order[i]
        rows.append([i, code_of(i), cands[k1][1], float(best[i, k1]), cands[k2][1], float(best[i, k2]), ""])
    # JIS-order check over the kanji run (JIS row >= 0x30): pick within the neighbours' range when broken
    kan = [r for r in rows if r[2] and jis[[c for _, c in cands].index(r[2])] >= 0x3000]
    names = [c for _, c in cands]
    for k in range(1, len(kan) - 1):
        lo = jis[names.index(kan[k - 1][2])]
        hi = jis[names.index(kan[k + 1][2])]
        me = jis[names.index(kan[k][2])]
        if lo < hi and not lo < me < hi:
            i = kan[k][0]
            m = (jis > lo) & (jis < hi)
            if m.any() and kan[k][3] < 0.85:  # the font is JIS order in segments: trust a strong raw match
                j = np.where(m)[0][np.argmax(best[i][m])]
                kan[k][4], kan[k][5] = kan[k][2], kan[k][3]
                kan[k][2], kan[k][3] = cands[j][1], float(best[i, j])
            kan[k][6] = "order"
    for r in rows:
        if not r[6] and r[3] < 0.75:
            r[6] = "low"
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    with open(a.out, "w", encoding="utf-8", newline="\n") as f:
        f.write("index\tcode\tchar\tscore\tchar2\tscore2\tflag\n")
        for r in rows:
            f.write(f"{r[0]}\t{r[1]}\t{r[2]}\t{r[3]:.3f}\t{r[4]}\t{r[5]:.3f}\t{r[6]}\n")
    flags = sum(1 for r in rows if r[6] in ("order", "low"))
    print(f"{len(rows)} glyphs, {flags} flagged -> {a.out}")


if __name__ == "__main__":
    main()
