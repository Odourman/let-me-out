NUSIZ_TEST=0

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
 ldx #13
PositionPlayer:
 dex
 bne PositionPlayer
 sta RESP0
 sta WSYNC
 ldx #14
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

 lda FRAME
 and #1
 beq EvenJump
 jmp RasterOdd
EvenJump:
 jmp RasterEven
RasterEven:
 ldx #68
TopFillEven:
 sta WSYNC
 lda #0
 sta VBLANK
 dex
 bne TopFillEven
LineEven_68:
 sta WSYNC
 lda #$00
 sta GRP0
 lda #$00
 sta ENAM0
 lda #0
 sta GRP1
LineEven_69:
 sta WSYNC
 lda #$00
 sta GRP0
 lda #$00
 sta ENAM0
 lda #0
 sta GRP1
LineEven_70:
 sta WSYNC
 lda #$00
 sta GRP0
 lda #$00
 sta ENAM0
 lda #0
 sta GRP1
 bit FRAME
 nop
 nop
 nop
 nop
 nop
 nop
 lda #$3c
 sta RESP1
 sta GRP1
LineEven_71:
 sta WSYNC
 lda #$00
 sta GRP0
 lda #$00
 sta ENAM0
 lda #0
 sta GRP1
 bit FRAME
 nop
 nop
 nop
 nop
 nop
 nop
 lda #$3c
 sta RESP1
 sta GRP1
LineEven_72:
 sta WSYNC
 lda #$3c
 sta GRP0
 lda #$00
 sta ENAM0
 lda #0
 sta GRP1
 nop
 lda #$3c
 sta RESP1
 sta GRP1
 bit FRAME
 nop
 lda #$18
 sta RESP1
 sta GRP1
LineEven_73:
 sta WSYNC
 lda #$7e
 sta GRP0
 lda #$00
 sta ENAM0
 lda #0
 sta GRP1
 nop
 lda #$3c
 sta RESP1
 sta GRP1
 bit FRAME
 nop
 lda #$ff
 sta RESP1
 sta GRP1
LineEven_74:
 sta WSYNC
 lda #$18
 sta GRP0
 lda #$00
 sta ENAM0
 lda #0
 sta GRP1
 nop
 lda #$18
 sta RESP1
 sta GRP1
 bit FRAME
 nop
 lda #$18
 sta RESP1
 sta GRP1
 nop
 lda #$00
 sta RESP1
 sta GRP1
LineEven_75:
 sta WSYNC
 lda #$7e
 sta GRP0
 lda #$02
 sta ENAM0
 lda #0
 sta GRP1
 nop
 lda #$ff
 sta RESP1
 sta GRP1
 bit FRAME
 nop
 lda #$24
 sta RESP1
 sta GRP1
 nop
 lda #$00
 sta RESP1
 sta GRP1
LineEven_76:
 sta WSYNC
 lda #$1e
 sta GRP0
 lda #$02
 sta ENAM0
 lda #0
 sta GRP1
 nop
 lda #$3c
 sta RESP1
 sta GRP1
 bit FRAME
 nop
 lda #$24
 sta RESP1
 sta GRP1
 nop
 lda #$3c
 sta RESP1
 sta GRP1
LineEven_77:
 sta WSYNC
 lda #$3c
 sta GRP0
 lda #$00
 sta ENAM0
 lda #0
 sta GRP1
 nop
 lda #$7e
 sta RESP1
 sta GRP1
 bit FRAME
 nop
 lda #$42
 sta RESP1
 sta GRP1
 nop
 lda #$3c
 sta RESP1
 sta GRP1
LineEven_78:
 sta WSYNC
 lda #$18
 sta GRP0
 lda #$00
 sta ENAM0
 lda #0
 sta GRP1
 nop
 lda #$7e
 sta RESP1
 sta GRP1
 bit FRAME
 nop
 lda #$42
 sta RESP1
 sta GRP1
 nop
 lda #$18
 sta RESP1
 sta GRP1
LineEven_79:
 sta WSYNC
 lda #$24
 sta GRP0
 lda #$00
 sta ENAM0
 lda #0
 sta GRP1
 nop
 lda #$24
 sta RESP1
 sta GRP1
 bit FRAME
 nop
 nop
 nop
 nop
 nop
 nop
 lda #$7e
 sta RESP1
 sta GRP1
LineEven_80:
 sta WSYNC
 lda #$42
 sta GRP0
 lda #$00
 sta ENAM0
 lda #0
 sta GRP1
 nop
 lda #$24
 sta RESP1
 sta GRP1
 bit FRAME
 nop
 nop
 nop
 nop
 nop
 nop
 lda #$3c
 sta RESP1
 sta GRP1
LineEven_81:
 sta WSYNC
 lda #$00
 sta GRP0
 lda #$00
 sta ENAM0
 lda #0
 sta GRP1
 bit FRAME
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
 lda #$24
 sta RESP1
 sta GRP1
LineEven_82:
 sta WSYNC
 lda #$00
 sta GRP0
 lda #$00
 sta ENAM0
 lda #0
 sta GRP1
 bit FRAME
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
 lda #$00
 sta RESP1
 sta GRP1
LineEven_83:
 sta WSYNC
 lda #$00
 sta GRP0
 lda #$00
 sta ENAM0
 lda #0
 sta GRP1
LineEven_84:
 sta WSYNC
 lda #$00
 sta GRP0
 lda #$00
 sta ENAM0
 lda #0
 sta GRP1
LineEven_85:
 sta WSYNC
 lda #$00
 sta GRP0
 lda #$00
 sta ENAM0
 lda #0
 sta GRP1
 sta WSYNC
 lda #0
 sta GRP1
 sta GRP0
 sta ENAM0
 ldx #105
BottomFillEven:
 sta WSYNC
 dex
 bne BottomFillEven
 jmp EndRaster

RasterOdd:
 ldx #68
TopFillOdd:
 sta WSYNC
 lda #0
 sta VBLANK
 dex
 bne TopFillOdd
LineOdd_68:
 sta WSYNC
 lda #$00
 sta GRP0
 lda #$00
 sta ENAM0
 lda #0
 sta GRP1
LineOdd_69:
 sta WSYNC
 lda #$00
 sta GRP0
 lda #$00
 sta ENAM0
 lda #0
 sta GRP1
LineOdd_70:
 sta WSYNC
 lda #$00
 sta GRP0
 lda #$00
 sta ENAM0
 lda #0
 sta GRP1
LineOdd_71:
 sta WSYNC
 lda #$00
 sta GRP0
 lda #$00
 sta ENAM0
 lda #0
 sta GRP1
 bit FRAME
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
 nop
 nop
 nop
 nop
 nop
 nop
 nop
 nop
 nop
 lda #$3c
 sta RESP1
 sta GRP1
LineOdd_72:
 sta WSYNC
 lda #$3c
 sta GRP0
 lda #$00
 sta ENAM0
 lda #0
 sta GRP1
 bit FRAME
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
 nop
 nop
 nop
 nop
 nop
 nop
 nop
 nop
 nop
 lda #$3c
 sta RESP1
 sta GRP1
LineOdd_73:
 sta WSYNC
 lda #$7e
 sta GRP0
 lda #$00
 sta ENAM0
 lda #0
 sta GRP1
 bit FRAME
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
 nop
 nop
 nop
 nop
 lda #$00
 sta RESP1
 sta GRP1
 nop
 lda #$18
 sta RESP1
 sta GRP1
LineOdd_74:
 sta WSYNC
 lda #$18
 sta GRP0
 lda #$00
 sta ENAM0
 lda #0
 sta GRP1
 bit FRAME
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
 nop
 nop
 nop
 nop
 lda #$00
 sta RESP1
 sta GRP1
 nop
 lda #$ff
 sta RESP1
 sta GRP1
LineOdd_75:
 sta WSYNC
 lda #$7e
 sta GRP0
 lda #$02
 sta ENAM0
 lda #0
 sta GRP1
 bit FRAME
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
 nop
 nop
 nop
 nop
 lda #$3c
 sta RESP1
 sta GRP1
 nop
 lda #$18
 sta RESP1
 sta GRP1
LineOdd_76:
 sta WSYNC
 lda #$1e
 sta GRP0
 lda #$02
 sta ENAM0
 lda #0
 sta GRP1
 bit FRAME
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
 nop
 nop
 nop
 nop
 lda #$3c
 sta RESP1
 sta GRP1
 nop
 lda #$24
 sta RESP1
 sta GRP1
LineOdd_77:
 sta WSYNC
 lda #$3c
 sta GRP0
 lda #$00
 sta ENAM0
 lda #0
 sta GRP1
 bit FRAME
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
 nop
 nop
 nop
 nop
 lda #$18
 sta RESP1
 sta GRP1
 nop
 lda #$24
 sta RESP1
 sta GRP1
LineOdd_78:
 sta WSYNC
 lda #$18
 sta GRP0
 lda #$00
 sta ENAM0
 lda #0
 sta GRP1
 bit FRAME
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
 nop
 nop
 nop
 nop
 lda #$7e
 sta RESP1
 sta GRP1
 nop
 lda #$42
 sta RESP1
 sta GRP1
LineOdd_79:
 sta WSYNC
 lda #$24
 sta GRP0
 lda #$00
 sta ENAM0
 lda #0
 sta GRP1
 bit FRAME
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
 nop
 nop
 nop
 nop
 lda #$18
 sta RESP1
 sta GRP1
 nop
 lda #$42
 sta RESP1
 sta GRP1
LineOdd_80:
 sta WSYNC
 lda #$42
 sta GRP0
 lda #$00
 sta ENAM0
 lda #0
 sta GRP1
 bit FRAME
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
 nop
 nop
 nop
 nop
 lda #$24
 sta RESP1
 sta GRP1
LineOdd_81:
 sta WSYNC
 lda #$00
 sta GRP0
 lda #$00
 sta ENAM0
 lda #0
 sta GRP1
 bit FRAME
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
 nop
 nop
 nop
 nop
 lda #$00
 sta RESP1
 sta GRP1
LineOdd_82:
 sta WSYNC
 lda #$00
 sta GRP0
 lda #$00
 sta ENAM0
 lda #0
 sta GRP1
LineOdd_83:
 sta WSYNC
 lda #$00
 sta GRP0
 lda #$00
 sta ENAM0
 lda #0
 sta GRP1
LineOdd_84:
 sta WSYNC
 lda #$00
 sta GRP0
 lda #$00
 sta ENAM0
 lda #0
 sta GRP1
LineOdd_85:
 sta WSYNC
 lda #$00
 sta GRP0
 lda #$00
 sta ENAM0
 lda #0
 sta GRP1
 sta WSYNC
 lda #0
 sta GRP1
 sta GRP0
 sta ENAM0
 ldx #105
BottomFillOdd:
 sta WSYNC
 dex
 bne BottomFillOdd
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
