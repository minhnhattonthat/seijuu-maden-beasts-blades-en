-- Log each distinct string the 8x8 menu printer C32912 is called with (pointer at $4F-$51), from frame FROM on.
--   emu.py ROM --state-in S --route-str ... --script tools/lua/print8.lua   (log: "P8 <addr> f<frame>")
local M = emu.memType.snesMemory
local from, seen = FROM or 0, {}
L.on_exec(0xC32912, 0xC32912, function()
  if L.frame < from then return end
  local a = emu.read(0x7E004F, M) | emu.read(0x7E0050, M) << 8 | emu.read(0x7E0051, M) << 16
  if seen[a] then return end
  seen[a] = true
  L.log(string.format("P8 %06X f%d", a, L.frame))
  if a >= 0x7E0000 then  -- built in RAM: dump it, to find where its pieces come from
    local b = {}
    for i = 0, (P8_DUMP or 255) do b[#b + 1] = string.format("%02X", emu.read(a + i, M)) end
    L.log("   " .. table.concat(b, " "))
  end
end)
