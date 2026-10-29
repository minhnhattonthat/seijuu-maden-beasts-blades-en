"""release.py: build, gate and package the English patch. Stops at the first failure:
build -> check (tests + text lint, incl. no Japanese left in script/) -> smoke -> screen tour (textlog coverage, manifest)
-> visual-QA gate -> BPS patch (re-applied and compared) -> release/<version>/ zip of patch + README.txt.

    python -X utf8 tools/release.py --version 1.0 [--no-tour] [--force]

--no-tour reuses the last tour (the gate still has to pass on it). Never publishes: that's the owner's call.
The debug tool lives in Lua (tools/debug/), so the built ROM carries none of it.
"""
import argparse
import hashlib
import shutil
import subprocess
import sys
import zipfile
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import bps  # noqa: E402
from build import ROM  # noqa: E402
from skill import SKILL  # noqa: E402

PY = [sys.executable, "-X", "utf8"]
BUILT = ROOT / "build" / "seijuu_en.sfc"
NAME = "Seijuu_Maden_EN"


def step(title, cmd):
    print(f"== {title}", flush=True)
    if subprocess.run(PY + [str(c) for c in cmd], cwd=ROOT).returncode:
        sys.exit(f"release stopped: {title} failed")


def hashes(b):
    return {"crc": f"{zlib.crc32(b):08X}", "md5": hashlib.md5(b).hexdigest(), "sha1": hashlib.sha1(b).hexdigest(),
            "size": f"{len(b):,}"}


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--version", required=True)
    ap.add_argument("--no-tour", action="store_true")
    ap.add_argument("--force", action="store_true", help="overwrite this version's files")
    a = ap.parse_args()
    out = ROOT / "release" / a.version
    if out.exists() and not a.force:
        sys.exit(f"{out} exists (--force to overwrite)")
    skill = Path(SKILL) / "scripts"
    step("build", [ROOT / "tools" / "build.py"])
    step("check", [ROOT / "tools" / "check.py"])
    step("smoke", [skill / "emu.py", BUILT, "--out", ROOT / "work" / "qa" / "smoke", "--route",
                   ROOT / "tools" / "routes" / "boot.txt", "--smoke"])
    if not a.no_tour:
        step("tour", [ROOT / "tools" / "tour.py"])
    step("visual-QA gate", [skill / "qa_gate.py", "check", ROOT / "work" / "qa" / "manifest.tsv",
                            ROOT / "work" / "qa" / "verdicts"])
    shutil.rmtree(out, ignore_errors=True)
    out.mkdir(parents=True)
    patch = out / f"{NAME}_v{a.version}.bps"
    step("patch", [ROOT / "tools" / "bps.py", "make", ROM, BUILT, patch])
    orig, built = ROM.read_bytes(), BUILT.read_bytes()
    applied = out / "applied.sfc"
    step("re-apply", [ROOT / "tools" / "bps.py", "apply", ROM, patch, applied])
    if applied.read_bytes() != built:
        sys.exit("release stopped: the patch applied to a clean original differs from the build")
    applied.unlink()
    o, p = hashes(orig), hashes(built)
    readme = (ROOT / "docs" / "release-readme.txt").read_text(encoding="utf-8").format(
        version=a.version, patch=patch.name, o=o, p=p)
    (out / "README.txt").write_text(readme, encoding="utf-8", newline="\r\n")
    with zipfile.ZipFile(out / f"{NAME}_v{a.version}.zip", "w", zipfile.ZIP_DEFLATED) as z:
        z.write(patch, patch.name)
        z.write(out / "README.txt", "README.txt")
    print(f"release ok: {out / f'{NAME}_v{a.version}.zip'} (patched SHA-1 {p['sha1']}); not published")


if __name__ == "__main__":
    main()
