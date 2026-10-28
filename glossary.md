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
| エカース | Ekers | 8 | female (she) | |
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
| 第1の王 | First King | | form of address for the 1st Holy Beast King | |
| 獣の剣 | Beast Sword | | same item as ケモノの剣 | |
| 第二の旗 | Second Banner | | | |
| 女神のクリスタル | Goddess Crystal | | | |
| リファールの塔 | Rifar Tower | | | |
| ハイネス | Heines | | the mountain; Heines Temple | |
| クルト | Kurt | 8 | female adventurer from Leeroyle | |
| 祝福 | bless | | blessing, blessed; also the purple lightning when a king is born | |
| シオシオ草 | Shioshio Grass | | | |
| 翼の民 | Winged Folk | | | |
| 暗がりの野 | Gloomy Fields | | | |
| ジミー | Jimmy | 8 | | |
| ルーナスの剣 | Sword of Lunas | | quest sword | |
| ルーナス騎士団 | Lunas Knights | | | |
| トーマス | Thomas | | サー・トーマス・フィリップス Sir Thomas Phillips; フィリップス司令 Commander Phillips | |
| ブリッジス | Bridges | 8 | | |
| 司祭 | Priest | | speaker label | |
| シスター | Sister | | 修道女X -> Sister X (Sister Saria); 修道女 alone -> nun (not linted) | |
| ポチ | Spot | | a soldier's griffon | |
| エルフの秘宝 / エルフの王冠 | Elven Treasure / Elven Crown | | quest items (data names keep "Elf X") | |
| 魔道の杖 / 魔導の杖 | Staff of Sorcery / Staff of Sorcery | | | |
| 時の凍る平原 | Plain of Frozen Time | | | |
| スノーフェスティバル | Snow Festival | | | |
| 詩人 | Poet | | speaker label (Odell); 吟遊詩人 is the bard | |
| グリーンビースト | Green Beast | | activist group | |
| カッパ | kappa | | common noun; signs signed "-- The Kappa" | |
| 力の王冠 | Crown of Power | | Titan superweapon | |
| ドラグーン | Dragoon | | Pal's clan | |
| ブーケ | Bouquet | | Pal's beast | |
| ルホウキ | Ruhoki | 8 | Winged Folk leader | |
| 闇の司祭 | Priest of Darkness | | Eris | |
| 闇の教え / 光の教え | Teachings of Darkness / Teachings of Light | | | |
| ベーオウルフ / ドラゴンバスター | Beowulf / Dragon Buster | | | |
| ガラッシュ | Galash | 8 | 剣聖ガラッシュ Galash, the Sword Saint | |
| フレイ | Frey | 8 | gender unknown so far | |
| ブヒュテンヒルト | Buchtenhild | | Frey's beast | |
| あやしい商人 | Shady Merchant | | | |
| ラバルス6世 / ラバルス7世 | Rabals VI / Rabals VII | | | |
| スクラップ / ジャン | Scrap / Jean | 8 | Landenbaum | |
| カーハ・ラー | Kaha Ra | | card player, Akeania | |
| 近衛隊 | Royal Guard | | | |
| ワイズマン | Wiseman | | ロバート・ワイズマン Robert Wiseman, Blue Whale expert | |
| ムツジロウ | Mutsujiro | | ムツさん Mutsu-san, beast breeder | |
| ひなぎくの戦士 | Daisy Warrior | | | |
| トロン / ウンヌ / ステラ | Tron / Unnu / Stella | 8 | | |
| 結界 | barrier | | | |
| 生命の女神 / 大地の女神 | Goddess of Life / Goddess of the Earth | | | |
| 新しき女神 / 古の女神 | New Goddess / Ancient Goddess | | | |
| 闇の法 | Law of Darkness | | | |
| スネイランド | Sneyland | | | |
| 冥王 | Lord of the Underworld | | 冥府の王 king of the Underworld | |
| リサ | Lisa | 8 | Tsunami's sister | |
| 死神ルベク | Death Lubek | | speaker label | |
| バロックス | Barocks | | ボルク・バロックス Bork Barocks (ending card) | |
| カースン | Carson | | エカース・カースン Ekers Carson | |
| カクリ | Kakuri | | ウイルソン・カクリ Wilson Kakuri | |
| ガラパゴス | Galapagos | | Alba's father | |
| リゲス / ローヒーシー / ジーグ / ターナリ | Riges / Lohisea / Sieg / Turnery | | ending cards: Riges Lorenz, Napier Lohisea, Sieg Eibesfeldt, Brian Turnery | |
| ビーク / フェイドリー | Beek / Faidley | | Beek Charcot, Zona Faidley | |
| ブラックダイアモンド | Black Diamond | | statue holding Prana's soul | |
| 獣魔 | Beast Fiend | | 獣魔オーディン Odin, the Beast Fiend | |
| 婿殿 | son-in-law | | | |
| 占い師 | fortune-teller | | | |
| 白の森 / 黒の森 / 銀の森 | White Forest / Black Forest / Silver Forest | | | |
| 竜族 | dragon folk | | | |
| 天界 / 下界 | the heavens / the world below | | | |
| 忘れられた村 | Forgotten Village | | | |
| 光の魔術師 | sorcerer of Light | | | |
| トマソン | Thomason | 8 | hired swordsman | |
| 疾風の剣士 | Swordsman of the Gale | | | |
| 市長補佐 | Deputy Mayor | | | |
| クマ殺し | Bear-Slayer | | クマ殺しのカリスト Callisto the Bear-Slayer | |
| けむけむ | Smokey | | | |
| パラピー | Parapi | | パラピーちゃん Parapi-chan, a pet beast | |
| 光の司祭 | Priest of Light | | Mona's title (Mona, Priest of Light); 光の司祭長 is Lang | |

Notes (not linted): オカマ -> "drama queen" (Wertheim's campy voice, never a slur; the mayor in E3559B is "drag queen");
ゼジルお父さん/とうちゃん -> Papa Zejil / Daddy Zejil (Father X is the priest form); 詩人 Poet (Odell) vs
吟遊詩人 Bard (may be two different bards); ドラグーン Dragoon(s), 竜騎士 dragon knights; 海賊 Pirate, 魔女 Witch,
聖獣 Holy Beast, マーメイド Mermaid as speaker labels; 地下世界 = 地底世界 underground world; ミコ/みこ priestess; 銀のエルフ/光のエルフ/闇のエルフ silver/light/dark elf (elves); 死神ども reapers; the lesser Deaths' ナリ tic -> archaic
thou/thee ("thou ... forsooth" in b089, ", verily" in b094: unify in polish).

| 魂返しの秘法 | secret rite of soul-returning | | the Light-side name for 反魂の外法 | |
| 地底世界 | underground world | | | |
| ババ / おババ | Granny / Granny | | the Old Woman's name for herself | |
| ツナミ | Tsunami | 8 | boss of the thieves | |
| ブラックバード | Blackbird | | the thieves' gang | |
| 戦いの女神 | Goddess of Battle | | | Goddess of War |
| マイマイの騎士 | Snail Knight | | Brian's nickname | |
| ペルナ | Perna | | ペルナ・パル Perna Pal | |
| 従属度 | obedience | | beast stat in dialogue (label: Loyal) | |
| 野聖 | Wild Saint | | pun on 野生; Jade's title Wild Saint Knight | |
| 闇の司祭長 | High Priest of Darkness | | Barnaios | |
| 聖王 | Holy King | | prophecy poem | |

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
| 特訓 | train | | training, trained; ranch: とっくんちゅう Training, とっくんしゅうりょう Trained | |
| ちょうきょう | Taming | | 調教 in dialogue = tame / taming / tamed (not linted: no one substring); ranch: ちょうきょうちゅう Taming, ちょうきょうしゅうりょう Tamed | |
| あずかり | Kept | | ranch status | |
| 守備隊 | garrison | | a town's garrison; the world-map info box label is "Guard:" (C0BAF7 slot: 11 chars, colons cost extra) | |
| 支持率 | support | | a town's support rating; info box label "Favor" (no room for "Support:") | |

Formations (labels split over two lines, so not linted): フォーメーション Formation; チャリオット Chariot, スクウェア Square,
ドラゴン Dragon, ハーフムーン Half Moon, ナイトフォース Knight Force, アタックフォース Attack Force, ダイヤモンド Diamond,
グリフォン Griffon.

## Buildings and town menus
| JP | EN | max | notes | Avoid |
|---|---|---|---|---|
| さかば / かじや / どうぐや / きょうかい | Tavern / Smithy / Items / Church | 8 | town building list | |
| ビーストいちば / とうぎじょう / やどや | Beast Market / Arena / Inn | 8 | 酒場/鍛冶屋/道具屋/教会/闘技場/宿屋 in dialogue: tavern, smithy, item shop, church, arena, inn | |
| しゅうかいじょう / ひろば / みんか / しゅじんこうんち / しろ / ごうてい | Hall / Plaza / House / Home / Castle / Mansion | 8 | | |
| 酒場 / 鍛冶屋 / 道具屋 / 教会 / 宿屋 | tavern / smith / shop / church / inn | | lint terms for dialogue | |

## Data names (generated: items, beasts, enemies, skills)
The game's own names, binding in dialogue. Regenerate with `python -X utf8 tools/glossary_names.py --write`
after renaming one in `script/`; hand rows above win over these.

<!-- names:begin (tools/glossary_names.py) -->

### Weapons
| JP | EN | max | notes | Avoid |
|---|---|---|---|---|
| おれたたんけん | Broken Dagger | | | |
| おれたけん | Broken Sword | | | |
| おれたおの | Broken Axe | | | |
| おれたメイス | Broken Mace | | | |
| おれたつえ | Broken Staff | | | |
| おれたやり | Broken Spear | | | |
| おれたフレイル | Broken Flail | | | |
| おれたまけん | Broken Demon Blade | | | |
| キッチンナイフ | Kitchen Knife | | | |
| ブロンズダガー | Bronze Dagger | | | |
| ダガー | Dagger | | | |
| はばひろダガー | Broad Dagger | | | |
| カタール | Katar | | | |
| ククリ | Kukri | | | |
| シルバーダガー | Silver Dagger | | | |
| ハンターナイフ | Hunting Knife | | | |
| グラディウス | Gladius | | | |
| ホーリーダガー | Holy Dagger | | | |
| はでなナイフ | Flashy Knife | | | |
| プラチナダガー | Platinum Dagger | | | |
| ボーディー | Bodkin | | | |
| ダーク | Dirk | | | |
| ショートソード | Short Sword | | | |
| ブレイカー | Breaker | | | |
| あいくち | Aikuchi | | | |
| トリプルダガー | Triple Dagger | | | |
| つらぬきナイフ | Piercing Knife | | | |
| クリス | Kris | | | |
| ファイアダガー | Fire Dagger | | | |
| アイスダガー | Ice Dagger | | | |
| ウインドダガー | Wind Dagger | | | |
| サンダーダガー | Thunder Dagger | | | |
| ブロンズのけん | Bronze Sword | | | |
| おうごんのけん | Golden Sword | | | |
| ブロードソード | Broadsword | | | |
| レイピア | Rapier | | | |
| まぞくのけん | Demon Sword | | | |
| シミター | Scimitar | | | |
| みずちなぎ | Wyrmcutter | | | |
| ロングソード | Longsword | | | |
| シャムシール | Shamshir | | | |
| サーベル | Saber | | | |
| オーガーキラー | Ogre Killer | | | |
| きせきのけん | Miracle Sword | | | |
| ルーンソード | Rune Sword | | | |
| らいこうのけん | Lightning Sword | | | |
| かぜきりのけん | Windcutter | | | |
| フリーズソード | Freeze Sword | | | |
| ナイトセイバー | Knight Saber | | | |
| ファルシオン | Falchion | | | |
| ドラゴンのきば | Dragon Fang | | | |
| きらめきのけん | Gleaming Sword | | | |
| ブレイズソード | Blaze Sword | | | |
| フレイソード | Frey Sword | | | |
| シグルドソード | Sigurd Sword | | | |
| レーヴァテイン | Laevateinn | | | |
| グレートソード | Greatsword | | | |
| ちからのけん | Power Sword | | | |
| カリバーン | Caliburn | | | |
| なた | Hatchet | | | |
| ハンドアックス | Hand Axe | | | |
| ダブルアックス | Double Axe | | | |
| フランシスカ | Francisca | | | |
| しっぷうのおの | Gale Axe | | | |
| セルティス | Celtis | | | |
| キラーアックス | Killer Axe | | | |
| トマホーク | Tomahawk | | | |
| バトルアックス | Battle Axe | | | |
| デッドバスター | Dead Buster | | | |
| きんのおの | Golden Axe | | | |
| バルティシュ | Bardiche | | | |
| ミンチメーカー | Mincemaker | | | |
| デスストーマー | Death Stormer | | | |
| デスフリーザー | Death Freezer | | | |
| ヘルクエイカー | Hell Quaker | | | |
| きんときのおの | Kintoki's Axe | | | |
| インドラのおの | Indra's Axe | | | |
| ウッドクラブ | Wood Club | | | |
| ウッドメイス | Wood Mace | | | |
| ストーンクラブ | Stone Club | | | |
| ブラジオン | Bludgeon | | | |
| ライトメイス | Light Mace | | | |
| アイアンクラブ | Iron Club | | | |
| ウォーハンマー | War Hammer | | | |
| ホーリーメイス | Holy Mace | | | |
| モール | Maul | | | |
| アイスクラブ | Ice Club | | | |
| ヘビーメイス | Heavy Mace | | | |
| パワーセプター | Power Scepter | | | |
| トールハンマー | Thor's Hammer | | | |
| ワンド | Wand | | | |
| ロッド | Rod | | | |
| スタッフ | Staff | | | |
| ファイアロッド | Fire Rod | | | |
| アイスロッド | Ice Rod | | | |
| サンダーロッド | Thunder Rod | | | |
| アイアンケイン | Iron Cane | | | |
| スタンワンド | Stun Wand | | | |
| フレイムワンド | Flame Wand | | | |
| ガイアホーン | Gaia Horn | | | |
| スノースタッフ | Snow Staff | | | |
| かなぼう | Kanabo | | | |
| ウインドロッド | Wind Rod | | | |
| ホーリーロッド | Holy Rod | | | |
| たけやり | Bamboo Spear | | | |
| ショートスピア | Short Spear | | | |
| ロングスピア | Long Spear | | | |
| !フォーシャル | Fauchard | | | |
| !ポールアック | Poleaxe | | | |
| てつのやり | Iron Spear | | | |
| きぼうのやり | Spear of Hope | | | |
| はがねのやり | Steel Spear | | | |
| ごっついやり | Hefty Spear | | | |
| パルチザン | Partisan | | | |
| きらめきのやり | Gleaming Spear | | | |
| ゲイボルグ | Gae Bolg | | | |
| トライデント | Trident | | | |
| みつばのやり | Clover Spear | | | |
| あざやかなやり | Vivid Spear | | | |
| グレイブ | Glaive | | | |
| !ポールハンマ | Pole Hammer | | | |
| ハルバード | Halberd | | | |
| ドラゴンスピア | Dragon Spear | | | |
| ダイヤスピア | Diamond Spear | | | |
| ホーリースピア | Holy Spear | | | |
| けもののやり | Beast Spear | | | |
| ズフタススピア | Zuftas Spear | | | |
| !ゼライアスス | Zeraias Spear | | | |
| ライトフレイル | Light Flail | | | |
| ヘビーフレイル | Heavy Flail | | | |
| とげのフレイル | Spiked Flail | | | |
| どうのフレイル | Copper Flail | | | |
| はがねフレイル | Steel Flail | | | |
| らいせつこん | Thunder Nunchaku | | | |
| えんせつこん | Flame Nunchaku | | | |
| れいせつこん | Frost Nunchaku | | | |
| きんのフレイル | Gold Flail | | | |
| パワーフレイル | Power Flail | | | |
| けものたたき | Beast Beater | | | |
| きょうしのむち | Teacher's Whip | | | |
| レザーウイップ | Leather Whip | | | |
| いばらのむち | Thorn Whip | | | |
| いかりのむち | Wrath Whip | | | |
| れっぷうのむち | Storm Whip | | | |
| くさりのむち | Chain Whip | | | |
| ほのおのむち | Flame Whip | | | |
| いかずちのむち | Thunder Whip | | | |
| あいのむち | Love Whip | | | |
| へびのむち | Snake Whip | | | |
| キラーウィップ | Killer Whip | | | |
| やいばのむち | Blade Whip | | | |
| たけのゆみ | Bamboo Bow | | | |
| きのゆみ | Wooden Bow | | | |
| ショートボウ | Shortbow | | | |
| ロングボウ | Longbow | | | |
| ごうせいきゅう | Composite Bow | | | |
| トルコボウ | Turkish Bow | | | |
| てつのゆみ | Iron Bow | | | |
| はがねのゆみ | Steel Bow | | | |
| しげとうゆみ | Shigeto Bow | | | |
| アルテミスボウ | Artemis Bow | | | |
| ひごゆみ | Higo Bow | | | |
| エルフのゆみ | Elf Bow | | | |
| わきゅう | Wakyu | | | |
| マジックボウ | Magic Bow | | | |
| エンジェルボウ | Angel Bow | | | |
| シルフボウ | Sylph Bow | | | |
| アポロンのゆみ | Apollo's Bow | | | |
| しんぴきゅう | Mystic Bow | | | |
| クロスボウ | Crossbow | | | |
| ボウガン | Bowgun | | | |
| しょかつきゅう | Zhuge Crossbow | | | |
| アローショット | Arrow Shot | | | |
| リピーター | Repeater | | | |
| クレーンクイン | Cranequin | | | |
| アーバレスト | Arbalest | | | |
| きのパチンコ | Wood Slingshot | | | |
| てつのパチンコ | Iron Slingshot | | | |
| きんのパチンコ | Gold Slingshot | | | |
| メタルパチンコ | Metal Slingshot | | | |
| キラーパチンコ | Killer Slingshot | | | |
| パワーパチンコ | Power Slingshot | | | |
| デススロアー | Death Thrower | | | |

### Armor
| JP | EN | max | notes | Avoid |
|---|---|---|---|---|
| ずきん | Hood | | | |
| むぎわらぼうし | Straw Hat | | | |
| さんかくぼうし | Tricorn | | | |
| きんのティアラ | Gold Tiara | | | |
| クロースヘルム | Close Helm | | | |
| バンダナ | Bandana | | | |
| しんぷのぼうし | Priest's Hat | | | |
| ティアラ | Tiara | | | |
| とりばねぼうし | Plumed Hat | | | |
| サレット | Sallet | | | |
| けがわのかぶと | Fur Helm | | | |
| ひたちがね | Hachigane | | | |
| きんのわっか | Gold Hoop | | | |
| にじのおうかん | Rainbow Crown | | | |
| サークレット | Circlet | | | |
| にじのティアラ | Rainbow Tiara | | | |
| てっかめん | Iron Mask | | | |
| ピロス | Pilos | | | |
| なべがたかぶと | Pot Helm | | | |
| ハットヘルム | Hat Helm | | | |
| オープンヘルム | Open Helm | | | |
| グリークヘルム | Greek Helm | | | |
| かぶと | Helmet | | | |
| かいぞくかぶと | Pirate Helm | | | |
| なんばんかぶと | Nanban Helm | | | |
| スケイルヘルム | Scale Helm | | | |
| チェインヘルム | Chain Helm | | | |
| おおかぶと | Great Helm | | | |
| ナイトヘルム | Knight Helm | | | |
| ドラゴンヘルム | Dragon Helm | | | |
| エギルヘルム | Aegir Helm | | | |
| ローブ | Robe | | | |
| あさのふく | Linen Garb | | | |
| ジプシーのふく | Gypsy Garb | | | |
| ぼうかんふく | Winter Garb | | | |
| アザラシコート | Sealskin Coat | | | |
| みずぎ | Swimsuit | | | |
| もめんのふく | Cotton Garb | | | |
| ぶどうぎ | Martial Arts Gi | | | |
| きふじんのふく | Lady's Gown | | | |
| けがわのふく | Fur Garb | | | |
| けがわのコート | Fur Coat | | | |
| エルフのふく | Elf Garb | | | |
| ほうい | Vestments | | | |
| ウールのふく | Wool Garb | | | |
| キルト | Quilted Armor | | | |
| キルボアール | Cuir Bouilli | | | |
| ぬののよろい | Cloth Armor | | | |
| ソフトレザー | Soft Leather | | | |
| ハードレザー | Hard Leather | | | |
| ウッドアーマー | Wood Armor | | | |
| にんじゃふく | Ninja Garb | | | |
| リングメイル | Ring Mail | | | |
| チェインメイル | Chain Mail | | | |
| スケイルメイル | Scale Mail | | | |
| モーモーつなぎ | Moo-Moo Suit | | | |
| かわのむねあて | Leather Breastplate | | | |
| ミスリルよろい | Mithril Armor | | | |
| プレートコート | Plate Coat | | | |
| おおよろい | Great Armor | | | |
| ブレストメイル | Breast Mail | | | |
| てつのむねあて | Iron Breastplate | | | |
| プレートメイル | Plate Mail | | | |
| ガウスアーマ | Gauss Armor | | | |
| はがねのよろい | Steel Armor | | | |
| マジックメイル | Magic Mail | | | |
| スーツアーマー | Suit Armor | | | |
| ドラゴンメイル | Dragon Mail | | | |
| レザーシールド | Leather Shield | | | |
| ウッドシールド | Wood Shield | | | |
| バックラー | Buckler | | | |
| きんのたて | Gold Shield | | | |
| むふうのたて | Windless Shield | | | |
| ほのおのたて | Flame Shield | | | |
| アイスシールド | Ice Shield | | | |
| りゅうのうろこ | Dragon Scale | | | |
| てつのたて | Iron Shield | | | |
| はがねのたて | Steel Shield | | | |
| いくさのたて | War Shield | | | |
| ウインシールド | Wind Shield | | | |
| かいぞくのたて | Pirate Shield | | | |
| エッグシールド | Egg Shield | | | |
| かちどきのたて | Victory Shield | | | |
| ガイアシールド | Gaia Shield | | | |
| カイトシールド | Kite Shield | | | |
| クロスシールド | Cross Shield | | | |
| タワーシールド | Tower Shield | | | |
| アテナのたて | Athena's Shield | | | |
| ガイアリング | Gaia Ring | | | |
| ぎんのうでわ | Silver Bracelet | | | |
| ふみんのうでわ | Sleepless Bracelet | | | |
| ルビーのうでわ | Ruby Bracelet | | | |
| サーコート | Surcoat | | | |
| まもりのマント | Ward Cloak | | | |
| くろマント | Black Cloak | | | |
| プラチナリング | Platinum Ring | | | |
| パワーバンド | Power Band | | | |
| ラッパのリング | Trumpet Ring | | | |
| むてきのリング | Invincible Ring | | | |
| さんごのリング | Coral Ring | | | |
| トパーズリング | Topaz Ring | | | |
| エルフのリング | Elf Ring | | | |
| ネコのリング | Cat Ring | | | |
| ルーンのリング | Rune Ring | | | |
| まもりのリング | Ward Ring | | | |
| プラナのまもり | Prana's Ward | | | |
| エーバリング | Eva Ring | | | |
| ゴッデスリング | Goddess Ring | | | |

### Items
| JP | EN | max | notes | Avoid |
|---|---|---|---|---|
| きのや | Wood Arrow | | | |
| てつのや | Iron Arrow | | | |
| ぎんのや | Silver Arrow | | | |
| きのえだ | Branch | | | |
| バーストアロー | Burst Arrow | | | |
| ポイズンアロー | Poison Arrow | | | |
| フリーズアロー | Freeze Arrow | | | |
| サンダーアロー | Thunder Arrow | | | |
| スリープアロー | Sleep Arrow | | | |
| キュアアロー | Cure Arrow | | | |
| ヘルスアロー | Health Arrow | | | |
| いやしのや | Healing Arrow | | | |
| アポロンアロー | Apollo Arrow | | | |
| てつのたま | Iron Ball | | | |
| なまりのたま | Lead Ball | | | |
| スプリンター | Splinter | | | |
| マジックボール | Magic Ball | | | |
| きのブーメラン | Wood Boomerang | | | |
| ばくちく | Firecracker | | | |
| ウルフのきば | Wolf Fang | | | |
| しゅりけん | Shuriken | | | |
| ダート | Dart | | | |
| くない | Kunai | | | |
| こいし | Pebble | | | |
| Mトパーズ | M Topaz | | | |
| Mジルコン | M Zircon | | | |
| Mジェイド | M Jade | | | |
| Mルビー | M Ruby | | | |
| Mアクアマリン | M Aquamarine | | | |
| てつブーメラン | Iron Boomerang | | | |
| きずぐすり | Salve | | | |
| きずぐすり2 | Salve 2 | | | |
| めんそエーテる | Mentho-Ether | | | |
| ロイヤルゼリー | Royal Jelly | | | |
| Sきずぐすり | S Salve | | | |
| ヒールメダル | Heal Medal | | | |
| 36きんし | 36 Unused | | | |
| ソーマ | Soma | | | |
| ふしぎなつの | Mystic Horn | | | |
| どくけし | Antidote | | | |
| きつけぐすり | Smelling Salts | | | |
| ほしのこな | Stardust | | | |
| ごうらいおん | Roaring Thunder | | | |
| ほうおうのはね | Phoenix Feather | | | |
| ほうおうのめ | Phoenix Eye | | | |
| マムシドリンク | Viper Drink | | | |
| めがみのまもり | Goddess's Ward | | | |
| ときのかがみ | Time Mirror | | | |
| ひかりのふだ | Light Seal | | | |
| せいしょうせき | Holy Crystal | | | |
| ホーリーオーブ | Holy Orb | | | |
| ひかりのたま | Light Gem | | | |
| かえんのふだ | Flame Seal | | | |
| えんしょうせき | Fire Crystal | | | |
| ファイアオーブ | Fire Orb | | | |
| かりゅうのたま | Fire Drake Gem | | | |
| こおりのふだ | Ice Seal | | | |
| ひょうけつせき | Frost Crystal | | | |
| アイスブリッド | Ice Bullet | | | |
| りゅうのたま | Dragon Gem | | | |
| かぜのふだ | Wind Seal | | | |
| ふうしょうせき | Wind Crystal | | | |
| ウインドオーブ | Wind Orb | | | |
| たつまきのたま | Tornado Gem | | | |
| つちのふだ | Earth Seal | | | |
| がんしょうせき | Rock Crystal | | | |
| アースオーブ | Earth Orb | | | |
| どりゅうのたま | Earth Drake Gem | | | |
| らいげきのふだ | Thunder Seal | | | |
| らいしょうせき | Thunder Crystal | | | |
| サンダーオーブ | Thunder Orb | | | |
| いかずちのたま | Thunder Gem | | | |
| ブレスカード | Bless Card | | | |
| しあわせのつえ | Staff of Happiness | | | |
| いくさのラッパ | War Trumpet | | | |
| 75きんし | 75 Unused | | | |
| ヘルメスのふえ | Hermes' Flute | | | |
| 77きんし | 77 Unused | | | |
| ほろびのふえ | Flute of Ruin | | | |
| どくのはり | Poison Needle | | | |
| あくまのかがみ | Devil Mirror | | | |
| デスニードル | Death Needle | | | |
| 82きんし | 82 Unused | | | |
| どくのくも | Poison Cloud | | | |
| 84きんし | 84 Unused | | | |
| しにがみのかま | Reaper's Scythe | | | |
| 86きんし | 86 Unused | | | |
| 87きんし | 87 Unused | | | |
| 88きんし | 88 Unused | | | |
| 89きんし | 89 Unused | | | |
| 90きんし | 90 Unused | | | |
| イリュージョン | Illusion | | | |
| ねむりのすな | Sleep Sand | | | |
| ともだちのみS | Friend Fruit S | | | |
| ともだちのみ | Friend Fruit | | | |
| ともだちのみG | Friend Fruit G | | | |

### Items 2
| JP | EN | max | notes | Avoid |
|---|---|---|---|---|
| おおしんじゅ | Large Pearl | | | |
| サファイア | Sapphire | | | |
| ルビー | Ruby | | | |
| ブラッドダイヤ | Blood Diamond | | | |
| にじのダイヤ | Rainbow Diamond | | | |
| しようきんし | Do Not Use | | | |
| いのちのきのみ | Fruit of Life | | | |
| すばやそう | Swift Herb | | | |
| ちからのリンゴ | Power Apple | | | |
| せんにんのもも | Sage's Peach | | | |
| シルフのなみだ | Sylph's Tear | | | |
| ネクタル | Nectar | | | |
| げんきそう | Vigor Herb | | | |
| せんたん | Elixir | | | |
| きんたん | Gold Elixir | | | |
| いだてんのみ | Dash Fruit | | | |
| せんしゅ | Sage's Wine | | | |
| めがみのかじつ | Goddess Fruit | | | |
| ゲートリング | Gate Ring | | | |
| みちびきのいと | Guiding Thread | | | |
| まつくじ | Gold Ticket | | | |
| たけくじ | Silver Ticket | | | |
| うめくじ | Bronze Ticket | | | |
| まつ1とうくじ | Gold 1st Prize | | | |
| たけ1とうくじ | Silver 1st Prize | | | |
| たけ2とうくじ | Silver 2nd Prize | | | |
| たけ3とうくじ | Silver 3rd Prize | | | |
| うめ1とうくじ | Bronze 1st Prize | | | |
| うめ2とうくじ | Bronze 2nd Prize | | | |
| うめ3とうくじ | Bronze 3rd Prize | | | |
| うめ4とうくじ | Bronze 4th Prize | | | |
| はずれくじ | Losing Ticket | | | |
| やみのおふだ | Dark Seal | | | |
| あかいハンカチ | Red Handkerchief | | | |
| てがみ | Letter | | | |
| ノミ | Chisel | | | |
| しんでんのカギ | Temple Key | | | |
| なぞのけん | Mystery Sword | | | |
| なぞのやり | Mystery Spear | | | |
| なぞのゆみ | Mystery Bow | | | |
| やくそう | Herb | | | |
| なぞのせきばん | Mystery Tablet | | | |
| かみかざり | Hair Ornament | | | |
| もんしょう | Crest | | | |
| タリスマン | Talisman | | | |
| じゅふ | Spell Seal | | | |
| クリスタルキー | Crystal Key | | | |
| マスターキー | Master Key | | | |
| けいかくしょ | Plans | | | |
| りゅうのいかり | Dragon's Wrath | | | |
| しにがみのみみ | Reaper's Ear | | | |
| むくのたま | Pure Gem | | | |
| プラナのぞう | Prana Statue | | | |
| あんないじょう | Invitation | | | |
| わかいのてがみ | Letter of Peace | | | |
| はるのあしおと | Footsteps of Spring | | | |
| きょうきのさけ | Wine of Madness | | | |
| こうきなひかり | Noble Light | | | |
| やみのしずけさ | Silence of Darkness | | | |
| いにしえのうた | Ancient Song | | | |
| あたらしきこえ | New Voice | | | |
| いぶきのこどう | Pulse of Life | | | |
| はんせん | Sailing Ship | | | |
| ひくうてい | Airship | | | |

### Food
| JP | EN | max | notes | Avoid |
|---|---|---|---|---|
| くろパン | Black Bread | | | |
| じゃがいも | Potato | | | |
| フルーツケーキ | Fruitcake | | | |
| ていしょく | Set Meal | | | |
| にくりょうり | Meat Dish | | | |
| やまのさち | Mountain Bounty | | | |
| うみのさち | Sea Bounty | | | |
| りくだこのにく | Land Octopus Meat | | | |
| ほしぶどう | Raisins | | | |
| チーズ | Cheese | | | |
| かんパン | Hardtack | | | |
| ひもの | Dried Fish | | | |
| おむすび | Rice Ball | | | |
| しおづけにく | Salted Meat | | | |
| ペミカン | Pemmican | | | |
| クスクスのみ | Giggle Nut | | | |

### Beasts
| JP | EN | max | notes | Avoid |
|---|---|---|---|---|
| フェニックス | Phoenix | | | |
| ペガサス | Pegasus | | | |
| アークエンジェル | Archangel | | | |
| グリフォン | Griffin | | | |
| マイマイ | Snail | | | |
| まほうのこびと | Magic Dwarf | | | |
| カーバンクル | Carbuncle | | | |
| サーペント | Serpent | | | |
| サラマンダー | Salamander | | | |
| フェアリー | Fairy | | | |
| サンダードラゴン | Thunder Dragon | | | |
| ユラヌス | Uranus | | | |
| キングコロン | King Koron | | | |
| ファイアドラゴン | Fire Dragon | | | |
| バーンドラゴン | Burn Dragon | | | |
| プチドラゴン | Petit Dragon | | | |
| シルバードラゴン | Silver Dragon | | | |
| スタードラゴン | Star Dragon | | | |
| フロストドラゴン | Frost Dragon | | | |
| シルフ | Sylph | | | |
| サイクロプス | Cyclops | | | |
| ヴァルキリー | Valkyrie | | | |
| ワルキューレ | Walkure | | | |
| ノーム | Gnome | | | |
| リヴィングアーマ | Living Armor | | | |
| MK46アーマー | MK46 Armor | | | |
| エンジェル | Angel | | | |
| オーディン | Odin | | | |
| タイタン | Titan | | | |
| サイコろ | Psycho Dice | | | |
| うろうろツリー | Wandering Tree | | | |
| メロウ | Merrow | | | |
| スライム | Slime | | | |
| けつえきスライム | Blood Slime | | | |
| くさったスライム | Rotten Slime | | | |
| じゃしん | Evil God | | | |
| ワーム | Worm | | | |
| インプ | Imp | | | |
| ヒドラ | Hydra | | | |
| すいしょうヒドラ | Crystal Hydra | | | |
| りくダコ | Land Octopus | | | |
| ケムケム | Smokey | | | |
| ゴーレム | Golem | | | |
| ゆきのようせい | Snow Fairy | | | |
| プラチナドラゴン | Platinum Dragon | | | |
| ふわふわぐも | Fluffy Cloud | | | |
| ウィースプ | Wisp | | | |
| ダイアヒドラ | Diamond Hydra | | | |
| デーモン | Demon | | | |
| ヘルドラゴン | Hell Dragon | | | |
| デスドラゴン | Death Dragon | | | |
| ドラゴネット | Dragonet | | | |
| ケルベロス | Cerberus | | | |
| ガーゴイル | Gargoyle | | | |
| ハルピュイア | Harpy | | | |
| ヴァンパイア | Vampire | | | |
| キメラ | Chimera | | | |
| ナイトメア | Nightmare | | | |
| スケルトン | Skeleton | | | |
| メデューサ | Medusa | | | |
| セイレーン | Siren | | | |
| ゾンビ | Zombie | | | |
| マミー | Mummy | | | |
| ベルゼベブ | Beelzebub | | | |
| アルラウネ | Alraune | | | |
| リッチ | Lich | | | |
| ミノタウロス | Minotaur | | | |
| オーガー | Ogre | | | |
| ゴースト | Ghost | | | |

### Enemies
| JP | EN | max | notes | Avoid |
|---|---|---|---|---|
| ごうとう | Robber | | | |
| アドベンチャラー | Adventurer | | | |
| ハンター | Hunter | | | |
| ごうとうのかしら | Robber Boss | | | |
| ビーストメイジ | Beast Mage | | | |
| ウイッチ | Witch | | | |
| やみのせんし | Dark Warrior | | | |
| やみのきし | Dark Knight | | | |
| バーバリアン | Barbarian | | | |
| しょうきんかせぎ | Bounty Hunter | | | |
| アーチャー | Archer | | | |
| ビーストナイト | Beast Knight | | | |
| アマゾネス | Amazon | | | |
| とうぞくのかしら | Thief Boss | | | |
| とうぞく | Thief | | | |
| やみのあきんど | Dark Merchant | | | |
| ビーストハンター | Beast Hunter | | | |
| ダークスミス | Dark Smith | | | |
| ダークプリースト | Dark Priest | | | |
| やみのモンク | Dark Monk | | | |
| やみのシスター | Dark Sister | | | |
| やみのじょさい | Dark Priestess | | | |
| ヘビトカゲマン | Snake-Lizard Man | | | |
| アサッシン | Assassin | | | |
| かいぞくのかしら | Pirate Boss | | | |
| かいぞく | Pirate | | | |
| デスパー | Desper | | | |
| アンフィスバエナ | Amphisbaena | | | |
| しろながすクジラ | Blue Whale | | | |
| クラーケン | Kraken | | | |
| しょくしゅA | Tentacle A | | | |
| しょくしゅB | Tentacle B | | | |
| しょくしゅC | Tentacle C | | | |
| しょくしゅD | Tentacle D | | | |
| しょくしゅE | Tentacle E | | | |
| しょくしゅF | Tentacle F | | | |
| しょくしゅG | Tentacle G | | | |
| はじまりのくび | Head of Beginning | | | |
| こんとんのくび | Head of Chaos | | | |
| はめつのくび | Head of Ruin | | | |

### Skills
| JP | EN | max | notes | Avoid |
|---|---|---|---|---|
| タックル | Tackle | | | |
| ファイアーブレス | Fire Breath | | | |
| サンダーブレス | Thunder Breath | | | |
| スノーブレス | Snow Breath | | | |
| ソードアタック | Sword Attack | | | |
| アイスブリット | Ice Bullet | | | |
| サンダースピア | Thunder Spear | | | |
| スピアアタック | Spear Attack | | | |
| フレイル | Flail | | | |
| りんぷん | Scale Dust | | | |
| ウインドブレード | Wind Blade | | | |
| クラブアタック | Club Attack | | | |
| プレス | Press | | | |
| なぐる | Punch | | | |
| ライトニング | Lightning | | | |
| ひっかく | Scratch | | | |
| とつげき | Charge | | | |
| ふぶき | Snowstorm | | | |
| さばきのひかり | Judgment Light | | | |
| エナジードレイン | Energy Drain | | | |
| かみつき | Bite | | | |
| どくが | Poison Fang | | | |
| とりこむ | Engulf | | | |
| ダークブレス | Dark Breath | | | |
| しせん | Gaze | | | |
| ヒーリング | Healing | | | |
| ダークメイス | Dark Mace | | | |
| キック | Kick | | | |
| ダガーアタック | Dagger Attack | | | |
| コロコロこうげき | Rolling Attack | | | |
| グングニル | Gungnir | | | |
| らいげき | Thunderbolt | | | |
| バースト | Burst | | | |
| かまいたち | Sickle Wind | | | |
| きせき | Miracle | | | |
| ブレスプラス | Bless Plus | | | |
| いやしのひかり | Healing Light | | | |
| ミラクルライト | Miracle Light | | | |
| ちりょう | Treatment | | | |
| ちゆのひかり | Curing Light | | | |
| なめる | Lick | | | |
| キュアポイズン | Cure Poison | | | |
| ひっぱたく | Slap | | | |
| しずく | Droplet | | | |
| ファイアアタック | Fire Attack | | | |
| アイスブレス | Ice Breath | | | |
| スノーアタック | Snow Attack | | | |
| フリーズ | Freeze | | | |
| アイス | Ice | | | |
| ブリザード | Blizzard | | | |
| ソニックブレード | Sonic Blade | | | |
| じょうか | Purify | | | |
| スターブリッド | Star Bullet | | | |
| かえん | Flames | | | |
| あくむのせっぷん | Nightmare Kiss | | | |
| バーニングフレア | Burning Flare | | | |
| らくらい | Lightning Bolt | | | |
| ヘルウインド | Hell Wind | | | |
| ポイズンクラウド | Poison Cloud | | | |
| じごくのかえん | Hell Flames | | | |
| じゃがん | Evil Eye | | | |
| バーサクチャーム | Berserk Charm | | | |
| フィア | Fear | | | |
| スリープソング | Sleep Song | | | |
| メンタルアタック | Mental Attack | | | |
| じごくのごうか | Hell Inferno | | | |
| ソウルスチル | Soul Steal | | | |
| じょうかのひかり | Purifying Light | | | |
| プラズマブレス | Plasma Breath | | | |
| ごうか | Inferno | | | |
| ヘルフレア | Hell Flare | | | |
| ブリザードブレス | Blizzard Breath | | | |
| エレクトリック | Electric | | | |
| バーストブレス | Burst Breath | | | |
| フレアブレス | Flare Breath | | | |
| ハリケーン | Hurricane | | | |
| メテオストライク | Meteor Strike | | | |
| かみのいかずち | Divine Thunder | | | |
| プラズマアタック | Plasma Attack | | | |
| ヒールライト | Heal Light | | | |
| デスウインド | Death Wind | | | |
| ハエ | Flies | | | |
| ロックアタック | Rock Attack | | | |
| しのしせん | Death Gaze | | | |
| フェザーアタック | Feather Attack | | | |
| はっきょう | Frenzy | | | |
| どくぎり | Poison Mist | | | |
| フェナティクアイ | Fanatic Eye | | | |
| パワーロード | Power Load | | | |
| いかり | Rage | | | |
| ふるいたつ | Rouse | | | |
| ソニックブレス | Sonic Breath | | | |
| いしつぶて | Stone Throw | | | |
| キュア | Cure | | | |
| すみこうげき | Ink Attack | | | |
| アックス | Axe | | | |
| フリーズブレス | Freeze Breath | | | |
| さいせいのほのう | Rebirth Flame | | | |
| スリープクラウド | Sleep Cloud | | | |
| ねむりのしせん | Sleep Gaze | | | |
| ショック | Shock | | | |
| ねむりのといき | Sleep Sigh | | | |
| ねむりのこな | Sleep Powder | | | |
| でんりゅう | Electric Shock | | | |
| デスソング | Death Song | | | |
| きょうきのうた | Song of Madness | | | |
| コロコロダンス | Rolling Dance | | | |
| スリープアタック | Sleep Attack | | | |
| カース | Curse | | | |
| ソウルコフィン | Soul Coffin | | | |
| りゅうさんのきり | Sulfuric Mist | | | |
| しょくしゅ | Tentacle | | | |
| こおりのきば | Ice Fang | | | |
| かみつく | Bite | | | |
| ほのおのきば | Fire Fang | | | |
| ポイズンブレス | Poison Breath | | | |
| すみ | Ink | | | |
| ダイン | Dyne | | | |
| ウインドブレス | Wind Breath | | | |
| ブリッドブレス | Bullet Breath | | | |
| おたけび | War Cry | | | |

<!-- names:end -->

## Decisions from earlier batches
- <batch> <JP> -> <EN> (reason)
