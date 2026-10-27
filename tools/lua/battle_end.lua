-- Force the end of a dungeon battle: the next battle-end check (C56AD4, dispatch at C56ADA) jumps to
-- the victory (BATTLE_END=1, C56B10) or defeat (BATTLE_END=2, C56B2B) path, which prints its battle message
-- (C57C00, index in $B1 = entry * 2 of C57CD8). Logs each printed message as "BMSG <$B1>".
--   warp.py battle_t10 --lua tools/lua/battle_end.lua (BATTLE_END defaults to 1)
local M = emu.memType.snesMemory
local done = false
L.on_exec(0xC56ADA, 0xC56ADA, function()
  if done then return end
  done = true
  local s = emu.getState()
  s["cpu.pc"] = (BATTLE_END or 1) == 2 and 0x6AE6 or 0x6AE3
  emu.setState(s)
  L.log("BATTLE_END " .. (BATTLE_END or 1))
end)
L.on_exec(0xC57C16, 0xC57C16, function() L.log("BMSG " .. emu.read(0x7E00B1, M)) end)
