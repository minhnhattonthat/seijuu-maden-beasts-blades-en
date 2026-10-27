# Glossary - Seijuu Maden: Beasts & Blades

Binding for every translator and reviewer. Agents propose additions in reports; only the controller edits this file.
`tools/batches.py check` fails a line whose JP has a katakana/kanji term below but whose English lacks the EN form
(whole-run match), or that uses a spelling from the Avoid column. Hiragana-only rows are menu labels, not linted.

## Rulings (asked of the user once; options and reasons in docs/decisions.md)
- Honorifics: kept, hyphenated (Lang-sama, Zona-dono, Elma-san). Name order: Western (D1). 姫 -> Princess X,
  神父 -> Father X, 殿下 -> Your Highness.
- Romanisation source: the game's own English (title, intro crawl, credits), else an earlier fan patch (none found),
  else Hepburn without macrons (D2). Most names here are European (German-flavoured): spell them as the European
  name they transcribe (ルントシュテット Rundstedt, ローレンツ Lorenz), not Hepburn.
- Credits: English (D3; the staff names are already English in the ROM).
- Register: plain modern fantasy English, light JP flavour (honorifics). Sound effects: *Bong* style words in
  plain text (ゴーン -> Bong, bong...).
- Abbreviations: never to fit (D4); report the line as LONG instead.

## Style rules
- Punctuation map: 「」 -> "...", 『』 -> '...' (titles, quoted names), …/・・・ -> ..., ！？ -> ?!, ー long vowels
  (ハーハハハッ) -> Ha ha ha ha!
- Dialogue lines start with the speaker's name on its own line (`Lang / "Well done..."`): keep that layout, the
  name translated per this glossary. The wrap tool indents a quote's continuation lines by one space.
- Katakana-heavy speech is a voice, not a name: the foreign merchant (デスゥ, WAO!, SORRY!) speaks broken,
  sing-song English with his English words kept; monsters/demi-folk who mix katakana in (エルマサンデテイッタアト)
  speak short, broken English. Kansai-ben (ほな、まひょか) -> folksy, casual English.
- The game's own English words (YOU HAVE LITTLE OR NOTHING!, SOUNDS GOOD!) stay as written.

## Characters
| JP | EN | max | notes | Avoid |
|---|---|---|---|---|
| ガイアス | Gaius | 8 | Dark-side rival; knows the hero | Gaias |
| ウオレス | Wallace | 8 | | |
| エルマ | Elma | 8 | | |
| バッヘルベル | Bachelbel | 9 | | Pachelbel |
| ウエルトハイム | Wertheim | 8 | | |
| テュイエ | Tuie | 8 | | |
| ハネス | Hannes | 8 | | |
| シュルツ | Schulz | 8 | | |
| マイケンバウム | Meikenbaum | 10 | | |
| ラディゲ | Radiguet | 8 | | |
| アークマスター | Arch Master | 11 | | |
| ラビウス | Rabius | 8 | | |
| ローレンツ | Lorenz | 8 | | |
| ネイピア | Napier | 8 | | |
| アイベスフェルト | Eibesfeldt | 10 | | |
| ブライアン | Brian | 8 | | |
| シャルコー | Charcot | 8 | | |
| ゾナ | Zona | 8 | | |
| ボルク | Bork | 8 | | |
| エカース | Ekers | 8 | | |
| ウイルソン | Wilson | 8 | | |
| パル | Pal | 8 | | |
| プラナ | Prana | 8 | | |
| ルントシュテット | Rundstedt | 9 | the hero's advisor | |
| ラング | Lang | 8 | High Priest of Light (光の司祭長) | |
| モナ | Mona | 8 | | |
| アリアンナ | Arianna | 8 | princess | |
| シンシア | Cynthia | 8 | | |
| ルクレール | Leclerc | 8 | | |
| イーブリン | Evelyn | 8 | | |
| エリンシェ | Erinshe | 8 | | |
| シュアリー | Shuary | 8 | ノモ・シュアリー = Nomo Shuary (baseball gag: Nomo, Major League, Play ball) | |
| ヒダリー | Hidary | 8 | | |
| オデル | Odell | 8 | | |
| リムカ | Rimka | 8 | | |
| カロン | Charon | 8 | | |
| サリア | Saria | 8 | | |
| メネーウ | Meneu | 8 | | |
| リリス | Lilith | 8 | | |
| リファール | Rifar | 8 | | |
| グラプダー | Grapder | 8 | | |
| セガアー | Segaar | 8 | セガアー神父 = Father Segaar | |
| ハイーネ | Haine | 8 | | |
| カリスト | Callisto | 8 | | |
| フィリップス | Phillips | 8 | | |
| ラバルス | Rabals | 8 | | |
| ターロ | Taro | 8 | | |
| ミリー | Millie | 8 | | |
| アルバ | Alba | 8 | | |
| アミー | Amy | 8 | | |
| ハフマン | Huffman | 8 | | |
| パウエル | Powell | 8 | | |
| バルナイオス | Barnaios | 8 | Dark-side lord of the castle (闇に仕えしもの) | |
| ストラボン | Strabo | 8 | | |
| ゼジル | Zejil | 8 | | |
| エリス | Eris | 8 | | |
| ジェイド | Jade | 8 | | |
| ラブレス | Loveless | 8 | | |
| ルベク | Lubek | 8 | | |
| アンソニィ | Anthony | 8 | | |
| 至高神 | the Supreme God | | | |
| 光の女神 | Goddess of Light | | 女神様 alone -> the Goddess / Lady Goddess | |
| 闇の女神 | Goddess of Darkness | | | |
| 死神 | Death | | the reaper character; speaks formally | Grim Reaper |

## Places
| JP | EN | max | notes | Avoid |
|---|---|---|---|---|
| メイシルヴァ | Meisilva | 16 | メイシルヴァ城 Meisilva Castle | Melshiva |
| ルーナス | Lunas | 16 | ルーナス城 Lunas Castle | |
| 山賊砦 | Bandit Fort | 16 | | |
| ダスカー | Dusker | 16 | ダスカー城 Dusker Castle | |
| タイタンの海城 | Titan Sea Castle | 16 | | |
| 海底神殿 | Undersea Temple | 16 | | |
| ソーンの塔 | Thorn Tower | 16 | | |
| デスパーの塔 | Desper Tower | 16 | | |
| アケアニア | Akeania | 16 | | |
| アナキア | Anakia | 16 | | |
| アルフェニア | Alfenia | 16 | | |
| ウルファニア | Ulfania | 16 | | |
| オーディンセ | Odinse | 16 | | |
| カールスザーク | Karlszaak | 16 | | |
| カールメイヤー | Karlmeyer | 16 | | |
| ゴーム | Gorm | 16 | | |
| スタボンシー | Stabonsea | 16 | | |
| ストス | Stos | 16 | | |
| パイロニア | Pyronia | 16 | | |
| バファイアム | Bafaiam | 16 | | |
| ヘサ | Hesa | 16 | | |
| ボイル | Boyle | 16 | | |
| メロー | Mellow | 16 | | |
| ラクサス | Raksas | 16 | | |
| ランデンバウム | Landenbaum | 16 | | |
| ルーク | Rook | 16 | | |
| ルンド | Lund | 16 | | |
| ロンシャオ | Longxiao | 16 | | |
| ゴルーブ | Golub | 16 | | |
| ギガン | Gigan | 16 | | |
| ラヴィウス | Ravius | 16 | | |
| リーロイル | Leeroyle | 16 | | |
| ヘビトカゲ | lizardfolk | 16 | the race (snake-lizard people); ヘビトカゲ族の村 Lizardfolk Town | |
| 海賊村 | Pirate Village | 16 | | |
| ノスク | Nosk | 16 | | |
| タルティウム | Tartium | 16 | | |
| マーメイド | mermaid | 16 | マーメイドの村 Mermaid Village | |
| 人さらいの洞窟 | Kidnappers' Cave | 16 | | |
| ベルン | Bern | 16 | | |
| ヘクトス | Hectos | 16 | ヘクトス郊外 Hectos Outskirts | |
| ルカ | Luca | 16 | | |
| 森の家 | Forest House | 16 | | |
| フェナン | Fenan | 16 | | |
| 霊園 | Cemetery | 16 | | |
| ウルン | Ulun | 16 | | |
| 天族の村 | Sky Folk Village | 16 | | |
| サイの迷宮 | Sai Labyrinth | 16 | | |
| ドラゴンの洞窟 | Dragon Cave | 16 | | |
| 古の洞窟 | Ancient Cave | 16 | | |
| 魔族の洞窟 | Demon Cave | 16 | | |
| オーガーの洞窟 | Ogre Cave | 16 | | |
| 炎の目 | Eye of Flame | 16 | | |
| 女神達の神殿 | Goddess Temple | 16 | | |
| 地底洞窟 | Underground Cave | 16 | | |
| 森の廃城 | Ruined Castle | 16 | | |
| 産卵地 | Spawning Ground | 16 | | |
| 闇エルフの洞窟 | Dark Elf Cave | 16 | | |
| オーディンの山 | Mt. Odin | 16 | | |
| 双頭蛇 | Twin Serpent | 16 | | |
| フェアリーリング | Fairy Ring | 16 | | |
| ドラゴンの森 | Dragon Forest | 16 | | |
| ヘロイ砂漠 | Heroi Desert | 16 | | |
| タイタンの神殿 | Temple of Titan | 16 | | |
| セイレーンの島 | Siren Isle | 16 | | |
| ハイネス神殿 | Heines Temple | 16 | | |
| 魔女の森 | Witch's Forest | 16 | | |
| 封印の洞窟 | Sealed Cave | 16 | | |
| 次元の扉 | Dimension Door | 16 | | |
| 結界の洞窟 | Barrier Cave | 16 | | |
| 封印の門 | Sealed Gate | 16 | | |
| 転生の洞窟 | Cave of Rebirth | 16 | | |

## Story terms
| JP | EN | max | notes | Avoid |
|---|---|---|---|---|
| 聖獣王 | Holy Beast King | 20 | the 11 Light-side kings; the hero is one. 第N聖獣王 -> Nth Holy Beast King (list), Holy Beast King No. {num} (variable) | Sacred Beast King |
| 魔獣王 | Demon Beast King | 20 | the 11 Dark-side kings | Evil Beast King |
| 獣王 | Beast King | | either side | |
| 聖魔戦争 | Holy-Demon War | | | |
| 光対闇 | Light vs. Dark | | | |
| 第一の旗 | First Banner | | the signal that starts the war (rung like a bell) | First Flag |
| 伝説の獣 | Legendary Beast | | | |
| シロナガスクジラ | Blue Whale | | giant monster wrecking coastal towns (Rook, Mellow); 'Blue Whale' when quoted | |
| 光の司祭長 | High Priest of Light | | Lang | |
| ビーストマスター | Beast Master | | | |
| 獣皇士 | Beast Sovereign | | Akeania's champion Beast Master | |
| 外法師 | heretic mage | | 外法 = heretic art; 反魂の外法 = the heretic art of soul-summoning | |
| 亜族 | demi-folk | | half-blood races (demon or elf blood) | |
| 魔族 | demon | | demons / Demon Cave | |
| 天族 | Sky Folk | | winged race | |
| ケモノの剣 | Beast Sword | | quest item (ケモノのケン) | |
| コロン | Koron | | beast; キングコロン King Koron | Colon |
| アークデーモン | Archdemon | | beast and enemy | Diabolos |
| 女神の果実 | Goddess Fruit | | item めがみのかじつ too | |
| ズーカン | Zukan | | beast-lore old man (pun on 図鑑) | |
| ビーストパック | Beast Pack | | | |
| 光の法 | Law of Light | | 人間は光の法で治める -> Humanity shall obey the Law of Light. | |
| 冥府 | the Underworld | | | |
| 現世 | the mortal world | | | |
| 騎士団 | knights | | X騎士団 -> the X Knights | |
| シルヴァラ騎士団 | Silvara Knights | | Rundstedt's order (Meisilva) | |
| こおりのしずく | Ice Drop | | quest item, Evil Eye's cave | |
| イービルアイ | Evil Eye | | boss | |
| 吟遊詩人 | bard | | | |
| 老婆 | Old Woman | | speaker label | |
| 市長 | Mayor | | speaker label | |
| 神父 | Father | | priest | |

## Items / skills / menu terms
| JP | EN | max | notes | Avoid |
|---|---|---|---|---|
| ちから | Strength | 8 | status stat (labels in tools/build.py `STATS`) | Str |
| たいりょく | Stamina | 8 | | |
| すばやさ | Agility | 8 | | Speed |
| ちせい | Wisdom | 8 | | Int |
| やせい | Instinct | 8 | beasts' stat in place of Wisdom | |
| じゅうりょう | Weight | 7 | | |
| こうげき | Attack | 7 | | |
| ぼうぎょ | Defense | 7 | | |
| きどうりょく | Move | 7 | movement range on the battle grid | Mobility (too long) |
| ぶき / ぼうぐ | Weapon / Armor | 7 | equip rows "Armor 1".."Armor 3" | |
| ぶきレベル | LV | 2 | weapon level, "LV:" | |
| りんせつ / かいふく / えんぽう / とくべつ | Melee / Heal / Ranged / Special | 7 | beast skill ranges | |
| どく | Poison | 7 | | |
| じゅうぞく | Loyal | 5 | beast/master row label, the bar starts right after it | |

## Decisions from earlier batches
- <batch> <JP> -> <EN> (reason)
