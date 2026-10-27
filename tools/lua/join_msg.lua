-- Show the "<name> joined the party." line (C0530A): the field message poll (C03BEA, runs at home) tests bit
-- $20 of $7EA10C at C03C20 and JSRs C052EA, which prints it with the name at $7EA114. Set the flag once.
--   emu.py ROM --state-in work/states/home.mss --script tools/lua/join_msg.lua --route-str "300 -"
local M = emu.memType.snesMemory
local done = false
L.on_exec(0xC03BF1, 0xC03BF1, function()
  if done then return end
  done = true
  emu.write(0x7EA10C, 0x20, M)
  L.log("JOIN f" .. L.frame)
end)
L.on_exec(0xC052EA, 0xC052EA, function() L.log("JOIN_PRINT f" .. L.frame) end)
