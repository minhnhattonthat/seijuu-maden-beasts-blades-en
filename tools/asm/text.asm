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
; and its window (popup off the command panel at $12B2; text buffer 7F:6400): 11 -> 23 cells, so a name gets
; 19 chars and the count moves to col 20. On the right half of the screen it also moves 12 cells left (boff)
org $C52F73
	db $17			; width (open)
org $C52FB0
	db $17			; width (close)
org $C53051
	db $17			; width (text copy)
org $C5305A
	jsl btext		; text origin LDA $12B2 / CLC / ADC #$0042
	nop #3
org $C5597F			; empty list (C557C8 copies raw tiles, en.tbl code - $10; E7 = window blank), 10 + 00
	db $18,$4E,$E7,$48,$53,$44,$4C,$52,$00	; "No items" (was アイテムをもってない)
org $C52F60
	jsl bwin		; frame origin (open)
	nop
org $C52F9D
	jsl bwinc		; frame origin (close)
	nop
org $C52F8A
	jsl bframe		; frame + text drawn into the BG map (C52D68)
	nop
; the ▶ cursor is a BG tile on the frame's left column, drawn by the shared menu-cursor routine C52E6A at $12B2:
; 12 cells left only while the list is open (flag 7F:66FE = $4C57, set by bframe, cleared by bwinc)
org $C52E88			; LDX $12B2 / PHB / LDA #$7F / PHA / PLB / REP #$20
	phb
	jsl bcur
	nop #5
org $C52EAF
	jsl bcur2		; ADC $0012B2
org $C52FD2
	jsl bsave		; save the BG under the window
	nop #2
org $C5300F
	jsl bsave		; restore it
	nop #2
; saved BG (25 x 5 cells, $FA bytes now): 7F:6442 -> 7F:6600-66F9 (3 text rows reach 648A, C53D68 uses 64C4-6505).
; shortcut: 7F:66xx is untouched in mashed battle/world map/town/home runs (tools/lua/wram_pages.lua), not proven free
org $C52FEF
	sta $6600,x
org $C53029
	lda $6600,x
org $C5574F
	db $2C			; clear 23 cells per row
org $C55756
	sta $642E,x		; rows $16 -> $2E apart
	sta $645C,x
org $C5578D
	db $2E			; attribute fill per row
org $C557B8
	db $2D			; next row (+carry)
org $C5307D
	db $28			; count col 8 -> 20
org $C5309D
	db $2E

; member names ([$BF] -> a RAM member record's name, copied raw from a C6 field, so it may be a {call} stub):
; status/formation name cells C254A9 (REP #$30 / LDY #0) and the battle name box C5329A (LDY #0 / LDA [$BF],y)
org $C254AA
	jsl mname
	nop
org $C5329A
	jsl bbox
	nop
; that box (template C5336F, 3 rows x 14 cells into 7F:4C00 + $12B4): 14 -> 23 cells, so a name gets 17 cells
; (longest: enemy "Head of Beginning") and the HP digits move from col 10 to col 19. Left box stays at col 1;
; the right one ($12AE set) moves 9 more cells left, col 17 -> 8, to keep its right edge at col 30
org $C53278
	lda.l bbox_t,x
org $C5327F
	lda.l bbox_t+46,x
org $C53286
	lda.l bbox_t+92,x
org $C53291
	cpx #$002E
org $C53256
	sbc #$001E
org $C532D6
	lda #$0066
org $C52CCA
	db $17			; its two clears (C50280, 3 rows at $12B4): 14 -> 23 cells
org $C55B1D
	db $17

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
; the exchange screen's item trade (C2D114, dispatcher index E): its own cursor (list in $E11E, X = list) and highlight
org $C2D226
	db $1B			; down while index < 27
org $C2D238
	nop #3			; second INC $E11F,x
org $C2D27D
	db $01			; up while index >= 1
org $C2D28A
	nop			; second DEC A
org $C2D2AD
	db $20			; scroll-up guard
org $C2D2D7
	db $80			; left: BEQ -> BRA
org $C2D337
	db $80			; right: BEQ -> BRA
org $C2D59F
	nop #3			; highlight row = index
org $C2D5F7
	db $17			; highlight 24 cells

; shop buy list (weapon C0FAE9, armor C0FB29): a name over 10 chars goes on onto the entry's lower tile row
; (entries are 16 px apart, that row is blank; on the status screen HDMA hides it)
org $C0FAE9
	jsl wrapname
org $C0FB29
	jsl wrapname

; status equip rows (names col 9, build.STATUS_CODE) and beast skills (col 16): C26C9E blanks the whole field
; before a name, not a fixed 10 cells. Was LDA #n / JSR $6CE0 / SEP #$20 (C26CE0 restores M8 from P)
org $C26C9F
	jsl eqcount
	jsr $6CE0
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

boff:				; battle list window shift in tilemap bytes: $18 (12 cells) on the right half, else 0. M16, keeps X/Y
	lda $7E12B2
	and #$003F
	cmp #$0020
	lda #$0018
	bcs +
	lda #$0000
+:
	rtl

btext:				; C5305A: A = $12B2 + $42 - shift. M16
	jsl boff
	eor #$FFFF
	sec
	adc $7E12B2
	clc
	adc #$0042
	rtl

bwin:				; C52F60/C52F9D: LDA $AF / STA $264D (frame column, in cells) minus the shift. M16, DB 7E
	jsl boff
	lsr
	eor #$FFFF
	sec
	adc $AF
	sta $264D
	rtl

bwinc:				; C52F9D: bwin for the close, and clear the list-open flag
	lda #$0000
	sta $7F66FE
	bra bwin

bcur:				; C52E88 (after PHB): DB = 7F, X = cursor column origin, M16. In M8 X16
	lda #$7F
	pha
	plb
	rep #$20
	lda #$0000
	jsl bcur2
	tax
	rtl

bcur2:				; C52EAF: A += $12B2, minus the shift while the list is open. M16 X16, DB 7F, C clear
	clc
	adc $7E12B2
	tax
	lda $66FE
	cmp #$4C57
	bne .r
	phx
	jsl boff
	eor #$FFFF
	sec
	adc $01,s
	plx
	rtl
.r:
	txa
	rtl

bframe:				; C52F8A: LDA $12B2 / STA $AF (tilemap index) minus the shift; flag the list open. M16, DB 7E
	lda #$4C57
	sta $7F66FE
	jsl boff
	eor #$FFFF
	sec
	adc $12B2
	sta $AF
	rtl

bsave:				; C52FD2/C5300F: REP #$10 / TAY / LDA #$001E (A = window origin) minus the shift. M16
	rep #$10
	pha
	jsl boff
	eor #$FFFF
	sec
	adc $01,s
	tay
	pla
	lda #$001E
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
	cmp #$10		; space: tile 0 is a dark block here, the window blank is tile E7
	bne +
	lda #$F7
+:
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

bbox_t:				; the 23-cell name box: top edge with the HP label, middle row, bottom edge
	dw $214A,$214B,$214C
	rep 19 : dw $214D
	dw $214E
	dw $20EB
	rep 21 : dw $20E7
	dw $20EC
	dw $20ED
	rep 21 : dw $20EE
	dw $20EF

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

eqcount:			; C26C9F: cells to blank - 1 for C26CE0 at $4BA4. Out M8
	rep #$20
	lda $4BA4
	cmp #$AE00		; item list (7F:AE10..): 10 as before, it blanks its rows itself
	bcs .bag
	and #$FFC0
	cmp #$AB80		; row 46: the weapon's LV from col 27
	php
	lda $4BA4
	and #$003F
	lsr a
	eor #$FFFF
	sec
	adc #$001E		; 30 - col: through col 30
	plp
	bne .out
	cmp #$0011
	bcc .out
	lda #$0011		; cols 9-26
	bra .out
.bag:	lda #$0009
.out:	sep #$20
	rtl

wrapname:			; as JSL $C32912 for a name: line 1 up to its last space within 10 chars, the rest one tile row
	php			; down (empty: blanks it); a line over 10 starts that much further left. Any M/X
	rep #$30
	pei ($50)		; $4F-$51 kept: the shop sets the bank once for the whole list
	pei ($4F)
-:	lda [$4F]		; follow {call} stubs
	cmp #$FF0F
	bne +
	ldy #$0002
	lda [$4F],y
	tax
	ldy #$0003
	lda [$4F],y
	sta $50
	stx $4F
	bra -
+:	sep #$20
	ldy #$FFFF
-:	iny
	lda [$4F],y
	bne -
	tyx			; X = length
	cpy #$000B
	bcc .one
	ldy #$000A
-:	lda [$4F],y
	cmp #$10		; space
	beq .two
	dey
	bne -
.one:	txy			; one line: cut = length
.two:	rep #$20
	phx			; length
	phy			; cut
	tya
	ldy #$0000
	ldx #$000A
	jsr wn_put		; line 1: 10 cells
	inc $4B9F
	inc $4B9D
	pla			; cut
	cmp $01,s
	beq +			; one line: line 2 blank
	inc a			; past the space
+:	tay
	eor #$FFFF
	sec
	adc $01,s		; length - offset
	ldx #$0009
	jsr wn_put		; line 2: indented, 9 cells
	dec $4B9D
	dec $4B9F
	pla
	pla
	sta $4F
	pla
	sta $50
	plp
	rtl

wn_put:				; draw A chars of [$4F] from offset Y, blank-padded to X cells, at col $4B9D minus the
	pha			; chars over X. [$4F] kept. M16 X16
	phx
	pei ($4F)
	pei ($50)
	tya
	clc
	adc $4F
	sta $4F
	tsc
	sec
	sbc #$0018		; 24-byte buffer at S+1: cells at $1D,s, length at $1F,s
	tcs
	inc a
	sta $87
	sep #$20
	lda #$7E
	sta $89
	ldy #$0000
-:	tya
	cmp $1F,s
	bcs .pad
	lda [$4F],y
	sta [$87],y
	iny
	bra -
.pad:	tya
	cmp $1D,s
	bcs .end
	lda #$10
	sta [$87],y
	iny
	bra .pad
.end:	lda #$00
	sta [$87],y
	rep #$20
	lda $1F,s
	sec
	sbc $1D,s
	bcs +
	lda #$0000
+:	pha			; shift
	eor #$FFFF
	sec
	adc $4B9D
	sta $4B9D
	lda $87
	sta $4F
	sep #$20
	lda #$7E
	sta $51
	jsl $C32912
	rep #$20
	pla
	clc
	adc $4B9D
	sta $4B9D
	tsc
	clc
	adc #$0018
	tcs
	pla
	sta $50
	pla
	sta $4F
	plx
	pla
	rts
	warnpc $E81000

org $E81000
font:				; codes 10-7F, 16 bytes each (tools/font.py)
	incbin "../../build/en6.bin"
	warnpc $E84000
