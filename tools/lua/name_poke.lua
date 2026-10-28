-- Long member name test: copy soldier 0's name field (C63F7E, a {call} stub when built with
-- --qa C63F7E=<long name>) over the RAM name a member-name drawer is about to read ([$BF], or the
-- hero's $7E6052 for the battle box), so every drawn member name is the long one.
--   warp.py status_hero --rom build/seijuu_en.sfc --lua tools/lua/name_poke.lua
local M = emu.memType.snesMemory
local function poke(dst)
  for i = 0, 5 do emu.write(dst + i, emu.read(0xC63F7E + i, M), M) end
end
L.on_exec(0xC254A9, 0xC254A9, function()  -- status / formation / exchange NAME, BEAST/MASTER row
  local p = emu.read(0xBF, M) | emu.read(0xC0, M) << 8 | emu.read(0xC1, M) << 16
  if p >> 16 == 0x7E then poke(p) end
end)
L.on_exec(0xC5329A, 0xC5329A, function() poke(0x7E6052) end)  -- dungeon-battle name box
