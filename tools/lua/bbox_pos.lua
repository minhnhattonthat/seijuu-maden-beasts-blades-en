-- Log the dungeon-battle name box's position each time it is drawn (C53259: A = tilemap offset into 7F:4C00, $12AE = shift).
--   emu.py ROM --state-in work/states/en_battle_t10.mss --frames 300 --script tools/lua/bbox_pos.lua
local M = emu.memType.snesMemory
L.on_exec(0xC53259, 0xC53259, function()
  local a = emu.getState()["cpu.a"]
  L.log(string.format("BBOX f%d off %04X shift %04X", L.frame, a, emu.read(0x7E12AE, M) | emu.read(0x7E12AF, M) << 8))
end)
