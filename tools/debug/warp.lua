-- Debug warp: cold boot -> any scene in tools/debug/scenes.lua, by name.
--   emu.py ROM --out DIR --script tools/debug/scenes.lua --script tools/debug/warp.lua --var "SCENE='shop'"
--          --frames N [--state-out work/states/SCENE.mss]
-- (tools/debug/warp.py wraps this and knows each scene's frame budget.)
-- Boot: title -> new game -> default name -> prologue (mash A). The new-game code calls the scenario start at
-- C08344 with $505A = 35 (opening); a scene with `scn` swaps that number there. Then, once the field is idle
-- ($A10C bit 7 clear = no event script running), a scene with `map` injects a one-op event script into WRAM:
--   10 00 SCN MAP X Y DIR 03 00 00 EV FF       (op 10: change scenario+map, then run event EV; FF = none)
-- or `script` = raw bytes. `vars` = {[n]=v} nibble story vars ($4F69, var FF = progress), `gold`, `ram`
-- = {[addr]=byte} are written just before the injection. `after` = presses (route syntax) once it ran, `mash`
-- = A every N frames meanwhile. `wait_pc` = keep mashing until that code runs, then `after` (mash_after).
-- `scn_start` = scenario for the new-game start (default 6 when warping, else the game's 35); `boot_only` =
-- just the boot route (`boot` overrides it). At the end it checks `check` = {[addr]=byte}, shoots
-- scene_<name>.png and logs "SCENE OK name" (warp.py looks for it).
-- Opt-in globals: GOD=1 (pin hero HP), NOENC=1 (no random encounters; not mapped yet).
local S = assert(SCENES, "load tools/debug/scenes.lua first")
local name = assert(SCENE, "set --var \"SCENE='name'\"")
local sc = assert(S[name], "unknown scene " .. tostring(name))
local M = emu.memType.snesMemory
local function rd(a) return emu.read(a, M) end
local function wr(a, v) emu.write(a, v & 0xFF, M) end
local BUF = 0x7EEF00  -- 256 free bytes (zero in every dump; survives map loads, unlike $7F)

local function route(spec)
  for step in spec:gmatch("[^;]+") do
    local n, b = step:match("^%s*(%d+)%s+(%S+)%s*$")
    L.press(b, tonumber(n))
  end
end

local phase = "boot"
local t0 = 0
MASH = 30
MASH_KEY = "a"
-- title (~f1450, two Starts), name entry (accept "ああ"), into the prologue
route(sc.boot or "1500 -;8 start;120 -;8 start;150 -;6 a;30 -;6 a;30 -;6 a;30 -;6 start;60 -")
if sc.boot_only then MASH = sc.mash or 0 end

L.on_exec(0xC08344, 0xC08344, function()
  if sc.boot_only then return end
  -- a warp starts in Melshiva Castle (6: no entry event) instead of the opening cutscene, then injects
  local st = sc.scn_start or ((sc.map or sc.script) and 6)
  if st then wr(0x7E505A, st) end
  phase, t0 = "started", L.frame
  L.log(string.format("f%d new game, scenario %d", L.frame, rd(0x7E505A)))
end)

-- wait_pc: the scene starts when this code runs (e.g. an event opcode handler), not at a fixed frame
if sc.wait_pc then
  L.on_exec(sc.wait_pc, sc.wait_pc, function()
    if phase ~= "waiting" then return end
    phase, t0 = "warped", L.frame
    MASH = sc.mash_after or 0
    L.log(string.format("f%d reached %06X", L.frame, sc.wait_pc))
    if sc.after then route(sc.after) end
  end)
end

local function inject()
  for k, v in pairs(sc.vars or {}) do
    local a = 0x7E4F69 + (k >> 1)
    local old = rd(a)
    if k & 1 == 1 then wr(a, (old & 0x0F) | (v << 4)) else wr(a, (old & 0xF0) | v) end
  end
  if sc.gold then wr(0x7E600C, sc.gold); wr(0x7E600D, sc.gold >> 8); wr(0x7E600E, sc.gold >> 16) end
  for a, v in pairs(sc.ram or {}) do wr(a, v) end
  local s = sc.script or { 0x10, 0x00, sc.scn, sc.map, sc.x or 0x80, sc.y or 0x80, sc.dir or 2, 3, 0, 0,
    sc.ev or 0xFF, 0xFF }
  for i = 1, #s do wr(BUF + i - 1, s[i]) end
  wr(0x7E0069, BUF & 0xFF); wr(0x7E006A, (BUF >> 8) & 0xFF); wr(0x7E006B, BUF >> 16)
  wr(0x7EA10C, rd(0x7EA10C) | 0x80)
  L.log(string.format("f%d inject (A0C5=%02X) %s", L.frame, rd(0x7EA0C5), (function()
    local t = {}; for i = 1, #s do t[#t + 1] = string.format("%02X", s[i]) end; return table.concat(t, " ") end)()))
end

-- the VM can be busy or reset $69 right after a map load: confirm it ran our buffer, else inject again
local ran, tries = false, 0
L.on_exec(0xC03C48, 0xC03C48, function()
  if rd(0x7E006B) == BUF >> 16 then ran = true end
end)

-- arrived: play `after` now, or (wait_pc) keep mashing until that code runs
local function arrive(f)
  MASH = sc.mash or 0
  if sc.wait_pc then phase = "waiting"; return end
  phase, t0 = "warped", f
  if sc.after then route(sc.after) end
end

L.on_frame(function(f)
  if GOD then wr(0x7E6065, rd(0x7E6066)) end
  local warp = sc.map or sc.script
  -- field ready: the scenario start set $505B to FF until the first map is loaded
  if phase == "started" and rd(0x7E505B) == 0xFF then t0 = f end
  if phase == "injected" and not ran and f - t0 > 30 then
    tries = tries + 1
    if tries > 10 then L.fail("SCENE FAIL " .. name .. ": the event VM never ran the injected script") end
    inject(); t0 = f
  end
  if phase == "injected" and ran and sc.jump then
    phase, t0 = "jump", f
  elseif phase == "injected" and ran then
    arrive(f)
  elseif phase == "jump" and f - t0 > 60 and rd(0x7EA10C) & 0x80 == 0 and rd(0x7E505B) ~= 0xFF then
    -- `jump` = run the scenario's script from this address (mid-event, e.g. after a battle it can't win)
    wr(0x7E0069, sc.jump & 0xFF); wr(0x7E006A, (sc.jump >> 8) & 0xFF); wr(0x7E006B, sc.jump >> 16)
    wr(0x7EA10C, rd(0x7EA10C) | 0x80)
    L.log(string.format("f%d jump %06X", f, sc.jump))
    arrive(f)
  elseif phase == "started" and warp and f - t0 > 120 and rd(0x7EA10C) & 0x80 == 0 then
    inject()
    phase, t0 = "injected", f
  elseif phase == "started" and not warp then
    arrive(f)
  elseif sc.boot_only and phase == "boot" and L.route_done() then
    phase, t0 = "warped", f
    if sc.after then route(sc.after) end
  elseif phase == "warped" and L.route_done() and f - t0 >= (sc.settle or 240) then
    phase = "checked"
    local bad = {}
    for a, v in pairs(sc.check or {}) do
      if rd(a) ~= v then bad[#bad + 1] = string.format("%06X=%02X (want %02X)", a, rd(a), v) end
    end
    L.shot("scene_" .. name .. ".png")
    if #bad > 0 then L.fail("SCENE FAIL " .. name .. ": " .. table.concat(bad, ", ")) end
    L.log(string.format("SCENE OK %s f%d scn=%d map=%d", name, f, rd(0x7E505A), rd(0x7E505B)))
  end
end)
