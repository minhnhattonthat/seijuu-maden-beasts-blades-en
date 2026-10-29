-- Action-name tiles (LZ D2AD77, unpacked by C52B95 to $7F31AB, 3424 bytes) reach VRAM through the DMA queue at
-- $1000 (C500F0: slots of 7 bytes, src $1001, VRAM word $1004, size $1006). Log each queued slot that points into
-- the buffer (offset, VRAM, size) and the PC that queued it.
--   warp.py battle_fort --lua tools/lua/actreads.lua
local M = emu.memType.snesMemory
local function rd(a) return emu.read(a, M) | emu.read(a + 1, M) << 8 end
for slot = 0, 1 do
  local base = 0x1000 + slot * 7
  L.on_write(0x7E0000 + base + 3, 0x7E0000 + base + 3, function(_, v)  -- bank byte of the source
    if v ~= 0x7F then return end
    L.log(string.format("AQ slot%d pc=%06X f%d", slot, L.pc(), L.frame))
  end)
end
L.on_exec(0xC5011A, 0xC5011A, function()
  local src = rd(0x1001) | emu.read(0x1003, M) << 16
  if src >= 0x7F31AB and src < 0x7F31AB + 3424 then
    L.log(string.format("AD f%d off=%04X vram=%04X size=%04X", L.frame, src - 0x7F31AB, rd(0x1004), rd(0x1006)))
  end
end)
