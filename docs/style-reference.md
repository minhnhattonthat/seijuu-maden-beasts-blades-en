# Style reference

Pilot lines (b001 prologue, b002 intro, b003 the ice cave / Rundstedt scene), checked in-game
(`work/qa/warp/prologue/`, `--qa E7792E=` in the opening box). Match this voice.

## Layout
- Dialogue: `Speaker / "Text..."`. The name line is the speaker's name per `glossary.md` (`{var:02}` = the hero).
  Don't copy the JP line breaks: write the page as one run of text and `tools/batches.py` wraps it (35 cells per
  line, a quote's continuation lines indented one space). `{c0C}` = new page: keep each one where the JP has it.
  A page that continues the same speech starts with one space (` And if it turns out...`), as in the JP.
- Inner monologue in 『』 opening a speech -> parentheses: `{var:02} / (The Goddess said it was fate.` ... `stop to it!!)`.
- Narration / scroll lines (prologue, intro, endings, credits): one English line per JP line, 40 chars max, reading
  on from line to line; rebalance words between neighbouring lines so none is a stub.
- Choices: `Question? / {choice:0201} Yes /  No` - each option on its own " / " line with its leading space.

## Voices
| Who | Voice | Example |
|---|---|---|
| Supreme God (至高神) | archaic, lofty ("O maidens", "I ask you") | "Then fight, and settle it: / which of you is worthy of the true Law!" |
| Goddesses (prologue) | formal, courtly ("I humbly ask", "I pray you") | "Please wait. I humbly ask / that the honor be mine." |
| Rundstedt | stiff, formal military aide; calls the hero "my king" (王よ) / "Holy Beast King-sama" | "Indeed. Lang-sama, the High Priest of Light. The First Banner will soon be raised." |
| Hero (`{var:02}`) | plain, young, earnest (僕) | "Uh-oh... this cave is caving in! I have to get out of here, fast!" |

## Pairs
| JP | EN |
|---|---|
| 至高神は告げた。 | The Supreme God spoke. |
| 「待て待て、 / 2人もめとるわけにはいかぬ」 | "Wait, wait! / I cannot take two of you as wives." |
| ゴーン、ゴーン… | Bong... bong... |
| 「王よ、 / これが…『第一の旗』でしょう。 | "My king, / that must be... the First Banner. |
| お待ちしておりました、聖獣王様。わたしは、『シルヴァラ騎士団』侍従武官長のルントシュテットです。 | I have been waiting for you, Holy Beast King-sama. I am Rundstedt, chief aide-de-camp of the Silvara Knights. |
| 「い、{delay:14}いや…{delay:28}何でもありません。 | "N-{delay:14}no...{delay:28} it's nothing. |

Corrected example: `For a while, a mix of hope, shyness / and fear / held sway over them all.` left a stub line
("and fear"); rebalanced to `For a while, feelings of hope, / shyness and fear, all mingled, / held sway over them.`
