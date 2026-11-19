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
LONG=$80
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
 IF SEGMENTED
CACHE=$a2
 ELSE
CACHE=$a3
 ENDIF
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
 IF SEGMENTED = 0
 lda #2
 sta MODE
 ENDIF
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

 IF SEGMENTED
LeaveLong:
 lda #0
 sta GRP1
 sta GRP0
 ldx #100
 jmp Bottom
 ENDIF
 IF DYNAMIC
DefaultX:
 byte BOOT_RIGHT,19,BOOT_X,BOOT_FOURTH,BOOT_SECOND
DefaultY:
 IF BOOT_FAR
 byte 74,68,83,71,76
 ELSE
 byte 73,72,73,71,72
 ENDIF
 IF SEGMENTED
PointerOffsets:
 byte 0,2,4,6,8
 ENDIF
SecondBank:
 byte 1,$ff,$ff,0,$ff,$ff,2,$ff,$ff,3
FourthX:
 IF UNIFIED
 byte 100,97,103,100
 ELSE
 byte 100,100,100,100
 ENDIF
RightX:
 IF UNIFIED
 byte 127,127,133,136
 ELSE
 byte 127,127,127,127
 ENDIF
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
 IF SEGMENTED
 sta LONG
 ENDIF
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
 IF SEGMENTED
 cpx #3
 bne TailMaskPointerReady
 clc
 lda PTR+4
 adc #17
 sta ORDER
 lda PTR+5
 adc #0
 sta ORDER+1
TailMaskPointerReady:
 ENDIF
 ldy ORDER,x
 lda XP,y
 cpx #1
 beq SelectBank
 cpx #2
 beq SelectClock
 cpx #3
 beq ValidateFourth
 cpx #4
 beq ValidateRight
 cmp #19
 beq CheckY
 bne InvalidX
SelectBank:
 sec
 sbc #43
 cmp #10
 bcs InvalidX
 tax
 lda SecondBank,x
 bmi BadSecond
 ldx #1
 sta BANKSEL
 jmp CheckY
BadSecond:
 ldx #1
 jmp InvalidX
ValidateFourth:
 IF SEGMENTED
 ldx BANKSEL
 cmp FourthX,x
 beq FourthXReady
 lda #0
 sta VALID
FourthXReady:
 ldx #3
 lda YP,y
 sta WSYNC
 ; START is the minimum Y or a lower clamp on valid inputs.
 cmp LIMIT_Y
 bcc FourthYReady
 beq FourthYReady
 lda #0
 sta VALID
 lda START
FourthYReady:
 jmp StoreY
 ELSE
 ldx BANKSEL
 cmp FourthX,x
 bne BadFourth
 ldx #3
 jmp CheckY
BadFourth:
 ldx #3
 jmp InvalidX
 ENDIF
ValidateRight:
 ldx BANKSEL
 cmp RightX,x
 bne BadRight
 ldx #4
 jmp CheckY
BadRight:
 ldx #4
 jmp InvalidX
SelectClock:
 cmp #64
 bcc InvalidX
 cmp #83
 bcs InvalidX
 sec
 sbc #64
 tax
 lda ThirdXs,x
 bmi BadThird
 ldx #2
 sta STENCIL
 jmp CheckY
BadThird:
 ldx #2
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
 IF SEGMENTED
 cpx #2
 bne BadY
 sta WSYNC
 cmp #84
 bcc LateY
 lda #0
 sta VALID
 lda START
 jmp StoreY
LateY:
 inc LONG
 jmp StoreY
 ENDIF
BadY:
 lda #0
 sta VALID
 lda START
UseY:
 sta WSYNC
StoreY:
 sta TMP
 lda LIMIT_Y
 IF SEGMENTED
 clc
 adc #7
 ENDIF
 sec
 sbc TMP
 clc
 adc MaskLo,y
 IF SEGMENTED
 sta TMP
 lda MaskHi,y
 adc #0
 ldy PointerOffsets,x
PeakStack:
 sta PTR+1,y
 lda TMP
 sta PTR,y
 ELSE
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
 ENDIF
 inx
 cpx #5
 bcs PointersDone
 jmp PreparePointers
PointersDone:
 ldy #0
 ldx #0
CacheRow:
 sta WSYNC
 lda (PTR),y
 sta CACHE,x
 lda (PTR+2),y
 sta CACHE+1*ROWS,x
 IF SEGMENTED
 cpy #7
 bcs FetchThird
 lda LONG
 beq FetchThird
 lda (ORDER),y
 sta CACHE+85,x
 lda #0
 beq StoreThird
FetchThird:
 ENDIF
 lda (PTR+4),y
StoreThird:
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
 IF SEGMENTED
 lda LONG
 and VALID
 beq OrdinaryTail
 lda START
 cmp #68
 bne BadTail
 lda LongAllowed,x
 beq BadTail
 lda #<FarTail
 sta ORDER
 lda #>FarTail
 sta ORDER+1
 jmp TailPrepared
BadTail:
 lda #0
 sta VALID
OrdinaryTail:
 lda #<LeaveBand
 sta ORDER
 lda #>LeaveBand
 sta ORDER+1
TailPrepared:
 ENDIF
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
 include "roms/unified-bank0.inc"
 ELSE
 include "chain.inc"
 ENDIF
 ALIGN 256
PlayerRows:
 ds 72,0
 byte $3c,$7e,$18,$7e,$1e,$3c,$18,$24,$42
 IF SEGMENTED
 ds 11,0
 ELSE
 ds 8,0
 ENDIF
 ORG $fffa
 word Reset,Reset,Reset
