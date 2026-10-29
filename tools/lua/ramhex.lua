-- Hex-dump a WRAM range once at frame AT: --var LO=0x7E498A --var N=256 --var AT=7400
local M = emu.memType.snesMemory
L.on_frame(function(n)
  if n ~= AT then return end
  for row = 0, N - 1, 16 do
    local t = {}
    for i = 0, math.min(15, N - 1 - row) do t[#t + 1] = string.format("%02X", emu.read(LO + row + i, M)) end
    L.log(string.format("%06X %s", LO + row, table.concat(t, " ")))
  end
end)
