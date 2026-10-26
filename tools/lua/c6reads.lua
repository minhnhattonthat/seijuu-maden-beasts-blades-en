-- Log each distinct code address that reads the C6 name-field tables (C60F50-C67C00: weapons ... monster bosses),
-- with the address read and registers: finds the routines that draw item/skill/beast names and their widths.
--   python -X utf8 tools/debug/warp.py shop_buy --lua tools/lua/c6reads.lua   (log: work/qa/warp/<scene>/)
-- FROM (default 7000, about where warps land): only reads from that frame on (boot copies records too).
local from = FROM or 7000
local seen = {}
local function hook(addr, value)
  if L.frame < from then return end
  local s = emu.getState()
  local pc = (s["cpu.k"] << 16) | s["cpu.pc"]
  if seen[pc] then return end
  seen[pc] = true
  L.log(string.format("f%d pc=%06X read %06X=%02X A=%04X X=%04X Y=%04X", L.frame, pc, addr, value, s["cpu.a"],
    s["cpu.x"], s["cpu.y"]))
end
emu.addMemoryCallback(L.safe(hook), emu.callbackType.read, 0xC60F50, 0xC67C00, emu.cpuType.snes,
  emu.memType.snesMemory)
