"""tilescan.py: find menu text stored as BG tilemap words (tile = text code - $10, 8x8 menu font CBC255).

A run = >= MIN consecutive 16-bit words with the same high byte whose low byte + $10 decodes (tbl/jp.tbl) to kana,
or to a space-like tile ($E7 = blank cell) inside the run. Prints offset, high byte, word count and the text.

    python -X utf8 tools/tilescan.py [--min 3] [--hi 20]
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import extract  # noqa: E402

BLANK = 0xE7  # empty menu cell


def kana(t, lo):
    c = t.dec.get(bytes([lo + 0x10])) if lo + 0x10 < 0x100 else None
    return c if c and 0x50 <= lo + 0x10 < 0xF2 else None


def scan(rom, t, nmin=3, his=None):
    out, i = [], 0
    while i < len(rom) - 1:
        hi = rom[i + 1]
        if (his is None or hi in his) and kana(t, rom[i]):
            j, s, n = i, "", 0
            while j < len(rom) - 1 and rom[j + 1] == hi and (kana(t, rom[j]) or rom[j] == BLANK):
                c = kana(t, rom[j])
                s += c or " "
                n += bool(c)
                j += 2
            if n >= nmin:
                out.append((i, hi, (j - i) // 2, s))
                i = j
                continue
        i += 1
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--min", type=int, default=3)
    ap.add_argument("--hi", type=lambda x: int(x, 16), action="append")
    a = ap.parse_args()
    rom = extract.ROM.read_bytes()
    for off, hi, n, s in scan(rom, extract.table(), a.min, a.hi):
        print(f"{0xC00000 | off:06X}\t{hi:02X}\t{n}\t{s}")


if __name__ == "__main__":
    main()
