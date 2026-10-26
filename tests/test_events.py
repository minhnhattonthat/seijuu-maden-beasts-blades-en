import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import evdis  # noqa: E402

ROM = evdis.ROM.read_bytes()
DUMMY = 0xCE3467  # unused scenario slots point here; its "events" are not code
KNOWN_BAD = {(4, 0)}  # scenario 4 event 0 calls CE757D, a message followed by plain text (dead path)


def test_every_event_walks():
    bad = []
    n = 0
    for s in range(evdis.NSCN):
        sc = evdis.scenario(ROM, s)
        if sc["base"] == DUMMY:
            continue
        seen = set()
        for i, e in enumerate(sc["events"]):
            try:
                for _ in evdis.walk(ROM, e, seen):
                    n += 1
            except evdis.Bad:
                if (s, i) not in KNOWN_BAD:
                    bad.append((s, i))
    assert not bad
    assert n > 20000


def test_opening_script():
    # E771B6: the opening cutscene (scenario 35 event 0), traced with tools/lua/evtrace.lua
    ops = [ROM[a & 0x3FFFFF] for a, _ in evdis.walk(ROM, 0xE771B6)][:6]
    assert ops == [0x44, 0x4A, 0x0A, 0x4A, 0x0A, 0x48]
