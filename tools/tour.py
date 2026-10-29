"""tour.py: the QA screen tour. Every warp scene on a build -> work/qa/tour/<scene>/ (final.png + contact sheets of
the frames after the warp arrived; boot-path scenes keep the whole boot), the printed-text coverage check, then the
visual-QA manifest re-init (docs/visual-qa-brief.md; verdicts in work/qa/verdicts/).

    python -X utf8 tools/tour.py [--rom build/seijuu_en.sfc] [--jobs 2] [scene ...]
"""
import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from skill import SKILL  # noqa: E402

PY = [sys.executable, "-X", "utf8"]
WARP, TOUR = ROOT / "work" / "qa" / "warp", ROOT / "work" / "qa" / "tour"
BOOT_END = 2600  # scenes that arrive before this are on the boot path (intro .. name entry): sheet the whole run


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("scenes", nargs="*", default=["all"])
    ap.add_argument("--rom", default=str(ROOT / "build" / "seijuu_en.sfc"))
    ap.add_argument("--jobs", default="2")  # 4 ran the host out of memory
    a = ap.parse_args()
    r = subprocess.run(PY + [str(ROOT / "tools" / "debug" / "warp.py"), *a.scenes, "--rom", a.rom, "--jobs", a.jobs,
                             "--sheet", "--lua", str(ROOT / "tools" / "lua" / "textlog.lua")], cwd=ROOT)
    fails = r.returncode
    if a.scenes == ["all"]:
        shutil.rmtree(TOUR, ignore_errors=True)  # drops scenes that left the list
    for line in subprocess.run(PY + [str(ROOT / "tools" / "debug" / "warp.py"), "--list"], cwd=ROOT,
                               capture_output=True, text=True).stdout.splitlines():
        name = line.split()[0]
        src, log = WARP / name, WARP / name / "log.txt"
        if a.scenes != ["all"] and name not in a.scenes or not log.exists():
            continue
        m = re.search(rf"SCENE OK {name} f(\d+)", log.read_text(encoding="utf-8", errors="replace"))
        if not m:
            print(f"tour: {name} did not arrive")
            fails = 1
            continue
        arrived = int(m[1])
        dst = TOUR / name
        shutil.rmtree(dst, ignore_errors=True)
        dst.mkdir(parents=True)
        jump = re.search(r"^f(\d+) jump ", log.read_text(encoding="utf-8", errors="replace"), re.M)
        # a mid-event jump (msg, war_talk) plays its pages during `after`, before the arrival: sheet from the jump
        lo = 0 if arrived < BOOT_END else int(jump[1]) if jump else arrived - 300
        subprocess.run(PY + [str(Path(SKILL) / "scripts" / "sheet.py"), str(src), "--from", str(lo),
                             "--out", str(dst / "sheet.png")], cwd=ROOT, check=True, capture_output=True)
        shutil.copy(src / "final.png", dst / "final.png")
    if subprocess.run(PY + [str(ROOT / "tools" / "textlog_check.py")], cwd=ROOT).returncode:
        fails = 1
    manifest = ROOT / "work" / "qa" / "manifest.tsv"
    # init re-hashes the kept ids, so a sheet whose pixels changed loses its old verdict (never unlink the manifest:
    # that resets every "changed" time and old-build verdicts would pass the gate)
    subprocess.run(PY + [str(Path(SKILL) / "scripts" / "qa_gate.py"), "init", str(manifest), str(TOUR),
                         "--glob", "*.png"], cwd=ROOT, check=True)
    if a.scenes == ["all"]:  # a full tour replaces the sheet set: drop ids whose sheet is gone
        rows = manifest.read_text(encoding="utf-8").splitlines()
        manifest.write_text("".join(r + "\n" for r in rows if "\t" not in r or Path(r.split("\t")[1]).exists()),
                            encoding="utf-8")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
