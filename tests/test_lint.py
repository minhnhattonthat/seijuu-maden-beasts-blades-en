"""tools/lint.py catches the phase-6 review's misses: a glossary misspelling and a dropped honorific."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import lint  # noqa: E402

TERMS = [("グリフォン", "Griffin", []), ("ジミー", "Jimmy", []), ("ルクレール", "Leclerc", [])]


def run(jp, en):
    return [m for _, _, m in lint.lint({"event_CF": [{"id": "X", "jp": jp + "{end}", "en": en + "{end}"}]}, TERMS)]


def test_glossary_spelling():
    assert run("グリフォンを買う", "buy a Griffon") == ["glossary: グリフォン -> Griffin"]
    assert run("グリフォンを買う", "buy a{nl}Griffin") == []


def test_honorific_kept():
    assert run("ジミーちゃん!", "Jimmy!") == ["honorific: ジミーちゃん -> Jimmy-chan"]
    assert run("ジミーちゃん!", "Jimmy-chan!") == []
    assert run("ルクレール殿下", "His Highness Leclerc") == []  # 殿下 is a title, not 殿


def test_dialogue_width():
    assert run("あ", "x" * 36)[0].startswith("line over 35")
