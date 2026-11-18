 processor 6502
; LM-D32 diagnostic only. All raster origins are derived from X/Y in RIOT RAM.
; Runtime emits the timed scanline program in RIOT RAM. Cartridge banks are
; identical and no bank selector or precompiled scene is used.
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
SWCHB=$0282
HMP0=$20
HMOVE=$2a
HMCLR=$2b
GRP0=$1b
GRP1=$1c
ENAM0=$1d
INTIM=$0284
TIM64T=$0296
FRAME=$80
XP=$81
YP=$86
ORDER=$8b
SORTI=$90
SORTJ=$91
SAVEDID=$92
ITER=$93
KT=$94
TARGET=$95
GAP=$96
ADDRLO=$97
ADDRHI=$98
BRANCH=$99
PAIRX=$9a
PARTNER=$9b
USED=$9c              ; count of diagnostic misses this frame
ROTATE=$9d
ACTOR=$9e
UNION=$a0            ; 24 bytes, used only when a pair's origins coincide
CODE=$b8             ; 64 bytes; stack uses $f8-$ff
STARTY=64
ROWS=24

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
 ldx #4
InitCoordinates:
 lda InitialX,x
 sta XP,x
 lda #72
 sta YP,x
 dex
 bpl InitCoordinates
 lda #$1e
 sta COLUP0
 lda #$0e
 sta COLUP1
 lda #$26
 sta COLUPF
 lda #1
 sta CTRLPF
 IF POSITIONED
 lda #0
 ENDIF
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
 lda #0
 sta VSYNC
 sta GRP0
 sta GRP1
 sta ENAM0
 lda #44
 sta TIM64T
 ; Set P0 and M0 in blanked scanlines, at fixed x ~10 and x ~25.
 sta WSYNC
 ldx #4
PosPlayer:
 dex
 bne PosPlayer
 sta RESP0
 sta WSYNC
 ldx #2
PosMissile:
 dex
 bne PosMissile
 sta RESM0
 ; This sort is outside the active band. Five independent X bytes determine
 ; the current index order from scratch each frame.
 IF UNION_ENABLED
 lda SWCHB
 and #2
 bne NoSelect
 ldx #4
SelectFixture:
 lda SameX,x
 sta XP,x
 lda SameY,x
 sta YP,x
 dex
 bpl SelectFixture
NoSelect:
 ENDIF
 jsr Sort
 IF POSITIONED
 sta HMCLR
 ldy #0
 IF ROTATING
 ldy ROTATE
 ENDIF
 lda XP,y
 clc
 adc #9                  ; calibrate RESP1/HMOVE to visible X
 ldx #1
 jsr PositionP1
 sta WSYNC
 sta HMOVE
 ENDIF
BlankTimer:
 lda INTIM
 bne BlankTimer
 sta WSYNC
VisibleStart:
 sta VBLANK
 lda #76
 sta TIM64T
 jsr MakeKernel
TopTimer:
 lda INTIM
 bne TopTimer
BandEntry:
 lda #2
 sta ENAM0
 ldy #$ff
 jsr CODE
BandExit:
 ; The RAM program synchronized to the first line after the band and exited.
 lda #0
 sta GRP0
 sta GRP1
 sta ENAM0
 ldx #103
Bottom:
 sta WSYNC
 dex
 bne Bottom
 ldx #30
Over:
 sta WSYNC
 lda #2
 sta VBLANK
 dex
 bne Over
 inc FRAME
 inc ROTATE
 lda ROTATE
 cmp #5
 bne FrameJump
 lda #0
 sta ROTATE
FrameJump:
 jmp Frame

 IF POSITIONED
PositionP1:
 sta WSYNC
 sec
CoarseP1:
 sbc #15
 bcs CoarseP1
 eor #7
 asl
 asl
 asl
 asl
 sta RESP0,x
 sta HMP0,x
 rts
 ENDIF

InitialX:
 byte 19,52,85,118,151
SameX:
 byte 79,79,19,112,49
SameY:
 byte 75,74,73,72,71

Sort:
 ldx #4
OrderInit:
 txa
 sta ORDER,x
 dex
 bpl OrderInit
 lda #1
 sta SORTI
SortOuter:
 ldx SORTI
 lda ORDER,x
 sta SAVEDID
 tay
 lda XP,y
 sta PAIRX
 stx SORTJ
SortInner:
 ldx SORTJ
 beq SortPlace
 dex
 lda ORDER,x
 tay
 lda XP,y
 cmp PAIRX
 bcc SortPlace
 beq SortPlace
 tya
 sta ORDER+1,x
 dec SORTJ
 jmp SortInner
SortPlace:
 ldx SORTJ
 lda SAVEDID
 sta ORDER,x
 inc SORTI
 lda SORTI
 cmp #5
 bcc SortOuter
 rts

; X=output byte offset, Y scratch. No nesting beyond two JSRs.
Emit:
 sta CODE,x
 inx
 rts

MakeKernel:
 ldx #0
 ldy #0
CopyPrefix:
 lda Prefix,y
 jsr Emit
 iny
 cpy #PrefixEnd-Prefix
 bcc CopyPrefix
 lda #0
 sta ITER
 sta USED
 lda #$ff
 sta PARTNER
 lda #13                ; cycle at end of the RAM prefix
 sta KT
 IF POSITIONED
 lda #0
 IF ROTATING
 lda ROTATE
 ENDIF
 sta ACTOR
 jsr MaskAddress
 lda #$b9
 jsr Emit
 lda ADDRLO
 jsr Emit
 lda ADDRHI
 jsr Emit
 lda #$85
 jsr Emit
 lda #GRP1
 jsr Emit
 jmp FinishKernel
 ENDIF
NextActor:
 lda ITER
 cmp #ACTORS
 bcc ActorValid
 jmp FinishKernel
ActorValid:
 tay
 lda ORDER,y
 IF ACTORS = 1
 lda #0
 ENDIF
 IF ROTATING
 lda ROTATE
 ENDIF
 sta ACTOR
 tay
 lda XP,y
 tay
 lda CyclesByPixel,y
 sta TARGET
 sec
 sbc KT
 bcc CannotSchedule
 sbc #7               ; absolute indexed LDA (4), zp RESP1 (3)
 bcs CanSchedule
CannotSchedule:
 inc USED
 jmp Advance
CanSchedule:
 sta GAP
 jsr MaskAddress
 IF UNION_ENABLED
 ; Only one composite per frame. An additional identical-X actor is
 ; reported as a miss if its required time cannot be scheduled.
 lda PARTNER
 cmp #$ff
 bne EmitActor
 lda ITER
 cmp #ACTORS-1
 bcs EmitActor
 tay
 lda ORDER+1,y
 tay
 lda XP,y
 ldy ACTOR
 cmp XP,y
 bne EmitActor
 jsr MergePair
 ENDIF
EmitActor:
 jsr Delay
 lda #$b9             ; LDA nn,Y; padded source masks cannot cross a page
 jsr Emit
 lda ADDRLO
 jsr Emit
 lda ADDRHI
 jsr Emit
 lda GAP
 cmp #1
 beq FourCycleStrobe
 lda #$85
 jsr Emit
 lda #RESP1
 jsr Emit
 jmp StoreMask
FourCycleStrobe:
 lda #$8d
 jsr Emit
 lda #RESP1
 jsr Emit
 lda #0
 jsr Emit
StoreMask:
 lda #$85
 jsr Emit
 lda #GRP1
 jsr Emit
 lda TARGET
 clc
 adc #3
 sta KT
Advance:
 inc ITER
 jmp NextActor
FinishKernel:
 lda #$4c
 jsr Emit
 lda #CODE
 jsr Emit
 lda #0
 jsr Emit
 txa
 sec
 sbc #7                ; branch instruction ends at CODE+7
 sta CODE+6
 lda #$60
 jsr Emit
 rts

; GAP is the strobe delay before loading the row. A one-cycle remainder
; is emitted as absolute rather than zero-page STA RESP1.
Delay:
 lda GAP
 cmp #2
 bcc Delayed
 and #1
 beq EvenDelay
 lda #$24
 jsr Emit
 lda #FRAME
 jsr Emit
 lda GAP
 sec
 sbc #3
 sta GAP
EvenDelay:
 lda GAP
 beq Delayed
 lda #$ea
 jsr Emit
 dec GAP
 dec GAP
 jmp EvenDelay
Delayed:
 rts

MaskAddress:
 ldy ACTOR
 lda #32+STARTY
 sec
 sbc YP,y
 clc
 adc MaskLow,y
 sta ADDRLO
 lda MaskHigh,y
 adc #0
 sta ADDRHI
 rts

; OR a pair sharing an exact RAM X. A0..B7 are reused each frame.
MergePair:
 stx SORTI
 ldy #ROWS-1
CopyFirst:
 lda (ADDRLO),y
 sta UNION,y
 dey
 bpl CopyFirst
 ldy ITER
 lda ORDER+1,y
 sta ACTOR
 ; inline MaskAddress to bound stack use
 tay
 lda #32+STARTY
 sec
 sbc YP,y
 clc
 adc MaskLow,y
 sta ADDRLO
 lda MaskHigh,y
 adc #0
 sta ADDRHI
 ldy #ROWS-1
OrSecond:
 lda (ADDRLO),y
 ora UNION,y
 sta UNION,y
 dey
 bpl OrSecond
 lda #UNION
 sta ADDRLO
 lda #0
 sta ADDRHI
 inc ITER
 sta PARTNER
 ldx SORTI
 rts

Prefix:
 sta WSYNC
 iny
 cpy #ROWS
 byte $f0,0            ; BEQ exits after syncing to the first line below band
 lda PlayerRows,y
 sta GRP0
PrefixEnd:
MaskLow:
 byte <Male,<Male,<Female,<SmallM,<SmallF
MaskHigh:
 byte >Male,>Male,>Female,>SmallM,>SmallF
 ALIGN 32
PlayerRows:
 byte 0,0,0,0,0,0,0,0,$3c,$7e,$18,$7e,$1e,$3c,$18,$24,$42
 byte 0,0,0,0,0,0,0
EndProgram:
 include "tables.inc"
 ORG $fffa
 word Reset,Reset,Reset
