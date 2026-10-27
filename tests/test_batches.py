import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import batches  # noqa: E402


def test_cells():
    assert batches.cells("そこには2人の女性が向き合っていた。", "12") == 34  # full-width 2, 2 and 。 half-width 1
    assert batches.cells("ゴーン、ゴーン…", "12") == 14
    assert batches.cells("{var:02} ok", "12") == 11
    assert batches.cells("かう", "8") == 2


def test_wrap_and_tail():
    s = batches.to_en("event_CE", "あ{nl}い{end}", "word " * 10 + "{c0C}x")
    assert s.endswith("{nl}{end}") is False and s.endswith("x{end}")
    for ln in batches.lines(batches.body(s)[0]):
        assert batches.cells(ln, "12") <= 35
    assert s.count("{c0C}") == 1
    s = batches.to_en("worldmap", "着いた{nl}{choice:0201} はい{nl} いいえ{end}", "Here. / {choice:0201} Yes /  No")
    assert s == "Here.{nl}{choice:0201} Yes{nl} No{end}"


def test_quote_indent():
    s = batches.wrap('Rund / "My king, this must be the First Banner. All the Beast Kings have come down."', 35, "12")
    rows = s.split("{nl}")
    assert rows[0] == "Rund" and rows[1].startswith('"') and all(r.startswith(" ") for r in rows[2:])
    assert batches.wrap(" indented page", 35, "12") == " indented page"


def test_c0b_is_its_own_break():
    assert batches.wrap("Welcome!{c0B}Win big!{c0B}", 35, "12") == "Welcome!{c0B}Win big!{c0B}"
    assert batches.wrap('Mom /"Get up!"', 35, "12") == 'Mom{nl}"Get up!"'


def test_menu_padding():
    assert batches.to_en("party_menu", "あいう  {end}", "ab") == "ab   {end}"


def test_term_whole_run():
    assert not batches.term_in("ミン", "タイミング")
    assert batches.term_in("ガイアス", "ガイアスは来た")
    assert not batches.term_in("ちから", "ちから")  # hiragana rows are menu labels, not lint terms
