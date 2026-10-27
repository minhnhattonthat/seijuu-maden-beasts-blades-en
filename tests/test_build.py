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
    w = build.repack(ORIG, {**TEXT, off: (None, "あ{end}")}, {**GFX, gfx_off: bytes(raw)})
    b = build.Table.load(ROOT / "tbl" / "jp.tbl").encode("あ{end}")
    assert w.rom[off:off + len(b)] == b
    assert lz.decompress(w.rom, gfx_off)[0] == bytes(raw)
    assert romdiff.check(ORIG, bytes(w.rom), set(), w.log)[0] == []
    assert {n for *_, n in w.log} >= {"text_E77A0A", "lz_CCAB70", "checksum"}


def test_status_map():
    en = build.Table.load(ROOT / "tbl" / "en.tbl")
    raw = build.status_map(en, GFX[build.STATUS_MAP])
    cells = [raw[i] | raw[i + 1] << 8 for i in range(0, len(raw), 2)]
    row = "".join(en.decode(bytes([(x & 0xFF) + 0x10, 0]), 0)[0][:1] for x in cells[36 * 32 + 8:36 * 32 + 28])
    assert row == "Strength:" + row[9:11] + "  Weight:"
    assert cells[46 * 32 + 15] == 0x0140  # the weapon icon cell moved to col 15
    assert len(raw) == len(GFX[build.STATUS_MAP])
    party = build.status_map(en, GFX[build.PARTY_MAP], party=True)
    cells = [party[i] | party[i + 1] << 8 for i in range(0, len(party), 2)]
    row = "".join(en.decode(bytes([(x & 0xFF) + 0x10, 0]), 0)[0][:1] for x in cells[36 * 32 + 8:36 * 32 + 28])
    assert row == "Strength:" + row[9:11] + "  Weight:"
    assert cells[36 * 32 + 8] >> 8 == 0x20  # party view cells keep their attribute
    assert len(lz.compress(party)) <= lz.decompress(ORIG, build.PARTY_MAP)[1]


def test_relocation_and_packed_runs():
    en = build.Table.load(ROOT / "tbl" / "en.tbl")
    long = "Good morning! " * 20 + "{end}"
    pro = 0x1622A  # a prologue line (SEQ run): the whole run is rewritten as stubs
    w = build.repack(ORIG, {**TEXT, 0x277A0A: (None, long), pro: (None, "Long ago...{end}")}, GFX, asm=True)
    rom = bytes(w.rom)
    assert len(rom) == build.END and rom[0x277A0A:0x277A0C] == b"\x0f\xff" and rom[0x277A0F] == 0
    dest = int.from_bytes(rom[0x277A0C:0x277A0F], "little") & 0x3FFFFF
    assert dest >= build.EXP + build.ASM_SPACE and en.decode(rom, dest)[0] == long
    assert "run_prologue" in {n for *_, n in w.log}
    assert romdiff.check(ORIG, rom, set(), w.log)[0] == []
