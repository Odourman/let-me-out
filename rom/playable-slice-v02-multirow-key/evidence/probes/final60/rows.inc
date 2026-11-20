Row0:
 sta $02
 lda #0
 sta $1d
 lda #126
 sta $1b
 lda #$0e
 sta $07
 lda #252
 sta $1c
 ldy #112
 ldx #1
 stx $05
 bit $80
FirstResp0:
 sta $11
 ldx #$1e
 nop
 nop
 nop
SecondResp0:
 sta $11
SecondGrp0:
 sty $1c
 stx $07
 nop
 nop
 lda #0
 sta $05
Row1:
 sta $02
 lda #0
 sta $1d
 lda #30
 sta $1b
 lda #$0e
 sta $07
 lda #48
 sta $1c
 ldy #80
 ldx #1
 stx $05
 bit $80
FirstResp1:
 sta $11
 ldx #$1e
 nop
 nop
 nop
SecondResp1:
 sta $11
SecondGrp1:
 sty $1c
 stx $07
 nop
 nop
 lda #0
 sta $05
Row2:
 sta $02
 lda #2
 sta $1d
 lda #60
 sta $1b
 lda #$0e
 sta $07
 lda #72
 sta $1c
 ldy #126
 ldx #1
 stx $05
 bit $80
FirstResp2:
 sta $11
 ldx #$1e
 nop
 nop
 nop
SecondResp2:
 sta $11
SecondGrp2:
 sty $1c
 stx $07
 nop
 nop
 lda #0
 sta $05
Row3:
 sta $02
 lda #0
 sta $1d
 lda #24
 sta $1b
 lda #$0e
 sta $07
 lda #0
 sta $1c
 ldy #36
 ldx #1
 stx $05
 bit $80
FirstResp3:
 sta $11
 ldx #$1e
 nop
 nop
 nop
SecondResp3:
 sta $11
SecondGrp3:
 sty $1c
 stx $07
 nop
 nop
 lda #0
 sta $05
Row4:
 sta $02
 lda #0
 sta $1d
 lda #36
 sta $1b
 lda #$0e
 sta $07
 lda #0
 sta $1c
 ldy #4
 ldx #1
 stx $05
 bit $80
FirstResp4:
 sta $11
 ldx #$1e
 nop
 nop
 nop
SecondResp4:
 sta $11
SecondGrp4:
 sty $1c
 stx $07
 nop
 nop
 lda #0
 sta $05
 sta $02
