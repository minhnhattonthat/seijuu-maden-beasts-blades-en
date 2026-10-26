"""check.py: the one-command check (tests + text lint). The pre-commit hook runs this; exit code gates the commit."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

steps = [[sys.executable, "-X", "utf8", "-m", "pytest", "-q", "-p", "no:cacheprovider", str(ROOT / "tests")]]
if (ROOT / "tools" / "lint.py").exists():
    steps.append([sys.executable, "-X", "utf8", str(ROOT / "tools" / "lint.py")])

for cmd in steps:
    r = subprocess.run(cmd, cwd=ROOT)
    if r.returncode:
        sys.exit(r.returncode)
print("check ok")
