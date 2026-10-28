-- Log which 256-byte pages of WRAM bank 7F get written or read (to find free RAM for hooks).
--   emu.py ROM --state-in S --mash N --script tools/lua/wram_pages.lua   (log: "f<n> UNTOUCHED 7F pages: .." every 500 frames)
local hit = {}
local function mark(a) hit[(a >> 8) & 0xFF] = true end
L.on_write(0x7F0000, 0x7FFFFF, mark)
L.on_read(0x7F0000, 0x7FFFFF, mark)
L.on_frame(function(n)
  if n % 500 ~= 0 then return end
  local free = {}
  for p = 0, 255 do if not hit[p] then free[#free + 1] = string.format("%02X", p) end end
  L.log(string.format("f%d UNTOUCHED 7F pages: %s", n, table.concat(free, " ")))
end)
