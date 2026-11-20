; Isolated beam experiment. Both yellow glyphs are rendered through P0.
; No production kernel, controller state or collision code is modified.
 processor 6502
 ORG $f000
Reset:
 sei
 cld
 ldx #$ff
 txs
 lda #0
 ldx #$2c
Clear:
 sta 0,x
 dex
 bpl Clear
 lda #$1e
 sta $06
 lda #$0e
 sta $07
 lda #$26
 sta $08
 lda #1
 sta $0a
 lda #$10
 sta $0d
Frame:
 lda #2
 sta $01
 sta $00
 REPEAT 3
 sta $02
 REPEND
 lda #0
 sta $00
 lda #FIRST_X-3
 ldx #0
 jsr Position
 lda #SM_X-3
 ldx #1
 jsr Position
 lda #SHOT_X-2
 ldx #2
 jsr Position
 sta $02
 sta $2a
 sta $02
 sta $2b
 REPEAT 31
 sta $02
 REPEND
 sta $02
 lda #0
 sta $01
 REPEAT 32
 sta $02
 REPEND
 include "rows.inc"
 lda #0
 sta $1b
 sta $1c
 sta $04
 REPEAT 154
 sta $02
 REPEND
 lda #2
 sta $01
 REPEAT 30
 sta $02
 REPEND
 jmp Frame
Position:
 sta $02
 sec
Coarse:
 sbc #15
 bcs Coarse
 eor #7
 asl
 asl
 asl
 asl
 sta $20,x
 sta $10,x
 rts
 ORG $fffa
 word Reset,Reset,Reset
