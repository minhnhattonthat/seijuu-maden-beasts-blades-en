-- Reach the CD5812 screen (equip change from the army-exchange screen) from the world map.
-- The first A on the party (C09F15) jumps to C0A19D, the "A on another army" path: exchange screen
-- (C2 dispatcher idx 1, C293C5, E0FB=1 loads CD5812). Its next command (idx D, C2CA56) is redirected to
-- idx 4 (C2A302, "whose equipment?"); A on a member then opens the equip page (idx 8, C2A361).
-- Unit TARGET (default 1) need not exist: the other army shows garbage, the hero's side is real.
--   emu.py ROM --state-in work/states/world_map.mss --script tools/lua/exchange_equip.lua
--     --route-str "60 -;6 a;300 -;6 a;400 -;6 a;200 -;6 a;300 -"
local M = emu.memType.snesMemory
local function once(pc, fn)
  local done = false
  L.on_exec(pc, pc, function()
    if done then return end
    done = true
    fn()
  end)
end
local function jump(pc)
  local s = emu.getState()
  s["cpu.pc"] = pc & 0xFFFF
  emu.setState(s)
end
once(0xC09F15, function()
  emu.write(0x7E6014, TARGET or 1, M); emu.write(0x7E6015, 0, M)
  L.log("EXCHANGE f" .. L.frame)
  jump(0xA19D)
end)
once(0xC2CA56, function() L.log("EQUIP f" .. L.frame); jump(0xA302) end)
once(0xC2A361, function() L.log("EQUIP_PAGE f" .. L.frame) end)
