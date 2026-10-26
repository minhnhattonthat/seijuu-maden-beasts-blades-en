import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import build  # noqa: E402
import lz  # noqa: E402
import romdiff  # noqa: E402

ORIG = build.ROM.read_bytes()
TEXT = build.unpack_text(ORIG)
GFX = build.unpack_gfx(ORIG)


def test_identity_build():
    w = build.repack(ORIG, TEXT, GFX)
    assert bytes(w.rom) == ORIG and w.log == []
    assert len(TEXT) > 3000 and len(GFX) > 100


def test_edits_land_and_log():
    off = 0x277A0A  # hero's mother's first line (tests/test_text.py)
    gfx_off = 0x0CAB70  # intro poem graphic
    raw = bytearray(GFX[gfx_off])
    raw[0] ^= 0xFF
    w = build.repack(ORIG, {**TEXT, off: "あ{end}"}, {**GFX, gfx_off: bytes(raw)})
    b = build.Table.load(ROOT / "tbl" / "jp.tbl").encode("あ{end}")
    assert w.rom[off:off + len(b)] == b
    assert lz.decompress(w.rom, gfx_off)[0] == bytes(raw)
    assert romdiff.check(ORIG, bytes(w.rom), set(), w.log)[0] == []
    assert {n for *_, n in w.log} >= {"text_E77A0A", "lz_CCAB70", "checksum"}
