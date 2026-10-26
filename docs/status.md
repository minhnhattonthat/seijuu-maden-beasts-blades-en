# Status

Updated at the end of every session. Keep it to what the next session needs; history is in git.

- **Phase:** Step 0 done; next is phase 1 (research and recon). No build yet.
- **Done:** repo set up from template; MesenCE 2.2.1 in `tools/mesen/`, asar 1.91 in `tools/asar/` (both gitignored, URLs in AGENTS.md); `rom.sha1` pinned (No-Intro dump, HiROM FastROM 2.5 MB, header title `ﾋﾞｰｽﾄ ｱﾝﾄﾞﾌﾞﾚｲﾄﾞ`); pre-commit runs `tools/check.py` (verified it rejects a failing test); plugin guard hook blocks `sed -i` (verified); smoke of original ROM ok, scripted input reaches name entry, Lua probe log works.
- **Observed:** the intro crawl is already in English in the original ("Peace of mind is available for those who search..."); title logo is English "Beasts & Blades" with small kanji 聖獣魔伝. New game opens a kana name-entry grid with the hero portrait.
- **Next:** phase 1: look for earlier patches/docs; find text encoding (relative search / draw hook), pointer tables, compression, control codes, free space; graphics-text survey. Write findings to `docs/re/`.
- **Open bugs:** none.
- **Waiting on the user:** nothing. (Not checked: the Mesen GUI's keyboard input, since this run is headless; emu.py writes default key mappings to `tools/mesen/settings.json`, copied to `tools/emu-config/`.)
