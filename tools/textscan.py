"""textscan.py: find text in the ROM. Splits at 00, decodes each run with tbl/jp.tbl, keeps runs that read as
Japanese (known codes only, enough kana), and merges neighbours into regions.

    python -X utf8 tools/textscan.py [--min 3] [--gap 64] [--show]

Prints one line per region: file range, CPU range, string count, first string. A survey, not the extractor:
it misses strings with no kana and can split a region at a pointer table.
"""
import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tbl import Table  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
ROM = ROOT / "rom" / "Seijuu Maden Beasts & Blades (Japan).sfc"
KANA = re.compile(r"[ぁ-んァ-ヴー]")


HIRA = re.compile(r"[ぁ-ん]")
COMMON = re.compile(r"[のはをにがでとたしてるいう。、…!?]")


def textlike(s):
    if "[" in s or "‹" in s:
        return False
    body = re.sub(r"\{[^}]*\}", "", s).strip()
    if len(body) < 3:
        return False
    # real lines are mostly kana with particles; random bytes spread over ~2700 kanji codes
    return len(KANA.findall(body)) >= len(body) * 0.5 and len(COMMON.findall(body)) >= max(1, len(body) // 6)


def scan(rom, t, minlen):
    """Strings start right after a 00 (the previous string's end)."""
    hits = []
    pos = 1
    while pos < len(rom):
        if rom[pos - 1] != 0:
            pos += 1
            continue
        try:
            s, n = t.decode(rom, pos, maxlen=600)
        except (ValueError, IndexError):
            pos += 1
            continue
        if n >= minlen and textlike(s):
            hits.append((pos, n, s))
            pos += n
        else:
            pos += 1
    return hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--min", type=int, default=3)
    ap.add_argument("--gap", type=int, default=64)
    ap.add_argument("--nmin", type=int, default=3, help="drop regions with fewer strings")
    ap.add_argument("--show", action="store_true")
    a = ap.parse_args()
    rom = ROM.read_bytes()
    t = Table.load(ROOT / "tbl" / "jp.tbl")
    hits = scan(rom, t, a.min)
    regions = []
    for h in hits:
        if regions and h[0] - (regions[-1][-1][0] + regions[-1][-1][1]) <= a.gap:
            regions[-1].append(h)
        else:
            regions.append([h])
    total = 0
    regions = [r for r in regions if len(r) >= a.nmin]
    for r in regions:
        lo, hi = r[0][0], r[-1][0] + r[-1][1]
        total += hi - lo
        print(f"{lo:06X}-{hi:06X} ${0xC00000 + lo:06X} n={len(r):4d} {hi - lo:6d}B  {r[0][2][:40]}")
        if a.show:
            for p, n, s in r:
                print(f"   {p:06X} {s}")
    print(f"{len(regions)} regions, {sum(len(r) for r in regions)} strings, {total} bytes")


if __name__ == "__main__":
    main()
