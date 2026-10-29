-- Log each PC that writes byte VAL to the VRAM data port $2118 (low byte of a tilemap word), from frame FROM on,
-- with the 16 bytes at the 65816 direct-page pointers $9F/$A1/$4C (where the tile came from).
--   emu.py ROM --state-in S --route-str ... --script tools/lua/vramval.lua --var VAL=0x26 [--var FROM=60]
local M = emu.memType.snesMemory
local val, from, seen = assert(VAL, "set --var VAL=0x.."), FROM or 0, {}
L.on_write(0x2118, 0x2118, function(_, v)
  if v ~= val or L.frame < from then return end
  local pc = L.pc()
  if seen[pc] then return end
  seen[pc] = true
  local s = emu.getState()
  L.log(string.format("VW pc=%06X f%d A=%04X X=%04X Y=%04X db=%02X", pc, L.frame, s["cpu.a"], s["cpu.x"], s["cpu.y"],
    s["cpu.dbr"] or s["cpu.db"] or -1))
end)
