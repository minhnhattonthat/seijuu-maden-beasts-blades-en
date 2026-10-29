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
import gfxtext  # noqa: E402
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
    return lo + len(out)


# 16-bit pointer tables into RUNS strings (own bank; found by a whole-ROM scan for >= 3 words that
# all hit string starts), and single pointers: menu-script 0A ops C14812/C14819, the status screen's
# LDA #$69xx/#$6Bxx (C26D31 strings, bank C2)
RUN_TABLES = [(0xC0BBCB, 8), (0xC0BBDD, 14), (0xC0BBFB, 21), (0xC0E4BB, 5), (0xC252E5, 13), (0xC38DFF, 4),
              (0xC60B3C, 98), (0xC60E44, 11), (0xC60ECA, 11), (0xC63008, 11), (0xC630C3, 4), (0xC63129, 96),
              (0xC634E6, 69)]
RUN_PTRS = [0xC14814, 0xC1481B, 0xC268FA, 0xC26919, 0xC2692C, 0xC26B62, 0xC26B75, 0xC26B8C, 0xC26BF5, 0xC26C34,
            0xC0A29A, 0xC0C75C]  # + menu records C0BAF7, C0C30D (extract.MENUS)
MENU_SCRIPTS = (0x014094, 0x014C19)  # C1 menu scripts: their op 10 lo hi points at an extract.MENUS record


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
    lo, hi = MENU_SCRIPTS
    for p in range(lo, hi):  # menu-script op 10 lo hi: open a menu record
        r = 0x010000 | orig[p + 1] | orig[p + 2] << 8
        if orig[p] == 0x10 and r in extract.MENU_SET:
            sites.setdefault(r, []).append(p + 1)
    for p in town_lists(orig):
        sites.setdefault(0x0E0000 | orig[p] | orig[p + 1] << 8, []).append(p)
    return sites


def town_lists(orig):
    """Offsets of the 16-bit building-name pointers in every town's building list (55 nn, then (ptr, map)
    triples until FF FF; one list per town, in its scenario's bank; the names are in CE, the buildings run)."""
    lo, hi = next((a & 0xFFFF, b & 0xFFFF) for n, a, b in extract.RUNS if n == "buildings")
    out = []
    for i in range(len(orig) - 6):
        if orig[i] == 0x55 and lo <= (orig[i + 2] | orig[i + 3] << 8) < hi:
            j, ptrs = i + 2, []
            while lo <= (orig[j] | orig[j + 1] << 8) < hi:
                ptrs.append(j)
                j += 3
            if orig[j:j + 2] == b"\xff\xff" and len(ptrs) >= 2:
                out += ptrs
    return out


def repoint(w, t, orig, text, short, free, strict):
    """Strings whose slot can't hold a 6-byte stub, and menu records that grew: put the stub (or the record) in a
    freed tail in the same bank and move every pointer to it there."""
    sites, errs = pointer_sites(orig) if short else {}, []
    for off in short:
        wd, s = text[off]
        menu = off in extract.MENU_SET
        b = extract.encode(t, s, wd, off) if menu else None
        need = len(b) if menu else 6
        hole = next((h for h in free if h[0] >> 16 == off >> 16 and h[1] - h[0] >= need), None)
        if off in extract.field_offsets() or off not in sites or not hole:
            errs.append(f"text {0xC00000 | off:06X}: {len(extract.encode(t, s, wd, off))} bytes > "
                        f"{extract.slot(orig, t, off, wd)}-byte slot")
            continue
        name = f"text_{0xC00000 | off:06X}"
        if not menu:
            b = stub(w.put(t.encode(s if s.endswith("{end}") else s + "{end}"), "reloc" + name[4:]))
        w.write(hole[0], b, name)
        for p in sites[off]:
            w.write(p, (hole[0] & 0xFFFF).to_bytes(2, "little"), "ptr" + name[4:])
        hole[0] += need
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


def repack(orig, text, gfx, strict=True, asm=False, maps=()):
    """strict=False (marker build): a line that can't be placed stays in Japanese, with a warning.
    asm=True: apply tools/asm/text.asm and encode with tbl/en.tbl (decoding the original stays tbl/jp.tbl).
    maps: [(offset, bytes)] menu tilemap records to rewrite (gfxtext.menus)."""
    t = Table.load(ROOT / "tbl" / "jp.tbl")
    w = Writer(orig)
    if asm:
        t = SimpleNamespace(decode=t.decode, encode=Table.load(ROOT / "tbl" / "en.tbl").encode)
        for off, b in assemble(orig):
            w.write(off, b, "asm")
        for a, old, new in STATUS_CODE:
            o = a & 0x3FFFFF
            if orig[o] | orig[o + 1] << 8 != old:
                raise SystemExit(f"status code {a:06X}: expected {old:04X}")
            w.write(o, new.to_bytes(2, "little"), "status_code")
    for off, b in maps:
        w.write(off, b, f"menu_map_{0xC00000 | off:06X}")
    seq =[(n, lo & 0x3FFFFF, hi & 0x3FFFFF) for n, lo, hi in extract.RUNS if n in extract.SEQ]
    fields, short, free = extract.field_offsets(), [], []
    base = unpack_text(orig)
    for off, (wd, s) in sorted(text.items()):
        if any(lo <= off < hi for _, lo, hi in seq) or base[off][1] == s:  # untouched: keep the original bytes
            continue
        b = extract.encode(t, s, wd, off)
        n = extract.slot(orig, t, off, wd)
        if len(b) > n:
            if n < 6 or off in extract.MENU_SET:
                short.append(off)
                continue
            # the 8x8 menu printer (C32912) has {call} too (its code 0F, C32A1D), so a name field takes a stub;
            # member names copied to RAM records are drawn by hooked code (text.asm mname/bbox)
            b = stub(w.put(t.encode(s if s.endswith("{end}") else s + "{end}"), f"reloc_{0xC00000 | off:06X}"))
            if off in fields:
                b += bytes(n - 6)
            else:
                free.append([off + 6, off + n])  # the old string's tail: nothing points into it
        elif off not in fields and off not in extract.MENU_SET and n - len(b) >= 6:
            free.append([off + len(b), off + n])  # same for a string that shrank in place
        w.write(off, b, f"text_{0xC00000 | off:06X}")
    if asm:  # the old half-width glyph code text.asm cut off (docs/re/hooks.md): free space in bank C3
        free += [[0x031B84, 0x031C12], [0x03276D, 0x03278C]]
    for name, lo, hi in seq:
        if any(lo <= o < hi and text[o][1] != t.decode(orig, o)[0] for o in text):
            free.append([pack_run(w, t, orig, text, name, lo, hi), hi])  # nothing points past the packed list
    repoint(w, t, orig, text, short, free, strict)
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
    run led by [id]; control codes stay."""
    tag = f"{0xC00000 | off:06X}"
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


NAME_GRID = 0x07EAC9  # LZ: name-entry grid tilemap, 20 tiles x 39 rows (tile = code - $10, $20xx; E7 = blank).
# The picked cell's tile is the stored letter (C1156C reads it from the map in RAM), so the map is the alphabet.
# Pages of 8 lines (every other tilemap row): hiragana, katakana, then 0-9 A-Z and END (kept, ー -> -).
GRID_PAGE1 = ["ABCDEFGHIJ", "KLMNOPQRST", "UVWXYZ.,'-", "abcdefghij", "klmnopqrst", "uvwxyz!?&/",
              "0123456789", "():+=#*~\"_"]


def name_grid(t, raw):
    """The grid tilemap with English on page 1, page 2 blank."""
    w = [raw[i] | raw[i + 1] << 8 for i in range(0, len(raw), 2)]
    letters = iter("".join(GRID_PAGE1))
    for i, x in enumerate(w):
        row = i // 20
        if x >> 8 != 0x20 or x & 0xFF == extract.BLANK:
            continue
        if row < 16:
            c = next(letters)
            w[i] = 0x2000 | (extract.BLANK if c == "_" else t.encode(c)[0] - 0x10)
        elif row < 32:
            w[i] = 0x2000 | extract.BLANK
        elif x & 0xFF == 0xE1:  # ー
            w[i] = 0x2000 | (t.encode("-")[0] - 0x10)
    return b"".join(x.to_bytes(2, "little") for x in w)


STATUS_MAP = 0x0D51CD  # LZ: own status/equip screen, 32 x 128 cells, tile = code - $10 (docs/re/graphics.md G12)
# rows 36-42: label right-aligned to col 15, ':' 16, value 17-18 | label to col 26, ':' 27, value 28-30
STATS = [(36, "Strength", "Weight"), (38, "Stamina", "Attack"), (40, "Agility", "Defense"), (42, "Wisdom", "Move")]
# rows 46-52: icon col 8, name 9-26 (armor rows: to 30); row 46 also LV: 27-29, weapon level 30. No labels: the
# icon gives the slot, and full names need the room (D4). The beast page draws its own (Melee..) over cols 8-14
EQUIP = [46, 48, 50, 52]
# C2 operands that place the values, names and blanks of that layout: (address, original, new). A cell is
# $A000 + (row*32 + col)*2; C26CE0 blanks LDA #n + 1 cells.
STATUS_CODE = [
    (0xC26C50, 0xA91C, 0xA922), (0xC26C5B, 0xA99C, 0xA9A2), (0xC26C66, 0xAA1C, 0xAA22),  # left values col 17
    (0xC26C71, 0xAA9C, 0xAAA2),
    (0xC26B59, 0xA930, 0xA938), (0xC26904, 0xA930, 0xA938), (0xC26C7E, 0xA9B0, 0xA9B8),  # right values col 28
    (0xC26C89, 0xAA30, 0xAA38), (0xC26C94, 0xAAB0, 0xAAB8),
    (0xC26923, 0xAA94, 0xAA90), (0xC26B6C, 0xAA94, 0xAA90),  # やせい / ちせい drawn over row 42's label: col 8
    (0xC268AB, 0xAB9A, 0xABA0),  # beast skill names col 16 (blank before each: text.asm eqcount)
    (0xC26963, 0xAB9A, 0xAB90), (0xC269FE, 0xAC1A, 0xAC10), (0xC26A71, 0xAC9A, 0xAC90),  # icons col 8
    (0xC26AE4, 0xAD1A, 0xAD10),
    (0xC26996, 0xAB9C, 0xAB92), (0xC26A33, 0xAC1C, 0xAC12), (0xC26AA6, 0xAC9C, 0xAC92),  # names col 9
    (0xC26B19, 0xAD1C, 0xAD12),
    (0xC268E4, 7, 14),  # empty skill: cols 16-30
    (0xC269CE, 7, 18), (0xC26A6B, 7, 22), (0xC26ADE, 7, 22), (0xC26B51, 7, 22),  # empty slot: icon + name to 26/30
    # the one-cell blank after a name (JSR $6CE0 -> BIT $6CE0): eqcount blanks the whole field, and on the
    # weapon row this cell would be the tilemap's "LV"
    (0xC269C6, 0xE020, 0xE02C), (0xC26A63, 0xE020, 0xE02C), (0xC26AD6, 0xE020, 0xE02C), (0xC26B49, 0xE020, 0xE02C),
    (0xC2690D, 0xABB0, 0xABB6), (0xC26913, 7, 3), (0xC269F2, 0xABB0, 0xABB6), (0xC269F8, 7, 3),  # LV: col 27
    (0xC26B96, 0xABB0, 0xABB6),
    (0xC26C3E, 0xA7A6, 0xA79E),  # どく (C26BC0) over the whole HP value from col 15, not the max HP alone
    (0xC2A471, 0x0D, 0x14),  # selected equip row's highlight (C25485 from col 8): 20 cells, through col 27
    (0xC0E056, 0x11, 0x10),  # beast-list right column (C0DFD7) col 16: "Beast Pack" (C0E109) inside the row highlight
    # member NAME (C254A9) from col 12 over the "NAME:" label, 13 cells up to the blood-type icon (col 25)
    (0xC265EB, 0x22, 0x18), (0xC2668D, 0x22, 0x18), (0xC266E4, 0x22, 0x18),
    (0xC265FA, 0x2008, 0x200D), (0xC2669C, 0x2008, 0x200D), (0xC266F3, 0x2008, 0x200D),  # LDX #8 (X8), then JSR
    (0xC254BB, 0xFC00, 0xE000),  # drawer keeps priority/flip, not the "NAME:" graphic's palette 1 (lowercase went dark)
    # BEAST/MASTER list rows (C29FEA, template C29F7C, cols 8-30): name 8 -> 13 cells, "LV" tiles col 17 -> 22,
    # LV value col 19 -> 24, loyalty bar stays at cols 27-30 (no room left for the じゅうぞく label)
    (0xC29F64, 8, 13), (0xC29FB5, 0x12, 0x1C), (0xC29FC8, 0x12, 0x08),
    (0xC2A1DB, 0x16, 0x20), (0xC2A1FF, 0x16, 0x20),
]


PARTY_MAP = 0x0D5812  # LZ: party-member view (ステータス -> pick a member), same rows; right values already at col 28,
# no icon column (names at col 13 drawn by the same shared C26 code as the own view)


def status_map(t, raw, party=False):
    """The status tilemap with English labels (STATS, EQUIP), values and icons moved to match STATUS_CODE."""
    w = [raw[i] | raw[i + 1] << 8 for i in range(0, len(raw), 2)]
    hi = w[36 * 32 + 8] & 0xFF00  # cell attribute: $00 own view, $20 party view

    def put(row, col, s):
        for i, c in enumerate(s):
            w[row * 32 + col + i] = hi | t.encode(c)[0] - 0x10

    nr = (2 if party else 28) * 32  # "NAME:" graphic (tiles $100-$103, cols 13-16): the name is drawn from col 12
    assert [x & 0x3FF for x in w[nr + 13:nr + 17]] == [0x100, 0x101, 0x102, 0x103]
    w[nr + 12:nr + 17] = [hi] * 5
    rv = 28 if party else 24
    for row, left, right in STATS:
        r = row * 32
        colon, lval, rval = w[r + 13], w[r + 14:r + 16], w[r + rv:r + rv + 3]
        w[r + 8:r + 31] = [hi] * 23
        put(row, 16 - len(left), left)
        put(row, 27 - len(right), right)
        w[r + 16], w[r + 27] = colon, colon
        w[r + 17:r + 19], w[r + 28:r + 31] = lval, rval
    for row in EQUIP:
        r = row * 32
        icon, colon, lv = (hi if party else w[r + 13]), w[r + 12], w[r + 30]
        w[r + 8:r + 31] = [hi] * 23
        w[r + 8] = icon
        if row == 46:
            put(row, 27, "LV")
            w[r + 29], w[r + 30] = colon, lv
    if party:  # item-slot placeholders (アイテムNN, rows 56+) are always drawn over: blank, so the map fits its slot
        w[56 * 32:] = [hi if 0x9A <= x & 0xFF <= 0xBA and x >> 8 == 0x20 else x for x in w[56 * 32:]]
    return b"".join(x.to_bytes(2, "little") for x in w)


def build(orig, mark=False, qa=()):
    """qa: ["ID=text", ...] overrides single entries after the script/marker overlay (width tests)."""
    text, gfx = unpack_text(orig), unpack_gfx(orig)
    gfx[MENU_FONT] = font.menu_font(gfx[MENU_FONT])
    gfx[NAME_GRID] = name_grid(Table.load(ROOT / "tbl" / "en.tbl"), gfx[NAME_GRID])
    gfx[STATUS_MAP] = status_map(Table.load(ROOT / "tbl" / "en.tbl"), gfx[STATUS_MAP])
    gfx[PARTY_MAP] = status_map(Table.load(ROOT / "tbl" / "en.tbl"), gfx[PARTY_MAP], party=True)
    maps = gfxtext.menus(orig, gfx)
    gfxtext.plain(gfx)
    gfxtext.poem(gfx, gfx[MENU_FONT], Table.load(ROOT / "tbl" / "en.tbl"))
    gfxtext.title(gfx, gfx[MENU_FONT], Table.load(ROOT / "tbl" / "en.tbl"))
    if mark:
        skip = {o for n, es in extract.units(orig).items() if n in NO_MARKER for o, *_ in es}
        t = Table.load(ROOT / "tbl" / "jp.tbl")
        # blank lines stay blank: a SEQ run's spacer lines would otherwise all become stubs and overflow it
        text = {o: (w, s if o in skip or not s.replace("{end}", "").strip() else marker(t, o, w, s))
                for o, (w, s) in text.items()}
    else:
        en = extract.load_en()  # script/*.json translations over the original units
    over = {int(k, 16) & 0x3FFFFF: v for k, v in (q.split("=", 1) for q in qa)}
    for off, s in (({} if mark else en) | over).items():
        if off not in text:
            raise SystemExit(f"{0xC00000 | off:06X} is not a text unit (re-run tools/extract.py)")
        text[off] = (text[off][0], s)
    return repack(orig, text, gfx, strict=not mark, asm=True, maps=maps)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", type=Path)
    ap.add_argument("--marker", action="store_true", help="every line -> [id] filler (build/seijuu_marker.sfc)")
    ap.add_argument("--qa", action="append", default=[], metavar="ID=TEXT", help="override one entry (en.tbl text)")
    a = ap.parse_args()
    a.out = a.out or ROOT / "build" / ("seijuu_marker.sfc" if a.marker else "seijuu_en.sfc")
    check_rom.check()
    orig = ROM.read_bytes()
    w = build(orig, a.marker, a.qa)
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
