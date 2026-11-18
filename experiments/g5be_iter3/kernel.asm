 processor 6502
VSYNC=$00
VBLANK=$01
WSYNC=$02
NUSIZ0=$04
NUSIZ1=$05
COLUP0=$06
COLUP1=$07
COLUPF=$08
CTRLPF=$0a
PF0=$0d
RESP0=$10
RESP1=$11
RESM0=$12
GRP0=$1b
GRP1=$1c
ENAM0=$1d
FRAME=$80
XP=$81
YP=$86
ORDER=$8b
PTR=$90
VALID=$9a
TMP=$9c
LIMIT_Y=$9d
STENCIL=$9b
CACHE=$b8
MODE=$a8
START=$a9
POINTER=$aa

 ORG $f000
Reset:
 sei
 cld
 ldx #$ff
 txs
 ldx #$7f
 lda #0
Clear:
 sta $80,x
 dex
 bpl Clear
 lda #2
 sta MODE
 IF DYNAMIC
 ldx #4
InitCoordinates:
 lda DefaultX,x
 sta XP,x
 lda DefaultY,x
 sta YP,x
 dex
 bpl InitCoordinates
 ENDIF
 lda #$1e
 sta COLUP0
 lda #$0e
 sta COLUP1
 lda #$26
 sta COLUPF
 lda #1
 sta CTRLPF
 sta NUSIZ1
 lda #$30
 sta PF0
Frame:
 sta WSYNC
 lda #2
 sta VSYNC
 sta VBLANK
 sta WSYNC
 sta WSYNC
 sta WSYNC
SyncOff:
 lda #0
 sta VSYNC
 sta ENAM0
 sta GRP0
 sta GRP1
 sta NUSIZ0
 sta WSYNC
 ldx #4
PlayerPosition:
 dex
 bne PlayerPosition
 sta RESP0
 sta WSYNC
 ldx #2
MissilePosition:
 dex
 bne MissilePosition
 sta RESM0
 IF DYNAMIC
 jmp SetupDynamic
 ELSE
 ; Latch the requested diagnostic fixture in blanking.
 ldx MODE
 cpx #3
 bcc ValidMode
 ldx #2
ValidMode:
 lda Starts,x
 sta START
 lda SceneLo,x
 sta POINTER
 lda SceneHi,x
 sta POINTER+1
 ldx #35
Blank:
 sta WSYNC
 dex
 bne Blank
 ENDIF
Visible:
 lda #0
 sta VBLANK
 ldx #64
Top:
 sta WSYNC
 dex
 bne Top
 lda #2
 sta ENAM0
 ldy #64
Lead:
 lda PlayerRows,y
 sta GRP0
 iny
 cpy START
 beq Prepare
 sta WSYNC
 jmp Lead
Prepare:
 IF DYNAMIC
 lda VALID
 bne ValidBand
 sta WSYNC
 jmp Trail
ValidBand:
 ENDIF
 dey
 ; Wide copy only after the potential X66 shot on this lead line.
 IF DYNAMIC
 ldx #6
 ELSE
 ldx #8
 ENDIF
DelayLate:
 dex
 bne DelayLate
 lda #0
 sta NUSIZ0
 jmp (POINTER)
LeaveBand:
 lda #0
 sta NUSIZ0
 sta GRP1
 iny
Trail:
 lda PlayerRows,y
 sta GRP0
 cpy #88
 beq EndShot
 iny
 sta WSYNC
 jmp Trail
EndShot:
 ; Clear after the ordinary X2 shot, before the next scanline.
 ldx #4
ShotDelay:
 dex
 bne ShotDelay
 lda #0
 sta ENAM0
 sta WSYNC
 ldx #103
Bottom:
 sta WSYNC
 dex
 bne Bottom
Overscan:
 lda #2
 sta VBLANK
 ldx #29
BottomBlank:
 sta WSYNC
 dex
 bne BottomBlank
 inc FRAME
 jmp Frame

 IF DYNAMIC
DefaultX:
 byte 127,19,BOOT_X,100,46
DefaultY:
 byte 73,72,73,71,72
ExpectedX:
 byte 19,46,0,100,127
 MAC SWAP_PAIR
 SUBROUTINE
 sta WSYNC
 ldy ORDER+{1}
 lda XP,y
 ldy ORDER+{2}
 cmp XP,y
 bcc .Done
 beq .Done
 ldx ORDER+{1}
 sty ORDER+{1}
 stx ORDER+{2}
.Done:
 ENDM

SetupDynamic:
 sta WSYNC
 lda #1
 sta VALID
 lda #$ff
 sta START
 ldx #4
InitOrder:
 txa
 sta ORDER,x
 dex
 bpl InitOrder
 SWAP_PAIR 0,1
 SWAP_PAIR 1,2
 SWAP_PAIR 2,3
 SWAP_PAIR 3,4
 SWAP_PAIR 0,1
 SWAP_PAIR 1,2
 SWAP_PAIR 2,3
 SWAP_PAIR 0,1
 SWAP_PAIR 1,2
 SWAP_PAIR 0,1
 sta WSYNC
 lda #$ff
 cmp YP+0
 bcc NextY0
 lda YP+0
NextY0:
 cmp YP+1
 bcc NextY1
 lda YP+1
NextY1:
 cmp YP+2
 bcc NextY2
 lda YP+2
NextY2:
 cmp YP+3
 bcc NextY3
 lda YP+3
NextY3:
 cmp YP+4
 bcc NextY4
 lda YP+4
NextY4:
 sta START
 cmp #66
 bcc InvalidBand
 cmp #77
 bcc SetLimit
InvalidBand:
 lda #0
 sta VALID
 lda #71
 sta START
SetLimit:
 clc
 adc #2
 sta LIMIT_Y
 ldx #0
PreparePointers:
 sta WSYNC
 ldy ORDER,x
 lda XP,y
 cpx #2
 beq SelectClock
 cmp ExpectedX,x
 beq CheckY
 bne InvalidX
SelectClock:
 cmp #64
 bcc InvalidX
 cmp #83
 bcs InvalidX
 sec
 sbc #64
 tax
 lda ThirdXs,x
 ldx #2
 bmi InvalidX
 sta STENCIL
 jmp CheckY
InvalidX:
 lda #0
 sta VALID
CheckY:
 lda YP,y
 cmp START
 bcc BadY
 cmp LIMIT_Y
 bcc UseY
 beq UseY
BadY:
 lda #0
 sta VALID
 lda START
UseY:
 sta WSYNC
 sta TMP
 lda LIMIT_Y
 sec
 sbc TMP
 clc
 adc MaskLo,y
 pha
 lda MaskHi,y
 adc #0
 ldy #0
 pha
 txa
 asl
 tay
 pla
 sta PTR+1,y
 pla
 sta PTR,y
 inx
 cpx #5
 bcc PreparePointers
 ldy #0
 ldx #0
CacheRow:
 sta WSYNC
 lda (PTR),y
 sta CACHE,x
 lda (PTR+2),y
 sta CACHE+11,x
 lda (PTR+4),y
 sta CACHE+22,x
 lda (PTR+6),y
 sta CACHE+33,x
 lda (PTR+8),y
 sta CACHE+44,x
 inx
 iny
 cpx #11
 bcc CacheRow
 sta WSYNC
 ldx STENCIL
 lda DynamicClocks,x
 and VALID
 sta VALID
 lda DynamicLo,x
 sta POINTER
 lda DynamicHi,x
 sta POINTER+1
 ldx #1
TailBlank:
 sta WSYNC
 dex
 bne TailBlank
 jmp Visible
 include "dynamic.inc"
 ELSE
 include "chain.inc"
 ENDIF
 ALIGN 256
PlayerRows:
 ds 72,0
 byte $3c,$7e,$18,$7e,$1e,$3c,$18,$24,$42
 ds 8,0
 ORG $fffa
 word Reset,Reset,Reset
