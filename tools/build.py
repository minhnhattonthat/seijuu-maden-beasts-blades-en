"""build.py: build build/seijuu_en.sfc from the original ROM (checked against rom.sha1 first).

Unpack -> repack: every unit the translation can change is read out of the original and written back:
  - text: every string an event-script message op (0A/0C) points at (tools/evdis.py walk), decoded with
    tbl/jp.tbl and re-encoded in place;
  - graphics: every LZ block tools/lzblocks.py finds; a block whose raw data is unchanged keeps its original
    bytes, a changed one is recompressed (tools/lz.py) and must fit its old slot.
Then the header checksum is recomputed. With no edits the output equals the original byte for byte
(tests/test_build.py). Every changed write goes to build/writes.log and romdiff.py checks the output against it.

    python -X utf8 tools/build.py [--out build/seijuu_en.sfc]
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bps  # noqa: E402
import check_rom  # noqa: E402
import evdis  # noqa: E402
import lz  # noqa: E402
import lzblocks  # noqa: E402
import romdiff  # noqa: E402
from tbl import Table  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
ROM = evdis.ROM
DUMMY = 0xCE3467  # unused scenario slots point here (tests/test_events.py)


def unpack_text(rom):
    """{file offset: text} for every event-script message string."""
    t = Table.load(ROOT / "tbl" / "jp.tbl")
    out = {}
    for s in range(evdis.NSCN):
        sc = evdis.scenario(rom, s)
        if sc["base"] == DUMMY:
            continue
        seen = set()
        for e in sc["events"]:
            try:
                for a, _ in evdis.walk(rom, e, seen):
                    o = a & 0x3FFFFF
                    if rom[o] in (0x0A, 0x0C):
                        p = (a & 0x3F0000) | rom[o + 2] | rom[o + 3] << 8
                        if p not in out:
                            out[p] = t.decode(rom, p)[0]
            except evdis.Bad:
                pass  # known dead path (tests/test_events.py KNOWN_BAD); its earlier messages are kept
    return out


def unpack_gfx(rom):
    """{file offset: raw bytes} for every LZ block found statically."""
    seeds, _ = lzblocks.blocks(rom)
    for table, bank, n in lzblocks.TABLES:
        for i in range(n):
            seeds.setdefault(bank << 16 | rom[table + 2 * i] | rom[table + 2 * i + 1] << 8, [])
    return {off: raw for off, (raw, _) in lzblocks.chain(rom, seeds).items()}


class Writer:
    def __init__(self, orig):
        self.orig, self.rom, self.log = orig, bytearray(orig), []

    def write(self, off, data, name):
        old = bytes(self.rom[off:off + len(data)])
        if old != data:
            self.rom[off:off + len(data)] = data
            self.log.append((off, bytes(self.orig[off:off + len(data)]), bytes(data), name))


def repack(orig, text, gfx):
    t = Table.load(ROOT / "tbl" / "jp.tbl")
    w = Writer(orig)
    for off, s in sorted(text.items()):
        b = t.encode(s)
        n = t.decode(orig, off)[1]
        if len(b) > n:  # relocation via {call} comes with the engine work (phase 5)
            raise SystemExit(f"text {0xC00000 | off:06X}: {len(b)} bytes > {n}-byte slot")
        w.write(off, b, f"text_{0xC00000 | off:06X}")
    for off, raw in sorted(gfx.items()):
        old, used = lz.decompress(orig, off)
        if raw == old:
            continue
        z = lz.compress(raw)
        if len(z) > used:
            raise SystemExit(f"lz {0xC00000 | off:06X}: {len(z)} bytes > {used}-byte slot")
        w.write(off, z, f"lz_{0xC00000 | off:06X}")
    rom, _ = bps.snes_checksum(w.rom)
    w.write(0xFFDC, rom[0xFFDC:0xFFE0], "checksum")
    return w


def build(orig):
    # phase 4 overlays script/*.json translations on these units
    return repack(orig, unpack_text(orig), unpack_gfx(orig))


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", type=Path, default=ROOT / "build" / "seijuu_en.sfc")
    a = ap.parse_args()
    check_rom.check()
    orig = ROM.read_bytes()
    w = build(orig)
    errs, _ = romdiff.check(orig, bytes(w.rom), set(), w.log)
    if errs:
        sys.exit("romdiff:\n" + "\n".join(errs))
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_bytes(w.rom)
    (a.out.parent / "writes.log").write_text(
        "".join(f"{o:06X} {x.hex()} {y.hex()} {n}\n" for o, x, y, n in w.log), encoding="utf-8")
    print(f"{a.out}: {len(w.log)} writes, {'identical to the original' if w.rom == orig else 'patched'}")


if __name__ == "__main__":
    main()
