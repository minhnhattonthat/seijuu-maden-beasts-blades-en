-- Reach the army-exchange screen's item trade (C2 dispatcher idx E, C2D114) from the world map, with both bags full.
-- The first A on the party (C09F15) jumps to C0A19D, the "A on another army" path (as exchange_equip.lua);
-- unit 1 (the other army) need not exist: only its bag at $631B + $296 is poked.
--   emu.py ROM --state-in work/states/en_world_map.mss --script tools/lua/exchange_items.lua
--     --route-str "60 -;6 a;300 -;6 a;400 -;6 a;400 -"
local M = emu.memType.snesMemory
local BAG = { 0x00, 0x01, 0x01, 0x00, 0x02, 0x01, 0x00, 0x03, 0x02, 0x00, 0x04, 0x01, 0x00, 0x05, 0x01,
              0x00, 0x06, 0x01, 0x00, 0x07, 0x01, 0x00, 0x08, 0x01, 0x00, 0x09, 0x01, 0x00, 0x0A, 0x01,
              0x01, 0x00, 0x01, 0x01, 0x01, 0x01, 0x02, 0x00, 0x02, 0x03, 0x00, 0x03, 0xFF }
local done = false
L.on_exec(0xC09F15, 0xC09F15, function()
  if done then return end
  done = true
  for i = 1, #BAG do emu.write(0x7E62B0 + i - 1, BAG[i], M); emu.write(0x7E65B1 + i - 1, BAG[i], M) end
  emu.write(0x7E6014, 1, M); emu.write(0x7E6015, 0, M)
  local s = emu.getState()
  s["cpu.pc"] = 0xA19D
  emu.setState(s)
  L.log("EXCHANGE f" .. L.frame)
end)
-- アイテム is greyed for the fake army, so the swap command (idx D, as exchange_equip.lua) is sent to idx E instead
local redirected = false
L.on_exec(0xC2CA56, 0xC2CA56, function()
  if redirected then return end
  redirected = true
  local s = emu.getState()
  s["cpu.pc"] = 0xD114
  emu.setState(s)
  L.log("ITEMS f" .. L.frame)
end)
