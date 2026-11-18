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
 ldx #13
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

RasterAll:
 ldx #68
TopFillAll:
 sta WSYNC
 lda #0
 sta VBLANK
 dex
 bne TopFillAll
LineAll_68:
 sta WSYNC
 lda #$00
 sta GRP0
 lda #$00
 sta ENAM0
 lda #0
 sta GRP1
LineAll_69:
 sta WSYNC
 lda #$00
 sta GRP0
 lda #$00
 sta ENAM0
 lda #0
 sta GRP1
LineAll_70:
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
 lda #$3c
 sta RESP1
 sta GRP1
LineAll_71:
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
 lda #$3c
 sta RESP1
 nop
 sta GRP1
 bit FRAME
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
LineAll_72:
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
 lda #$18
 sta RESP1,x
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
 lda #$3c
 sta RESP1
 sta GRP1
LineAll_73:
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
 lda #$ff
 sta RESP1,x
 sta GRP1
 nop
 nop
 nop
 nop
 nop
 lda #$00
 sta RESP1
 sta GRP1
 lda #$18
 sta RESP1,x
 sta GRP1
LineAll_74:
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
 lda #$18
 sta RESP1,x
 sta GRP1
 lda #$00
 sta RESP1,x
 sta GRP1
 lda #$00
 sta RESP1,x
 sta GRP1
 lda #$ff
 sta RESP1,x
 sta GRP1
LineAll_75:
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
 lda #$24
 sta RESP1,x
 sta GRP1
 lda #$00
 sta RESP1,x
 sta GRP1
 lda #$3c
 sta RESP1,x
 sta GRP1
 lda #$18
 sta RESP1,x
 sta GRP1
LineAll_76:
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
 lda #$24
 sta RESP1,x
 sta GRP1
 lda #$3c
 sta RESP1,x
 sta GRP1
 lda #$3c
 sta RESP1,x
 sta GRP1
 lda #$24
 sta RESP1,x
 sta GRP1
LineAll_77:
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
 lda #$42
 sta RESP1,x
 sta GRP1
 lda #$3c
 sta RESP1,x
 sta GRP1
 lda #$18
 sta RESP1,x
 sta GRP1
 lda #$24
 sta RESP1,x
 sta GRP1
LineAll_78:
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
 lda #$42
 sta RESP1,x
 sta GRP1
 lda #$18
 sta RESP1,x
 sta GRP1
 lda #$7e
 sta RESP1,x
 sta GRP1
 lda #$42
 sta RESP1,x
 sta GRP1
LineAll_79:
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
 nop
 nop
 nop
 nop
 nop
 lda #$7e
 sta RESP1
 sta GRP1
 lda #$18
 sta RESP1,x
 sta GRP1
 lda #$42
 sta RESP1,x
 sta GRP1
LineAll_80:
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
 nop
 nop
 nop
 nop
 nop
 lda #$3c
 sta RESP1
 sta GRP1
 lda #$24
 sta RESP1,x
 sta GRP1
LineAll_81:
 sta WSYNC
 lda #$00
 sta GRP0
 lda #$00
 sta ENAM0
 lda #0
 sta GRP1
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
 lda #$00
 sta RESP1,x
 sta GRP1
LineAll_82:
 sta WSYNC
 lda #$00
 sta GRP0
 lda #$00
 sta ENAM0
 lda #0
 sta GRP1
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
LineAll_83:
 sta WSYNC
 lda #$00
 sta GRP0
 lda #$00
 sta ENAM0
 lda #0
 sta GRP1
LineAll_84:
 sta WSYNC
 lda #$00
 sta GRP0
 lda #$00
 sta ENAM0
 lda #0
 sta GRP1
LineAll_85:
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
BottomFillAll:
 sta WSYNC
 dex
 bne BottomFillAll
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
