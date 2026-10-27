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
	warnpc $E81000

org $E81000
font:				; codes 10-7F, 16 bytes each (tools/font.py)
	incbin "../../build/en6.bin"
	warnpc $E84000
