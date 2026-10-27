"""jp_left_check.py: Japanese prose still reachable in the English build, outside every extracted unit.

    python -X utf8 tools/jp_left_check.py [build/seijuu_en.sfc]

Runs the skill's jp_left.py (--orig: bytes the build never touched), then drops runs inside a unit's slot (dead
tails of relocated lines) and runs that read as data (mostly not hiragana, or one char on every other byte: tile and
pointer tables decode that way). What is left is text the extractor missed. Exit 1 if any.
"""
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import extract  # noqa: E402
from skill import SKILL  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


def common_pairs(rom, t):
    """The 400 commonest char pairs of the game's own lines: prose is made of them, decoded data is not."""
    c = Counter(s[i:i + 2] for entries in extract.units(rom, t).values() for _, _, s in entries
                for i in range(len(s) - 1))
    return {p for p, _ in c.most_common(400)}


def prose(s, pairs):
    hits = sum(s[i:i + 2] in pairs for i in range(len(s) - 1))
    return len(s) >= 6 and hits * 2 >= len(s) - 1


def main():
    built = sys.argv[1] if len(sys.argv) > 1 else str(ROOT / "build" / "seijuu_en.sfc")
    rom = extract.ROM.read_bytes()
    t = extract.table()
    cov = set()
    for entries in extract.units(rom, t).values():
        for off, w, _ in entries:
            cov.update(range(off, off + extract.slot(rom, t, off, w)))
    cov.update(extract.not_text())
    out = subprocess.run([sys.executable, "-X", "utf8", str(Path(SKILL) / "scripts" / "jp_left.py"), built,
                          "--orig", str(extract.ROM), "--tbl", str(ROOT / "tbl" / "jp.tbl"), "--min", "6",
                          "--limit", "1000000"], capture_output=True, text=True, encoding="utf-8").stdout
    left = [(int(m[1], 16), m[2]) for m in re.finditer(r"^0x([0-9A-F]+)\s+\d+B\s+(\S+)", out, re.M)]
    pairs = common_pairs(rom, t)
    left = [(a, s) for a, s in left if a not in cov and prose(s, pairs)]
    for a, s in left:
        print(f"{extract.cpu(a)} {s}")
    print(f"{len(left)} prose-like runs outside units")
    return 1 if left else 0


if __name__ == "__main__":
    sys.exit(main())
