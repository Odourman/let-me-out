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
 lda #56
 ldx #1
 jsr Position
 sta $02
 sta $2a
 sta $02
 sta $2b
 REPEAT 32
 sta $02
 REPEND
 sta $02
 lda #0
 sta $01
 REPEAT 32
 sta $02
 REPEND
LineSync:
 sta $02
 lda #FIRST_BITS
 sta $1b
 lda #$18
 sta $1c
 lda #SECOND_BITS
 IF SECOND_COPY
 REPEAT 8
 nop
 REPEND
 bit $80
 nop
 ldx #1
 stx $04
 ELSE
 REPEAT 16
 nop
 REPEND
 ENDIF
 REPEAT DELAY
 nop
 REPEND
SecondGrp:
 sta $1b
SecondResp:
 sta $10
 sta $02
 lda #0
 sta $1b
 sta $1c
 sta $04
 REPEAT 158
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
