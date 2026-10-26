-- Log every string the text engines (C318D1 typed, C32575 bulk) read: frame, 24-bit pointer at DP $32, first bytes.
-- Hooks the code reads and the glyph calls; logs when the pointer jumps (a new string), not while it advances.
--   emu.py ROM --out DIR ... --script tools/lua/textlog.lua [--var N=48]
local mem = emu.memType.snesMemory
local n = N or 48
local last = -1
local function log_str()
  local d = emu.getState()["cpu.d"]
  local p = emu.read(d + 0x32, mem) | emu.read(d + 0x33, mem) << 8 | emu.read(d + 0x34, mem) << 16
  if p >= last and p <= last + 6 then last = p return end  -- same string advancing (codes take up to 5 bytes)
  last = p
  local t = {}
  for i = 0, n - 1 do t[#t + 1] = string.format("%02X", emu.read(p + i, mem)) end
  L.log(string.format("f%d str %06X %s", L.frame, p, table.concat(t, " ")))
end
L.on_exec(0xC318EA, 0xC318EA, log_str)  -- typed dialogue engine: LDA [$32]
L.on_exec(0xC32589, 0xC32589, log_str)  -- bulk print engine (prologue scroll, choices)
L.on_exec(0xC32912, 0xC32912, function()  -- 8x8 menu printer (names, menu labels): pointer at DP $4F
  local d = emu.getState()["cpu.d"]
  local p = emu.read(d + 0x4F, mem) | emu.read(d + 0x50, mem) << 8 | emu.read(d + 0x51, mem) << 16
  local t = {}
  for i = 0, n - 1 do t[#t + 1] = string.format("%02X", emu.read(p + i, mem)) end
  L.log(string.format("f%d str %06X %s menu", L.frame, p, table.concat(t, " ")))
end)
L.on_exec(0xC31979, 0xC31979, log_str)  -- full-width glyph, typed
L.on_exec(0xC31B74, 0xC31B74, log_str)  -- half-width glyph
L.on_exec(0xC32614, 0xC32614, log_str)  -- full-width glyph, bulk
-- the 00 code (end, or return from a call): the next read starts a new string even if it sits right after this one
L.on_exec(0xC318EE, 0xC318EE, function() last = -1 end)
L.on_exec(0xC3258D, 0xC3258D, function() last = -1 end)
