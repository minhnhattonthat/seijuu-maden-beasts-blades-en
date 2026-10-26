"""lz.py: the game's LZSS (decompressor at C3035D; docs/re/compression.md).

Block: u16 output size, then tokens. Flag bytes are read 8 bits MSB-first; 1 = literal byte, 0 = match:
one byte = absolute position in a 256-byte ring (zeroed, write position starts at $EF), and a length nibble
(length = nibble + 2). Nibbles are packed two per byte: the first match of a pair reads a new byte right
after its position byte and uses the high nibble; the next match uses the saved low nibble.

    python -X utf8 tools/lz.py dump OFFSET OUT.bin      # decompress a block from the ROM
    python -X utf8 tools/lz.py --selftest
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROM = ROOT / "rom" / "Seijuu Maden Beasts & Blades (Japan).sfc"


def decompress(data, off):
    """Returns (output bytes, compressed length)."""
    size = data[off] | data[off + 1] << 8
    p = off + 2
    ring = bytearray(256)
    w = 0xEF
    out = bytearray()
    flags = bits = 0
    nib = None
    while len(out) < size:
        if bits == 0:
            flags, bits = data[p], 8
            p += 1
        bit = flags & 0x80
        flags = (flags << 1) & 0xFF
        bits -= 1
        if bit:
            b = data[p]
            p += 1
            ring[w] = b
            w = (w + 1) & 0xFF
            out.append(b)
            continue
        r = data[p]
        p += 1
        if nib is None:
            n = data[p]
            p += 1
            length, nib = (n >> 4) + 2, n & 0x0F
        else:
            length, nib = nib + 2, None
        for _ in range(length):
            if len(out) >= size:
                break
            b = ring[r]
            r = (r + 1) & 0xFF
            ring[w] = b
            w = (w + 1) & 0xFF
            out.append(b)
    return bytes(out), p - off


def compress(data):
    """Greedy LZSS for decompress(). Output differs from the game's packer; the roundtrip is what counts."""
    ring = bytearray(256)
    w = 0xEF
    out = bytearray([len(data) & 0xFF, len(data) >> 8])
    flag_at, bits = None, 8
    nib_at = None
    i = 0
    while i < len(data):
        if bits == 8:
            flag_at, bits = len(out), 0
            out.append(0)
        best_len, best_pos = 0, 0
        maxlen = min(17, len(data) - i)
        for r in range(256):
            # simulate the overlapping copy: the ring is written while it is read
            sim = bytearray(ring)
            sw, sr, n = w, r, 0
            while n < maxlen and sim[sr] == data[i + n]:
                sim[sw] = sim[sr]
                sw, sr, n = (sw + 1) & 0xFF, (sr + 1) & 0xFF, n + 1
            if n > best_len:
                best_len, best_pos = n, r
                if n == maxlen:
                    break
        if best_len >= 2:
            out.append(best_pos)
            if nib_at is None:
                nib_at = len(out)
                out.append((best_len - 2) << 4)
            else:
                out[nib_at] |= best_len - 2
                nib_at = None
            for k in range(best_len):
                ring[w] = ring[best_pos]
                w, best_pos = (w + 1) & 0xFF, (best_pos + 1) & 0xFF
            i += best_len
        else:
            out[flag_at] |= 0x80 >> bits
            out.append(data[i])
            ring[w] = data[i]
            w = (w + 1) & 0xFF
            i += 1
        bits += 1
    return bytes(out)


def selftest():
    import random
    rnd = random.Random(1)
    cases = [b"", b"A", bytes(300), b"abcabcabcabcabc" * 20, bytes(rnd.randrange(4) for _ in range(2000))]
    for c in cases:
        z = compress(c)
        back, used = decompress(z, 0)
        assert back == c and used == len(z), (len(c), len(back))
    if ROM.exists():
        rom = ROM.read_bytes()
        raw, used = decompress(rom, 0x0CAB70)  # intro poem graphic (docs/re/graphics.md)
        assert decompress(compress(raw), 0)[0] == raw
    print("lz selftest ok")


if __name__ == "__main__":
    if sys.argv[1:2] == ["--selftest"]:
        selftest()
    elif sys.argv[1:2] == ["dump"]:
        rom = ROM.read_bytes()
        raw, used = decompress(rom, int(sys.argv[2], 16))
        Path(sys.argv[3]).write_bytes(raw)
        print(f"{len(raw)} bytes from {used} compressed")
    else:
        print(__doc__)
