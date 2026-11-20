Row0:
 sta $02
 lda #0
 sta $1d
 lda #252
 sta $1b
 ldy #112
 ldx #1
 stx $04
 nop
 nop
FirstResp0:
 sta $10
 lda #126
 sta $1c
 bit $80
 nop
 nop
 nop
SecondGrp0:
 sty $1b
SecondResp0:
 sta $10
 bit $80
 nop
 nop
 nop
 lda #0
 sta $04
Row1:
 sta $02
 lda #0
 sta $1d
 lda #60
 sta $1b
 ldy #80
 ldx #1
 stx $04
 nop
 nop
FirstResp1:
 sta $10
 lda #24
 sta $1c
 bit $80
 nop
 nop
 nop
SecondGrp1:
 sty $1b
SecondResp1:
 sta $10
 bit $80
 nop
 nop
 nop
 lda #0
 sta $04
Row2:
 sta $02
 lda #2
 sta $1d
 lda #120
 sta $1b
 ldy #126
 ldx #1
 stx $04
 nop
 nop
FirstResp2:
 sta $10
 lda #36
 sta $1c
 bit $80
 nop
 nop
 nop
SecondGrp2:
 sty $1b
SecondResp2:
 sta $10
 bit $80
 nop
 nop
 nop
 lda #0
 sta $04
Row3:
 sta $02
 lda #0
 sta $1d
 lda #48
 sta $1b
 ldy #36
 ldx #1
 stx $04
 nop
 nop
FirstResp3:
 sta $10
 lda #0
 sta $1c
 bit $80
 nop
 nop
 nop
SecondGrp3:
 sty $1b
SecondResp3:
 sta $10
 bit $80
 nop
 nop
 nop
 lda #0
 sta $04
Row4:
 sta $02
 lda #0
 sta $1d
 lda #72
 sta $1b
 ldy #4
 ldx #1
 stx $04
 nop
 nop
FirstResp4:
 sta $10
 lda #0
 sta $1c
 bit $80
 nop
 nop
 nop
SecondGrp4:
 sty $1b
SecondResp4:
 sta $10
 bit $80
 nop
 nop
 nop
 lda #0
 sta $04
 sta $02
