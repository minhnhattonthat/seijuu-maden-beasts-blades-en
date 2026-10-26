"""warp.py: reach scenes from a cold boot with tools/debug/warp.lua; regenerate the savestate library.

    python -X utf8 tools/debug/warp.py SCENE [SCENE ..] [--rom ROM] [--states] [--jobs 3] [--sheet]
    python -X utf8 tools/debug/warp.py all --states          every scene -> work/states/<scene>.mss
    python -X utf8 tools/debug/warp.py --list

Each scene runs in work/qa/warp/<scene>/ (scene_<name>.png is the proof shot) and must log "SCENE OK";
exit 1 if any scene fails. --states saves work/states/<scene>.mss at the end of the run (cold boot, so after
code/font/graphics changes this is the one command that refreshes every state).
"""
import argparse
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
from skill import SKILL  # noqa: E402

SCENES = ROOT / "tools" / "debug" / "scenes.lua"
DEFAULT_ROM = ROOT / "rom" / "Seijuu Maden Beasts & Blades (Japan).sfc"


def scenes():
    """name -> frame budget, in file order (a scene starts at `name = {` at two-space indent)."""
    text = re.sub(r"--[^\n]*", "", SCENES.read_text(encoding="utf-8"))
    heads = list(re.finditer(r"^  ([a-z0-9_]+)\s*=\s*\{", text, re.M))
    out = {}
    for i, m in enumerate(heads):
        body = text[m.end():heads[i + 1].start() if i + 1 < len(heads) else len(text)]
        f = re.search(r"frames\s*=\s*(\d+)", body)
        if not f:
            sys.exit(f"scenes.lua: {m[1]} has no frames")
        out[m[1]] = int(f[1])
    return out


def run(name, frames, rom, states, sheet, lua=()):
    out = ROOT / "work" / "qa" / "warp" / name
    cmd = [sys.executable, "-X", "utf8", str(Path(SKILL) / "scripts" / "emu.py"), str(rom), "--out", str(out),
           "--script", str(SCENES), "--script", str(ROOT / "tools" / "debug" / "warp.lua"),
           *[x for f in lua for x in ("--script", str(Path(f).resolve()))],
           "--var", f"SCENE='{name}'", "--frames", str(frames), "--timeout", "900"]
    if states:
        cmd += ["--state-out", str(ROOT / "work" / "states" / f"{name}.mss")]
    if sheet:
        cmd += ["--shot-every", "300", "--sheet"]
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    log = (out / "log.txt").read_text(encoding="utf-8", errors="replace") if (out / "log.txt").exists() else ""
    ok = p.returncode == 0 and f"SCENE OK {name} " in log
    out_lines = (p.stdout + p.stderr).strip().splitlines()
    last = ([l for l in log.splitlines() if "SCENE" in l] or [l for l in out_lines if "rror" in l][-1:]
            or out_lines[-1:])
    return name, ok, (last[-1] if last else f"exit {p.returncode}"), out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("names", nargs="*")
    ap.add_argument("--rom", default=str(DEFAULT_ROM))
    ap.add_argument("--states", action="store_true")
    ap.add_argument("--sheet", action="store_true")
    ap.add_argument("--jobs", type=int, default=3)
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--lua", action="append", default=[], help="extra probe script(s), e.g. tools/lua/textlog.lua")
    a = ap.parse_args()
    sc = scenes()
    if a.list or not a.names:
        for n, f in sc.items():
            print(f"{n:24} {f}")
        return 0
    names = list(sc) if a.names == ["all"] else a.names
    for n in names:
        if n not in sc:
            sys.exit(f"unknown scene {n} (see --list)")
    fails = 0
    with ThreadPoolExecutor(a.jobs) as ex:
        for name, ok, msg, out in ex.map(lambda n: run(n, sc[n], a.rom, a.states, a.sheet, a.lua), names):
            fails += not ok
            print(f"{'ok  ' if ok else 'FAIL'} {name:24} {msg}  {out / f'scene_{name}.png'}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
