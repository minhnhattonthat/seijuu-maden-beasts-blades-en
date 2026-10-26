"""evdis.py: event-script disassembler (VM at C03BE6, docs/re/events.md).

    python -X utf8 tools/evdis.py SCN [EVENT]       list a scenario's events (or one), decoded with text
    python -X utf8 tools/evdis.py --all [--find OP]  walk every event of every scenario; report bad opcodes,
                                                      or list each instruction with opcode OP (hex)

Scenario table: CE0002 + 3*$505A -> header (entry list, ?, event table, map table), all 16-bit in its bank.
Walks by control flow (goto 00, conditional 02/04, call 06) from each event entry, so data after an FF is never
read as code.
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tbl import Table  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
ROM = ROOT / "rom" / "Seijuu Maden Beasts & Blades (Japan).sfc"
NSCN = 98

# fixed argument bytes after the opcode; None = special-cased in length()
ARGS = {
    0x00: 2, 0x02: None, 0x04: None, 0x06: 2, 0x08: 0, 0x0A: 3, 0x0C: 3, 0x0E: 7, 0x10: 10, 0x12: 5,
    0x14: 0, 0x16: 0, 0x18: None, 0x1A: 1, 0x1C: 0, 0x1E: 1, 0x20: 3, 0x22: 3, 0x24: 3, 0x26: 2, 0x28: 2,
    0x2A: 2, 0x2C: 2, 0x2E: 2, 0x30: 2, 0x32: 1, 0x34: 1, 0x36: 1, 0x38: 2, 0x3A: 1, 0x3C: 0, 0x3E: 2,
    0x40: 1, 0x42: 4, 0x44: 1, 0x46: 3, 0x48: 2, 0x4A: 5, 0x4C: 2, 0x4E: 1, 0x50: 2, 0x52: 1, 0x54: 2,
    0x56: 1, 0x58: 1, 0x5A: 0, 0x5C: 1, 0x5E: 5, 0x60: None, 0x62: None, 0x64: None, 0x66: 2, 0x68: 0,
    0x6A: None, 0x6C: None, 0x6E: 0, 0x70: 0, 0x72: 0, 0x74: 0, 0x76: 0, 0x78: 0, 0x7A: 1, 0x7C: 1, 0x7E: 1,
    0x80: 0, 0x82: 3, 0x84: 3, 0x86: 2, 0x88: 0, 0x8A: 3, 0x8C: 0, 0x8E: 4, 0x90: 8, 0x92: 1, 0x94: 3,
    0x96: 3, 0x98: 3, 0x9A: 0, 0x9C: 3, 0x9E: 2, 0xA0: 2, 0xA2: 1, 0xA4: 0, 0xA6: 0, 0xA8: 0,
}
NAMES = {0x00: "goto", 0x02: "ifnot", 0x04: "ifnot2", 0x06: "call", 0x08: "ret", 0x0A: "msg", 0x0C: "msg",
         0x0E: "map", 0x10: "scene", 0x12: "map2", 0x30: "setvar", 0x32: "incvar", 0x1A: "decvar",
         0x34: "setflag", 0x36: "clrflag", 0x5E: "battle", 0x60: "menu60", 0x62: "menu62", 0x64: "menu64",
         0x66: "menu66", 0x68: "menu68", 0x6A: "menu6A", 0x6C: "menu6C", 0x6E: "menu6E", 0x70: "menu70",
         0x72: "menu72", 0x74: "menu74", 0x76: "menu76", 0x78: "rest", 0x24: "addgold", 0x26: "paygold",
         0x5C: "sfx", 0x58: "music", 0x5A: "musicoff", 0xFF: "end", 0xFE: "halt"}
# condition sub-ops of 02/04 (table C03D46): extra argument bytes
COND_EXTRA = {0x00: 0, 0x02: 1, 0x04: 1, 0x06: 1, 0x08: 1, 0x0A: 1, 0x0C: 1, 0x0E: 1, 0x10: 1, 0x12: 0}


class Bad(Exception):
    pass


def length(rom, a):
    """Instruction length at CPU address a (opcode included)."""
    o = a & 0x3FFFFF
    op = rom[o]
    if op in (0xFF, 0xFE):
        return 1
    if op not in ARGS:
        raise Bad(f"bad opcode {op:02X}")
    n = ARGS[op]
    if n is not None:
        return 1 + n
    if op == 0x02:
        t = rom[o + 5]
        if t == 0x14:
            return 7
        if t not in COND_EXTRA:
            raise Bad(f"02 cond {t:02X}")
        return 6 + COND_EXTRA[t]
    if op == 0x04:
        t = rom[o + 3]
        if t not in COND_EXTRA:
            raise Bad(f"04 cond {t:02X}")
        return 4 + COND_EXTRA[t]
    if op == 0x18:
        i = o + 5
        while rom[i] | rom[i + 1] << 8 != 0xFFFF:
            i += 2
        return i + 2 - o
    if op in (0x60, 0x62, 0x6A, 0x6C):
        i = o + 1
        while True:
            b = rom[i]; i += 1
            if b == 0xFF:
                return i - o
            i += 1
    if op == 0x64:
        i = o + 1
        while rom[i] != 0xFF:
            i += 1
        return i - o  # the FF is left as the next opcode (handler DEYs)
    raise Bad(f"no length rule {op:02X}")


def targets(rom, a, n):
    o = a & 0x3FFFFF
    op, bank = rom[o], a & 0xFF0000
    w = lambda k: bank | rom[o + k] | rom[o + k + 1] << 8
    if op == 0x00:
        return [w(1)], False
    if op == 0x02:
        return [w(3)], True
    if op == 0x04:
        return [w(1)], True
    if op == 0x06:
        return [w(1)], True
    return [], op not in (0xFF, 0xFE, 0x08)


def walk(rom, entry, seen=None):
    """Yield (addr, length) of every instruction reachable from entry; raises Bad."""
    seen = set() if seen is None else seen
    todo = [entry]
    while todo:
        a = todo.pop()
        while a not in seen:
            seen.add(a)
            n = length(rom, a)
            yield a, n
            tg, falls = targets(rom, a, n)
            todo.extend(tg)
            if not falls:
                break
            a += n


def scenario(rom, s):
    o = 0x0E0002 + 3 * s
    base = rom[o] | rom[o + 1] << 8 | rom[o + 2] << 16
    bank = base & 0xFF0000
    r = lambda a: rom[a & 0x3FFFFF] | rom[(a & 0x3FFFFF) + 1] << 8
    ev = bank | r(base + 4)
    maps, a = [], base + 6
    while r(a) != 0x00FF and a < ev:
        maps.append(bank | r(a)); a += 2
    events, a = [], ev
    while True:
        v = r(a)
        if events and (v < (ev & 0xFFFF) or bank | v == base):
            break
        events.append(bank | v); a += 2
        if a >= min(e for e in events) or len(events) > 400:
            break
    return dict(base=base, entry=bank | r(base), maps=maps, events=events)


def fmt(rom, t, a, n):
    o = a & 0x3FFFFF
    op = rom[o]
    s = f"{a:06X}  {rom[o:o + n].hex(' '):<30} {NAMES.get(op, f'op{op:02X}')}"
    if op in (0x0A, 0x0C):
        p = (a & 0xFF0000) | rom[o + 2] | rom[o + 3] << 8
        try:
            s += "  " + t.decode(rom, p & 0x3FFFFF)[0][:120]
        except ValueError:
            s += "  <undecodable>"
    return s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("scn", nargs="?", type=int)
    ap.add_argument("event", nargs="?", type=int)
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--find")
    a = ap.parse_args()
    rom = ROM.read_bytes()
    t = Table.load(ROOT / "tbl" / "jp.tbl")
    if a.all:
        bad = 0
        find = int(a.find, 16) if a.find else None
        for s in range(NSCN):
            sc = scenario(rom, s)
            seen = set()
            for i, e in enumerate(sc["events"]):
                try:
                    for addr, n in walk(rom, e, seen):
                        if find is not None and rom[addr & 0x3FFFFF] == find:
                            print(f"scn {s} ev {i}: {fmt(rom, t, addr, n)}")
                except Bad as ex:
                    bad += 1
                    if find is None:
                        print(f"scn {s} ev {i} @{e:06X}: {ex}")
        print(f"bad walks: {bad}", file=sys.stderr)
        return
    sc = scenario(rom, a.scn)
    print(f"scn {a.scn} @{sc['base']:06X} maps={len(sc['maps'])} events={len(sc['events'])}")
    evs = [a.event] if a.event is not None else range(len(sc["events"]))
    for i in evs:
        e = sc["events"][i]
        print(f"-- event {i} @{e:06X}")
        try:
            for addr, n in sorted(walk(rom, e)):
                print("  " + fmt(rom, t, addr, n))
        except Bad as ex:
            print(f"  !! {ex}")


if __name__ == "__main__":
    main()
