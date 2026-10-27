; text.asm: English for the 12 px text engine (asar 1.91). tools/build.py applies it to the 4 MB image.
; Hooks: docs/re/hooks.md. Bank E8 $0000-$3FFF is reserved for this file; build.py's text allocator starts at $4000.
;
; Codes 10-7F are 6 px English glyphs (fonts/en6.txt). Two of them share one 12 px full-width cell: compose
; builds the cell in the glyph buffer exactly as the full-width loader C3199A would, then the game's own
; full-width code shifts, shadows and uploads it. A lone glyph (next byte is a control code or kanji) gets a
; blank right half.
hirom

; typed engine C318D1 and bulk engine C32575: half-width range 10-4F -> 10-7F
org $C3193A
	cmp.b #$80
org $C325D5
	cmp.b #$80
org $C3194E
	jmp typed_half
org $C325E9
	jmp bulk_half

; the old half-width glyph routines C31B74 / C3275D are unreachable now: trampolines live there
org $C31B74
typed_half:
	jsl compose
	jsr $19BE		; rest of the full-width loader: half-tile phase shift
	ldx $4754
	jsr ($133B,x)		; typed draw for the current box mode (as C31993)
	jmp $1933		; engine exit (PLB PLP RTL)
	warnpc $C31BA7

org $C3275D
bulk_half:
	jsl compose
	jsr $19BE
	ldx $4754
	jsr ($1343,x)		; bulk draw (as C32627)
	jmp $2587		; next code
	warnpc $C3278C

; line width for centred scroll lines (prologue, intro, endings, credits): follow {call} stubs, count an English
; pair as one full-width cell
org $C32CA4
	jml measure

; the column check after each cell (C31B58 full-width, C31D13: $4770 past $4768 and next byte not 00 -> new
; line): an English line can fill the row exactly, and the {nl} after it then left a blank line
org $C31B69
	jsl wrapchk
	beq wrap_rts2
	nop
	warnpc $C31B70
org $C31B73
wrap_rts2:
org $C31D1E
	jsl wrapchk
	beq wrap_rts		; a literal `beq $C31D28` came out as F0 28 (to $1D4C) in asar 1.91
	nop
	warnpc $C31D25
org $C31D28
wrap_rts:

; battle weapon/item list (C557A3: LDA [$C2],y / BEQ): C6 name fields are {call} stubs now
org $C557A3
	jsl bname

; member names ([$BF] -> a RAM member record's name, copied raw from a C6 field, so it may be a {call} stub):
; status/formation name cells C254A9 (REP #$30 / LDY #0) and the battle name box C5329A (LDY #0 / LDA [$BF],y)
org $C254AA
	jsl mname
	nop
org $C5329A
	jsl bbox
	nop

; item list (status アイテム: use/discard/valuables; drawer C26140, buffer 7F:AE10, entry rows $80 apart): one column
; instead of two 12-cell columns, so a name gets cols 9-27 (19 chars) and the count/LV moves to col 28
org $C26144
	db $80			; BCC -> BRA: no right-column offset (+$18)
org $C26152
	nop			; LSR: row = slot, not slot/2
org $C26167
	jsr $B798		; was LDA #$0000: blank the whole row first (names shorter than the old one)
org $C2620C
	db $28			; weapon LV: col 16 -> 28
org $C262AB
	db $28			; armor's blank count field
org $C26457
	db $28			; food/item count
org $C26436
	db $17			; empty slot: blank 24 cells
; highlight C2B76B: row = index (the odd-index path is dead, the row blank lives there), 24 cells
org $C2B776
	nop #3			; LSR / BCS odd
org $C2B798			; 29 bytes up to the join at B7B5
	phy
	lda #$0017
	jsr $6CE0		; A+1 blank cells from $4BA4 (cols 8-31)
	lda $4BA4		; and zero the row's lower half (+$40, squeezed out by HDMA but its top shows):
	tax			; other screens leave tiles there, unseen while the list had 16 rows
	ldy #$0018
	lda #$0000
-	sta $7F0040,x
	inx
	inx
	dey
	bne -
	ply
	rts
warnpc $C2B7B5
org $C2B7BD
	db $17
; cursor (C2B3F9..): down/up move one row, left/right do nothing
org $C2B3FD
	db $1B			; down while index < 27
org $C2B40F
	nop #3			; second INC $E11F
org $C2B452
	db $01			; up while index >= 1
org $C2B465
	nop			; second DEC A
org $C2B482
	db $20			; scroll-up guard (row < 12): 28 rows now
org $C2B4A8
	db $80			; left: BEQ -> BRA (no move)
org $C2B50B
	db $80			; right: BEQ -> BRA
; the same for the equip page's bag list (C2A5B0, dispatcher index 9): twin cursor code and highlight C2ABD8
org $C2A658
	db $1B
org $C2A66A
	nop #3
org $C2A6AB
	db $01
org $C2A6BE
	nop
org $C2A6DE
	db $20
org $C2A701
	db $80
org $C2A75D
	db $80
org $C2ABE4
	nop #3
org $C2AC2B
	db $17
org $C2B175
	dw $B990		; ▽ arrow: last scroll top is row 23 (AE10 + 23 * $80), was row 9
org $C2B831
	dw $B990
; the second list (C2610F, other unit on the exchange screen) sat at 7F:B6D0, inside list 1's 32 rows now: 7F:BED0
org $C2612D
	dw $BED0
org $C2D150
	dw $BEC0		; its scroll start (E127)
org $C2D7C3
	dw $BED0		; its ▲ / ▽ bounds
org $C2D7C8
	dw $CA50
org $C2D5EB
	dw $10C0		; its highlight: list 1 position + $8C0 -> + $10C0
; TODO exchange item cursor (C2D114.., highlight C2D593 LSR/width) is still two-column: docs/status.md

org $E80000
compose:			; in: [$32] at an English code. out: $36DD buffer filled, $32 past 1-2 codes, M8 X16
	phb
	sep #$20
	lda #$7E
	pha
	plb
	rep #$30
	lda [$32]
	and #$00FF
	sec
	sbc #$0010
	asl
	asl
	asl
	asl
	pha			; first glyph's offset
	inc $32
	lda [$32]
	and #$00FF
	cmp #$0010
	bcc .single
	cmp #$0080
	bcs .single
	inc $32
	sec
	sbc #$0010
	asl
	asl
	asl
	asl
	bra .go
.single:
	lda #$0000		; glyph 10 = space
.go:
	sta $7F			; second glyph's offset
	plx
	sep #$20
	lda #$02
	sta $474D		; full-width cell (as C31979)
	ldy #$001F
.first:				; rows 0-11 -> $36DD+$1F..$14 (left 8 px), as C3199A
	lda.l font,x
	sta $36DD,y
	inx
	dey
	cpy #$0013
	bne .first
	ldx $7F
	ldy #$001F
.second:			; columns 6-7 into the left byte, 8-11 into the right nibble ($36DD+$0F..$04)
	lda.l font,x
	pha
	lsr
	lsr
	lsr
	lsr
	lsr
	lsr
	ora $36DD,y
	sta $36DD,y
	pla
	asl
	asl
	and #$F0
	sta $36CD,y
	inx
	dey
	cpy #$0013
	bne .second
	plb
	rtl

measure:			; replaces C32CA4: width of the line at [$32] in 8 px cells -> $4B8E
	php
	rep #$20
	lda $32
	pha
	sep #$20
	lda $34
	pha
	rep #$10
	ldy #$0000
	sty $4B8E
	stz $474E
.loop:
	lda [$32],y
	beq .done
	cmp #$0F
	bne .notcall
	iny
	lda [$32],y
	dey
	cmp #$FF
	bne .narrow
	iny			; {call:lo hi bank}: measure the called string instead
	iny
	rep #$20
	lda [$32],y
	tax
	iny
	iny
	sep #$20
	lda [$32],y
	sta $34
	stx $32
	ldy #$0000
	bra .loop
.notcall:
	cmp #$10
	bcc .narrow
	cmp #$80
	bcc .pair
	cmp #$F2
	bcc .wide1
	iny
.wide1:
	iny
.wide:				; one full-width cell: 12 px = 1.5 cells, as the original
	lda $474E
	eor #$01
	sta $474E
	lda $4B8E
	clc
	adc #$01
	adc $474E
	sta $4B8E
	bra .loop
.pair:
	iny
	lda [$32],y
	cmp #$10
	bcc .wide
	cmp #$80
	bcs .wide
	iny
	bra .wide
.narrow:
	iny
	lda $4B8E
	clc
	adc #$01
	sta $4B8E
	bra .loop
.done:
	pla
	sta $34
	rep #$20
	pla
	sta $32
	plp
	rtl

bname:				; battle weapon/item list C557A3 (name bytes -> tiles): follow a {call} stub. M8 X16
	lda [$C2],y
	beq .end
	cmp #$0F
	bne .ret
	iny			; 0F FF lo hi bank: draw the called string instead
	iny
	phx			; X = the caller's tilemap index
	rep #$20
	lda [$C2],y
	tax
	iny
	iny
	sep #$20
	lda [$C2],y
	sta $C4
	stx $C2
	plx
	ldy #$0000
	lda [$C2],y
	beq .end
.ret:
	sec			; the caller's SBC #$10 (the CMP above may have cleared it)
	rtl
.end:
	pla			; drop the JSL return: take the caller's BEQ to the end of the name
	pla
	pla
	jml $C557B1

mname:				; C254AA: the replaced REP #$30 / LDY #0, after following a stub. X (cell count) kept
	rep #$30
	jsr bf_follow
	ldy #$0000
	rtl

bbox:				; C5329A: the replaced LDY #0 / LDA [$BF],y, after following a stub. M8 X16, X kept
	rep #$20
	jsr bf_follow
	sep #$20
	ldy #$0000
	lda [$BF],y
	rtl

bf_follow:			; [$BF] at 0F FF lo hi bank: point $BF-$C1 at the called string. M16 X16, X kept
	lda [$BF]
	cmp #$FF0F
	bne .ret
	phx
	ldy #$0002
	lda [$BF],y
	tax
	ldy #$0003
	lda [$BF],y		; hi, bank
	sta $C0
	stx $BF
	plx
.ret:
	rts

wrapchk:			; C31D1E: auto-wrap after a full line unless the line ends here anyway. M16; out A = 0
	php			; (no wrap: end, c0B, c0C or nl next, past delays/sfx), else 1; Z from A
	rep #$30
	phy
	ldy #$0000
.loop:
	lda [$32],y
	and #$00FF
	beq .no
	cmp #$0003		; {delay:1}
	beq .skip
	cmp #$0008		; {sfx:1}
	beq .skip
	cmp #$000B
	bcc .yes
	cmp #$000E		; 0B 0C 0D
	bcc .no
.yes:
	lda #$0001
	bra .out
.skip:
	iny
	iny
	bra .loop
.no:
	lda #$0000
.out:
	ply
	plp
	ora #$0000
	rtl
	warnpc $E81000

org $E81000
font:				; codes 10-7F, 16 bytes each (tools/font.py)
	incbin "../../build/en6.bin"
	warnpc $E84000
