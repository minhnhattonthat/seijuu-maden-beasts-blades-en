"""batches.py: script/*.json -> translator batches (work/tl/bNNN.tsv), check their output, merge it back.

    python -X utf8 tools/batches.py split [--files a,b] [--chars 3500]   new batches for untranslated entries
    python -X utf8 tools/batches.py check b001 [b002..]                   validate work/tl/<b>.out.tsv (exit 1 on errors)
    python -X utf8 tools/batches.py merge b001 [b002..]                   check, then write `en` into script/*.json
    python -X utf8 tools/batches.py fit "English text" [--file event_CE]  show the wrapped lines and widths

Batch TSV: id<TAB>speaker<TAB>form<TAB>limit<TAB>jp, with {nl} shown as " / " and the trailing {end} tail cut.
Output TSV: id<TAB>English. " / " forces a line break; dialogue (form dlg) is word-wrapped to its limit by merge,
so translators don't place {nl} themselves. Every code except {nl}/{c0C} must appear as often as in the JP.
Widths: docs/re/windows.md. A 12 px engine line counts a JP full-width code as 2 cells and each English letter as 1;
8x8 menu text counts every code as 1 cell.
"""
import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tbl import Table  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
SCRIPT, TL, BUILD = ROOT / "script", ROOT / "work" / "tl", ROOT / "build"
GLOSSARY = ROOT / "glossary.md"
CODE = re.compile(r"\{\w+(?::[0-9A-Fa-f]*)?\}|\[[0-9A-F]{2}\]")
TAIL = re.compile(r"((?:\{nl\})*\{end\})?$")
FREE = {"{nl}", "{c0C}"}  # page layout: English may break differently
SKIP_FILES = {"name_grid"}  # layout codes (build.name_grid), not lines

# file -> (form, limit, engine). limit "orig" = the JP entry's own cell count (unmeasured 8x8 text, padded slots)
DLG = ("dlg", 35, "12")
FORMS = {
    "prologue": ("narration", 40, "12"), "intro": ("narration", 40, "12"), "endings": ("narration", 40, "12"),
    "credits": ("narration", 40, "12"), "copy_warning": ("narration", 40, "12"),
    # item names: the battle list is the tightest screen (11); shop wraps, equip 18, beast skills 15, bag 19
    "weapons": ("name", 11, "8"), "armor": ("name", 11, "8"), "food": ("name", 11, "8"), "items": ("name", 11, "8"),
    "items2": ("name", 11, "8"), "skills": ("name", 11, "8"),
    "generals": ("name", 8, "8"), "soldiers": ("name", 8, "8"), "beasts": ("name", 8, "8"),
    "people": ("name", 8, "8"), "enemies": ("name", 8, "8"),
    "menus": ("menu", 8, "8"), "buildings": ("menu", 8, "8"), "item_types": ("menu", 14, "8"),
    "locations": ("name", 16, "12"), "ranks": ("name", 20, "12"),
    "party_menu": ("menu", "orig", "8"), "effects": ("menu", "orig", "8"), "effects2": ("menu", "orig", "8"),
    "ranch_status": ("menu", "orig", "8"), "camp_menu": ("menu", "orig", "8"), "item_menu": ("menu", "orig", "8"),
    "name_entry": ("menu", "orig", "12"),
}


def form(name):
    return FORMS.get(name, DLG)


JP = Table.load(ROOT / "tbl" / "jp.tbl")


def cells(s, engine):
    """Display width of one line in cells; codes count 0 except names/numbers drawn in their place."""
    n = 0
    for tok in re.findall(CODE.pattern + r"|.", s):
        if tok.startswith("{var") or tok.startswith("{icall"):
            n += 16 if tok == "{icall:1D947E}" else 8  # 1D947E: a location name (locations.json), else a member name
        elif tok.startswith("{num"):
            n += int(tok[5:7], 16) & 0x0F or 5  # low nibble = digits; 0 = not pinned down, assume 5
        elif tok.startswith("{"):
            pass
        elif engine == "12" and not tok.isascii() and len(tok) == 1:
            n += 2 if JP.encode(tok)[0] >= 0x50 else 1  # full-width cell; 「」、。… are half-width codes
        else:
            n += 1
    return n


def body(jp):
    """(body, tail): the JP without its trailing {nl}..{end}, which merge re-appends."""
    m = TAIL.search(jp)
    return jp[:m.start()], m.group(0)


def lines(s):
    return re.split(r"\{nl\}|\{c0C\}|\{c0B\}|\{clear\}", s)


def wrap(text, limit, engine):
    """Word-wrap each page segment of English dialogue to `limit` cells; ' / ' is a forced break."""
    out = []
    for page in text.split("{c0C}"):
        segs = []
        # {c0B} (shop text) is the translator's own line break; ' /"' (no space) is a forced break too
        for seg in re.split(r" / ?|(?<=\{c0B\})", page):
            # a quote's (or an indented page's) continuation lines sit one cell in, under the text, as in the JP
            indent = " " if seg[:1] in ('"', " ") else ""
            words = seg.split(" ")
            line = words.pop(0)  # "" when the segment is indented: the next word then keeps its space
            for word in words:
                cand = line + " " + word
                if line.strip() and cells(cand, engine) > limit:
                    segs.append(line)
                    line = indent + word
                else:
                    line = cand
            segs.append(line)
        out.append("{nl}".join(segs).replace("{c0B}{nl}", "{c0B}"))  # {c0B} breaks the line itself
    return "{c0C}".join(out)


def choice_split(text):
    """Text before a {choice} gets wrapped; the option lines after it stay as written."""
    i = text.find("{choice")
    return (text, "") if i < 0 else (text[:i], text[i:])


def to_en(name, jp, en):
    """Translator English -> the script `en` string (wrapped, breaks as {nl}, the JP tail re-appended)."""
    f, limit, engine = form(name)
    b, tail = body(jp)
    if f == "dlg":
        head, opts = choice_split(en)
        if opts and head.endswith(" / "):
            head, opts = head[:-3], "{nl}" + opts
        s = wrap(head, limit, engine) + opts.replace(" / ", "{nl}")
    else:
        s = en.replace(" / ", "{nl}")
    if f == "menu" and b.endswith(" "):  # space-padded slot: pad each line to the JP's width so old text is cleared
        lim = limit_of(name, jp)
        s = "{nl}".join(x + " " * max(0, lim - cells(x, engine)) for x in s.split("{nl}"))
    return s + tail


def limit_of(name, jp):
    f, limit, engine = form(name)
    if limit == "orig":
        return max(cells(x, engine) for x in lines(body(jp)[0]))
    return limit


def has_jp(s):
    # punctuation-only lines (…… 「!?」 、) count too: their JP codes draw garbage in the English font
    return bool(re.search(r"[…、。「」『』぀-ヿ一-鿿！-～]", CODE.sub("", s)))


def load_script():
    return {f.stem: json.loads(f.read_text(encoding="utf-8")) for f in sorted(SCRIPT.glob("*.json"))}


def glossary():
    """[(jp, en)] from every glossary table row; 'A / B' cells pair up."""
    rows = []
    for line in GLOSSARY.read_text(encoding="utf-8").splitlines():
        cols = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cols) < 2 or not line.startswith("|") or cols[0] in ("JP", "") or set(cols[0]) <= set("-"):
            continue
        jps, ens = cols[0].split(" / "), cols[1].split(" / ")
        avoid = [a.strip() for a in cols[4].split(",") if a.strip()] if len(cols) > 4 else []
        for j, e in zip(jps, ens) if len(jps) == len(ens) else [(cols[0], cols[1])]:
            rows.append((j, e, avoid))
    return rows


def kind(ch):
    o = ord(ch)
    return "k" if 0x30A0 <= o <= 0x30FF else "h" if 0x3040 <= o <= 0x309F else "c" if 0x4E00 <= o <= 0x9FFF else ""


def term_in(term, jp):
    """Whole-run match: the term isn't glued to more of the same script (ミン inside タイミング)."""
    if not any(kind(c) in "kc" and kind(c) for c in term):  # hiragana-only rows are menu labels, not lint terms
        return False
    for m in re.finditer(re.escape(term), jp):
        a, b = jp[m.start() - 1] if m.start() else "", jp[m.end()] if m.end() < len(jp) else ""
        if not (a and kind(a) == kind(term[0]) and kind(a)) and not (b and kind(b) == kind(term[-1]) and kind(b)):
            return True
    return False


def split(files, chars):
    TL.mkdir(parents=True, exist_ok=True)
    BUILD.mkdir(exist_ok=True)
    queued = set()
    nums = [0]
    for p in TL.glob("b[0-9][0-9][0-9].tsv"):
        nums.append(int(p.stem[1:]))
        queued |= {ln.split("\t", 1)[0] for ln in p.read_text(encoding="utf-8").splitlines() if ln}
    n, terms = max(nums), glossary()
    script = load_script()
    for name in files or script:
        if name in SKIP_FILES:
            continue
        f, _, _ = form(name)
        todo = [e for e in script[name] if not e["en"] and e["id"] not in queued and has_jp(e["jp"])]
        while todo:
            batch, size = [], 0
            while todo and (not batch or size + len(todo[0]["jp"]) <= chars):
                e = todo.pop(0)
                batch.append(e)
                size += len(e["jp"])
            n += 1
            b = f"b{n:03d}"
            out = TL / f"{b}.tsv"
            if out.exists():
                sys.exit(f"{out} exists: refusing to overwrite")
            rows = [f"{e['id']}\t\t{f}\t{limit_of(name, e['jp'])}ch\t{body(e['jp'])[0].replace('{nl}', ' / ')}"
                    for e in batch]
            out.write_text("\n".join(rows) + "\n", encoding="utf-8")
            hit = [f"{j}\t{e}" + (f"\t(avoid: {', '.join(a)})" if a else "")
                   for j, e, a in terms if any(term_in(j, x["jp"]) for x in batch)]
            (BUILD / f"terms_{b}.txt").write_text("\n".join(hit) + ("\n" if hit else ""), encoding="utf-8")
            print(f"{b}: {name} {len(batch)} entries, {size} JP chars, {len(hit)} terms")


def index():
    """id -> (file name, entry)."""
    return {e["id"]: (name, e) for name, es in load_script().items() for e in es}


def read_out(b):
    p = TL / f"{b}.out.tsv"
    if not p.exists():
        return None, [f"{p.name} missing"]
    out, errs = [], []
    for k, ln in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
        if not ln.strip():
            continue
        if ln.count("\t") != 1:
            errs.append(f"line {k}: want exactly one tab (id<TAB>English)")
            continue
        out.append(tuple(ln.split("\t")))
    return out, errs


def check(b, idx=None, en_tbl=None, terms=None):
    """[(id, message)] errors for one batch, plus warnings printed but not counted."""
    idx = idx or index()
    en_tbl = en_tbl or Table.load(ROOT / "tbl" / "en.tbl")
    terms = terms if terms is not None else glossary()
    want = [ln.split("\t", 1)[0] for ln in (TL / f"{b}.tsv").read_text(encoding="utf-8").splitlines() if ln]
    out, errs = read_out(b)
    errs = [("-", m) for m in errs]
    if out is None:
        return errs, []
    got = [i for i, _ in out]
    for i, c in (Counter(got) - Counter(want)).items():
        errs.append((i, "extra or duplicate id" if c else ""))
    for i in set(want) - set(got):
        errs.append((i, "missing"))
    warns = []
    for i, en in out:
        if i not in idx:
            continue
        name, e = idx[i]
        jp = body(e["jp"])[0]
        f, _, engine = form(name)
        lim = limit_of(name, e["jp"])
        if not en.strip():
            errs.append((i, "empty English"))
            continue
        if not en.isascii() or "\\u" in en or any(ord(c) < 32 for c in en):
            errs.append((i, f"non-ASCII / control character: {en!r}"))
            continue
        codes = Counter(c for c in CODE.findall(jp) if c not in FREE)
        mine = Counter(c for c in CODE.findall(en) if c not in FREE)
        if codes != mine:
            errs.append((i, f"codes differ: missing {dict(codes - mine)} extra {dict(mine - codes)}"))
        s = to_en(name, e["jp"], en)
        try:
            en_tbl.encode(s)
        except Exception as x:  # noqa: BLE001 - any unencodable character
            errs.append((i, f"not encodable with en.tbl: {x}"))
        for ln in lines(body(s)[0]):
            if cells(ln, engine) > lim:
                msg = f"line over {lim} cells ({cells(ln, engine)}): {ln!r}"
                # names/menus: full English stays (D4); the screen gets widened (engine work), `long` lists them
                (warns if f in ("name", "menu") else errs).append((i, ("LONG " if f in ("name", "menu") else "") + msg))
        if f == "dlg":
            for pg in body(s)[0].split("{c0C}"):
                if pg.count("{nl}") >= 6:  # the JP itself often runs name + 3 lines; the 4th+ waits for a button
                    warns.append((i, f"page of {pg.count('{nl}') + 1} lines (box shows 3, the rest scrolls)"))
        if re.search(r"(\{(var|icall|num)[^}]*\})(st|nd|rd|th)\b", en):
            errs.append((i, "ordinal suffix glued to a variable"))
        for j, t, avoid in terms:
            if term_in(j, jp) and t.lower() not in en.lower():  # "The Supreme God" at a sentence start is fine
                errs.append((i, f"glossary: {j} -> {t}"))
            for a in avoid:
                if re.search(rf"\b{re.escape(a)}\b", en):
                    errs.append((i, f"glossary avoid: {a} (use {t})"))
    return errs, warns


def run_check(bs):
    idx, en_tbl, terms = index(), Table.load(ROOT / "tbl" / "en.tbl"), glossary()
    bad = 0
    for b in bs:
        errs, warns = check(b, idx, en_tbl, terms)
        for i, m in warns:
            print(f"{b} {i}: warning: {m}")
        for i, m in errs:
            print(f"{b} {i}: {m}")
        print(f"{b}: {'OK' if not errs else f'{len(errs)} errors'}")
        bad += bool(errs)
    return bad


def merge(bs):
    if run_check(bs):
        sys.exit("merge refused: fix the errors above")
    script = load_script()
    where = {e["id"]: (name, k) for name, es in script.items() for k, e in enumerate(es)}
    touched = set()
    for b in bs:
        for i, en in read_out(b)[0]:
            name, k = where[i]
            script[name][k]["en"] = to_en(name, script[name][k]["jp"], en)
            touched.add(name)
    for name in touched:
        (SCRIPT / f"{name}.json").write_text(
            "[\n" + ",\n".join(json.dumps(r, ensure_ascii=False) for r in script[name]) + "\n]\n", encoding="utf-8",
            newline="\n")
    print(f"merged {', '.join(bs)} into {', '.join(sorted(touched))}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("split")
    s.add_argument("--files", default="")
    s.add_argument("--chars", type=int, default=3500)
    for c in ("check", "merge"):
        sub.add_parser(c).add_argument("batches", nargs="+")
    ft = sub.add_parser("fit")
    ft.add_argument("text")
    ft.add_argument("--file", default="event_CE")
    a = ap.parse_args()
    if a.cmd == "split":
        split([x for x in a.files.split(",") if x], a.chars)
    elif a.cmd == "check":
        sys.exit(1 if run_check(a.batches) else 0)
    elif a.cmd == "merge":
        merge(a.batches)
    else:
        f, limit, engine = form(a.file)
        s = wrap(a.text, limit, engine) if f == "dlg" else a.text.replace(" / ", "{nl}")
        for ln in lines(s):
            print(f"{cells(ln, engine):3} {'!' if cells(ln, engine) > (limit if limit != 'orig' else 99) else ' '} {ln}")


if __name__ == "__main__":
    main()
