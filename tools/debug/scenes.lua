-- Scene list for tools/debug/warp.lua. Grow it whenever a bug report names a place it can't reach.
-- Fields (all optional; see warp.lua): boot_only, boot, scn, map, x, y, dir, ev, script, vars, gold, ram,
-- after, mash, settle, check, frames (budget for warp.py). Scenario numbers: docs/re/events.md (scenario table).
-- check: RAM that must hold at the end. $505A = scenario, $505B = map.
SCENES = {
  -- boot path (route only)
  intro = { boot_only = true, boot = "1400 -", settle = 30, frames = 1500 },
  title = { boot_only = true, boot = "1500 -;8 start;120 -", settle = 30, frames = 1700 },
  name_entry = { boot_only = true, boot = "1500 -;8 start;120 -;8 start;300 -", settle = 30, frames = 2000 },
  prologue = { boot_only = true, mash = 30, settle = 1500, frames = 3600 },
  -- new game as the game does it: opening cutscene in the castle (scenario 35 event 0)
  opening = { scn_start = 35, mash = 0, after = "600 -", check = { [0x7E505A] = 35 }, frames = 7600 },
  -- the poem cutscene (G4, op 80) and the hero's room after it
  poem = { scn_start = 35, mash = 30, wait_pc = 0xC0541F, after = "300 -", settle = 0, frames = 11000 },
  -- Lunas Castle (scenario 1) building events: each runs the shopkeeper's lines and its menu op
  -- (event op in the name: 60 buy/sell/forge, 62, 64, 66 inn, 68, 6A, 6C, 6E, 70, 72, 74, 76; then A on item 1)
  shop_60 = { scn = 1, map = 0, ev = 12, after = "500 -;6 a;200 -", frames = 8000 },
  -- weapon shop: buy list (C6 name fields in the 8x8 font)
  shop_buy = { scn = 1, map = 0, ev = 12, after = "500 -;6 a;200 -;6 a;200 -", frames = 8200 },
  shop_62 = { scn = 1, map = 0, ev = 9, after = "500 -;6 a;200 -", frames = 8000 },
  shop_64 = { scn = 1, map = 0, ev = 2, after = "500 -;6 a;200 -", frames = 8000 },
  inn_66 = { scn = 1, map = 0, ev = 21, after = "500 -;6 a;200 -", frames = 8000 },
  shop_68 = { scn = 1, map = 0, ev = 40, after = "500 -;6 a;200 -", frames = 8000 },
  shop_6a = { scn = 1, map = 0, ev = 20, after = "500 -;6 a;200 -", frames = 8000 },
  shop_6c = { scn = 1, map = 0, ev = 14, after = "500 -;6 a;200 -", frames = 8000 },
  shop_6e = { scn = 1, map = 0, ev = 15, after = "500 -;6 a;200 -", frames = 8000 },
  shop_70 = { scn = 6, map = 0, ev = 66, after = "500 -;6 a;200 -", frames = 8000 },
  shop_72 = { scn = 1, map = 0, ev = 17, after = "500 -;6 a;200 -", frames = 8000 },
  shop_74 = { scn = 1, map = 0, ev = 48, after = "500 -;6 a;200 -", frames = 8000 },
  shop_76 = { scn = 6, map = 0, ev = 62, after = "500 -;6 a;200 -", frames = 8000 },
  rest_78 = { scn = 13, map = 0, ev = 5, after = "150 -", frames = 8000 },
  -- field menu (A) in the hero's room: talk / examine / party / status (仲間 does nothing with a solo hero;
  -- ステータス opens the party formation/status screen)
  field_menu = { scn = 35, map = 2, x = 0x80, y = 0x68, after = "240 -;6 a;60 -", frames = 7800 },
  status_menu = { scn = 35, map = 2, x = 0x80, y = 0x68,
                  after = "240 -;6 a;40 -;6 down;20 -;6 down;20 -;6 down;20 -;6 a;400 -", settle = 0,
                  frames = 8200 },
  -- op 5E battle as scenario 2 (bandit fort) event 0 starts it
  battle_fort = { scn_start = 2, script = { 0x5E, 0x00, 0xFF, 0x00, 0x00, 0x6A, 0xFF }, after = "600 -;6 a;120 -;6 a;120 -",
                  frames = 8600 },
  battle_t10 = { scn_start = 3, script = { 0x5E, 0x10, 0xFF, 0x00, 0x10, 0x6A, 0xFF }, after = "900 -", frames = 8600 },
  -- battle end messages: from battle_t10's state, pass a turn (防御) with tools/lua/battle_end.lua
  -- (BATTLE_END=1 victory: C34B9D exp/food/gold + level up; 2 defeat: C57D3C, then an ending scroll)
  battle_t13 = { scn_start = 3, script = { 0x5E, 0x13, 0xFF, 0x00, 0x13, 0x6A, 0xFF }, after = "900 -", frames = 8600 },
  -- no game-over screen: a lost battle sends the party back to Melshiva; the Dark side's victory is ending_1/_4
  -- op 14: leave the building to the town menu; op 16: to the world map
  town_menu = { script = { 0x14, 0xFF }, after = "400 -", frames = 7600 },
  world_map = { script = { 0x16, 0xFF }, after = "400 -", frames = 7600 },
  town_enter = { script = { 0x14, 0xFF }, after = "400 -;6 right;40 -;6 a;150 -", frames = 7800 },
  -- world map: X = map / save; A on the party = its commands
  world_save = { script = { 0x16, 0xFF }, after = "400 -;6 x;60 -;6 down;20 -;6 a;120 -", frames = 7800 },
  world_walk = { script = { 0x16, 0xFF }, frames = 12000,
                 after = "400 -;6 a;60 -;6 a;80 -;6 a;60 -;6 a;60 -;60 down;20 -;6 a;30 -;60 left;20 -;6 a;30 -;" ..
                         "60 down;20 -;6 a;30 -;6 x;3000 -" },
  world_cmd = { script = { 0x16, 0xFF }, after = "400 -;6 a;60 -;6 a;80 -", frames = 7800 },
  -- the war begins: Heroi desert (58) event 1, the sky effect (op A6), progress var FF -> 2, on to Melshiva
  -- (the event itself needs its cave map and object setup; the effect alone is op A6)
  war_sky = { scn_start = 58, script = { 0xA6, 0xFF }, after = "300 -", frames = 7800 },
  -- war_start's dialogue after the Evil Eye battle (E42BB3, which a mash can't win), run from E42BCC
  war_talk = { scn = 58, map = 0, jump = 0xE42BCC, after = "200 -", settle = 0, frames = 7600 },
  -- op A2 n: ending sequence n (BG table C17012, text pointers C17044, 5 entries; scenario 72 uses 0 and 2);
  -- every ending runs on into the staff credits (C17C03)
  ending_0 = { script = { 0xA2, 0x00, 0xFF }, after = "1500 -", frames = 8600 },
  ending_1 = { script = { 0xA2, 0x01, 0xFF }, after = "1500 -", frames = 8600 },
  ending_2 = { script = { 0xA2, 0x02, 0xFF }, after = "1500 -", frames = 8600 },
  ending_3 = { script = { 0xA2, 0x03, 0xFF }, after = "1500 -", frames = 8600 },
  ending_4 = { script = { 0xA2, 0x04, 0xFF }, after = "1500 -", frames = 8600 },
  credits = { script = { 0xA2, 0x00, 0xFF }, after = "7000 -", frames = 14200 },
  home = { scn_start = 35, mash = 30, after = "4300 -", settle = 0, check = { [0x7E505B] = 2 }, frames = 11000 },
}
