"""Glossary rows for the game's data names (items, beasts, enemies, skills...) from script/*.json.

    python -X utf8 tools/glossary_names.py          # print the section
    python -X utf8 tools/glossary_names.py --write  # replace it in glossary.md (between the markers)

Rerun after renaming any of these in script/. Rows whose JP already has a hand-written glossary row are left out
(the hand row wins); one JP named two ways in the data is printed as a conflict to settle by hand.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GLOSSARY = ROOT / "glossary.md"
BEGIN, END = "<!-- names:begin (tools/glossary_names.py) -->", "<!-- names:end -->"
TABLES = [("weapons", "Weapons"), ("armor", "Armor"), ("items", "Items"), ("items2", "Items 2"), ("food", "Food"),
          ("beasts", "Beasts"), ("enemies", "Enemies"), ("skills", "Skills")]


def hand_terms(text):
    """JP cells of the rows outside the generated section."""
    text = re.sub(re.escape(BEGIN) + ".*?" + re.escape(END), "", text, flags=re.S)
    return {c.strip() for ln in text.splitlines() if ln.startswith("|")
            for c in ln.strip("|").split("|")[0].split(" / ")}


def section(text):
    hand, seen, out, conflicts = hand_terms(text), {}, [BEGIN], []
    for f, title in TABLES:
        rows = []
        for e in json.loads((ROOT / "script" / f"{f}.json").read_text(encoding="utf-8")):
            jp, en = e["jp"].strip(), e["en"].strip()
            if not en or jp in hand:
                continue
            if jp in seen:
                if seen[jp] != en:
                    conflicts.append(f"{jp}: {seen[jp]} / {en} ({f})")
                continue
            seen[jp] = en
            rows.append(f"| {jp} | {en} | | | |")
        out += ["", f"### {title}", "| JP | EN | max | notes | Avoid |", "|---|---|---|---|---|", *rows]
    return "\n".join(out + ["", END]), conflicts


def main():
    text = GLOSSARY.read_text(encoding="utf-8")
    sec, conflicts = section(text)
    for c in conflicts:
        print("conflict:", c, file=sys.stderr)
    if "--write" not in sys.argv:
        print(sec)
        return
    if BEGIN not in text or END not in text:
        sys.exit(f"glossary.md lacks the {BEGIN} ... {END} markers")
    a, b = text.index(BEGIN), text.index(END) + len(END)
    GLOSSARY.write_text(text[:a] + sec + text[b:], encoding="utf-8", newline="\n")
    print(f"glossary.md: {sec.count(chr(10) + '| ') - len(TABLES)} name rows, {len(conflicts)} conflicts")


if __name__ == "__main__":
    main()
