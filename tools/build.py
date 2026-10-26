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
import re
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bps  # noqa: E402
import check_rom  # noqa: E402
import evdis  # noqa: E402
import extract  # noqa: E402
import font  # noqa: E402
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


EXP, END = 0x280000, 0x400000  # banks E8-FF, the 4 MB expansion (docs/re/rom.md)
ASM, ASAR = ROOT / "tools" / "asm" / "text.asm", ROOT / "tools" / "asar" / "asar.exe"
MENU_FONT = 0x0BC255  # LZ block: the 8x8 menu font (docs/re/graphics.md), lowercase from fonts/en8.txt
ASM_SPACE = 0x4000  # E80000-E83FFF belong to tools/asm/text.asm; relocated text starts after it
SEQ_PTRS = {"endings": [(0xC17044, 5)]}  # 16-bit pointer tables into a SEQ run, rewritten when it is packed


class Writer:
    def __init__(self, orig):
        self.orig, self.rom, self.log, self.free = orig, bytearray(orig), [], EXP + ASM_SPACE

    def write(self, off, data, name):
        if off + len(data) > len(self.rom):
            self.rom += b"\xff" * (END - len(self.rom))
        old = bytes(self.rom[off:off + len(data)])
        if old != data:
            self.rom[off:off + len(data)] = data
            o = self.orig[off:off + len(data)]
            self.log.append((off, o + b"\xff" * (len(data) - len(o)), bytes(data), name))

    def put(self, data, name):
        """Place data in the expansion; returns its CPU address. Never crosses a bank, and the address has no
        00 byte (code that skips a string by scanning for 00 must not stop inside a {call} stub)."""
        p = self.free
        if (p & 0xFFFF) + len(data) > 0x10000:
            p = (p | 0xFFFF) + 1
        p = max(p, p & 0xFF0000 | 0x0101)
        p += (p & 0xFF) == 0
        if p + len(data) > END:
            raise SystemExit("expansion full")
        self.write(p, data, name)
        self.free = p + len(data)
        return 0xC00000 | p


def stub(addr):
    return b"\x0f\xff" + addr.to_bytes(3, "little") + b"\x00"  # {call:addr}{end}


def pack_run(w, t, orig, text, name, lo, hi):
    """A SEQ run rewritten in place as its lines in order: a line that fits in 6 bytes stays inline, a longer one
    becomes a {call} stub to the expansion; lone {end}s (list ends) stay. Pointer tables into it are moved."""
    out, moved, p = bytearray(), {}, lo
    while p < hi:
        s, n = t.decode(orig, p)
        b = t.encode(text[p][1]) if p in text and text[p][1] != s else orig[p:p + n]
        moved[p] = lo + len(out)
        out += b if len(b) <= 6 else stub(w.put(b, f"{name}_{0xC00000 | p:06X}"))
        p += n
    if len(out) > hi - lo:
        raise SystemExit(f"run {name}: {len(out)} bytes > {hi - lo}")
    w.write(lo, bytes(out), f"run_{name}")
    for tab, cnt in SEQ_PTRS.get(name, []):
        o, bank = tab & 0x3FFFFF, tab & 0x3F0000
        for i in range(cnt):
            q = moved[bank | orig[o + 2 * i] | orig[o + 2 * i + 1] << 8] & 0xFFFF
            w.write(o + 2 * i, q.to_bytes(2, "little"), f"ptr_{name}")


# 16-bit pointer tables into RUNS strings (own bank; found by a whole-ROM scan for >= 3 words that
# all hit string starts), and single pointers: menu-script 0A ops C14812/C14819, LDA #$6944 at C26918
RUN_TABLES = [(0xC0BBCB, 8), (0xC0BBDD, 14), (0xC0BBFB, 21), (0xC0E4BB, 5), (0xC252E5, 13), (0xC38DFF, 4),
              (0xC60B3C, 98), (0xC60E44, 11), (0xC60ECA, 11), (0xC63008, 11), (0xC630C3, 4), (0xC63129, 96),
              (0xC634E6, 69)]
RUN_PTRS = [0xC14814, 0xC1481B, 0xC26919]


def pointer_sites(orig):
    """{string offset: [offsets of 16-bit pointers to it]}: event message ops, PTRS and RUN_TABLES tables."""
    sites = {p: [o + 2 for o in ops] for p, ops in extract.event_sites(orig).items()}
    for a in RUN_PTRS:
        o = a & 0x3FFFFF
        sites.setdefault(o & 0x3F0000 | orig[o] | orig[o + 1] << 8, []).append(o)
    for _, tab, n, _ in extract.PTRS + [(None, a, n, None) for a, n in RUN_TABLES]:
        o, bank = tab & 0x3FFFFF, tab & 0x3F0000
        for i in range(n):
            sites.setdefault(bank | orig[o + 2 * i] | orig[o + 2 * i + 1] << 8, []).append(o + 2 * i)
    return sites


def repoint(w, t, orig, text, short, free, strict):
    """Strings whose slot can't hold a 6-byte stub: put the stub in a freed tail in the same bank and move every
    pointer to it there."""
    sites, errs = pointer_sites(orig) if short else {}, []
    for off in short:
        wd, s = text[off]
        hole = next((h for h in free if h[0] >> 16 == off >> 16 and h[1] - h[0] >= 6), None)
        if off in extract.field_offsets() or off not in sites or not hole:
            errs.append(f"text {0xC00000 | off:06X}: {len(extract.encode(t, s, wd))} bytes > "
                        f"{extract.slot(orig, t, off, wd)}-byte slot")
            continue
        name = f"text_{0xC00000 | off:06X}"
        w.write(hole[0], stub(w.put(t.encode(s if s.endswith("{end}") else s + "{end}"), "reloc" + name[4:])), name)
        for p in sites[off]:
            w.write(p, (hole[0] & 0xFFFF).to_bytes(2, "little"), "ptr" + name[4:])
        hole[0] += 6
    if errs and strict:
        raise SystemExit("\n".join(errs))
    for e in errs:
        print("left as is:", e)


def assemble(orig):
    """tools/asm/text.asm on the 4 MB image -> [(offset, bytes)] runs it changed."""
    out = ROOT / "build"
    out.mkdir(exist_ok=True)
    (out / "en6.bin").write_bytes(font.data())
    img = bytes(orig) + b"\xff" * (END - len(orig))
    tmp = out / "asm.sfc"
    tmp.write_bytes(img)
    r = subprocess.run([str(ASAR), "--fix-checksum=off", str(ASM), str(tmp)], capture_output=True, text=True)
    if r.returncode:
        raise SystemExit("asar:\n" + r.stdout + r.stderr)
    new, runs, i = tmp.read_bytes(), [], 0
    tmp.unlink()
    while i < END:
        if new[i] != img[i]:
            j = i
            while j < END and new[j] != img[j]:
                j += 1
            runs.append((i, new[i:j]))
            i = j
        i += 1
    return runs


def repack(orig, text, gfx, strict=True, asm=False):
    """strict=False (marker build): a line that can't be placed stays in Japanese, with a warning.
    asm=True: apply tools/asm/text.asm and encode with tbl/en.tbl (decoding the original stays tbl/jp.tbl)."""
    t = Table.load(ROOT / "tbl" / "jp.tbl")
    w = Writer(orig)
    if asm:
        t = SimpleNamespace(decode=t.decode, encode=Table.load(ROOT / "tbl" / "en.tbl").encode)
        for off, b in assemble(orig):
            w.write(off, b, "asm")
    seq = [(n, lo & 0x3FFFFF, hi & 0x3FFFFF) for n, lo, hi in extract.RUNS if n in extract.SEQ]
    fields, short, free = extract.field_offsets(), [], []
    base = unpack_text(orig)
    for off, (wd, s) in sorted(text.items()):
        if any(lo <= off < hi for _, lo, hi in seq) or base[off][1] == s:  # untouched: keep the original bytes
            continue
        b = extract.encode(t, s, wd)
        n = extract.slot(orig, t, off, wd)
        if len(b) > n:
            if off in fields or n < 6:
                short.append(off)
                continue
            b = stub(w.put(t.encode(s if s.endswith("{end}") else s + "{end}"), f"reloc_{0xC00000 | off:06X}"))
            free.append([off + 6, off + n])  # the old string's tail: nothing points into it
        w.write(off, b, f"text_{0xC00000 | off:06X}")
    repoint(w, t, orig, text, short, free, strict)
    for name, lo, hi in seq:
        if any(lo <= o < hi and text[o][1] != t.decode(orig, o)[0] for o in text):
            pack_run(w, t, orig, text, name, lo, hi)
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


FILLER = " The quick brown fox jumps over the lazy dog."
NO_MARKER = {"name_grid"}  # layout codes, not lines


def marker(t, off, w, s):
    """Marker text for one entry: every run of glyphs becomes filler of the same width in 6 px cells, the first
    run led by [id]; control codes stay. Fields get the id's last hex digits (their width is fixed)."""
    tag = f"{0xC00000 | off:06X}"
    if w is not None and off in extract.field_offsets():
        return tag[-min(w, 4):]
    out, first = [], True
    for k, part in enumerate(re.split(r"(\{\w+(?::[0-9A-Fa-f]*)?\})", s)):
        if k % 2 or not part:
            out.append(part)
            continue
        cells = sum(2 if t.encode(c)[0] >= 0x50 else 1 for c in re.findall(r"\[..\]|.", part))
        fill = (f"[{tag}]" if first else "") + FILLER * 9
        out.append(fill[:max(cells, len(tag) + 2 if first else 0)])
        first = False
    return "".join(out)


def build(orig, mark=False):
    text, gfx = unpack_text(orig), unpack_gfx(orig)
    gfx[MENU_FONT] = font.menu_font(gfx[MENU_FONT])
    if mark:
        skip = {o for n, es in extract.units(orig).items() if n in NO_MARKER for o, *_ in es}
        t = Table.load(ROOT / "tbl" / "jp.tbl")
        return repack(orig, {o: (w, s if o in skip else marker(t, o, w, s)) for o, (w, s) in text.items()},
                      gfx, strict=False, asm=True)
    for off, en in extract.load_en().items():  # script/*.json translations over the original units
        if off not in text:
            raise SystemExit(f"script: {0xC00000 | off:06X} is not a text unit (re-run tools/extract.py)")
        text[off] = (text[off][0], en)
    return repack(orig, text, gfx, asm=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", type=Path)
    ap.add_argument("--marker", action="store_true", help="every line -> [id] filler (build/seijuu_marker.sfc)")
    a = ap.parse_args()
    a.out = a.out or ROOT / "build" / ("seijuu_marker.sfc" if a.marker else "seijuu_en.sfc")
    check_rom.check()
    orig = ROM.read_bytes()
    w = build(orig, a.marker)
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
