"""lint.py: read-only text lint of the merged English in script/*.json (check.py runs it; exit 1 on errors).

Same rules as `batches.py check`, applied to what ships rather than to translator output, so direct JSON edits and a
clean clone (no work/tl/) are gated too: en.tbl encodes it, control codes match the JP (layout codes {nl}/{c0C}
aside), glossary terms and Avoid spellings, no ordinal glued to a variable, honorifics kept on glossary names (D1),
dialogue lines within 35 cells. Name/menu widths are not linted here: their screens were widened (D4) and the build
plus visual QA gate them.

    python -X utf8 tools/lint.py
"""
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import batches as B  # noqa: E402
from tbl import Table  # noqa: E402


def flat(s):
    """English as read: line/page breaks and the wrap indent folded to single spaces."""
    return re.sub(r"\s+", " ", re.sub(r"\{(nl|c0C|c0B|clear)\}", " ", s))


def lint(script=None, terms=None):
    """[(file, id, message)] for every shipped English entry."""
    script = script if script is not None else B.load_script()
    terms = terms if terms is not None else B.glossary()
    names = B.names(terms)
    en_tbl = Table.load(B.ROOT / "tbl" / "en.tbl")
    errs = []
    for name, es in script.items():
        if name in B.SKIP_FILES:
            continue
        f, lim, engine = B.form(name)
        for e in es:
            en, jp, i = e["en"], B.body(e["jp"])[0], e["id"]
            if not en:
                continue
            bad = lambda m: errs.append((name, i, m))  # noqa: E731
            try:
                en_tbl.encode(en)
            except Exception as x:  # noqa: BLE001 - any unencodable character
                bad(f"not encodable with en.tbl: {x}")
            codes = Counter(c for c in B.CODE.findall(e["jp"]) if c not in B.FREE)
            mine = Counter(c for c in B.CODE.findall(en) if c not in B.FREE)
            if codes != mine:
                bad(f"codes differ: missing {dict(codes - mine)} extra {dict(mine - codes)}")
            if re.search(r"(\{(var|icall|num)[^}]*\})(st|nd|rd|th)\b", en):
                bad("ordinal suffix glued to a variable")
            text = flat(en)
            for j, t, avoid in terms:
                if j in jp and B.term_in(j, jp) and t.lower() not in text.lower():  # `in` first: ~1000 terms
                    bad(f"glossary: {j} -> {t}")
                for a in avoid:
                    if re.search(rf"\b{re.escape(a)}\b", text):
                        bad(f"glossary avoid: {a} (use {t})")
            for m in B.honorifics(jp, en, names):
                bad(m)
            if f == "dlg":
                for ln in B.lines(B.body(en)[0]):
                    if B.cells(ln, engine) > lim:
                        bad(f"line over {lim} cells ({B.cells(ln, engine)}): {ln!r}")
    return errs


def main():
    errs = lint()
    for name, i, m in errs:
        print(f"{name} {i}: {m}")
    print(f"lint: {len(errs)} errors" if errs else "lint ok")
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()
