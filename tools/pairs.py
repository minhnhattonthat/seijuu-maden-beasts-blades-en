"""pairs.py: reviewer input for translated batches -> work/tl/<batch>.pairs.txt

    python -X utf8 tools/pairs.py b004 [b005..]

Each entry of the batch as `>> id | JP` then `   EN` (the batch's .out.tsv English), with the +-2 neighbouring
entries of the same script file as context (`   id | JP` / `   EN` when already translated).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import batches  # noqa: E402


def pairs(b, script):
    out = {i: en for i, en in batches.read_out(b)[0] or []}
    where = {e["id"]: (name, k) for name, es in script.items() for k, e in enumerate(es)}
    rows, shown = [], set()
    for i in out:
        name, k = where[i]
        es = script[name]
        for j in range(max(0, k - 2), min(len(es), k + 3)):
            e = es[j]
            if (name, j) in shown or not batches.has_jp(e["jp"]):
                continue
            shown.add((name, j))
            jp = batches.body(e["jp"])[0].replace("{nl}", " / ")
            en = out.get(e["id"]) or e["en"].replace("{nl}", " / ")
            mark = ">>" if e["id"] in out else "  "
            rows.append(f"{mark} {e['id']} | {jp}\n   {en or '(untranslated)'}")
    return "\n".join(rows) + "\n"


def main():
    script = batches.load_script()
    for b in sys.argv[1:]:
        p = batches.TL / f"{b}.pairs.txt"
        p.write_text(pairs(b, script), encoding="utf-8")
        print(p)


if __name__ == "__main__":
    main()
