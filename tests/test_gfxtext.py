import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import build  # noqa: E402
import gfxtext  # noqa: E402

ORIG = build.ROM.read_bytes()


def test_menu_entries_show_their_english():
    """Every rewritten record entry, drawn from the redrawn block's tiles, is exactly its English word."""
    gfx = build.unpack_gfx(ORIG)
    old = {o: gfx[o] for o in gfxtext.MENUS}
    writes = dict(gfxtext.menus(ORIG, gfx))
    g = gfxtext.glyphs()
    n = 0
    for off, (recs, words) in gfxtext.MENUS.items():
        assert len(gfx[off]) == len(old[off])
        for a, k in recs.items():
            for e in range(k):
                o = (a & 0x3FFFFF) + e * 24
                orig = [ORIG[o + i * 2] | ORIG[o + i * 2 + 1] << 8 for i in range(12)]
                new = [writes[o][i * 2] | writes[o][i * 2 + 1] << 8 for i in range(12)]
                px = gfxtext.draw(words[gfxtext.key(orig)], g)
                for i, x in enumerate(new):
                    cy, cx = divmod(i, 6)
                    want = gfxtext.tile(px, cx, cy)
                    got = gfx[off][(x & 0xFF) * 16:(x & 0xFF) * 16 + 16] if x != gfxtext.BLANK else want
                    assert x == gfxtext.BLANK or x & 0xFF00 == 0x2100, f"{a:06X}: {x:04X}"
                    assert got == want, f"{a:06X} entry {e} cell {i}"
                n += 1
    assert n == 86


def test_plain_words_fit_and_stay_in_place():
    """Every PLAIN word fits its tiles; tiles outside the words keep their pixels."""
    gfx = build.unpack_gfx(ORIG)
    old = dict(gfx)
    gfxtext.plain(gfx)
    for off, words in gfxtext.PLAIN.items():
        mine = {t + cy * 16 + cx for t, w, _ in words for cy in (0, 1) for cx in range(w)}
        mine |= {t + cx for t, w, _ in gfxtext.HALF.get(off, []) for cx in range(w)}
        for i in range(len(old[off]) // 32):
            if i not in mine:
                assert gfx[off][i * 32:i * 32 + 32] == old[off][i * 32:i * 32 + 32], f"{off:06X} tile {i:02X}"
    for off, halves in gfxtext.HALF.items():  # the header's rule line (row 7, non-zero) survives the redraw
        for t, w, _ in halves:
            for i in range(t, t + w):
                assert any(gfx[off][i * 32 + 14 + k * 16:i * 32 + 16 + k * 16] != b"\0\0" for k in (0, 1)), f"tile {i:02X}"


def test_untouched_tiles_stay():
    """Tiles no record entry used (the battle HP gauge art, unused words) keep their original pixels."""
    gfx = build.unpack_gfx(ORIG)
    old = dict(gfx)
    gfxtext.menus(ORIG, gfx)
    for off, ts in ((0x12A94E, range(0x46, 0x50)), (0x0BCEE0, [0x0C, 0x0D, 0x1C, 0x1D])):  # gauge; unused 確認
        for t in ts:
            assert gfx[off][t * 16:t * 16 + 16] == old[off][t * 16:t * 16 + 16], f"{off:06X} tile {t:02X}"
