-- Log the source buffer of the window blitter C311FB (copies a menu's tilemap rectangle to the BG3 map):
-- data bank, $9F (buffer base) and $A1 (row pointer), once per distinct source.
--   emu.py ROM --state-in S --route-str ... --script tools/lua/winsrc.lua   (log: "WIN db=.. 9F=.. A1=.. f<frame>")
local M = emu.memType.snesMemory
local seen = {}
L.on_exec(0xC311FB, 0xC311FB, function()
  local s = emu.getState()
  local db = s["cpu.dbr"] or s["cpu.db"] or -1
  local b = emu.read(0x7E009F, M) | emu.read(0x7E00A0, M) << 8
  local k = string.format("db=%02X 9F=%04X", db, b)
  if seen[k] then return end
  seen[k] = true
  L.log(string.format("WIN %s A1=%04X f%d", k, emu.read(0x7E00A1, M) | emu.read(0x7E00A2, M) << 8, L.frame))
end)
