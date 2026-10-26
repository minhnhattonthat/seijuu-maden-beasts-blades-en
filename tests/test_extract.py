import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import extract  # noqa: E402

ROM = extract.ROM.read_bytes()
T = extract.table()
UNITS = extract.units(ROM, T)


def test_roundtrip_every_entry():
    """Re-encoding every extracted string gives the original bytes of its slot."""
    n = 0
    for entries in UNITS.values():
        for off, w, s in entries:
            ln = extract.slot(ROM, T, off, w)
            assert extract.encode(T, s, w) == ROM[off:off + ln], f"{off | 0xC00000:06X} {s!r}"
            n += 1
    assert n > 6000


def test_no_overlaps():
    spans = sorted((off, off + extract.slot(ROM, T, off, w)) for e in UNITS.values() for off, w, _ in e)
    for (a, b), (c, _) in zip(spans, spans[1:]):
        assert b <= c, f"{a | 0xC00000:06X} overlaps {c | 0xC00000:06X}"


def test_coverage():
    """Every text-like region of the original is a unit or was read by eye and listed as not text."""
    known = extract.not_text()
    left = [f"{lo | 0xC00000:06X} {r[0][2][:30]}" for lo, hi, r in extract.gaps(ROM, T) if lo not in known]
    assert not left, "uncovered text-like regions (add a unit or a not_text.tsv line):\n" + "\n".join(left)


def test_script_files_match_rom():
    """script/*.json holds exactly the units, with the original text (re-run tools/extract.py if not)."""
    want = {off: s for e in UNITS.values() for off, _, s in e}
    got = {}
    for f in (ROOT / "script").glob("*.json"):
        for r in json.loads(f.read_text(encoding="utf-8")):
            got[int(r["id"], 16) & 0x3FFFFF] = r["jp"]
    assert got == want
