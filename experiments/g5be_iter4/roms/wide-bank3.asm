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
BANKSEL=$9e
FOURTH=$ad
STENCIL=$9b
 IF ROWS = 17
MODE=$a2
START=$9f
POINTER=$a0
CACHE=$a3
 ELSE
CACHE=$b8
MODE=$a8
START=$a9
POINTER=$aa
 ENDIF

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
 byte BOOT_RIGHT,19,BOOT_X,100,46
DefaultY:
 byte 73,72,73,71,72
ExpectedX:
 byte 19,46,0,100,0
RightBank:
 byte 0,$ff,$ff,1,$ff,$ff,2,$ff,$ff,3
 MAC SWAP_PAIR
 SUBROUTINE
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
 lda #0
 sta BANKSEL
 lda #0
 sta ORDER+0
 lda #1
 sta ORDER+1
 lda #2
 sta ORDER+2
 lda #3
 sta ORDER+3
 lda #4
 sta ORDER+4
 IF ROWS = 17
 SWAP_PAIR 0,3
 sta WSYNC
 SWAP_PAIR 1,4
 SWAP_PAIR 0,2
 sta WSYNC
 SWAP_PAIR 1,3
 SWAP_PAIR 0,1
 sta WSYNC
 SWAP_PAIR 2,4
 SWAP_PAIR 1,2
 sta WSYNC
 SWAP_PAIR 3,4
 SWAP_PAIR 2,3
 ELSE
 sta WSYNC
 SWAP_PAIR 0,1
 sta WSYNC
 SWAP_PAIR 1,2
 sta WSYNC
 SWAP_PAIR 2,3
 sta WSYNC
 SWAP_PAIR 3,4
 sta WSYNC
 SWAP_PAIR 0,1
 sta WSYNC
 SWAP_PAIR 1,2
 sta WSYNC
 SWAP_PAIR 2,3
 sta WSYNC
 SWAP_PAIR 0,1
 sta WSYNC
 SWAP_PAIR 1,2
 sta WSYNC
 SWAP_PAIR 0,1
 ENDIF
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
 IF ROWS = 17
 cmp #72
 bcc ClampDone
 lda #71
 sta START
ClampDone:
 ENDIF
 clc
 adc #(ROWS-9)
 sta LIMIT_Y
 ldx #0
PreparePointers:
 sta WSYNC
 ldy ORDER,x
 lda XP,y
 cpx #2
 beq SelectClock
 cpx #4
 beq SelectBank
 IF MIXED
 cpx #3
 beq StoreFourth
 ENDIF
 cmp ExpectedX,x
 beq CheckY
 bne InvalidX
 IF MIXED
StoreFourth:
 sta FOURTH
 jmp CheckY
 ENDIF
SelectBank:
 IF MIXED
 ldx #0
 cmp #127
 bne MixedRight
 lda FOURTH
 cmp #100
 beq MixedOK
 inx
 cmp #97
 beq MixedOK
 inx
 cmp #103
 bne MixedBad
 beq MixedOK
MixedRight:
 cmp #133
 bne MixedBad
 lda FOURTH
 cmp #103
 bne MixedBad
 ldx #3
MixedOK:
 stx BANKSEL
 ldx #4
 jmp CheckY
MixedBad:
 ldx #4
 jmp InvalidX
 ELSE
 sec
 sbc #127
 cmp #10
 bcs InvalidX
 tax
 lda RightBank,x
 ldx #4
 bmi InvalidX
 sta BANKSEL
 jmp CheckY
 ENDIF
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
PeakStack:
 txa
 asl
 tay
 pla
 sta PTR+1,y
 pla
 sta PTR,y
 inx
 cpx #5
 IF MIXED
 bcs PointersDone
 jmp PreparePointers
PointersDone:
 ELSE
 bcc PreparePointers
 ENDIF
 ldy #0
 ldx #0
CacheRow:
 sta WSYNC
 lda (PTR),y
 sta CACHE,x
 lda (PTR+2),y
 sta CACHE+1*ROWS,x
 lda (PTR+4),y
 sta CACHE+2*ROWS,x
 lda (PTR+6),y
 sta CACHE+3*ROWS,x
 lda (PTR+8),y
 sta CACHE+4*ROWS,x
 inx
 iny
 cpx #ROWS
 bcc CacheRow
 sta WSYNC
 ldx BANKSEL
 lda $fff6,x
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
 include "roms/wide-bank3.inc"
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
