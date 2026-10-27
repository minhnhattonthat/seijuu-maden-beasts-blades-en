"""extract.py: every text unit in the ROM -> script/*.json, and back (build.py overlays the `en` fields).

Units (addresses CPU; docs/re/text.md §Where strings come from):
  - event: every string an event-script message op (0A/0C) points at, walking all scenarios (tools/evdis.py)
    plus the common event table CE0128 (recruit lines etc.) -> script/event_<bank>.json
  - RUNS: contiguous {end}-terminated strings read by code (menus, shops, prologue/ending scrolls, credits);
    a lone {end} (empty string = list terminator or spacer) is structure, not an entry
  - PTRS: 16-bit pointer tables into their own bank; a string ends at {end} or at the next pointer
    (battle shouts are packed without terminators)
  - FIELDS: fixed-width 00-padded name fields in data records (items, skills, beasts), width = longest name
Each entry: {"id": "C1621D", "jp": ..., "en": ""} (+ "w" = slot bytes for fields and pointer spans).

    python -X utf8 tools/extract.py            write script/*.json (keeps existing "en")
    python -X utf8 tools/extract.py --gaps     list text-like regions no unit covers (docs/re/not_text.tsv excluded)
"""
import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import evdis  # noqa: E402
from tbl import Table  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
ROM = evdis.ROM
SCRIPT = ROOT / "script"
NOT_TEXT = ROOT / "docs" / "re" / "not_text.tsv"
DUMMY = 0xCE3467  # unused scenario slots point here (tests/test_events.py)
EVENT_TABLES = [(0xCE0128, 247)]  # common events (recruit/hire lines), not in any scenario header

# name, first string, end (exclusive). Boundaries read with tools/textdump.py.
RUNS = [
    ("worldmap", 0xC0BC25, 0xC0BF8F),       # world-map / camp / auto-battle messages, retreat lines
    ("ranch_status", 0xC0E4C8, 0xC0E4F7),   # beast training status words (menu font)
    ("name_entry", 0xC11A9C, 0xC11AC8),
    ("item_menu", 0xC14031, 0xC14094),
    ("shop", 0xC14D73, 0xC15DA5),           # building menus: menu-script VM (C0C4E7, op table C0BF8F)
    ("copy_warning", 0xC15FA6, 0xC15FF1),   # copier warning screen, centred lines (LDA #$5FA6 at C15F58)
    ("prologue", 0xC1621D, 0xC1659F),       # creation myth scroll (C16096)
    ("intro", 0xC167F7, 0xC169F0),          # bell scene scroll
    ("endings", 0xC1704E, 0xC17C03),        # ending scrolls, pointer table C17044
    ("credits", 0xC17C03, 0xC17FC9),
    ("name_grid", 0xC184C0, 0xC18585),      # name-entry kana grid ([FE] = layout codes)
    ("party_menu", 0xC25320, 0xC253FD),     # 17-byte space-padded prompts
    ("battle_result", 0xC34B9D, 0xC34C60),  # dungeon-battle victory/level-up/defeat (split lo/hi immediates)
    ("party_menu", 0xC26940, 0xC2695C),     # status screen: ---, やせい, formation ranges (C26D31)
    ("party_menu", 0xC26BA0, 0xC26BCA),     # status screen: human labels drawn back over them, どく, -----
    ("camp_menu", 0xC38E0A, 0xC38E1F),
    ("locations", 0xC60C00, 0xC60E44),      # location list (index = scenario for the first ones)
    ("ranks", 0xC60E5A, 0xC60ECA),          # 第N聖獣王 (pointer table C60E44)
    ("ranks", 0xC60EE0, 0xC60F50),          # 第N魔獣王 (pointer table C60ECA)
    ("item_types", 0xC6301E, 0xC630C3),     # weapon types, 15-byte slots
    ("item_types", 0xC630CB, 0xC63107),     # armor types (pointer table C630C3)
    ("item_types", 0xC6310B, 0xC63129),
    ("effects", 0xC631E9, 0xC634E6),        # item/skill effect lines, 15-byte slots
    ("effects2", 0xC63570, 0xC6368D),
    ("buildings", 0xCE3419, 0xCE3467),      # town-menu building names
]
# RUNS whose lines are read in order (no pointer per line): build.py packs them as a list of {call} stubs
SEQ = {"copy_warning", "prologue", "intro", "endings", "credits"}
# menu windows drawn as BG tiles from the 8x8 font (tools/tilescan.py): record = <w> <h> then w*h words
# (tile = code - $10, high byte $20; $E7 = blank cell), one row per item. Opened by menu-script op 10 lo hi
# (C1 scripts C14094-C14C18); build.py moves that pointer when a record grows.
# Two more are loaded by code: C0BAF7 (world-map info box, LDX #$BAF7 at C0A299; its [00] cells are where the
# numbers go) and C0C30D (yes/no, LDA #$C30D at C0C75B).
MENUS = [0xC14C19, 0xC14C39, 0xC14C4D, 0xC14C63, 0xC14C85, 0xC14CA7, 0xC14CBB, 0xC14CC9, 0xC14CEB, 0xC14D29,
         0xC14D37, 0xC14D4B, 0xC14D5D, 0xC0BAF7, 0xC0C30D]
MENU_SET = {a & 0x3FFFFF for a in MENUS}
MENU_ATTR, BLANK = 0x20, 0xE7
MENU_TILE = {0x10: BLANK, 0x00: 0x00}  # text code -> tile where not code - $10: space is the blank cell (tile 0
                                       # isn't blank in this font); [00] = tile 0, the number cells of C0BAF7
# name, single {end}-terminated strings (built-in event scripts in C0: 0A 01 lo hi FF + inline text)
STRINGS = [
    ("system", [0xC03A64, 0xC03A71, 0xC03A78, 0xC03AA3, 0xC03ADC, 0xC03AEE, 0xC03B01, 0xC03B11, 0xC03B23,
                0xC042F1, 0xC044E9]),
    # 8x8 printer (C32912) texts behind a {call} wrapper: C2A0D5 (no beasts), C2A52A (see the other members)
    ("party_menu", [0xC2A0DB, 0xC2A530]),
]
# name, table, pointer count (pointers into the table's bank), end of the last string if packed
PTRS = [
    ("retreat", 0xC50ABE, 11, None),        # monster retreat lines
    ("battle", 0xC57CD8, 21, 0xC57E03),     # battle results, capture, shouts (packed, no terminators)
    ("battle_idle", 0xC57E03, 7, None),     # "<name> is praying" etc.
]
# name, first field, stride, count
FIELDS = [
    ("weapons", 0xC60F50, 19, 183),
    ("armor", 0xC61CE5, 18, 108),
    ("food", 0xC62489, 12, 15),
    ("items", 0xC6253D, 18, 96),
    ("items2", 0xC62BFD, 15, 69),
    ("skills", 0xC6368D, 13, 153),
    ("beasts", 0xC6686C, 37, 85),
    ("people", 0xC674AE, 29, 12),           # named characters (ガイアス...), アークマスター
    ("enemies", 0xC6760C, 31, 31),          # human enemy classes
    ("enemies", 0xC679CF, 33, 17),          # monster bosses
]


def table():
    return Table.load(ROOT / "tbl" / "jp.tbl")


def cpu(off):
    return f"{0xC00000 | off:06X}"


def event_strings(rom, t):
    """{offset: text} for every 0A/0C message string, scenario walk + common tables."""
    return {p: t.decode(rom, p)[0] for p in event_sites(rom)}


def event_sites(rom):
    """{string offset: [offsets of the 0A/0C ops pointing at it]} (in walk order)."""
    out = {}

    def take(entries):
        seen = set()
        for e in entries:
            try:
                for a, _ in evdis.walk(rom, e, seen):
                    o = a & 0x3FFFFF
                    if rom[o] in (0x0A, 0x0C):
                        p = (a & 0x3F0000) | rom[o + 2] | rom[o + 3] << 8
                        if o not in out.setdefault(p, []):
                            out[p].append(o)
            except evdis.Bad:
                pass  # known dead path (tests/test_events.py KNOWN_BAD); its earlier messages are kept

    for s in range(evdis.NSCN):
        sc = evdis.scenario(rom, s)
        if sc["base"] != DUMMY:
            take(sc["events"])
    for tab, n in EVENT_TABLES:
        o = tab & 0x3FFFFF
        take([(tab & 0xFF0000) | rom[o + 2 * i] | rom[o + 2 * i + 1] << 8 for i in range(n)])
    return out


def units(rom, t=None):
    """{unit name: [(offset, slot length or None for {end}-terminated, text)]}; first unit claiming an offset wins."""
    t = t or table()
    out, taken = {}, set()

    def add(name, off, w, s):
        if off not in taken:
            taken.add(off)
            out.setdefault(name, []).append((off, w, s))

    ev = event_strings(rom, t)
    for off in sorted(ev):
        add(f"event_{cpu(off)[:2]}", off, None, ev[off])
    for name, lo, hi in RUNS:
        p, e = lo & 0x3FFFFF, hi & 0x3FFFFF
        while p < e:
            s, n = t.decode(rom, p)
            if s != "{end}":
                add(name, p, None, s)
            p += n
    for name, addrs in STRINGS:
        for a in addrs:
            add(name, a & 0x3FFFFF, None, t.decode(rom, a & 0x3FFFFF)[0])
    for name, tab, n, end in PTRS:
        o, bank = tab & 0x3FFFFF, tab & 0x3F0000
        ptrs = sorted({bank | rom[o + 2 * i] | rom[o + 2 * i + 1] << 8 for i in range(n)})
        for i, p in enumerate(ptrs):
            s, used = t.decode(rom, p)
            gap = ptrs[i + 1] - p if i + 1 < len(ptrs) else ((end & 0x3FFFFF) - p if end else used)
            if gap < used:  # packed: no terminator before the next string
                add(name, p, gap, t.decode(rom, p, length=gap)[0])
            else:
                add(name, p, None, s)
    for a in MENUS:
        s, n = menu_text(t, rom, a & 0x3FFFFF)
        add("menus", a & 0x3FFFFF, n, s)
    for name, lo, stride, n in FIELDS:
        offs = [(lo & 0x3FFFFF) + stride * i for i in range(n)]
        names = [rom[o:o + stride].split(b"\0")[0] for o in offs]
        w = max(map(len, names))
        for o, b in zip(offs, names):
            if b:
                add(name, o, w, t.decode(b, 0, length=len(b))[0])
    return out


def field_offsets():
    """Offsets of every FIELDS slot (fixed-width records: no {call}, must fit)."""
    return {(lo & 0x3FFFFF) + stride * i for _, lo, stride, n in FIELDS for i in range(n)}


def encode(t, s, w, off=None):
    """Bytes for an entry; fields and spans are 00-padded to their slot, a menu record is rebuilt (its width =
    the longest row, so it may outgrow its slot)."""
    if off in MENU_SET:
        rows = [t.encode(r) for r in s.split("{nl}")]
        wd = max(max(map(len, rows)), (w - 2) // (2 * len(rows)) if w else 0)  # never narrower than the original
        return bytes([wd, len(rows)]) + b"".join(
            bytes(x for c in r.ljust(wd, b"\xf7") for x in (MENU_TILE.get(c, c - 0x10), MENU_ATTR)) for r in rows)
    b = t.encode(s)
    return b if w is None else b + bytes(max(0, w - len(b)))


def menu_text(t, rom, off):
    """A menu record as its rows joined by {nl}; trailing blank cells dropped, inner ones kept as [F7]."""
    w, h = rom[off], rom[off + 1]
    cells = [rom[off + 2 + 2 * i] for i in range(w * h)]
    rows = ["".join("[F7]" if c == BLANK else "[00]" if c == 0 else t.dec[bytes([c + 0x10])]
                    for c in cells[r * w:(r + 1) * w]) for r in range(h)]
    return "{nl}".join(re.sub(r"(\[F7\])+$", "", r) for r in rows), 2 + 2 * w * h


def slot(rom, t, off, w):
    return t.decode(rom, off)[1] if w is None else w


def load_en():
    """{offset: en} from script/*.json, non-empty translations only."""
    out = {}
    for f in sorted(SCRIPT.glob("*.json")):
        for e in json.loads(f.read_text(encoding="utf-8")):
            if e.get("en"):
                out[int(e["id"], 16) & 0x3FFFFF] = e["en"]
    return out


def write(rom):
    old = load_en()
    SCRIPT.mkdir(exist_ok=True)
    n = 0
    for name, entries in units(rom).items():
        rows = []
        for off, w, s in entries:
            r = {"id": cpu(off), "jp": s, "en": old.get(off, "")}
            if w is not None:
                r["w"] = w
            rows.append(r)
        n += len(rows)
        (SCRIPT / f"{name}.json").write_text(
            "[\n" + ",\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n]\n", encoding="utf-8")
    print(f"script/: {n} entries")


CLEAN = re.compile(r"\{c0[1-9B]|\{var:[^0]|\{num|\{choice:[^0]")


def gaps(rom, t=None, nmin=3):
    """Text-like regions (textscan hits, >= nmin clean strings within 64 bytes) that no unit covers."""
    import textscan
    t = t or table()
    cov = set()
    for entries in units(rom, t).values():
        for off, w, _ in entries:
            cov.update(range(off, off + slot(rom, t, off, w)))
    hits = [h for h in textscan.scan(rom, t, 3)
            if cov.isdisjoint(range(h[0], h[0] + h[1])) and not CLEAN.search(h[2])]
    regions = []
    for h in hits:
        if regions and h[0] - (regions[-1][-1][0] + regions[-1][-1][1]) <= 64:
            regions[-1].append(h)
        else:
            regions.append([h])
    return [(r[0][0], r[-1][0] + r[-1][1], r) for r in regions if len(r) >= nmin]


def not_text():
    """{start offset: reason} of regions checked by eye and found not to be text."""
    out = {}
    for line in NOT_TEXT.read_text(encoding="utf-8").splitlines():
        if line and not line.startswith("#"):
            a, reason = line.split("\t", 1)
            out[int(a, 16) & 0x3FFFFF] = reason
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--gaps", action="store_true")
    ap.add_argument("--all", action="store_true", help="with --gaps: include regions in not_text.tsv")
    a = ap.parse_args()
    rom = ROM.read_bytes()
    if a.gaps:
        skip = {} if a.all else not_text()
        for lo, hi, r in gaps(rom):
            if lo not in skip:
                print(f"{cpu(lo)}\t{cpu(hi)} n={len(r)} | {r[0][2][:30]} | {r[len(r) // 2][2][:30]}")
        return
    write(rom)


if __name__ == "__main__":
    main()
