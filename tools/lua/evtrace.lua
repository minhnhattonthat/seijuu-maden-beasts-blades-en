-- Log every event-script opcode the VM (C03BE6) dispatches: frame, script address, opcode bytes.
--   emu.py ... --script tools/lua/evtrace.lua
-- Hooked at C03C48 (JSR ($3B31,x)): $69-$6B already points past the opcode byte.
local function rd(a) return emu.read(a, emu.memType.snesMemory) end
L.on_exec(0xC03C48, 0xC03C48, function()
  local p = rd(0x69) | (rd(0x6A) << 8) | (rd(0x6B) << 16)
  p = p - 1
  local t = {}
  for i = 0, 9 do t[#t + 1] = string.format("%02X", rd(p + i)) end
  L.log(string.format("%d %06X %s", L.frame, p, table.concat(t, " ")))
end)
