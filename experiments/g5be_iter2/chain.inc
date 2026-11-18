Scene0:
 sta WSYNC
Scene0Y76:
 iny
 lda PlayerRows,y
 sta.w GRP0
 lda #$18
 sta.b GRP1
 ldx #0
 lda #$18
 sty.b RESP1
 stx.w ENAM0
 ldx #$ff
 sty.b RESP1
 stx.b GRP0
 sta.b GRP1
 lda #14
 sta.b COLUP0
 nop
 lda #30
 sty.b RESP1
 ldx #$7e
 stx.b GRP1
 sty.w RESP1
 ldx #$ff
 stx.b GRP1
 nop
 sta.b COLUP0
 sta.b ENAM0
 bit FRAME
 nop
Scene0Y77:
 iny
 lda PlayerRows,y
 sta.w GRP0
 lda #$24
 sta.b GRP1
 ldx #0
 lda #$7e
 sty.b RESP1
 stx.w ENAM0
 ldx #$3c
 sty.b RESP1
 stx.b GRP0
 sta.b GRP1
 lda #14
 sta.b COLUP0
 nop
 lda #30
 sty.b RESP1
 ldx #$18
 stx.b GRP1
 sty.w RESP1
 ldx #$18
 stx.b GRP1
 nop
 sta.b COLUP0
 sta.b ENAM0
 nop
 jmp LeaveBand
Scene1:
 sta WSYNC
Scene1Y74:
 iny
 lda PlayerRows,y
 sta.w GRP0
 lda #$18
 sta.b GRP1
 ldx #0
 lda #$3c
 sty.b RESP1
 stx.w ENAM0
 ldx #$3c
 sty.b RESP1
 stx.b GRP0
 sta.b GRP1
 lda #14
 sta.b COLUP0
 nop
 lda #30
 sty.b RESP1
 ldx #$3c
 stx.b GRP1
 sty.w RESP1
 ldx #$3c
 stx.b GRP1
 nop
 sta.b COLUP0
 sta.b ENAM0
 bit FRAME
 nop
Scene1Y75:
 iny
 lda PlayerRows,y
 sta.w GRP0
 lda #$ff
 sta.b GRP1
 ldx #0
 lda #$3c
 sty.b RESP1
 stx.w ENAM0
 ldx #$18
 sty.b RESP1
 stx.b GRP0
 sta.b GRP1
 lda #14
 sta.b COLUP0
 nop
 lda #30
 sty.b RESP1
 ldx #$18
 stx.b GRP1
 sty.w RESP1
 ldx #$18
 stx.b GRP1
 nop
 sta.b COLUP0
 sta.b ENAM0
 bit FRAME
 nop
Scene1Y76:
 iny
 lda PlayerRows,y
 sta.w GRP0
 lda #$18
 sta.b GRP1
 ldx #0
 lda #$18
 sty.b RESP1
 stx.w ENAM0
 ldx #$ff
 sty.b RESP1
 stx.b GRP0
 sta.b GRP1
 lda #14
 sta.b COLUP0
 nop
 lda #30
 sty.b RESP1
 ldx #$7e
 stx.b GRP1
 sty.w RESP1
 ldx #$ff
 stx.b GRP1
 nop
 sta.b COLUP0
 sta.b ENAM0
 bit FRAME
 nop
Scene1Y77:
 iny
 lda PlayerRows,y
 sta.w GRP0
 lda #$24
 sta.b GRP1
 ldx #0
 lda #$7e
 sty.b RESP1
 stx.w ENAM0
 ldx #$3c
 sty.b RESP1
 stx.b GRP0
 sta.b GRP1
 lda #14
 sta.b COLUP0
 nop
 lda #30
 sty.b RESP1
 ldx #$18
 stx.b GRP1
 sty.w RESP1
 ldx #$18
 stx.b GRP1
 nop
 sta.b COLUP0
 sta.b ENAM0
 bit FRAME
 nop
Scene1Y78:
 iny
 lda PlayerRows,y
 sta.w GRP0
 lda #$24
 sta.b GRP1
 ldx #0
 lda #$3c
 sty.b RESP1
 stx.w ENAM0
 ldx #$7e
 sty.b RESP1
 stx.b GRP0
 sta.b GRP1
 lda #14
 sta.b COLUP0
 nop
 lda #30
 sty.b RESP1
 ldx #$24
 stx.b GRP1
 sty.w RESP1
 ldx #$24
 stx.b GRP1
 nop
 sta.b COLUP0
 sta.b ENAM0
 nop
 jmp LeaveBand
Scene2:
 sta WSYNC
Scene2Y71:
 iny
 lda PlayerRows,y
 sta.w GRP0
 lda #$00
 sta.b GRP1
 ldx #0
 lda #$00
 sty.b RESP1
 stx.w ENAM0
 ldx #$00
 sty.b RESP1
 stx.b GRP0
 sta.b GRP1
 lda #14
 sta.b COLUP0
 nop
 lda #30
 sty.b RESP1
 ldx #$00
 stx.b GRP1
 sty.w RESP1
 ldx #$00
 stx.b GRP1
 nop
 sta.b COLUP0
 sta.b ENAM0
 bit FRAME
 nop
Scene2Y72:
 iny
 lda PlayerRows,y
 sta.w GRP0
 lda #$3c
 sta.b GRP1
 ldx #0
 lda #$00
 sty.b RESP1
 stx.w ENAM0
 ldx #$00
 sty.b RESP1
 stx.b GRP0
 sta.b GRP1
 lda #14
 sta.b COLUP0
 nop
 lda #30
 sty.b RESP1
 ldx #$00
 stx.b GRP1
 sty.w RESP1
 ldx #$00
 stx.b GRP1
 nop
 sta.b COLUP0
 sta.b ENAM0
 bit FRAME
 nop
Scene2Y73:
 iny
 lda PlayerRows,y
 sta.w GRP0
 lda #$3c
 sta.b GRP1
 ldx #0
 lda #$00
 sty.b RESP1
 stx.w ENAM0
 ldx #$3c
 sty.b RESP1
 stx.b GRP0
 sta.b GRP1
 lda #14
 sta.b COLUP0
 nop
 lda #30
 sty.b RESP1
 ldx #$3c
 stx.b GRP1
 sty.w RESP1
 ldx #$3c
 stx.b GRP1
 nop
 sta.b COLUP0
 sta.b ENAM0
 bit FRAME
 nop
Scene2Y74:
 iny
 lda PlayerRows,y
 sta.w GRP0
 lda #$18
 sta.b GRP1
 ldx #0
 lda #$3c
 sty.b RESP1
 stx.w ENAM0
 ldx #$3c
 sty.b RESP1
 stx.b GRP0
 sta.b GRP1
 lda #14
 sta.b COLUP0
 nop
 lda #30
 sty.b RESP1
 ldx #$3c
 stx.b GRP1
 sty.w RESP1
 ldx #$3c
 stx.b GRP1
 nop
 sta.b COLUP0
 sta.b ENAM0
 bit FRAME
 nop
Scene2Y75:
 iny
 lda PlayerRows,y
 sta.w GRP0
 lda #$ff
 sta.b GRP1
 ldx #0
 lda #$3c
 sty.b RESP1
 stx.w ENAM0
 ldx #$18
 sty.b RESP1
 stx.b GRP0
 sta.b GRP1
 lda #14
 sta.b COLUP0
 nop
 lda #30
 sty.b RESP1
 ldx #$18
 stx.b GRP1
 sty.w RESP1
 ldx #$18
 stx.b GRP1
 nop
 sta.b COLUP0
 sta.b ENAM0
 bit FRAME
 nop
Scene2Y76:
 iny
 lda PlayerRows,y
 sta.w GRP0
 lda #$18
 sta.b GRP1
 ldx #0
 lda #$18
 sty.b RESP1
 stx.w ENAM0
 ldx #$ff
 sty.b RESP1
 stx.b GRP0
 sta.b GRP1
 lda #14
 sta.b COLUP0
 nop
 lda #30
 sty.b RESP1
 ldx #$7e
 stx.b GRP1
 sty.w RESP1
 ldx #$ff
 stx.b GRP1
 nop
 sta.b COLUP0
 sta.b ENAM0
 bit FRAME
 nop
Scene2Y77:
 iny
 lda PlayerRows,y
 sta.w GRP0
 lda #$24
 sta.b GRP1
 ldx #0
 lda #$7e
 sty.b RESP1
 stx.w ENAM0
 ldx #$3c
 sty.b RESP1
 stx.b GRP0
 sta.b GRP1
 lda #14
 sta.b COLUP0
 nop
 lda #30
 sty.b RESP1
 ldx #$18
 stx.b GRP1
 sty.w RESP1
 ldx #$18
 stx.b GRP1
 nop
 sta.b COLUP0
 sta.b ENAM0
 bit FRAME
 nop
Scene2Y78:
 iny
 lda PlayerRows,y
 sta.w GRP0
 lda #$24
 sta.b GRP1
 ldx #0
 lda #$3c
 sty.b RESP1
 stx.w ENAM0
 ldx #$7e
 sty.b RESP1
 stx.b GRP0
 sta.b GRP1
 lda #14
 sta.b COLUP0
 nop
 lda #30
 sty.b RESP1
 ldx #$24
 stx.b GRP1
 sty.w RESP1
 ldx #$24
 stx.b GRP1
 nop
 sta.b COLUP0
 sta.b ENAM0
 bit FRAME
 nop
Scene2Y79:
 iny
 lda PlayerRows,y
 sta.w GRP0
 lda #$42
 sta.b GRP1
 ldx #0
 lda #$24
 sty.b RESP1
 stx.w ENAM0
 ldx #$7e
 sty.b RESP1
 stx.b GRP0
 sta.b GRP1
 lda #14
 sta.b COLUP0
 nop
 lda #30
 sty.b RESP1
 ldx #$00
 stx.b GRP1
 sty.w RESP1
 ldx #$24
 stx.b GRP1
 nop
 sta.b COLUP0
 sta.b ENAM0
 bit FRAME
 nop
Scene2Y80:
 iny
 lda PlayerRows,y
 sta.w GRP0
 lda #$42
 sta.b GRP1
 ldx #0
 lda #$00
 sty.b RESP1
 stx.w ENAM0
 ldx #$24
 sty.b RESP1
 stx.b GRP0
 sta.b GRP1
 lda #14
 sta.b COLUP0
 nop
 lda #30
 sty.b RESP1
 ldx #$00
 stx.b GRP1
 sty.w RESP1
 ldx #$42
 stx.b GRP1
 nop
 sta.b COLUP0
 sta.b ENAM0
 bit FRAME
 nop
Scene2Y81:
 iny
 lda PlayerRows,y
 sta.w GRP0
 lda #$00
 sta.b GRP1
 ldx #0
 lda #$00
 sty.b RESP1
 stx.w ENAM0
 ldx #$24
 sty.b RESP1
 stx.b GRP0
 sta.b GRP1
 lda #14
 sta.b COLUP0
 nop
 lda #30
 sty.b RESP1
 ldx #$00
 stx.b GRP1
 sty.w RESP1
 ldx #$42
 stx.b GRP1
 nop
 sta.b COLUP0
 sta.b ENAM0
 nop
 jmp LeaveBand
Starts:
 byte 76,74,71
SceneLo:
 byte <Scene0,<Scene1,<Scene2
SceneHi:
 byte >Scene0,>Scene1,>Scene2
