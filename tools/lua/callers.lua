-- Log each distinct caller of a routine: on exec of AT, print the top 9 stack bytes (return addresses) and A/X/Y.
--   emu.py ROM ... --script tools/lua/callers.lua --var AT=0xC31979 [--var FROM=0 --var TO=1e9]
local mem = emu.memType.snesMemory
local from, to = FROM or 0, TO or math.huge
local seen = {}
L.on_exec(AT, AT, function()
  if L.frame < from or L.frame > to then return end
  local s = emu.getState()
  local sp = s["cpu.sp"]
  local t = {}
  for i = 1, 9 do t[#t + 1] = string.format("%02X", emu.read(sp + i, mem)) end
  local key = table.concat(t, "", 1, 6)
  if seen[key] then return end
  seen[key] = true
  L.log(string.format("f%d stack %s A=%04X X=%04X Y=%04X DB=%02X D=%04X", L.frame, table.concat(t, " "),
    s["cpu.a"], s["cpu.x"], s["cpu.y"], s["cpu.dbr"], s["cpu.d"]))
end)
