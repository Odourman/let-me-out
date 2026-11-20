Row0:
 sta $02
 lda #126
 sta $1c
 lda #252
 sta $1b
 ldy #112
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
FirstResp0:
 sta $10
 bit $80
 nop
SecondResp0:
 sta $10
SecondGrp0:
 sty $1b
 lda #0
 sta $1d
 nop
 lda #0
 sta $04
Row1:
 sta $02
 lda #24
 sta $1c
 lda #60
 sta $1b
 ldy #80
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
FirstResp1:
 sta $10
 bit $80
 nop
SecondResp1:
 sta $10
SecondGrp1:
 sty $1b
 lda #0
 sta $1d
 nop
 lda #0
 sta $04
Row2:
 sta $02
 lda #36
 sta $1c
 lda #120
 sta $1b
 ldy #126
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
FirstResp2:
 sta $10
 bit $80
 nop
SecondResp2:
 sta $10
SecondGrp2:
 sty $1b
 lda #2
 sta $1d
 nop
 lda #0
 sta $04
Row3:
 sta $02
 lda #0
 sta $1c
 lda #48
 sta $1b
 ldy #36
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
FirstResp3:
 sta $10
 bit $80
 nop
SecondResp3:
 sta $10
SecondGrp3:
 sty $1b
 lda #0
 sta $1d
 nop
 lda #0
 sta $04
Row4:
 sta $02
 lda #0
 sta $1c
 lda #72
 sta $1b
 ldy #4
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
FirstResp4:
 sta $10
 bit $80
 nop
SecondResp4:
 sta $10
SecondGrp4:
 sty $1b
 lda #0
 sta $1d
 nop
 lda #0
 sta $04
 sta $02
