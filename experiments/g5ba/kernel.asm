 processor 6502
; LM-D33 diagnostic only. All raster origins are derived from X/Y in RIOT RAM.
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
USED=$9c              ; count of diagnostic misses this frame
ACTOR=$9e
ANCHOR=$9f
PAIR_SLOT=$9d
SECOND=$9b
COMPACT_END=$92
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
  IF ACTORS = 2
 lda #0
  ENDIF
SetCopies:
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
 ; Select is a diagnostic input for the negative Stella fixture.
 lda SWCHB
 and #2
 bne SortCurrent
 ldx #4
SelectFixture:
 lda NegativeX,x
 sta XP,x
 dex
 bpl SelectFixture
SortCurrent:
 ; This sort is outside the active band. Five independent X bytes determine
 ; the current index order from scratch each frame.
 jsr Sort
 IF ACTORS = 2
 jsr PreparePair
 sta HMCLR
 lda ANCHOR
 clc
 adc #9
 ldx #1
 jsr PositionP1
 sta WSYNC
FineMove:
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
 IF ACTORS = 5
 jsr PreparePair
 jsr FindSecond
 ENDIF
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

FrameJump:
 jmp Frame

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

InitialX:
 IF ACTORS = 2
 byte 19,52,151,73,75
 ELSE
 byte 55,91,130,24,26
 ENDIF
NegativeX:
 IF ACTORS = 2
 byte 19,52,151,73,81
 ELSE
 byte 73,74,75,76,77
 ENDIF

Sort:
 IF ACTORS = 2
 ldx #1
 ELSE
 ldx #4
 ENDIF
OrderInit:
 txa
 IF ACTORS = 2
 clc
 adc #3
 ENDIF
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
 IF ACTORS = 2
 cmp #2
 ELSE
 cmp #5
 ENDIF
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
 lda #13                ; cycle at end of the RAM prefix
 sta KT
 IF ACTORS = 2
 jsr SelectCompactSource
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
 lda #20
 sta KT
 lda #2
 sta ITER
 ENDIF
NextActor:
 lda ITER
 cmp #ACTORS
 bcc ActorValid
 jmp FinishKernel
ActorValid:
 tay
 lda ORDER,y
 sta ACTOR
 tay
 lda XP,y
 IF ACTORS = 5
 ldy PAIRX
 beq OriginReady
 ldy ITER
 cpy PAIR_SLOT
 bne OriginReady
 lda ANCHOR
OriginReady:
 ENDIF
 tay
 lda CyclesByPixel,y
 sta TARGET
 sec
 sbc KT
 bcc CannotSchedule
 IF ACTORS = 5
 ldy ITER
 cpy SECOND
 bne NormalBudget
 sec
 sbc #11
 jmp BudgetReady
NormalBudget:
 sec
 ENDIF
 sbc #7               ; absolute indexed LDA (4), zp RESP1 (3)
BudgetReady:
 bcs CanSchedule
CannotSchedule:
 inc USED
 jmp Advance
CanSchedule:
 sta GAP
 IF ACTORS = 5
 lda PAIRX
 beq NormalMask
 lda ITER
 cmp PAIR_SLOT
 bne NormalMask
 lda #UNION
 sta ADDRLO
 lda #0
 sta ADDRHI
 jmp EmitActor
NormalMask:
 ENDIF
 jsr MaskAddress
EmitActor:
 jsr Delay
 lda #$b9             ; LDA nn,Y; padded source masks cannot cross a page
 jsr Emit
 lda ADDRLO
 jsr Emit
 lda ADDRHI
 jsr Emit
 IF ACTORS = 5
 lda ITER
 cmp SECOND
 bne NoInlineOr
 tay
 lda ORDER+1,y
 sta ACTOR
 jsr MaskAddress
 lda #$19             ; ORA abs,Y, four cycles on the padded source page
 jsr Emit
 lda ADDRLO
 jsr Emit
 lda ADDRHI
 jsr Emit
NoInlineOr:
 ENDIF
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
 IF ACTORS = 5
 jsr SkipPairPartner
 ENDIF
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

FindSecond:
 lda #$ff
 sta SECOND
 lda PAIRX
 beq ScanSecondStart
 lda PAIR_SLOT
 clc
 adc #1
 sta COMPACT_END
ScanSecondStart:
 ldx #0
ScanSecond:
 lda PAIRX
 beq InspectSecond
 txa
 clc
 adc #1
 cmp PAIR_SLOT
 beq NextSecond
 cpx PAIR_SLOT
 beq NextSecond
 cpx COMPACT_END
 beq NextSecond
InspectSecond:
 ldy ORDER,x
 lda XP,y
 ldy ORDER+1,x
 cmp XP,y
 bne NextSecond
 stx SECOND
 rts
NextSecond:
 inx
 cpx #4
 bcc ScanSecond
 rts

SkipPairPartner:
 lda ITER
 cmp SECOND
 beq SkipSlot
 lda PAIRX
 beq NoPartner
 lda ITER
 cmp PAIR_SLOT
 bne NoPartner
SkipSlot:
 inc ITER
NoPartner:
 rts

PreparePair:
 lda #0
 sta PAIRX
 sta PAIR_SLOT
TryPair:
 ldx PAIR_SLOT
 ldy ORDER,x
 lda XP,y
 sta ANCHOR
 lda ORDER+1,x
 tay
 lda XP,y
 sec
 sbc ANCHOR
 cmp #9
 bcs RejectWidth
 sta GAP
 lda ORDER,x
 cmp #3
 bcs LeftSmall
 cpy #3
 bcs WidthOne
 lda GAP
 beq PairLeftOrigin
 bne RejectWidth
WidthOne:
 lda GAP
 cmp #2
 bcs RejectWidth
 bcc PairLeftOrigin
LeftSmall:
 cpy #3
 bcs BothSmall
 lda GAP
 beq PairLeftOrigin
 cmp #2
 bcs RejectWidth
 bcc AnchorPlusOne
BothSmall:
 IF ROWSPLIT = 0
 lda GAP
 cmp #3
 bcs RejectWidth
 ENDIF
AnchorPlusOne:
 inc ANCHOR
 jmp PairLeftOrigin
RejectWidth:
 jmp PairRejected
PairLeftOrigin:
 ldx PAIR_SLOT
 lda ORDER,x
 sta ACTOR
 jsr MaskAddress
 lda ADDRLO
 sta SORTI
 lda ADDRHI
 sta SORTJ
 ldx PAIR_SLOT
 lda ORDER+1,x
 sta ACTOR
 jsr MaskAddress
 ldx PAIR_SLOT
 ldy ORDER,x
 lda XP,y
 eor ANCHOR
 sta TARGET             ; zero means unshifted first row (otherwise left by 1)
 ldy #ROWS-1
PairRow:
 lda (SORTI),y
 ldx TARGET
 beq FirstReady
 asl
 bcs PairRejected
FirstReady:
 sta UNION,y
 lda (ADDRLO),y
 IF ROWSPLIT
 beq PairRowReady
 ENDIF
 ldx GAP
 cpx #0
 bne PairRight
 ldx TARGET
 beq PairRowReady
 asl
 bcs PairRejected
 bcc PairRowReady
PairRight:
 ldx TARGET
 beq ShiftStart
 ldx GAP
 dex
 beq PairRowReady
 bne ShiftNext
ShiftStart:
 ldx GAP
ShiftNext:
 lsr
 IF ROWSPLIT
 bcs OnlyLeftRow
 ELSE
 bcs PairRejected       ; a lit pixel would be discarded, so reject
 ENDIF
 dex
 bne ShiftNext
PairRowReady:
 ora UNION,y
 sta UNION,y
OnlyLeftRow:
 dey
 bpl PairRow
 inc PAIRX
 rts
PairRejected:
 IF ACTORS = 5
 inc PAIR_SLOT
 lda PAIR_SLOT
 cmp #4
 bcs NoCompactPair
 jmp TryPair
NoCompactPair:
 ENDIF
 ldy ORDER
 lda XP,y
 sta ANCHOR
 rts

SelectCompactSource:
 lda PAIRX
 beq FirstMask
 lda #UNION
 sta ADDRLO
 lda #0
 sta ADDRHI
 rts
FirstMask:
 lda ORDER
 sta ACTOR
 jmp MaskAddress


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
