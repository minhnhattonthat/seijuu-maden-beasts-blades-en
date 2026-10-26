"""textfind.py: find Japanese words in the ROM by encoding them with tbl/jp.tbl, print each hit with context.

    python -X utf8 tools/textfind.py WORD [WORD ..] [--ctx 24]
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
    ap.add_argument("words", nargs="+")
    ap.add_argument("--ctx", type=int, default=24)
    a = ap.parse_args()
    rom = ROM.read_bytes()
    t = Table.load(ROOT / "tbl" / "jp.tbl")
    for w in a.words:
        pat = t.encode(w)
        i = rom.find(pat)
        while i >= 0:
            s = max(0, i - a.ctx)
            print(f"{w}  ${0xC00000 + i:06X}  {t.decode(rom, s, length=i - s + len(pat) + a.ctx)[0]}")
            i = rom.find(pat, i + 1)


if __name__ == "__main__":
    main()
