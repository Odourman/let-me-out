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
HMM0=$22
ENAM1=$1e
VDELP1=$26
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
FAST=$92
PREFETCHED=$90
NEXT_READY=$91
CACHED=UNION
SLOT_CLOCKS=UNION+1
CACHE_RIGHT=UNION+6
PHASE_INDEX=UNION+7
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
 lda #COPIES
SetCopies:
 sta NUSIZ1
 IF VDEL
 lda #1
 sta VDELP1
 ENDIF
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
 IF MISSILE
 sta HMCLR
 lda #77
 sta WSYNC
 sec
MissileCoarse:
 sbc #15
 bcs MissileCoarse
 eor #7
 asl
 asl
 asl
 asl
 ldx #1
 sta RESM0,x
 sta HMM0,x
 sta WSYNC
 sta HMOVE
 ENDIF
 ; Select is a diagnostic input for the negative Stella fixture.
 lda SWCHB
 and #2
 bne SortCurrent
 ldx #4
SelectFixture:
 lda NegativeX,x
 sta XP,x
 lda NegativeY,x
 sta YP,x
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
 IF PHASE_PROBE >= 10
 lda BRANCH
 cmp #7
 bne EnableMissile
 ; On the lead line, the narrow shot has already passed. Wait until
 ; the wide-mode second-copy position has passed too.
 bit FRAME
 bit FRAME
 bit FRAME
 nop
EnableMissile:
 ENDIF
 lda #2
 sta ENAM0
 IF PHASE_PROBE
 ldx CACHED
 ENDIF
 ldy #$ff
 IF PHASE_PROBE >= 3
 lda BRANCH
 cmp #6
 bne PhaseUseOriginalIndex
 iny
PhaseUseOriginalIndex:
 ENDIF
 jsr CODE
BandExit:
 ; The RAM program synchronized to the first line after the band and exited.
 lda #0
 sta GRP0
 sta GRP1
 IF MISSILE
 sta ENAM1
 ENDIF
 ldx #103
 IF PHASE_PROBE >= 10
 lda BRANCH
 cmp #7
 bne MissileLegacyExit
 ; First unmasked line keeps the original X2 shot. Clear before X66.
 lda #0
 sta ENAM0
 sta WSYNC
 dex
 jmp Bottom
MissileLegacyExit:
 lda #0
 ENDIF
 ldy FAST
 beq DisableMissile
 sta WSYNC
 dex
DisableMissile:
 sta ENAM0
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
 byte 19,46,73,100,127
 ENDIF
NegativeX:
 IF ACTORS = 2
 byte 19,52,151,73,81
 ELSE
 byte 127,19,73,100,46
 ENDIF

NegativeY:
 byte 73,72,73,71,72

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
 lda #0
 IF PHASE_PROBE >= 8
 sta NUSIZ0
 sta VDELP1
 ENDIF
 IF PHASE_PROBE >= 3
 sta PHASE_INDEX
 ENDIF
 IF PHASE_PROBE = 2
 sta VDELP1
 ENDIF
 sta FAST
 sta PREFETCHED
 sta NEXT_READY
 IF ACTORS = 5
 lda PAIRX
 bne UseNormalPrefix
 lda SECOND
 cmp #$ff
 bne UseNormalPrefix
 jsr CanReuseMask
 bcc CheckFastLimit
 jmp BuildReuse
CheckFastLimit:
 IF PHASE_PROBE
 jsr AdmitPhase
 bcs AdmitResource
 jmp CheckCache
AdmitResource:
 IF PHASE_PROBE >= 8
 jsr CheckResource
 bcs AcceptResource
 jmp CheckCache
AcceptResource:
 ENDIF
 IF PHASE_PROBE = 6
 lda SLOT_CLOCKS+1
 cmp #31
 bcc CheckCache
 lda SLOT_CLOCKS+4
 sec
 sbc SLOT_CLOCKS+2
 cmp #18
 bcc CheckCache
 ENDIF
 jmp BuildPhase
CheckCache:
CheckOrdinaryPhase:
 ENDIF
 IF CACHE_PROBE
 jsr AdmitCacheProbe
 bcc CheckOrdinaryFast
 jmp BuildCacheProbe
CheckOrdinaryFast:
 ENDIF
 ldy ORDER+4
 lda XP,y
 tay
 lda CyclesByPixel,y
 cmp #65
 bcs UseNormalPrefix
 inc FAST
 jmp FastPrefixStart
UseNormalPrefix:
 ENDIF
 ldx #0
 ldy #0
CopyPrefix:
 lda Prefix,y
 jsr Emit
 iny
 cpy #PrefixEnd-Prefix
 bcc CopyPrefix
 lda #13
 bne InitPlanner
FastPrefixStart:
 ldx #0
 ldy #0
FastCopy:
 lda FastPrefix,y
 jsr Emit
 iny
 cpy #FastPrefixEnd-FastPrefix
 bcc FastCopy
 lda #9
InitPlanner:
 sta KT
 lda #0
 sta ITER
 sta USED
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
 lda FAST
 beq StandardBudget
 lda TARGET
 sec
 sbc KT
 ldy PREFETCHED
 beq StandardBudget
 sbc #3
 jmp BudgetReady
StandardBudget:
 lda TARGET
 sec
 sbc KT
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
 lda FAST
 beq StandardMask
 lda #0
 sta NEXT_READY
 lda PREFETCHED
 bne EmitActor
 lda ITER
 cmp #4
 bcs StandardMask
 lda GAP
 cmp #4
 bcc StandardMask
 tay
 lda ITER
 tay
 lda ORDER+1,y
 tay
 lda XP,y
 tay
 lda CyclesByPixel,y
 sec
 sbc TARGET
 cmp #6
 bcc StandardMask
 cmp #10
 bcs StandardMask
 ; The follower's row is pipelined in X before the current RESP1.
 lda ITER
 tay
 lda ORDER+1,y
 ldy ACTOR
 sty NEXT_READY
 sta ACTOR
 jsr MaskAddress
 lda #$be
 jsr Emit
 lda ADDRLO
 jsr Emit
 lda ADDRHI
 jsr Emit
 lda NEXT_READY
 sta ACTOR
 lda #1
 sta NEXT_READY
 lda GAP
 sec
 sbc #4
 sta GAP
StandardMask:
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
 lda PREFETCHED
 bne EmitStrobe
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
EmitStrobe:
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
 lda PREFETCHED
 beq AccumulatorMask
 lda #$86
 bne EmitMaskStore
AccumulatorMask:
 lda #$85
EmitMaskStore:
 jsr Emit
 lda #GRP1
 jsr Emit
 lda TARGET
 clc
 adc #3
 sta KT
 lda NEXT_READY
 sta PREFETCHED
Advance:
 IF ACTORS = 5
 jsr SkipPairPartner
 ENDIF
 inc ITER
 jmp NextActor
FinishKernel:
 lda FAST
 beq FinishJump
 IF MISSILE
 ; Test only the missing F actor's full-width row, in the reorder fixture.
 lda TARGET
 cmp #58
 bne EndMissile
 lda XP+2
 cmp #73
 bne EndMissile
 lda YP+2
 cmp #73
 bne EndMissile
 ldy #0
CopyMissileTail:
 lda MissileTail,y
 jsr Emit
 iny
 cpy #MissileTailEnd-MissileTail
 bcc CopyMissileTail
EndMissile:
 ENDIF
 lda #$c0
 jsr Emit
 lda #ROWS-1
 jsr Emit
 lda #$d0
 jsr Emit
 txa
 eor #$ff
 jsr Emit
 lda #$85
 jsr Emit
 lda #WSYNC
 jsr Emit
 jmp EmitReturn
FinishJump:
 lda #$4c
 jsr Emit
 lda #CODE
 jsr Emit
 lda #0
 jsr Emit
PatchPrefix:
 txa
 sec
 sbc #7                ; branch instruction ends at CODE+7
 sta CODE+6
EmitReturn:
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


; Latch sharing is valid when the first two sorted M actors have the
; same Y. Costs are checked against the five runtime strobe deadlines.
CanReuseMask:
 lda ORDER
 ora ORDER+1
 cmp #1
 bne ReuseNo
 lda YP
 cmp YP+1
 bne ReuseNo
 ldx #0
ReuseCheck:
 ldy ORDER,x
 lda XP,y
 cmp #19
 bcc ReuseNo
 tay
 lda CyclesByPixel,y
 cmp #59
 bcs ReuseNo
 sta SLOT_CLOCKS,x
 sec
 sbc ReuseMin,x
 bcc ReuseNo
 cpx #0
 beq NextReuseCheck
 cmp SLOT_CLOCKS-1,x
 bcc ReuseNo
NextReuseCheck:
 inx
 cpx #5
 bcc ReuseCheck
 sec
 rts
ReuseNo:
 clc
 rts
; Conservative TIA spacing for the latch-sharing and prefetched slots.
; First clock needs the 9-cycle prefix, two loads, then RESP1.
ReuseMin:
 byte 20,8,8,8,9

BuildReuse:
 inc FAST
 ldx #0
 ldy #0
ReuseCopy:
 lda FastPrefix,y
 jsr Emit
 iny
 cpy #FastPrefixEnd-FastPrefix
 bcc ReuseCopy
 lda #0
 sta USED
 sta ITER
 lda #9
 sta KT
 lda ORDER+3
 sta ACTOR
 jsr MaskAddress
 lda #$be
 jsr EmitIndexed
 lda #13
 sta KT
ReuseSlot:
 ldy ITER
 lda SLOT_CLOCKS,y
 sta TARGET
 sec
 sbc KT
 sec
 sbc ReuseCost,y
 sta GAP
 jsr Delay
 ldy ITER
 cpy #1
 beq ReuseStrobe
 cpy #3
 beq ReuseStrobe
 cpy #4
 beq LoadCached
 lda ORDER,y
 sta ACTOR
 jsr MaskAddress
 lda #$b9
 jsr EmitIndexed
 jmp ReuseStrobe
LoadCached:
 lda #$a5
 jsr Emit
 lda #CACHED
 jsr Emit
ReuseStrobe:
 jsr EmitResp
 lda TARGET
 sta KT
 lda ITER
 cmp #1
 beq ReuseNext
 cmp #3
 beq ReuseStoreX
 lda #$85
 bne ReuseStore
ReuseStoreX:
 lda #$86
ReuseStore:
 jsr Emit
 lda #GRP1
 jsr Emit
 lda KT
 clc
 adc #3
 sta KT
ReuseNext:
 inc ITER
 lda ITER
 cmp #5
 bcc ReuseSlot
 ldy ORDER+4
 sty ACTOR
 jsr MaskAddress
 ldy #0
 lda (ADDRLO),y
 sta CACHED
 inc ADDRLO
 lda #$b9
 jsr EmitIndexed
 lda #$85
 jsr Emit
 lda #CACHED
 jsr Emit
 jmp FinishKernel
ReuseCost:
 byte 7,3,7,3,6

EmitIndexed:
 jsr Emit
 lda ADDRLO
 jsr Emit
 lda ADDRHI
 jmp Emit

EmitResp:
 lda GAP
 cmp #1
 beq RespAbsolute
 lda #$85
 jsr Emit
 lda #RESP1
 jmp Emit
RespAbsolute:
 lda #$8d
 jsr Emit
 lda #RESP1
 jsr Emit
 lda #0
 jmp Emit

 IF CACHE_PROBE
; Counterexample: four distinct masks can use nine-cycle strobes if two
; rows are streamed through zero page. The fifth slot is excluded up front
; so this diagnostic has enough time to refill both caches at line end.
AdmitCacheProbe:
 ldx #0
CacheCheck:
 ldy ORDER,x
 lda XP,y
 cmp #19
 bcc CacheReject
 tay
 lda CyclesByPixel,y
 cmp #52
 bcs CacheReject
 sta SLOT_CLOCKS,x
 cpx #0
 bne CacheGapCheck
 cmp #20
 bcc CacheReject
 bcs CacheNextCheck
CacheGapCheck:
 sec
 sbc #9
 cmp SLOT_CLOCKS-1,x
 bcc CacheReject
CacheNextCheck:
 inx
 cpx #4
 bcc CacheCheck
 sec
 rts
CacheReject:
 clc
 rts

BuildCacheProbe:
 lda #1
 sta FAST
 sta USED
 ldx #0
 ldy #0
CachePrefixLoop:
 lda FastPrefix,y
 jsr Emit
 iny
 cpy #FastPrefixEnd-FastPrefix
 bcc CachePrefixLoop
 lda ORDER+1
 sta ACTOR
 jsr MaskAddress
 lda #$be
 jsr EmitIndexed
 lda #13
 sta KT
 lda #0
 sta ITER
CacheSlot:
 ldy ITER
 lda SLOT_CLOCKS,y
 sta TARGET
 sec
 sbc KT
 sec
 sbc CacheCost,y
 sta GAP
 jsr Delay
 ldy ITER
 cpy #1
 beq CacheStrobe
 bcs LoadCacheByte
 lda ORDER
 sta ACTOR
 jsr MaskAddress
 lda #$b9
 jsr EmitIndexed
 jmp CacheStrobe
LoadCacheByte:
 lda #$a5
 jsr Emit
 ldy ITER
 lda CacheAddresses-2,y
 jsr Emit
CacheStrobe:
 jsr EmitResp
 lda ITER
 cmp #1
 beq CacheStoreX
 lda #$85
 bne CacheStore
CacheStoreX:
 lda #$86
CacheStore:
 jsr Emit
 lda #GRP1
 jsr Emit
 lda TARGET
 clc
 adc #3
 sta KT
 inc ITER
 lda ITER
 cmp #4
 bcc CacheSlot
 lda #2
 sta ITER
CacheRefill:
 ldy ITER
 lda ORDER,y
 sta ACTOR
 jsr MaskAddress
 ldy #0
 lda (ADDRLO),y
 ldy ITER
 pha
 lda CacheAddresses-2,y
 tay
 pla
 sta $0000,y
 inc ADDRLO
 lda #$b9
 jsr EmitIndexed
 lda #$85
 jsr Emit
 ldy ITER
 lda CacheAddresses-2,y
 jsr Emit
 inc ITER
 lda ITER
 cmp #4
 bcc CacheRefill
 jmp FinishKernel
CacheCost:
 byte 7,3,6,6
CacheAddresses:
 byte CACHED,CACHE_RIGHT
 ENDIF

 IF PHASE_PROBE
; Try independent masks with a held X register, graphics writes before
; selected strobes, and a cycle-locked (no WSYNC) loop after the first row.
AdmitPhase:
 ldx #0
PhaseCheck:
 ldy ORDER,x
 lda XP,y
 cmp #19
 bcc PhaseNo
 tay
 lda CyclesByPixel,y
 cmp #59
 bcs PhaseNo
 sta SLOT_CLOCKS,x
 cpx #0
 beq PhaseNext
 sec
 sbc SLOT_CLOCKS-1,x
 cmp PhaseMinimum,x
 bcc PhaseNo
PhaseNext:
 inx
 cpx #5
 bcc PhaseCheck
 sec
 rts
PhaseNo:
 clc
 rts
PhaseMinimum:
 IF PHASE_PROBE = 3
 byte 22,9,8,9,8
 ELSE
 IF PHASE_PROBE = 4
 byte 22,8,8,9,8
 ELSE
 byte 22,8,9,8,8
 ENDIF
 ENDIF

BuildPhase:
 IF PHASE_PROBE >= 8
 jmp BuildResource
 ENDIF
 IF PHASE_PROBE = 6
 jmp BuildShadow
 ENDIF
 lda #1
 IF PHASE_PROBE = 2
 sta VDELP1
 ENDIF
 sta FAST
 lda #0
 sta USED
 sta PHASE_INDEX
 ldx #0
 ldy #PhasePrefix-PhaseBytes
 jsr CopyPhaseBlock
 IF PHASE_PROBE = 3
 lda ORDER
 sta ACTOR
 jsr MaskAddress
 lda #$b9
 jsr EmitIndexed
 ldy #PhaseStoreA-PhaseBytes
 jsr CopyPhaseBlock
 lda ORDER+1
 ELSE
 IF PHASE_PROBE = 4
 lda ORDER+1
 sta ACTOR
 jsr MaskAddress
 lda #$b9
 jsr EmitIndexed
 ldy #PhaseStoreA-PhaseBytes
 jsr CopyPhaseBlock
 ENDIF
 lda ORDER+1
 ENDIF
 IF PHASE_PROBE != 4
 sta ACTOR
 jsr MaskAddress
 lda #$b9
 jsr EmitIndexed
 ENDIF
 IF PHASE_PROBE = 3
 lda #18
 ELSE
 lda #19
 ENDIF
 sta KT
PhaseSlot:
 ldy PHASE_INDEX
 lda SLOT_CLOCKS,y
 sta TARGET
 sec
 sbc KT
 sec
 sbc PhaseCost,y
 IF PHASE_PROBE = 7
 cpy #1
 bne SavePhaseDelay
 sec
 sbc #1
SavePhaseDelay:
 ENDIF
 sta GAP
 jsr Delay
 ldy PHASE_INDEX
 IF PHASE_PROBE = 3
 cpy #1
 bne Slot3LoadSM
 ldy #PhaseStoreA-PhaseBytes
 jsr CopyPhaseBlock
 jmp PhaseStrobe
Slot3LoadSM:
 cpy #2
 bne PhaseStrobe
 lda ORDER+3
 sta ACTOR
 jsr MaskAddress
 lda #$b9
 jsr EmitIndexed
 ELSE
 IF PHASE_PROBE = 4
 cpy #1
 bne Slot4PrefetchSM
 lda ORDER+2
 jmp Slot4LoadA
Slot4PrefetchSM:
 cpy #2
 bne Slot4PrefetchM
 lda ORDER+3
 sta ACTOR
 jsr MaskAddress
 lda #$be
 jsr EmitIndexed
 jmp PhaseStrobe
Slot4PrefetchM:
 cpy #4
 bne PhaseStrobe
 lda ORDER+4
Slot4LoadA:
 sta ACTOR
 jsr MaskAddress
 lda #$b9
 jsr EmitIndexed
 ELSE
 cpy #1
 beq PhasePrefetchF
 cpy #3
 bne PhaseStrobe
 lda ORDER+3
 sta ACTOR
 jsr MaskAddress
 lda #$b9
 jsr EmitIndexed
 jmp PhaseStrobe
PhasePrefetchF:
 lda ORDER+2
 sta ACTOR
 jsr MaskAddress
 lda #$be
 jsr EmitIndexed
 ENDIF
 ENDIF
PhaseStrobe:
 jsr EmitResp
 ldy PHASE_INDEX
 lda TARGET
 clc
 adc PhasePost,y
 sta KT
 lda PhaseBlock,y
 tay
 jsr CopyPhaseBlock
 ldy PHASE_INDEX
 cpy #4
 beq PhaseFinish
 inc PHASE_INDEX
 jmp PhaseSlot

PhaseFinish:
 IF PHASE_PROBE != 4
 lda ORDER+4
 sta ACTOR
 jsr MaskAddress
 lda #$b9
 jsr EmitIndexed
 ENDIF
 ldy #PhaseStoreA-PhaseBytes
 jsr CopyPhaseBlock
 IF PHASE_PROBE = 3
 lda ORDER+2
 ELSE
 lda ORDER
 ENDIF
 sta ACTOR
 jsr MaskAddress
 ldy #0
 lda (ADDRLO),y
 sta CACHED
 inc ADDRLO
 lda #$be
 jsr EmitIndexed
 IF PHASE_PROBE = 3
 lda #$c8
 jsr Emit
 lda #6
 sta BRANCH
 lda #58
 ELSE
 IF PHASE_PROBE = 4
 lda #64
 ELSE
 lda #60
 ENDIF
 ENDIF
 sec
 sbc TARGET
 sta GAP
 jsr Delay
 lda #$c0
 jsr Emit
 IF PHASE_PROBE = 3
 lda #ROWS
 ELSE
 lda #ROWS-1
 ENDIF
 jsr Emit
 lda #$d0
 jsr Emit
 txa
 eor #$ff
 clc
 adc #2                 ; loop starts at CODE+2, after its one initial WSYNC
 jsr Emit
 lda #$60
 jmp Emit

PhaseCost:
 IF PHASE_PROBE = 3
 byte 3,6,7,3,3
 ELSE
 IF PHASE_PROBE = 4
 byte 3,7,7,3,7
 ELSE
 byte 3,7,3,7,3
 ENDIF
 ENDIF
PhasePost:
 IF PHASE_PROBE = 3
 byte 0,0,3,3,11
 ELSE
 IF PHASE_PROBE = 4
 byte 0,0,6,0,3
 ELSE
 byte 0,6,0,3,11
 ENDIF
 ENDIF
PhaseBlock:
 IF PHASE_PROBE = 3
 byte PhaseEmpty-PhaseBytes,PhaseEmpty-PhaseBytes,PhaseStoreX-PhaseBytes,PhaseStoreA-PhaseBytes,PhaseEmpty-PhaseBytes
 ELSE
 IF PHASE_PROBE = 4
 byte PhaseEmpty-PhaseBytes,PhaseEmpty-PhaseBytes,PhaseStoreBoth-PhaseBytes,PhaseEmpty-PhaseBytes,PhaseEmpty-PhaseBytes
 ELSE
 byte PhaseEmpty-PhaseBytes,PhaseStoreBoth-PhaseBytes,PhaseEmpty-PhaseBytes,PhaseStoreA-PhaseBytes,PhaseEmpty-PhaseBytes
 ENDIF
 ENDIF

CopyPhaseBlock:
 lda PhaseBytes,y
 cmp #$ff
 beq PhaseBlockDone
 jsr Emit
 iny
 bne CopyPhaseBlock
PhaseBlockDone:
 rts

; Blocks are offset-addressed and terminated by sentinel $ff.
PhaseBytes:
PhasePrefix:
 IF PHASE_PROBE = 3
 byte $85,WSYNC,$b9,<PlayerRows,>PlayerRows,$85,GRP0,$ff
 ELSE
 IF PHASE_PROBE = 4
 byte $85,WSYNC,$c8,$b9,<PlayerRows,>PlayerRows,$85,GRP0,$86,GRP1,$ff
 ELSE
 byte $85,WSYNC,$c8,$24,FRAME,$b9,<PlayerRows,>PlayerRows,$85,GRP0,$86,GRP1,$ff
 ENDIF
 ENDIF
PhaseStoreX:
 byte $86,GRP1,$ff
PhaseStoreBoth:
 IF PHASE_PROBE = 7
 byte $8d,GRP1,0,$86,GRP1,$ff
 ELSE
 IF PHASE_PROBE = 5
 byte $85,GRP1,$24,FRAME,$ff
 ELSE
 byte $85,GRP1,$86,GRP1,$ff
 ENDIF
 ENDIF
PhaseStoreA:
 byte $85,GRP1,$ff
 IF PHASE_PROBE = 6
ShadowPrefix:
 byte $85,WSYNC,$c8,$be,<PlayerRows,>PlayerRows,$86,GRP0,$a9,1,$85,VDELP1,$ff
ShadowLatchSF:
 byte $85,GRP1,$86,GRP0,$ff
ShadowCommitF:
 byte $86,GRP0,$a9,0,$85,VDELP1,$ff
 ENDIF
PhaseEmpty:
 byte $ff
 ENDIF

 IF PHASE_PROBE = 6
; Deliberately test only sorted slots 1/2/4. Two omitted slots are counted
; as misses. X retains the actual player byte for every GRP0 trigger.
BuildShadow:
 lda #1
 sta FAST
 lda #2
 sta USED
 ldx #0
 ldy #ShadowPrefix-PhaseBytes
 jsr CopyPhaseBlock
 lda ORDER+1
 sta ACTOR
 jsr MaskAddress
 lda #$b9
 jsr EmitIndexed
 ldy #ShadowLatchSF-PhaseBytes
 jsr CopyPhaseBlock
 lda ORDER+2
 sta ACTOR
 jsr MaskAddress
 lda #$b9
 jsr EmitIndexed
 lda SLOT_CLOCKS+1
 sec
 sbc #31
 bcs ShadowSFDelay
 ; Negative control only when the strobe windows have enough room.
 jmp ShadowFallback
ShadowSFDelay:
 sta GAP
 jsr Delay
 jsr EmitResp
 ldy #PhaseStoreA-PhaseBytes
 jsr CopyPhaseBlock
 lda SLOT_CLOCKS+2
 sec
 sbc SLOT_CLOCKS+1
 sec
 sbc #6
 sta GAP
 jsr Delay
 jsr EmitResp
 ldy #ShadowCommitF-PhaseBytes
 jsr CopyPhaseBlock
 lda ORDER+4
 sta ACTOR
 jsr MaskAddress
 lda #$b9
 jsr EmitIndexed
 ldy #PhaseStoreA-PhaseBytes
 jsr CopyPhaseBlock
 lda SLOT_CLOCKS+4
 sec
 sbc SLOT_CLOCKS+2
 sec
 sbc #18
 sta GAP
 jsr Delay
 jsr EmitResp
 jmp FinishKernel
ShadowFallback:
 ; Admission guarantees this is unreachable.
 jmp CheckOrdinaryPhase
 ENDIF
 IF PHASE_PROBE >= 8
CheckResource:
 IF PHASE_PROBE >= 11
 lda SLOT_CLOCKS
 cmp #22
 bne ResourceNo
 ENDIF
 IF PHASE_PROBE >= 9
 ; P0 starts at physical X9. Its wide second copy can only help the
 ; actor at X73. No assumption on that actor's identity or Y.
 ldy ORDER+2
 lda XP,y
 cmp #73
 bne ResourceNo
 lda SLOT_CLOCKS+4
 cmp #58
 bne ResourceNo
 lda SLOT_CLOCKS+1
 cmp #31
 bne ResourceNo
 ELSE
 ; Only deadlines and dependency gaps determine this plan.
 lda SLOT_CLOCKS+1
 sec
 sbc SLOT_CLOCKS
 cmp #8
 bcc ResourceNo
 lda SLOT_CLOCKS+2
 sec
 sbc SLOT_CLOCKS+1
 cmp #9
 bcc ResourceNo
 lda SLOT_CLOCKS+4
 sec
 sbc SLOT_CLOCKS+2
 cmp #17
 bcc ResourceNo
 ENDIF
 sec
 rts
ResourceNo:
 clc
 rts

BuildResource:
 lda #1
 sta FAST
 IF PHASE_PROBE = 8
 sta VDELP1
 sta USED
 ELSE
 lda #4
 sta NUSIZ0
 IF PHASE_PROBE >= 10
 lda #7
 sta BRANCH
 ENDIF
 lda #2
 sta USED
 ENDIF
 ldx #0
 ldy #ResourcePrefix-ResourceBytes
 jsr CopyResource
 IF PHASE_PROBE = 8
 lda ORDER
 jsr LoadResourceMask
 ldy #ResourceCommit-ResourceBytes
 jsr CopyResource
 lda SLOT_CLOCKS
 sec
 sbc #22
 jsr ResourceResp
 lda #$b9
 jsr Emit
 lda #UNION
 jsr Emit
 lda #0
 jsr Emit
 lda SLOT_CLOCKS+1
 sec
 sbc SLOT_CLOCKS
 sec
 sbc #7
 jsr ResourceResp
 ldy #ResourceCommit-ResourceBytes
 jsr CopyResource
 lda SLOT_CLOCKS+2
 sec
 sbc SLOT_CLOCKS+1
 sec
 sbc #9
 jsr ResourceResp
 lda ORDER+2
 jsr LoadResourceMask
 ldy #ResourceCommit-ResourceBytes
 jsr CopyResource
 lda ORDER+4
 jsr LoadResourceMask
 lda SLOT_CLOCKS+4
 sec
 sbc SLOT_CLOCKS+2
 sec
 sbc #17
 jsr ResourceResp
 ldy #ResourceCommit-ResourceBytes
 jsr CopyResource
 ELSE
 IF PHASE_PROBE >= 11
 lda #1
 sta USED
 lda ORDER
 jsr LoadResourceMask
 ldy #ResourceLeft-ResourceBytes
 jsr CopyResource
 IF PHASE_PROBE = 12
 ldy #ResourceEarlySF-ResourceBytes
 jsr CopyResource
 ENDIF
 lda ORDER+1
 jsr LoadResourceMask
 ldy #ResourceFourSF-ResourceBytes
 jsr CopyResource
 lda ORDER+4
 jsr LoadResourceMask
 ldy #ResourceFourRight-ResourceBytes
 jsr CopyResource
 lda ORDER+2
 sta ACTOR
 jsr MaskAddress
 ldy #0
 lda (ADDRLO),y
 sta CACHED
 inc ADDRLO
 lda #$be
 jsr EmitIndexed
 lda #$c0
 jsr Emit
 lda #ROWS-1
 jsr Emit
 lda #$d0
 jsr Emit
 txa
 eor #$ff
 clc
 adc #2
 jsr Emit
 lda #$60
 jmp Emit
 ELSE
 lda ORDER+1
 jsr LoadResourceMask
 ldy #ResourceSF-ResourceBytes
 jsr CopyResource
 lda ORDER+2
 jsr LoadResourceMask
 ldy #ResourceP0-ResourceBytes
 jsr CopyResource
 lda ORDER+4
 jsr LoadResourceMask
 ldy #ResourceRight-ResourceBytes
 jsr CopyResource
 ENDIF
 ENDIF
 IF PHASE_PROBE = 8
 ; Prepare physical per-row SF events before the visible band. A zero
 ; byte is a blank row. Retain the cache index in the same Y register.
 lda ORDER+1
 sta ACTOR
 jsr MaskAddress
 ldy #ROWS-1
StageRows:
 lda (ADDRLO),y
 sta UNION,y
 dey
 bpl StageRows
 ENDIF
 jmp FinishKernel

LoadResourceMask:
 sta ACTOR
 jsr MaskAddress
 lda #$b9
 jmp EmitIndexed
ResourceResp:
 sta GAP
 jsr Delay
 jmp EmitResp
CopyResource:
 lda ResourceBytes,y
 cmp #$ff
 beq ResourceDone
 jsr Emit
 iny
 bne CopyResource
ResourceDone:
 rts
ResourceBytes:
ResourcePrefix:
 IF PHASE_PROBE = 8
 byte $85,WSYNC,$c8,$be,<PlayerRows,>PlayerRows,$86,GRP0,$ff
 ELSE
 byte $85,WSYNC,$c8,$b9,<PlayerRows,>PlayerRows,$85,GRP0,$ff
 ENDIF
ResourceCommit:
 byte $85,GRP1,$86,GRP0,$ff
 IF PHASE_PROBE >= 11
ResourceLeft:
 byte $85,GRP1,$24,FRAME,$85,RESP1,$ff
ResourceFourSF:
 IF PHASE_PROBE = 12
 byte $85,GRP1,$a9,$0e,$85,COLUP0,$86,GRP0,$ff
ResourceEarlySF:
 byte $a9,0,$85,ENAM0,$8d,RESP1,0,$ff
 ELSE
 byte $ea,$85,RESP1,$85,GRP1,$a9,0,$85,ENAM0,$a9,$0e,$85,COLUP0,$86,GRP0,$ff
 ENDIF
ResourceFourRight:
 IF PHASE_PROBE = 12
 byte $85,GRP1,$ea,$85,RESP1
 ELSE
 byte $85,GRP1,$8d,RESP1,0
 ENDIF
 byte $a9,$1e,$85,COLUP0,$8d,ENAM0,0,$ff
 ENDIF
 IF PHASE_PROBE >= 9
ResourceSF:
 ; c13 -> GRP1 c16 -> M0 off c27 -> RESP1 c31 -> white c36.
 byte $85,GRP1,$a9,0,$24,FRAME,$24,FRAME,$85,ENAM0
 byte $8d,RESP1,0,$a9,$0e,$85,COLUP0,$ff
ResourceP0:
 byte $85,GRP0,$ff
ResourceRight:
 ; GRP1 c50 -> RESP1 c58 -> yellow c63 -> M0 on c68.
 byte $85,GRP1,$24,FRAME,$ea,$85,RESP1,$a9,$1e,$85,COLUP0,$a9,2,$85,ENAM0,$ff
 ENDIF
 ENDIF

FastPrefix:
 sta WSYNC
 iny
 lda PlayerRows,y
 sta GRP0
FastPrefixEnd:
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
 IF MISSILE
MissileTail:
 lda MissileRows,y
 sta ENAM1
MissileTailEnd:
 ALIGN 32
MissileRows:
 ds 11,0
 byte 2
 ds 12,0
 ENDIF
EndProgram:
 include "tables.inc"
 ORG $fffa
 word Reset,Reset,Reset
