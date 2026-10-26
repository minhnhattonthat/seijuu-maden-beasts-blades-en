"""lzblocks.py: list LZ blocks the code loads with an immediate address (LDA #bank / LDY #addr / JSL C3035D),
decompress each and render it as 2bpp and 4bpp tile sheets for the graphics-text sweep.

    python -X utf8 tools/lzblocks.py [--render work/gfx]

Prints call site, block address, compressed and raw size. Seeds: immediate call sites plus TABLES; from each
seed it walks on through blocks packed back to back ('chain'). Call sites whose bank/address come from a
register are listed as 'dynamic': their blocks are found only if a chain reaches them.
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lz import decompress, ROM  # noqa: E402

JSL = b"\x22\x5d\x03\xc3"
# 16-bit block tables the dynamic call sites index: (file offset, bank, entries)
TABLES = [(0x0041E, 0xE1, 24), (0x25E3F, 0xCD, 20), (0x0D0380, 0xCD, 11)]


def blocks(rom):
    found, dynamic = {}, []
    for m in re.finditer(re.escape(JSL), rom):
        site = m.start()
        pre = rom[max(0, site - 12):site]
        # LDA #$00bb (A9 bb 00) or LDA #bb (A9 bb), then LDY #$hhll (A0 ll hh), right before the JSL
        mm = re.search(rb"\xa9([\xc0-\xff])\x00?\xa0(..)$", pre, re.S)
        if not mm:
            dynamic.append(site)
            continue
        addr = mm[1][0] << 16 | mm[2][0] | mm[2][1] << 8
        found.setdefault(addr, []).append(site)
    return found, dynamic


def plausible(rom, off):
    """A block header and body that look like this LZ: sane size, compresses, stays in the ROM."""
    size = rom[off] | rom[off + 1] << 8
    if not 32 <= size <= 0x8000:
        return None
    try:
        raw, used = decompress(rom, off)
    except IndexError:
        return None
    if used > size * 9 // 8 + 4 or len(set(raw)) < 2:
        return None
    return raw, used


def chain(rom, starts):
    """Blocks are packed back to back: walk on from each known block while the next one is plausible."""
    found = {}
    for addr in sorted(starts):
        off = addr & 0x3FFFFF
        while off not in found:
            r = plausible(rom, off)
            if not r:
                break
            found[off] = r
            off += r[1]
    return found


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--render", help="directory for tile sheets")
    a = ap.parse_args()
    rom = ROM.read_bytes()
    seeds, dynamic = blocks(rom)
    for table, bank, n in TABLES:
        for i in range(n):
            seeds.setdefault(bank << 16 | rom[table + 2 * i] | rom[table + 2 * i + 1] << 8, []).append(table)
    found = chain(rom, seeds)
    skill = subprocess.run([sys.executable, str(Path(__file__).parent / "skill.py")], capture_output=True,
                           text=True).stdout.strip()
    for off in sorted(found):
        raw, used = found[off]
        addr = 0xC00000 | off
        sites = " ".join(f"{0xC00000 + s:06X}" for s in seeds.get(addr, [])) or "chain"
        print(f"{addr:06X} z={used:5d} raw={len(raw):5d}  from {sites}")
        if a.render:
            out = Path(a.render)
            out.mkdir(parents=True, exist_ok=True)
            (out / f"{addr:06X}.bin").write_bytes(raw)
            for fmt in ("snes2", "snes4"):
                subprocess.run([sys.executable, "-X", "utf8", f"{skill}/scripts/tiles.py", "render",
                                str(out / f"{addr:06X}.bin"), str(out / f"{addr:06X}_{fmt}.png"), "--fmt", fmt,
                                "--cols", "32"], capture_output=True)
    print(f"{len(found)} blocks ({len(seeds)} seeds, rest by chain); dynamic call sites: "
          f"{' '.join(f'{0xC00000 + s:06X}' for s in dynamic)}")


if __name__ == "__main__":
    main()
