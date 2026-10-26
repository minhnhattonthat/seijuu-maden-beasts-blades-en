"""textlog_check.py: which strings the game printed (tools/lua/textlog.lua logs) are not extracted units.

    python -X utf8 tools/debug/warp.py all --lua tools/lua/textlog.lua
    python -X utf8 tools/textlog_check.py [work/qa/warp/*/log.txt ...]

A pointer inside a unit (the engine advancing, a {call} return) is fine; RAM pointers (7E/7F) are skipped.
Exit 1 if any ROM string start is not covered by a unit.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import extract  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


def main():
    logs = [Path(p) for p in sys.argv[1:]] or sorted((ROOT / "work" / "qa" / "warp").glob("*/log.txt"))
    rom = extract.ROM.read_bytes()
    t = extract.table()
    cov = {}
    for name, entries in extract.units(rom, t).items():
        for off, w, _ in entries:
            for o in range(off, off + extract.slot(rom, t, off, w)):
                cov[o] = name
    seen, bad = {}, {}
    for f in logs:
        for m in re.finditer(r"str ([0-9A-F]{6})", f.read_text(encoding="utf-8", errors="replace")):
            a = int(m[1], 16)
            if (a >> 16) in (0x7E, 0x7F) or a < 0xC00000 or a >= 0xE80000:  # RAM, expansion (relocated)
                continue
            o = a & 0x3FFFFF
            seen.setdefault(o, f.parent.name)
            if o not in cov:
                bad.setdefault(o, f.parent.name)
    print(f"{len(seen)} ROM string pointers in {len(logs)} logs, {len(bad)} not in a unit")
    for o, scene in sorted(bad.items()):
        try:
            s = t.decode(rom, o)[0]
        except ValueError:
            s = "?"
        print(f"  {o | 0xC00000:06X} {scene:16} {s[:60]}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
