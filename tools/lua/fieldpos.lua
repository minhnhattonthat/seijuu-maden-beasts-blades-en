-- Log the field state every EVERY frames (default 30): position, tile, facing, scenario, map, VM flags.
--   emu.py ... --script tools/lua/fieldpos.lua [--var EVERY=20]
local function rd(a) return emu.read(a, emu.memType.snesMemory) end
local function rw(a) return rd(a) | (rd(a + 1) << 8) end
L.on_frame(function(f)
  if f % (EVERY or 30) == 0 then
    L.log(string.format("%d x=%d y=%d tx=%d ty=%d dir=%d scn=%d map=%d A10C=%02X", f, rw(0x7E94CE), rw(0x7E94D0),
      rw(0x7E94E4), rw(0x7E94E6), rd(0x7E94C4), rd(0x7E505A), rd(0x7E505B), rd(0x7EA10C)))
  end
end)
