Seijuu Maden: Beasts & Blades - English translation patch v{version}
=====================================================================

Unofficial English fan translation of Seijuu Maden: Beasts & Blades (Super Famicom).
All text is in English: dialogue, menus, item/skill/beast names, the battle and world-map command menus,
the poem, the endings and the staff credits.

Patching
--------
Apply {patch} to your own dump of the Japanese cartridge with any BPS patcher
(Floating IPS / flips, beat, or https://www.marcrobinson.co.uk/rompatcher or RomPatcher.js in a browser).

Base ROM (No-Intro: Seijuu Maden - Beasts & Blades (Japan)), headerless:
  Size   {o[size]} bytes
  CRC32  {o[crc]}
  MD5    {o[md5]}
  SHA-1  {o[sha1]}

Patched ROM:
  Size   {p[size]} bytes
  CRC32  {p[crc]}
  SHA-1  {p[sha1]}

A ROM with a 512-byte copier header (2,621,952 bytes) must have the header removed first.

Playing
-------
Tested in Mesen (MesenCE 2.2.1). Start the patched game from a cold boot: savestates made with the Japanese
game or an older patch carry the old text code and will show garbage.

Known issues
------------
- A few long beast and enemy names are cut at 13 letters on status screens (they show in full in battle and shops).
- The status-screen header for an army is abbreviated ("№ N King").
Report anything else at https://github.com/minhnhattonthat/seijuu-maden-beasts-blades-en/issues
(a savestate or screenshot helps most).

Credits
-------
Translation, hacking and tools: minhnhattonthat, with extensive AI assistance (Claude by Anthropic).
Corrections are very welcome.

This is an unofficial fan work, not affiliated with the original developers or publishers.
Seijuu Maden: Beasts & Blades is (c) BPS / ORG / MediaWorks. Do not distribute pre-patched ROMs.
