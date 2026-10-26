# Seijuu Maden: Beasts & Blades (SNES) English translation

Skill: translate-retro-game; `python tools/skill.py` prints its folder. Read its SKILL.md before ROM, text or QA work. `"$(python tools/skill.py)"` works in bash and PowerShell; never paste a `plugins/cache/<hash>` path.

## Commands (run from repo root)
- Build:    `python -X utf8 tools/build.py`  -> build/seijuu_en.sfc (checks the dump against `rom.sha1` first)
- Check:    `python -X utf8 tools/check.py`  (tests + lint; the pre-commit hook runs this)
- Smoke:    `python -X utf8 "$(python tools/skill.py)/scripts/emu.py" build/seijuu_en.sfc --out work/qa/smoke --route tools/routes/boot.txt --smoke`
- Warp:     `python -X utf8 tools/debug/warp.py <scene>.. [--rom build/seijuu_en.sfc] [--states] [--sheet]` (cold boot -> scene, proof shot in `work/qa/warp/<scene>/`; `--list`; `all --states` regenerates `work/states/`; scenes: `tools/debug/scenes.lua`; never ask the user to play to a scene)
- Release:  `python -X utf8 tools/release.py` (patch + verify; never publish without the user)
- Clean:    `python -X utf8 tools/clean.py`

## Paths
- Original ROM: `rom/Seijuu Maden Beasts & Blades (Japan).sfc` (gitignored; SHA-1 in `rom.sha1`, checked by `tools/check_rom.py`). HiROM FastROM, 2.5 MB, no header.
- Emulator: this repo's own MesenCE in `tools/mesen/` (release 2.2.1, https://github.com/nesdev-org/MesenCE/releases/download/2.2.1/Mesen_2.2.1_Windows.zip; gitignored; refetch with `fetch_emu.py mesen`). Assembler: `tools/asar/asar.exe` (asar 1.91, https://github.com/RPGHacker/asar/releases/download/v1.91/asar191.zip). Savestates: `work/states/`.
- Text: `script/` (JSON). Tables: `tbl/`. Glossary: `glossary.md`. RE notes index: `docs/re/README.md`. Fonts and their licences: `docs/fonts.md`.

## Rulings
- Edit source files (.py .lua .asm .tbl .json) only with the file-edit tool; scripts here read and analyse, never `.replace()` and write back.
- Subagents: dispatch the `.claude/agents/` types (translator, reviewer, visual-qa, playtester), never general-purpose.
- The user's decisions, with the options and reasons: `docs/decisions.md`. Read it before asking the user anything; add each new ruling there the same session.
- Player bug reports: GitHub issues (`gh issue list --label bug`). Copy the attached save into `work/states/`, reproduce in the emulator, fix, commit with `Fixes #N`, and update `docs/status.md`.
- Cold boot reaches the title at ~1450 frames; no save -> Start goes straight to name entry.

## Status
`docs/status.md`: done, next, open bugs. Update it at the end of every session.
