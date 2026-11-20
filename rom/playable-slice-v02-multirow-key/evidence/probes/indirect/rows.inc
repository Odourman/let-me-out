Row0:
 sta $02
 lda #0
 sta $1d
 ldy #0
 lda ($89),y
 sta $1b
 lda ($d7),y
 sta $1c
 ldy #112
 ldx #1
 stx $05
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
 lda #$0e
 sta $07
Row1:
 sta $02
 lda #0
 sta $1d
 ldy #1
 lda ($89),y
 sta $1b
 lda ($d7),y
 sta $1c
 ldy #80
 ldx #1
 stx $05
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
 lda #$0e
 sta $07
Row2:
 sta $02
 lda #2
 sta $1d
 ldy #2
 lda ($89),y
 sta $1b
 lda ($d7),y
 sta $1c
 ldy #126
 ldx #1
 stx $05
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
 lda #$0e
 sta $07
Row3:
 sta $02
 lda #0
 sta $1d
 ldy #3
 lda ($89),y
 sta $1b
 lda ($d7),y
 sta $1c
 ldy #36
 ldx #1
 stx $05
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
 lda #$0e
 sta $07
Row4:
 sta $02
 lda #0
 sta $1d
 ldy #4
 lda ($89),y
 sta $1b
 lda ($d7),y
 sta $1c
 ldy #4
 ldx #1
 stx $05
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
 lda #$0e
 sta $07
 sta $02
