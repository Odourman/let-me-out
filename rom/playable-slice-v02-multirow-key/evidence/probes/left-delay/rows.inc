Row0:
 sta $02
 lda #126
 sta $1c
 lda #112
 sta $1b
 ldy #63
 ldx #1
 stx $04
 nop
 nop
 nop
 nop
 nop
 nop
 nop
 nop
 nop
 nop
 nop
 nop
FirstResp0:
 sta $10
 bit $80
SecondResp0:
 sta $10
 nop
SecondGrp0:
 sty $1b
 lda #0
 sta $1d
 lda #0
 sta $04
Row1:
 sta $02
 lda #24
 sta $1c
 lda #80
 sta $1b
 ldy #15
 ldx #1
 stx $04
 nop
 nop
 nop
 nop
 nop
 nop
 nop
 nop
 nop
 nop
 nop
 nop
FirstResp1:
 sta $10
 bit $80
SecondResp1:
 sta $10
 nop
SecondGrp1:
 sty $1b
 lda #0
 sta $1d
 lda #0
 sta $04
Row2:
 sta $02
 lda #36
 sta $1c
 lda #126
 sta $1b
 ldy #30
 ldx #1
 stx $04
 nop
 nop
 nop
 nop
 nop
 nop
 nop
 nop
 nop
 nop
 nop
 nop
FirstResp2:
 sta $10
 bit $80
SecondResp2:
 sta $10
 nop
SecondGrp2:
 sty $1b
 lda #2
 sta $1d
 lda #0
 sta $04
Row3:
 sta $02
 lda #0
 sta $1c
 lda #36
 sta $1b
 ldy #12
 ldx #1
 stx $04
 nop
 nop
 nop
 nop
 nop
 nop
 nop
 nop
 nop
 nop
 nop
 nop
FirstResp3:
 sta $10
 bit $80
SecondResp3:
 sta $10
 nop
SecondGrp3:
 sty $1b
 lda #0
 sta $1d
 lda #0
 sta $04
Row4:
 sta $02
 lda #0
 sta $1c
 lda #4
 sta $1b
 ldy #18
 ldx #1
 stx $04
 nop
 nop
 nop
 nop
 nop
 nop
 nop
 nop
 nop
 nop
 nop
 nop
FirstResp4:
 sta $10
 bit $80
SecondResp4:
 sta $10
 nop
SecondGrp4:
 sty $1b
 lda #0
 sta $1d
 lda #0
 sta $04
 sta $02
