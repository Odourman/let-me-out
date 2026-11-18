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

 lda FRAME
 lsr
 lsr
 and #3
 tax
 lda LowJump,x
 sta $81
 lda HighJump,x
 sta $82
 jmp ($0081)
LowJump:
 byte <Raster0,<Raster1,<Raster2,<Raster3
HighJump:
 byte >Raster0,>Raster1,>Raster2,>Raster3
Raster0:
 ldx #68
TopFill0:
 sta WSYNC
 lda #0
 sta VBLANK
 dex
 bne TopFill0
Line0_68:
 sta WSYNC
 lda #$00
 sta GRP0
 lda #$00
 sta ENAM0
 lda #0
 sta GRP1
Line0_69:
 sta WSYNC
 lda #$00
 sta GRP0
 lda #$00
 sta ENAM0
 lda #0
 sta GRP1
Line0_70:
 sta WSYNC
 lda #$00
 sta GRP0
 lda #$00
 sta ENAM0
 lda #0
 sta GRP1
Line0_71:
 sta WSYNC
 lda #$00
 sta GRP0
 lda #$00
 sta ENAM0
 lda #0
 sta GRP1
Line0_72:
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
 lda #$3c
 sta RESP1
 sta GRP1
 nop
 lda #$3c
 sta RESP1
 sta GRP1
 lda #$00
 sta RESP1,x
 sta GRP1
 lda #$00
 sta RESP1,x
 sta GRP1
Line0_73:
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
 lda #$3c
 sta RESP1
 sta GRP1
 nop
 lda #$3c
 sta RESP1
 sta GRP1
 lda #$00
 sta RESP1,x
 sta GRP1
 lda #$00
 sta RESP1,x
 sta GRP1
Line0_74:
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
 sta RESP1
 sta GRP1
 nop
 lda #$18
 sta RESP1
 sta GRP1
 lda #$3c
 sta RESP1,x
 sta GRP1
 lda #$3c
 sta RESP1,x
 sta GRP1
Line0_75:
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
 lda #$ff
 sta RESP1
 sta GRP1
 nop
 lda #$ff
 sta RESP1
 sta GRP1
 lda #$3c
 sta RESP1,x
 sta GRP1
 lda #$3c
 sta RESP1,x
 sta GRP1
Line0_76:
 sta WSYNC
 lda #$1e
 sta GRP0
 lda #$02
 sta ENAM0
 lda #0
 sta GRP1
 nop
 lda #$18
 sta RESP1
 sta GRP1
 lda #$18
 sta RESP1
 sta GRP1
 nop
 lda #$3c
 sta RESP1
 sta GRP1
 lda #$18
 sta RESP1,x
 sta GRP1
 lda #$18
 sta RESP1,x
 sta GRP1
Line0_77:
 sta WSYNC
 lda #$3c
 sta GRP0
 lda #$00
 sta ENAM0
 lda #0
 sta GRP1
 nop
 lda #$24
 sta RESP1
 sta GRP1
 lda #$24
 sta RESP1
 sta GRP1
 nop
 lda #$7e
 sta RESP1
 sta GRP1
 lda #$7e
 sta RESP1,x
 sta GRP1
 lda #$7e
 sta RESP1,x
 sta GRP1
Line0_78:
 sta WSYNC
 lda #$18
 sta GRP0
 lda #$00
 sta ENAM0
 lda #0
 sta GRP1
 nop
 lda #$24
 sta RESP1
 sta GRP1
 lda #$24
 sta RESP1
 sta GRP1
 nop
 lda #$7e
 sta RESP1
 sta GRP1
 lda #$18
 sta RESP1,x
 sta GRP1
 lda #$3c
 sta RESP1,x
 sta GRP1
Line0_79:
 sta WSYNC
 lda #$24
 sta GRP0
 lda #$00
 sta ENAM0
 lda #0
 sta GRP1
 nop
 lda #$42
 sta RESP1
 sta GRP1
 lda #$42
 sta RESP1
 sta GRP1
 nop
 lda #$24
 sta RESP1
 sta GRP1
 lda #$24
 sta RESP1,x
 sta GRP1
 lda #$24
 sta RESP1,x
 sta GRP1
Line0_80:
 sta WSYNC
 lda #$42
 sta GRP0
 lda #$00
 sta ENAM0
 lda #0
 sta GRP1
 nop
 lda #$42
 sta RESP1
 sta GRP1
 lda #$42
 sta RESP1
 sta GRP1
 nop
 lda #$24
 sta RESP1
 sta GRP1
 lda #$00
 sta RESP1,x
 sta GRP1
 lda #$00
 sta RESP1,x
 sta GRP1
Line0_81:
 sta WSYNC
 lda #$00
 sta GRP0
 lda #$00
 sta ENAM0
 lda #0
 sta GRP1
Line0_82:
 sta WSYNC
 lda #$00
 sta GRP0
 lda #$00
 sta ENAM0
 lda #0
 sta GRP1
Line0_83:
 sta WSYNC
 lda #$00
 sta GRP0
 lda #$00
 sta ENAM0
 lda #0
 sta GRP1
Line0_84:
 sta WSYNC
 lda #$00
 sta GRP0
 lda #$00
 sta ENAM0
 lda #0
 sta GRP1
Line0_85:
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
BottomFill0:
 sta WSYNC
 dex
 bne BottomFill0
 jmp EndRaster

Raster1:
 ldx #68
TopFill1:
 sta WSYNC
 lda #0
 sta VBLANK
 dex
 bne TopFill1
Line1_68:
 sta WSYNC
 lda #$00
 sta GRP0
 lda #$00
 sta ENAM0
 lda #0
 sta GRP1
Line1_69:
 sta WSYNC
 lda #$00
 sta GRP0
 lda #$00
 sta ENAM0
 lda #0
 sta GRP1
Line1_70:
 sta WSYNC
 lda #$00
 sta GRP0
 lda #$00
 sta ENAM0
 lda #0
 sta GRP1
Line1_71:
 sta WSYNC
 lda #$00
 sta GRP0
 lda #$00
 sta ENAM0
 lda #0
 sta GRP1
Line1_72:
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
 lda #$3c
 sta RESP1,x
 sta GRP1
 lda #$3c
 sta RESP1
 sta GRP1
 nop
 lda #$00
 sta RESP1
 sta GRP1
 lda #$00
 sta RESP1,x
 sta GRP1
Line1_73:
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
 lda #$3c
 sta RESP1,x
 sta GRP1
 lda #$3c
 sta RESP1
 sta GRP1
 nop
 lda #$00
 sta RESP1
 sta GRP1
 lda #$00
 sta RESP1,x
 sta GRP1
Line1_74:
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
 lda #$18
 sta RESP1
 sta GRP1
 nop
 lda #$3c
 sta RESP1
 sta GRP1
 lda #$3c
 sta RESP1,x
 sta GRP1
Line1_75:
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
 lda #$ff
 sta RESP1,x
 sta GRP1
 lda #$ff
 sta RESP1
 sta GRP1
 nop
 lda #$3c
 sta RESP1
 sta GRP1
 lda #$3c
 sta RESP1,x
 sta GRP1
Line1_76:
 sta WSYNC
 lda #$1e
 sta GRP0
 lda #$02
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
 lda #$3c
 sta RESP1
 sta GRP1
 nop
 lda #$18
 sta RESP1
 sta GRP1
 lda #$18
 sta RESP1,x
 sta GRP1
Line1_77:
 sta WSYNC
 lda #$3c
 sta GRP0
 lda #$00
 sta ENAM0
 lda #0
 sta GRP1
 nop
 lda #$24
 sta RESP1
 sta GRP1
 lda #$24
 sta RESP1,x
 sta GRP1
 lda #$7e
 sta RESP1
 sta GRP1
 nop
 lda #$7e
 sta RESP1
 sta GRP1
 lda #$7e
 sta RESP1,x
 sta GRP1
Line1_78:
 sta WSYNC
 lda #$18
 sta GRP0
 lda #$00
 sta ENAM0
 lda #0
 sta GRP1
 nop
 lda #$24
 sta RESP1
 sta GRP1
 lda #$24
 sta RESP1,x
 sta GRP1
 lda #$7e
 sta RESP1
 sta GRP1
 nop
 lda #$18
 sta RESP1
 sta GRP1
 lda #$3c
 sta RESP1,x
 sta GRP1
Line1_79:
 sta WSYNC
 lda #$24
 sta GRP0
 lda #$00
 sta ENAM0
 lda #0
 sta GRP1
 nop
 lda #$42
 sta RESP1
 sta GRP1
 lda #$42
 sta RESP1,x
 sta GRP1
 lda #$24
 sta RESP1
 sta GRP1
 nop
 lda #$24
 sta RESP1
 sta GRP1
 lda #$24
 sta RESP1,x
 sta GRP1
Line1_80:
 sta WSYNC
 lda #$42
 sta GRP0
 lda #$00
 sta ENAM0
 lda #0
 sta GRP1
 nop
 lda #$42
 sta RESP1
 sta GRP1
 lda #$42
 sta RESP1,x
 sta GRP1
 lda #$24
 sta RESP1
 sta GRP1
 nop
 lda #$00
 sta RESP1
 sta GRP1
 lda #$00
 sta RESP1,x
 sta GRP1
Line1_81:
 sta WSYNC
 lda #$00
 sta GRP0
 lda #$00
 sta ENAM0
 lda #0
 sta GRP1
Line1_82:
 sta WSYNC
 lda #$00
 sta GRP0
 lda #$00
 sta ENAM0
 lda #0
 sta GRP1
Line1_83:
 sta WSYNC
 lda #$00
 sta GRP0
 lda #$00
 sta ENAM0
 lda #0
 sta GRP1
Line1_84:
 sta WSYNC
 lda #$00
 sta GRP0
 lda #$00
 sta ENAM0
 lda #0
 sta GRP1
Line1_85:
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
BottomFill1:
 sta WSYNC
 dex
 bne BottomFill1
 jmp EndRaster

Raster2:
 ldx #68
TopFill2:
 sta WSYNC
 lda #0
 sta VBLANK
 dex
 bne TopFill2
Line2_68:
 sta WSYNC
 lda #$00
 sta GRP0
 lda #$00
 sta ENAM0
 lda #0
 sta GRP1
Line2_69:
 sta WSYNC
 lda #$00
 sta GRP0
 lda #$00
 sta ENAM0
 lda #0
 sta GRP1
Line2_70:
 sta WSYNC
 lda #$00
 sta GRP0
 lda #$00
 sta ENAM0
 lda #0
 sta GRP1
Line2_71:
 sta WSYNC
 lda #$00
 sta GRP0
 lda #$00
 sta ENAM0
 lda #0
 sta GRP1
Line2_72:
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
 lda #$3c
 sta RESP1,x
 sta GRP1
 lda #$3c
 sta RESP1,x
 sta GRP1
 lda #$00
 sta RESP1
 sta GRP1
 nop
 lda #$00
 sta RESP1
 sta GRP1
Line2_73:
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
 lda #$3c
 sta RESP1,x
 sta GRP1
 lda #$3c
 sta RESP1,x
 sta GRP1
 lda #$00
 sta RESP1
 sta GRP1
 nop
 lda #$00
 sta RESP1
 sta GRP1
Line2_74:
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
 lda #$18
 sta RESP1,x
 sta GRP1
 lda #$3c
 sta RESP1
 sta GRP1
 nop
 lda #$3c
 sta RESP1
 sta GRP1
Line2_75:
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
 lda #$ff
 sta RESP1,x
 sta GRP1
 lda #$ff
 sta RESP1,x
 sta GRP1
 lda #$3c
 sta RESP1
 sta GRP1
 nop
 lda #$3c
 sta RESP1
 sta GRP1
Line2_76:
 sta WSYNC
 lda #$1e
 sta GRP0
 lda #$02
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
 lda #$3c
 sta RESP1,x
 sta GRP1
 lda #$18
 sta RESP1
 sta GRP1
 nop
 lda #$18
 sta RESP1
 sta GRP1
Line2_77:
 sta WSYNC
 lda #$3c
 sta GRP0
 lda #$00
 sta ENAM0
 lda #0
 sta GRP1
 nop
 lda #$24
 sta RESP1
 sta GRP1
 lda #$24
 sta RESP1,x
 sta GRP1
 lda #$7e
 sta RESP1,x
 sta GRP1
 lda #$7e
 sta RESP1
 sta GRP1
 nop
 lda #$7e
 sta RESP1
 sta GRP1
Line2_78:
 sta WSYNC
 lda #$18
 sta GRP0
 lda #$00
 sta ENAM0
 lda #0
 sta GRP1
 nop
 lda #$24
 sta RESP1
 sta GRP1
 lda #$24
 sta RESP1,x
 sta GRP1
 lda #$7e
 sta RESP1,x
 sta GRP1
 lda #$18
 sta RESP1
 sta GRP1
 nop
 lda #$3c
 sta RESP1
 sta GRP1
Line2_79:
 sta WSYNC
 lda #$24
 sta GRP0
 lda #$00
 sta ENAM0
 lda #0
 sta GRP1
 nop
 lda #$42
 sta RESP1
 sta GRP1
 lda #$42
 sta RESP1,x
 sta GRP1
 lda #$24
 sta RESP1,x
 sta GRP1
 lda #$24
 sta RESP1
 sta GRP1
 nop
 lda #$24
 sta RESP1
 sta GRP1
Line2_80:
 sta WSYNC
 lda #$42
 sta GRP0
 lda #$00
 sta ENAM0
 lda #0
 sta GRP1
 nop
 lda #$42
 sta RESP1
 sta GRP1
 lda #$42
 sta RESP1,x
 sta GRP1
 lda #$24
 sta RESP1,x
 sta GRP1
 lda #$00
 sta RESP1
 sta GRP1
 nop
 lda #$00
 sta RESP1
 sta GRP1
Line2_81:
 sta WSYNC
 lda #$00
 sta GRP0
 lda #$00
 sta ENAM0
 lda #0
 sta GRP1
Line2_82:
 sta WSYNC
 lda #$00
 sta GRP0
 lda #$00
 sta ENAM0
 lda #0
 sta GRP1
Line2_83:
 sta WSYNC
 lda #$00
 sta GRP0
 lda #$00
 sta ENAM0
 lda #0
 sta GRP1
Line2_84:
 sta WSYNC
 lda #$00
 sta GRP0
 lda #$00
 sta ENAM0
 lda #0
 sta GRP1
Line2_85:
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
BottomFill2:
 sta WSYNC
 dex
 bne BottomFill2
 jmp EndRaster

Raster3:
 ldx #68
TopFill3:
 sta WSYNC
 lda #0
 sta VBLANK
 dex
 bne TopFill3
Line3_68:
 sta WSYNC
 lda #$00
 sta GRP0
 lda #$00
 sta ENAM0
 lda #0
 sta GRP1
Line3_69:
 sta WSYNC
 lda #$00
 sta GRP0
 lda #$00
 sta ENAM0
 lda #0
 sta GRP1
Line3_70:
 sta WSYNC
 lda #$00
 sta GRP0
 lda #$00
 sta ENAM0
 lda #0
 sta GRP1
Line3_71:
 sta WSYNC
 lda #$00
 sta GRP0
 lda #$00
 sta ENAM0
 lda #0
 sta GRP1
Line3_72:
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
 lda #$3c
 sta RESP1,x
 sta GRP1
 lda #$3c
 sta RESP1,x
 sta GRP1
 lda #$00
 sta RESP1,x
 sta GRP1
 lda #$00
 sta RESP1
 sta GRP1
Line3_73:
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
 lda #$3c
 sta RESP1,x
 sta GRP1
 lda #$3c
 sta RESP1,x
 sta GRP1
 lda #$00
 sta RESP1,x
 sta GRP1
 lda #$00
 sta RESP1
 sta GRP1
Line3_74:
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
 lda #$18
 sta RESP1,x
 sta GRP1
 lda #$3c
 sta RESP1,x
 sta GRP1
 lda #$3c
 sta RESP1
 sta GRP1
Line3_75:
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
 lda #$ff
 sta RESP1,x
 sta GRP1
 lda #$ff
 sta RESP1,x
 sta GRP1
 lda #$3c
 sta RESP1,x
 sta GRP1
 lda #$3c
 sta RESP1
 sta GRP1
Line3_76:
 sta WSYNC
 lda #$1e
 sta GRP0
 lda #$02
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
 lda #$3c
 sta RESP1,x
 sta GRP1
 lda #$18
 sta RESP1,x
 sta GRP1
 lda #$18
 sta RESP1
 sta GRP1
Line3_77:
 sta WSYNC
 lda #$3c
 sta GRP0
 lda #$00
 sta ENAM0
 lda #0
 sta GRP1
 nop
 lda #$24
 sta RESP1
 sta GRP1
 lda #$24
 sta RESP1,x
 sta GRP1
 lda #$7e
 sta RESP1,x
 sta GRP1
 lda #$7e
 sta RESP1,x
 sta GRP1
 lda #$7e
 sta RESP1
 sta GRP1
Line3_78:
 sta WSYNC
 lda #$18
 sta GRP0
 lda #$00
 sta ENAM0
 lda #0
 sta GRP1
 nop
 lda #$24
 sta RESP1
 sta GRP1
 lda #$24
 sta RESP1,x
 sta GRP1
 lda #$7e
 sta RESP1,x
 sta GRP1
 lda #$18
 sta RESP1,x
 sta GRP1
 lda #$3c
 sta RESP1
 sta GRP1
Line3_79:
 sta WSYNC
 lda #$24
 sta GRP0
 lda #$00
 sta ENAM0
 lda #0
 sta GRP1
 nop
 lda #$42
 sta RESP1
 sta GRP1
 lda #$42
 sta RESP1,x
 sta GRP1
 lda #$24
 sta RESP1,x
 sta GRP1
 lda #$24
 sta RESP1,x
 sta GRP1
 lda #$24
 sta RESP1
 sta GRP1
Line3_80:
 sta WSYNC
 lda #$42
 sta GRP0
 lda #$00
 sta ENAM0
 lda #0
 sta GRP1
 nop
 lda #$42
 sta RESP1
 sta GRP1
 lda #$42
 sta RESP1,x
 sta GRP1
 lda #$24
 sta RESP1,x
 sta GRP1
 lda #$00
 sta RESP1,x
 sta GRP1
 lda #$00
 sta RESP1
 sta GRP1
Line3_81:
 sta WSYNC
 lda #$00
 sta GRP0
 lda #$00
 sta ENAM0
 lda #0
 sta GRP1
Line3_82:
 sta WSYNC
 lda #$00
 sta GRP0
 lda #$00
 sta ENAM0
 lda #0
 sta GRP1
Line3_83:
 sta WSYNC
 lda #$00
 sta GRP0
 lda #$00
 sta ENAM0
 lda #0
 sta GRP1
Line3_84:
 sta WSYNC
 lda #$00
 sta GRP0
 lda #$00
 sta ENAM0
 lda #0
 sta GRP1
Line3_85:
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
BottomFill3:
 sta WSYNC
 dex
 bne BottomFill3
 jmp EndRaster

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
