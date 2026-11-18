NUSIZ_TEST=1

 processor 6502
VSYNC=$00
VBLANK=$01
WSYNC=$02
NUSIZ0=$04
NUSIZ1=$05
COLUP0=$06
COLUP1=$07
COLUPF=$08
COLUBK=$09
CTRLPF=$0a
PF0=$0d
PF1=$0e
PF2=$0f
RESP0=$10
RESP1=$11
RESM0=$12
GRP0=$1b
GRP1=$1c
ENAM0=$1d
FRAME=$80
 ORG $f000
Reset:
 sei
 cld
 ldx #$ff
 txs
 lda #0
 ldx #$7f
Clear:
 sta $80,x
 dex
 bpl Clear
 sta VBLANK
 sta VSYNC
 sta GRP0
 sta GRP1
 sta ENAM0
 sta NUSIZ0
 sta COLUBK
 sta PF1
 sta PF2
 lda #$1e
 sta COLUP0
 lda #$0e
 sta COLUP1
 lda #$26
 sta COLUPF
 lda #$01
 sta CTRLPF
 lda #$30
 sta PF0
 lda #NUSIZ_TEST
 sta NUSIZ1
Frame:
 sta WSYNC
 lda #2
 sta VSYNC
 sta VBLANK
 lda FRAME
 lsr
 lsr
 lsr
 lsr
 and #3
 tax
 lda $fff6,x
BankSwitched:
 sta WSYNC
 sta WSYNC
 ; First of 37 VBLANK scanlines.
 sta WSYNC
 lda #0
 sta VSYNC
 sta GRP0
 sta GRP1
 sta ENAM0
 ; Distinct right-side P0/M0 x. No HMOVE needed for these fixed witnesses.
 sta WSYNC
 ldx #4
PositionPlayer:
 dex
 bne PositionPlayer
 sta RESP0
 sta WSYNC
 ldx #5
PositionMissile:
 dex
 bne PositionMissile
 sta RESM0
 ldx #34
BlankFill:
 sta WSYNC
 dex
 bne BlankFill
 ; Visible line 0 is the following WSYNC.

RasterR2:
 ldx #72
 ldy #$38
TopFillR2:
 sta WSYNC
 lda #0
 sta VBLANK
 dex
 bne TopFillR2
 lda #2
 sta ENAM0
LineR2_72:
 sta WSYNC
 lda #$30
 sta PF0
 lda #$26
 sta COLUPF
 lda #$0e
 sta COLUP1
 lda #$3c
 sta GRP0
 ldx #$30
 lda #$3c
 sta RESP1
 sta GRP1
 lda #$3c
 sta RESP1
 sta GRP1
 lda #$3c
 sta RESP1
 sta GRP1
 lda #$00
 sta RESP1
 sta GRP1
 lda #$2c
 sta COLUP1
 lda #$38
 sta RESP1
 sta GRP1
 stx PF0
 sty COLUPF
LineR2_73:
 sta WSYNC
 lda #$30
 sta PF0
 lda #$26
 sta COLUPF
 lda #$0e
 sta COLUP1
 lda #$7e
 sta GRP0
 ldx #$30
 lda #$3c
 sta RESP1
 sta GRP1
 lda #$3c
 sta RESP1
 sta GRP1
 lda #$3c
 sta RESP1
 sta GRP1
 lda #$00
 sta RESP1
 sta GRP1
 lda #$2c
 sta COLUP1
 lda #$44
 sta RESP1
 sta GRP1
 stx PF0
 sty COLUPF
LineR2_74:
 sta WSYNC
 lda #$30
 sta PF0
 lda #$26
 sta COLUPF
 lda #$0e
 sta COLUP1
 lda #$18
 sta GRP0
 ldx #$20
 lda #$18
 sta RESP1
 sta GRP1
 lda #$18
 sta RESP1
 sta GRP1
 lda #$18
 sta RESP1
 sta GRP1
 lda #$3c
 sta RESP1
 sta GRP1
 lda #$2c
 sta COLUP1
 lda #$44
 sta RESP1
 sta GRP1
 stx PF0
 sty COLUPF
LineR2_75:
 sta WSYNC
 lda #$30
 sta PF0
 lda #$26
 sta COLUPF
 lda #$0e
 sta COLUP1
 lda #$7e
 sta GRP0
 ldx #$20
 lda #$ff
 sta RESP1
 sta GRP1
 lda #$ff
 sta RESP1
 sta GRP1
 lda #$ff
 sta RESP1
 sta GRP1
 lda #$3c
 sta RESP1
 sta GRP1
 lda #$2c
 sta COLUP1
 lda #$38
 sta RESP1
 sta GRP1
 stx PF0
 sty COLUPF
LineR2_76:
 sta WSYNC
 lda #$30
 sta PF0
 lda #$26
 sta COLUPF
 lda #$0e
 sta COLUP1
 lda #$1e
 sta GRP0
 ldx #$20
 lda #$18
 sta RESP1
 sta GRP1
 lda #$18
 sta RESP1
 sta GRP1
 lda #$3c
 sta RESP1
 sta GRP1
 lda #$18
 sta RESP1
 sta GRP1
 lda #$2c
 sta COLUP1
 lda #$10
 sta RESP1
 sta GRP1
 stx PF0
 sty COLUPF
LineR2_77:
 sta WSYNC
 lda #$30
 sta PF0
 lda #$26
 sta COLUPF
 lda #$0e
 sta COLUP1
 lda #$3c
 sta GRP0
 ldx #$30
 lda #$24
 sta RESP1
 sta GRP1
 lda #$24
 sta RESP1
 sta GRP1
 lda #$7e
 sta RESP1
 sta GRP1
 lda #$7e
 sta RESP1
 sta GRP1
 lda #$2c
 sta COLUP1
 lda #$1c
 sta RESP1
 sta GRP1
 stx PF0
 sty COLUPF
LineR2_78:
 sta WSYNC
 lda #$30
 sta PF0
 lda #$26
 sta COLUPF
 lda #$0e
 sta COLUP1
 lda #$18
 sta GRP0
 ldx #$30
 lda #$24
 sta RESP1
 sta GRP1
 lda #$24
 sta RESP1
 sta GRP1
 lda #$7e
 sta RESP1
 sta GRP1
 lda #$18
 sta RESP1
 sta GRP1
 lda #$2c
 sta COLUP1
 lda #$10
 sta RESP1
 sta GRP1
 stx PF0
 sty COLUPF
LineR2_79:
 sta WSYNC
 lda #$30
 sta PF0
 lda #$26
 sta COLUPF
 lda #$0e
 sta COLUP1
 lda #$24
 sta GRP0
 ldx #$30
 lda #$42
 sta RESP1
 sta GRP1
 lda #$42
 sta RESP1
 sta GRP1
 lda #$24
 sta RESP1
 sta GRP1
 lda #$24
 sta RESP1
 sta GRP1
 lda #$2c
 sta COLUP1
 lda #$18
 sta RESP1
 sta GRP1
 stx PF0
 sty COLUPF
LineR2_80:
 sta WSYNC
 lda #$30
 sta PF0
 lda #$26
 sta COLUPF
 lda #$0e
 sta COLUP1
 lda #$42
 sta GRP0
 ldx #$30
 lda #$42
 sta RESP1
 sta GRP1
 lda #$42
 sta RESP1
 sta GRP1
 lda #$24
 sta RESP1
 sta GRP1
 lda #$00
 sta RESP1
 sta GRP1
 lda #$2c
 sta COLUP1
 lda #$00
 sta RESP1
 sta GRP1
 stx PF0
 sty COLUPF
 sta WSYNC
 lda #0
 sta GRP1
 sta GRP0
 sta ENAM0
 lda #$30
 sta PF0
 lda #$26
 sta COLUPF
 ldx #110
BottomFillR2:
 sta WSYNC
 dex
 bne BottomFillR2
EndRaster:

 ldx #30
Overscan:
 sta WSYNC
 lda #2
 sta VBLANK
 dex
 bne Overscan
 inc FRAME
 jmp Frame
EndKernel:
 ORG $fffa
 word Reset,Reset,Reset
