"""build.py: build build/seijuu_en.sfc from the original ROM (checked against rom.sha1 first).

Unpack -> repack: every unit the translation can change is read out of the original and written back:
  - text: every unit tools/extract.py finds (event messages, code-read lists, pointer tables, name fields),
    decoded with tbl/jp.tbl, overlaid with the "en" fields of script/*.json and re-encoded in place;
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
import extract  # noqa: E402
import lz  # noqa: E402
import lzblocks  # noqa: E402
import romdiff  # noqa: E402
from tbl import Table  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
ROM = evdis.ROM


def unpack_text(rom):
    """{file offset: (slot width or None for {end}-terminated, text)} for every unit tools/extract.py knows."""
    return {off: (w, s) for entries in extract.units(rom).values() for off, w, s in entries}


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
    for off, (wd, s) in sorted(text.items()):
        b = extract.encode(t, s, wd)
        n = extract.slot(orig, t, off, wd)
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
    text = unpack_text(orig)
    for off, en in extract.load_en().items():  # script/*.json translations over the original units
        if off not in text:
            raise SystemExit(f"script: {0xC00000 | off:06X} is not a text unit (re-run tools/extract.py)")
        text[off] = (text[off][0], en)
    return repack(orig, text, unpack_gfx(orig))


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
