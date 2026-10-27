-- Force a dungeon battle's idle-line action: the battle state dispatcher C505D1 (JSR ($05EC,x), X = state $1018)
-- runs state $30 (C55E9B: bump the unit's counter, print its idle line from C57E03 via C57C40) once.
--   warp.py battle_t10 --lua tools/lua/battle_idle.lua   (FROM: first frame to act, default 7700)
-- STATE overrides the forced state: $0A = C50A8B, "can't escape" (C50AB5).
local done = false
L.on_exec(0xC505D1, 0xC505D1, function()
  if done or L.frame < (FROM or 7700) then return end
  done = true
  local s = emu.getState()
  L.log(string.format("IDLE f%d state=%02X", L.frame, s["cpu.x"] & 0xFF))
  s["cpu.x"] = STATE or 0x30
  emu.setState(s)
end)
L.on_exec(0xC57C40, 0xC57C40, function() L.log("IDLE_PRINT f" .. L.frame); L.shot("idle") end)
