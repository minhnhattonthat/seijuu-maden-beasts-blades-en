# Seijuu Maden: Beasts & Blades English translation

Unofficial English fan translation of **Seijuu Maden: Beasts & Blades** (聖獣魔伝 ビースト&ブレイド; Super Famicom,
BPS / ORG / MediaWorks): the source text and tools that build the patch.

**Just want to play?** Download the patch from [Releases](../../releases) and follow its README. This repository holds
no game data you can play; you need your own dump of the Japanese game.

**Found a bug?** [Report it](../../issues/new/choose): untranslated text, typos, overflow, crashes. Attaching a savestate
helps most.

## Translation status

| Part | Status |
|---|---|
| Dialogue / story | Translated |
| Menus, item/skill/beast names, shops, status screens | Translated |
| Battle and world-map command menus (graphics) | Translated |
| Title screen | Translated (the logo's 聖獣魔伝 romanised as "Seijuu Maden") |
| Intro crawl and poem | Translated (intro keeps the game's own English verses; its Japanese subtitles are removed) |
| Name entry | Translated (English letter grid) |
| Endings and staff credits | Translated |

Known issues: a few long beast/enemy names are cut at 13 letters on status screens; the army header is abbreviated
("№ N King"). Start from a cold boot: old savestates show garbage.

## What's here

| Path | What it is |
|---|---|
| `script/` | Every text block: original Japanese and English. Translation fixes go here. |
| `glossary.md` | Binding names, terms and style rules. |
| `tools/` | Python build chain: extract, insert, lint, release; `tools/asm/` engine hooks (asar), `tools/debug/` scene warps. |
| `tests/` | pytest suite (needs the ROM). |
| `fonts/` | The English 6 px dialogue font and 8x8 menu font, drawn for this project. |
| `docs/re/` | Reverse-engineering notes. |
| `docs/decisions.md`, `docs/status.md` | Rulings with their reasons; current progress and open bugs. |
| `docs/fonts.md` | Fonts used and their licences. |
| `AGENTS.md` | Instructions for coding agents (`CLAUDE.md` points to it). |
| `.claude/agents/` | Subagent types (translator, reviewer, visual QA, playtester) with only the tools each needs. |

## Build your own patched ROM

Needs Python 3.12+, [asar 1.91](https://github.com/RPGHacker/asar/releases/download/v1.91/asar191.zip) in
`tools/asar/`, and your own dump of the Japanese game.

```sh
git clone https://github.com/minhnhattonthat/seijuu-maden-beasts-blades-en
cd seijuu-maden-beasts-blades-en
# copy your dump to: rom/Seijuu Maden Beasts & Blades (Japan).sfc
#   (2,621,440 bytes, SHA-1 e0067694f59e5190bcf02c92ddf016ec3c55fb7a; the build refuses any other dump, see rom.sha1)
python -X utf8 tools/build.py                          # -> build/seijuu_en.sfc
python -X utf8 tools/check.py                          # tests + text lint
```

## Support

If you enjoy this translation, you can support my work on Ko-fi:

[![Support me on Ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/minhnhattonthat)

## Licence

Tools, fonts and English translation: MIT. The original Japanese text in `script/` is the rights holders' and is
included only so the translation can be checked against it. Seijuu Maden: Beasts & Blades is (c) BPS / ORG /
MediaWorks; this project is not affiliated with them. Do not share patched ROMs.

The translation was made with extensive AI assistance (Claude by Anthropic). Corrections are very welcome.
