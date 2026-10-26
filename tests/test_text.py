import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from tbl import Table  # noqa: E402
import lz  # noqa: E402

ROM = (ROOT / "rom" / "Seijuu Maden Beasts & Blades (Japan).sfc").read_bytes()
T = Table.load(ROOT / "tbl" / "jp.tbl")

# (file offset, text) decoded on screen in the original: docs/re/text.md
KNOWN = [
    (0x011A9C, "名前をいれてください。{end}"),
    (0x011AAA, "『{icall:2B4F7E}』{nl}でよろしいですか?{nl}{choice:0201} はい{nl} いいえ{end}"),
    (0x01621D, "至高神は告げた。{end}"),
    (0x277A0A, "{var:02}の母{nl}「{var:02}!{nl} 早く起きなさい!」{end}"),
]


def test_known_strings_decode():
    for off, want in KNOWN:
        assert T.decode(ROM, off)[0] == want


def test_table_is_one_to_one():
    vals = list(T.dec.values())
    assert len(vals) == len(set(vals)), "two codes share a reading: make_tbl.py marks the second ‹c›"


def test_scanned_strings_roundtrip():
    import textscan
    for pos, n, s in textscan.scan(ROM, T, 3):
        assert T.encode(s) == ROM[pos:pos + n], hex(pos)


def test_lz_roundtrip():
    lz.selftest()
