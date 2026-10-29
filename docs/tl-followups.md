# Translation follow-ups (from translator/reviewer reports, wave 1-2)

Work through these in the polish pass and the phase-8 QA tour. Remove a line once it is settled.
Settled 2026-10-29 (release prep): CF1FE9 'Ally' -> 'Party' (the field command 仲間's label); CE664B みてい "TBD"
(the game's own placeholder); E72F29 choice order mirrors the JP (Bork answers Odell either way); E41A2C "her" =
the Princess (only she can be killed there); E54241/E54327 'seal' kept generic (the JP says おふだ, not the item);
voices kept (でしゅ lisp, "drama queen", オカマ "drag queen" is the secretary's own prejudice, in the JP);
E77952 rewritten; laughs, statue it/them and W.M. label mirror the JP.

## Open, not blocking a release (none is visible as broken text)
- CE1DC3 delays inside a word ("ser{delay}va{delay}nt"): reads fine typed out, not seen in-game
- headline captions (`0C 00` ops: E6B37F/E6B446, E797D6, E357C2..): body seen, caption needs its newspaper screen
- E7EBD2/E7EBF0 song: ♪ written as '*' (seen in-game, reads ok; a note glyph would need a new en.tbl code)
- Story identities to confirm on a full playthrough: Erinshe (E54F70-E550D0 vs E55BA6..); ジャン vs Landenbaum Jean
  vs Old Man Junk (E70B23..); E48B93 speaker label (JP says プラナ); E760AC お姉様 to Hila; C1733E speaker;
  E43260 speakerless; E651E0 悪の華; E6A5CA/E7A94F/E7AA60 hints; CF3DD9-CF3EF3 compliment variants
- 至高神様 as "O Supreme God" in the endings; Zukan pun lost (C15928)
- Wave-1 review minors: `work/tl/b031/b037/b038/b039.review.md` (gitignored; summarised in git log aa5a84f)
