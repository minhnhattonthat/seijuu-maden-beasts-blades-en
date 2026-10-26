"""textdump.py: decode consecutive {end}-terminated strings in a CPU range, one per line, with addresses.

    python -X utf8 tools/textdump.py C1621D C1657A [--fixed N]   (--fixed: N-byte records instead of {end})
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tbl import Table  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
ROM = ROOT / "rom" / "Seijuu Maden Beasts & Blades (Japan).sfc"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("start")
    ap.add_argument("end")
    ap.add_argument("--fixed", type=int)
    a = ap.parse_args()
    rom = ROM.read_bytes()
    t = Table.load(ROOT / "tbl" / "jp.tbl")
    p, e = int(a.start, 16) & 0x3FFFFF, int(a.end, 16) & 0x3FFFFF
    while p < e:
        if a.fixed:
            s, n = t.decode(rom, p, length=a.fixed)
        else:
            try:
                s, n = t.decode(rom, p, maxlen=e - p + 8)
            except ValueError:
                s, n = t.decode(rom, p, length=e - p)
        print(f"{0xC00000 | p:06X} {n:3d} {rom[p:p + min(n, 8)].hex(' '):<24} {s}")
        p += n


if __name__ == "__main__":
    main()
