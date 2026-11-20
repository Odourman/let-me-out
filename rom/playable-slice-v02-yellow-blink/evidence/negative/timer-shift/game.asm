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
GRP0=$1b
GRP1=$1c
ENAM0=$1d
ENAM1=$1e
HMP0=$20
HMP1=$21
RESP1=$11
HMOVE=$2a
HMCLR=$2b
INPT4=$0c
SWCHA=$0280
SWCHB=$0282
INTIM=$0284
TIM64T=$0296

PX=$80
PY=$81
Aim=$82
Pressed=$83
Shot=$84
BX=$85
BY=$86
Direction=$87
Hunt=$88
P0Ptr=$89
BLine=$8b
TX=$8c
TY=$8d
Tmp=$8e
Tile=$8f
FrameClock=$90
 IF BLINK_ON
KeyColor=$1e
 ELSE
KeyColor=$1a
 ENDIF

NPCCount=5
NX=$91
NY=$96
NDir=$9b
Life=$a0               ; 255 active, 1..8 death, zero removed
Actor=$a5
Quota=$a6
TryDir=$a7
Retry=$a8
CapStart=$a9           ; unused by the game bank
Points=$aa
PointsHi=$ab
Lives=$ac
RandomState=$ad
Carrier=$ae
KeyState=$af
KeyX=$b0
KeyY=$b1
Unlocked=$b2
RoomDone=$b3
QueueY=$b4              ; seven entries, including sentinel
QueueX=$bb
QueueLo=$c2
QueueHi=$c9
QueueColor=$d0
P1Ptr=$d7
SortI=$d9
SortJ=$da
OrderEnd=$db
Omitted=$dc
Sound=$dd
Eligible=$de
Rendered=$ec
TempY=$ed
MinSetup=$ee
SetupRows=$ef
DoorColor=$ed           ; reuse TempY after Schedule
AssistRow=$8c           ; TX/TY/Tmp/Tile are dead until the logic bank
AssistX=$8d
AssistPtr=$8e
AssistColor=$a7         ; TryDir/Retry are assigned by logic before use
AssistQueue=$a8
CapPlayerFirst=AssistColor  ; the M1 path excludes both assist modes
CapPlayerNext=AssistQueue
CapWallColor=AssistPtr
AssistObject=$f5       ; pending NPC index+1 during planning, render bit afterward
BridgeOld=$f6
BridgeX=$f7
NextQueueY=$a5           ; Actor is dead after frame planning
SplitY=$ee
SplitLow=$8e
SplitHigh=$8f
EntryX=$d9              ; SortI is dead after Schedule
AssistID=$da
QueueFirst=$e5        ; seven first-line bytes; populated while blanked
AudioTicks=$df
Blocked=$e0     ; five retry flags, persistent across NPC update slots
AUDC0=$15
AUDF0=$17
AUDV0=$19

 MAC DrawPF
 lda PFData0,y
 sta PF0
 lda PFData1,y
 sta PF1
 lda PFData2,y
 sta PF2
 ENDM
 MAC DrawSprites
 SUBROUTINE
 IF CAP_KERNEL = 0
 sta ENAM0             ; RoomFlags was zero, clear before the left-edge shot.
 ENDIF
 lda (P0Ptr),y
 sta GRP0
 IF CAP_KERNEL
 lda #0
 cpy BLine
 bne .NoShot
 lda #2
.NoShot:
 stx HMP0
 ELSE
 cpy BLine
 bne .NoShot
 lda #2
 sta ENAM0
.NoShot:
 nop                   ; preserve the no-shot GRP1 phase
 ENDIF
 lda (P1Ptr),y
 sta GRP1
 ENDM
 IF LOGIC
 ORG $f000
 include "logic.asm"
 ELSE
 ORG $f000
VideoReset:
 sei
 cld
 ldx #$ff
 txs
 lda #0
 ldx #127
ClearRam:
 sta $80,x
 dex
 bpl ClearRam
 ldx #$2c
ClearTIA:
 sta 0,x
 dex
 bpl ClearTIA
 jmp InitBank
VideoStart:
 lda #1
 sta CTRLPF
 lda #$1e
 sta COLUP0
 lda #$0e
 sta COLUP1
 lda #$26
 sta COLUPF
Frame:
 lda #2
 sta WSYNC
 sta VBLANK
 sta VSYNC
 sta WSYNC
 sta WSYNC
 sta WSYNC
 lda #0
 sta VSYNC
 ; Three former top blank rows give the six-object planner more time.
 lda #48
 IF BLINK_ON
 jsr BlinkPrepare
 ELSE
 sta TIM64T
 ENDIF
 sta WSYNC
 jsr PlanFrame
PositionFrame:
 lda EntryX
 sec
 sbc #3
 ldx #0
 jsr Position
 lda Shot
 beq PositionDone
 lda BX
 sec
 sbc #2
 bcs MissileXReady
 lda #0
MissileXReady:
 ldx #2
 jsr Position
PositionDone:
 jsr FinishHorizontal
 lda #0
 sta PF0
 sta PF1
 sta PF2
 sta GRP0
 sta ENAM0
 jsr SelectDoorKernel
BlankWait:
 lda INTIM
 bne BlankWait
 sta WSYNC
 sta VBLANK
 ldy #80
 ldx #5
Top:
 sta WSYNC
 dex
 bne Top
 IF TOP_DOOR
 bit PX
 nop
 nop
 jmp BorderDoor
 ds 5,0
 ELSE
 lda #$ff
 sta PF0
 sta PF1
 sta PF2
 iny
 jmp NextRoom
 ENDIF
NextRoom:
 sta WSYNC
Room:
 lda RoomFlags,y
 beq RoomSprites
 bmi DoorScanline
 jmp WallScanline
RoomSprites:
 DrawSprites
 IF CAP_KERNEL
 cpy BLine
 bne UsualRoomTail
 nop
 nop
 nop
 nop
 lda #2
 sta ENAM1
 ENDIF
UsualRoomTail:
 jmp RoomTail
 IF CAP_KERNEL = 0
 include "left_encode.inc"
RejectNearLeftHere = RejectNearLeft
 ENDIF
DoorScanline:
 lsr
 bcc BorderDoor
 jmp SpecialScanline
BorderDoor:
 lda #$f0
 sta PF0
 lda #$ff
 sta PF1
 lda PFData2,y
 bit Unlocked
 beq ClosedBorder
 and #$0f
ClosedBorder:
DoorMaskWrite:
 sta PF2
 lda (P0Ptr),y
DoorPlayerWrite:
 sta GRP0
 lda #0
 sta GRP1
 sta ENAM0
 iny
 beq LastBorderLine
 jmp NextRoom
LastBorderLine:
 sta WSYNC
 jmp RoomFinishAfterSync
EncodeNearLeftShift:
 asl
 asl
 asl
 asl
 clc
 rts
RejectNearLeft:
 sec
 rts
RoomTail:
 iny
 beq RoomEnd
RoomQueueCheck:
 cpy NextQueueY
 bne NextRoom
 ; The dedicated RESP1 line holds PF/P0 until the first glyph line.
 ; AllowedSetup excludes the actual playfield transitions.
 lda QueueX,x
 beq BridgePreSync
NpcPreSync:
 sta WSYNC
NpcSetupFirst:
 sec
NpcCoarse:
 sbc #15
 bcs NpcCoarse
 eor #7
 asl
 asl
 asl
 asl
 sta HMP1
 sta RESP1
NpcSetupSync:
 sta WSYNC
GlyphStart:
 sta HMOVE
GlyphBody:
 iny
 lda (P0Ptr),y
 sta GRP0
 lda #0
 cpy BLine
 bne FirstNoShot
 lda #2
FirstNoShot:
 IF CAP_KERNEL
 sta ENAM1
 ELSE
 sta ENAM0
 ENDIF
GlyphP1:
 lda QueueFirst,x
 sta GRP1
 lda QueueColor,x
 sta COLUP1
 lda QueueLo,x
 sta P1Ptr
 lda QueueHi,x
 sta P1Ptr+1
 inx
 lda QueueY,x
 sta NextQueueY
 iny
 beq RoomEnd
 jmp NextRoom
RoomEnd:
 jmp RoomFinish
BridgePreSync:
 sta WSYNC
 IF CAP_KERNEL
 lda #$26
 sta COLUPF
 lda CapPlayerFirst
 sta GRP0
 nop
 ENDIF
 lda BridgeOld
 sta GRP1
 lda BridgeX
 IF CAP_KERNEL
 jmp CapPositionSF
 ELSE
 bit BridgeX
 jmp NpcSetupFirst
 ds 7,0
 ENDIF
SpecialScanline:
 lda #$26
 sta COLUPF
 lda (P1Ptr),y
 sta GRP1
 cpy AssistRow
 beq AssistStart
 lda (P0Ptr),y
 sta GRP0
 lda #0
 cpy BLine
 bne SpecialNoShot
 lda #2
SpecialNoShot:
 IF CAP_KERNEL
 stx HMP0
 ELSE
 sta ENAM0
 ENDIF
 iny                     ; generated special rows never end the room
 jmp RoomQueueCheck
AssistStart:
 cpy #156+80
 bne OrdinaryAssist
 jmp KeyAssistStart
OrdinaryAssist:
 stx AssistQueue
 lda #0
 sta GRP0
 sta GRP1
 sta ENAM0
 lda AssistX
 sta WSYNC
 sec
AssistCoarse:
 sbc #15
 bcs AssistCoarse
 eor #7
 asl
 asl
 asl
 asl
 sta HMP0
 sta RESP0
AssistSync:
 sta WSYNC
AssistMove:
 sta HMOVE
AssistInstallRegisters:
 lda AssistColor
 sta COLUP0
 lda AssistPtr
 sta P0Ptr
 lda AssistPtr+1
 sta P0Ptr+1
 lda #0
 sta HMP0
 ldx AssistQueue
 iny
 iny
 iny
 jmp NextRoom
WallScanline:
 ; The dispatcher stores PF0 shifted right so its flags stay positive.
 asl
 sta PF0
 lda PFData1,y
 sta PF1
 lda PFData2,y
 sta PF2
 ; Update P1 on the wall transition before selecting the missile row.
 lda (P1Ptr),y
 sta GRP1
 lda (P0Ptr),y
 sta GRP0
 lda #0
 cpy BLine
 bne WallNoShot
 lda #2
WallNoShot:
 IF CAP_KERNEL
 stx HMP0
 ELSE
 sta ENAM0
 ENDIF
 iny
 jmp NextRoom
RoomFinish:
 sta WSYNC
RoomFinishAfterSync:
 lda #0
 sta PF0
 sta PF1
 sta PF2
 sta GRP0
 sta ENAM0
 ldx #8
Bottom:
 sta WSYNC
 dex
 bne Bottom
 lda #2
 sta VBLANK
 lda #35
 nop
 nop
 nop
 nop
 nop
 nop
 sta TIM64T
 IF BLINK_ON
 jmp BlinkFinish
 ds 2,0
 ELSE
 inc FrameClock
 jmp GameBank
 ENDIF
Overscan:
 lda INTIM
 bne Overscan
 jmp Frame

; A is pixel X, X is 0 for P0 and 2 for M0.
PlanFrame:
 ; Reserve the upper P0 band before scheduling the overlapping floor key.
 lda #0
 sta AssistObject
 sta CapStart
 jsr PrepareKeyAssist
 jsr Schedule
 IF BLINK_ON
 lda KeyState
 and #$7f
 sta KeyState
 ELSE
 lda #$3c
 ldx Unlocked
 beq DoorColorReady
 lda #$26
DoorColorReady:
 sta DoorColor
 ENDIF
 sec
 lda #<(PlayerShape-80)
 sbc PY
 sta P0Ptr
 lda #>(PlayerShape-80)
 sbc #0
 sta P0Ptr+1
 lda #0
 ldx Shot
 beq NoRasterShot
 lda BY
 clc
 adc #80
NoRasterShot:
 ora CapStart
 sta BLine
 lda PX
 sta EntryX
 lda #$1e
 sta COLUP0
 lda #0
 sta AssistRow
 lda AssistObject
 beq OrdinaryAssistPlan
 jmp InstallKeyAssist
OrdinaryAssistPlan:
 lda Omitted
 beq AssistPlanDone
 jsr ScheduleAssist
AssistPlanDone:
 lda QueueY
 sta NextQueueY
 rts

Position:
 sta WSYNC
 sec
PositionCoarse:
 sbc #15
 bcs PositionCoarse
 eor #7
 asl
 asl
 asl
 asl
 sta HMP0,x
 sta RESP0,x
 rts


 ; Collect non-overlapping visible slots in increasing Y each frame.
 ; Simulation X/Y are read only; omitted actors continue normal updates.
Schedule:
 lda #2
 sta OrderEnd
 lda #0
 sta SortI
 sta Omitted
 sta Eligible
 sta Rendered
 ldx #4
MeasureEligible:
 lda #255
 sta SetupRows,x
 lda Life,x
 beq NextEligible
 inc Omitted
 lda Eligible
 ora ObjectBit,x
 sta Eligible
 lda Life,x
 bpl DeathCandidate
 lda LeadingBlank,x
 jmp Candidate
DeathCandidate:
 lda #1
Candidate:
 clc
 adc NY,x
 sec
 sbc #1
 jsr PreserveTile
 sta SetupRows,x
NextEligible:
 dex
 bpl MeasureEligible
 lda #255
 sta SetupRows+5
 ldy AssistObject
 beq PlanKeySlot
 sta SetupRows-1,y
PlanKeySlot:
 lda KeyState
 cmp #1
 bne PlanNext
 inc Omitted
 lda Eligible
 ora #32
 sta Eligible
 lda KeyY
 jsr PreserveTile
 sta SetupRows+5
PlanNext:
 lda #255
 sta MinSetup
 sta Actor
 ldx #5
FindNext:
 lda SetupRows,x
 cmp OrderEnd
 bcc SkipPlan
 cmp MinSetup
 bcs SkipPlan
 sta MinSetup
 stx Actor
SkipPlan:
 dex
 bpl FindNext
Planned:
 ldx SortI
 ldy Actor
 bmi EndPlan
 cpy #5
 beq LoadKeyOrigin
 lda NY,y
 jmp StoreOrigin
LoadKeyOrigin:
 lda KeyY
StoreOrigin:
 sta SortJ
 lda MinSetup
 clc
 adc #80
 sta QueueY,x
 lda Rendered
 ora ObjectBit,y
 sta Rendered
 cpy #5
 beq PlanKey
 lda NX,y
 clc
 adc #3
 sta QueueX,x
 lda #$0e
 sta QueueColor,x
 lda Life,y
 bmi LivePlan
 lda #4
 bne SetShape
LivePlan:
 lda Shapes,y
 jmp SetShape
PlanKey:
 lda KeyX
 clc
 adc #3
 sta QueueX,x
 lda #KeyColor
 sta QueueColor,x
 lda #5
SetShape:
 tay
 sec
 lda ShapeLo,y
 sbc SortJ
 sta QueueLo,x
 sta P1Ptr
 lda ShapeHi,y
 sbc #0
 sta QueueHi,x
 sta P1Ptr+1
 sty TempY
 ldy QueueY,x
 iny
 lda (P1Ptr),y
 sta QueueFirst,x
 ldy TempY
 lda SortJ
 clc
 adc LastPlusTwo,y
 sta OrderEnd
 inc SortI
 jmp PlanNext
EndPlan:
 jsr BridgeFloorKey
 jsr PlanSmallOverlap
 ldx SortI
 lda #<(PlayerShape-255)
 sta P1Ptr
 lda #>(PlayerShape-255)
 sta P1Ptr+1
 lda #0
 sta QueueY,x
 lda Omitted
 sec
 sbc SortI
 sta Omitted
 rts
PreserveTile:
 tay
 lda AllowedSetup,y
 rts
CompensateAssistX:
 sec
 lda AssistX
 sbc #45
 sta AssistX
 jmp AssistPlanDone

Shapes:
 byte 0,0,1,2,3
ShapeLo:
 byte <(Mask0-80),<(Mask1-80),<(Mask2-80),<(Mask3-80),<(DeathShape-80),<(KeyShape-80)
ShapeHi:
 byte >(Mask0-80),>(Mask1-80),>(Mask2-80),>(Mask3-80),>(DeathShape-80),>(KeyShape-80)
ObjectBit:
 byte 1,2,4,8,16,32
LeadingBlank:
 byte 0,0,0,2,2
LastPlusTwo:
 byte 10,10,9,9,9,7
 ds 175,0
PlayerShape:
 byte $3c,$7e,$18,$7e,$1e,$3c,$18,$24,$42
 ds 159,0             ; the upper solid tile keeps the player at Y >= 8
 include "bridge_color.inc"
 include "video.inc"
DeathShape:
 byte $00,$42,$24,$18,$a5,$18,$24,$42,$00
 ds 175,0
KeyShape:
 byte $00,$70,$50,$7e,$24,$04,$00,$00,$00
 ds 175,0
 include "schedule.inc"
 ; Search for room to reuse P0 on the other side of a quiet strip.
 ; The strip is a register-write window. The NPC still uses its RAM X/Y.
AssistNextStrip:
 dex
 bmi AssistCheckDone
 jmp AssistCheckStrip
AssistCheckDone:
 ; P1 needs the larger guard for its own setup. P0 and M0 can
 ; begin on the first line after the three-line P0 switch.
 lda SplitHigh
 sec
 sbc #3
 sta SplitHigh
 lda PY
 cmp SplitLow
 bcc AssistHumanFirst
 cmp SplitHigh
 bcc AssistReturn
 lda Shot
 beq AssistNpcFirst
 lda BY
 cmp SplitHigh
 bcc AssistReturn
AssistNpcFirst:
 lda #0
 beq AssistFind
AssistHumanFirst:
 lda Shot
 beq AssistHumanReady
 lda BY
 cmp SplitLow
 bcs AssistReturn
AssistHumanReady:
 lda #1
AssistFind:
 sta AssistID
 ldx #4
AssistCheckCandidate:
 lda Life,x
 bpl AssistNextCandidate
 lda ObjectBit,x
 bit Rendered
 bne AssistNextCandidate
 lda NY,x
 cmp SplitY
 lda AssistID
 rol
 and #1
 eor AssistID
 beq InstallAssist
AssistNextCandidate:
 dex
 bpl AssistCheckCandidate
AssistReturn:
 rts
InstallAssist:
 lda SplitY
 clc
 adc #80
 sta AssistRow
 lda ObjectBit,x
 sta AssistObject
 ora Rendered
 sta Rendered
 dec Omitted
 ldy Shapes,x
 sec
 lda ShapeLo,y
 sbc NY,x
 sta AssistPtr
 lda ShapeHi,y
 sbc #0
 sta AssistPtr+1
 lda NX,x
 ldy AssistID
 bne AssistSetSecond
 ; NPC in the upper band, then restore the player's original pointer.
 sta EntryX
 lda P0Ptr
 ldy AssistPtr
 sty P0Ptr
 sta AssistPtr
 lda P0Ptr+1
 ldy AssistPtr+1
 sty P0Ptr+1
 sta AssistPtr+1
 lda #$0e
 sta COLUP0
 lda #$1e
 ldy PX
 jmp AssistSetColor
AssistSetSecond:
 tay
 lda #$0e
AssistSetColor:
 sta AssistColor
 tya
 clc
 adc #3
 sta AssistX
 rts


 IF BLINK_ON
 include "blink.inc"
 ENDIF
 ENDIF

 ORG $ff80
Reset:
 sta $fff6
 IF LOGIC = 0
 jmp VideoReset
 ELSE
 jmp Reset
 ENDIF
GameBank:
 sta $fff7
 IF LOGIC
 jmp LogicUpdate
 ELSE
 jmp GameBank
 ENDIF
VideoBank:
 sta $fff6
 IF LOGIC = 0
 jmp Overscan
 ELSE
 jmp VideoBank
 ENDIF
InitBank:
 sta $fff7
 IF LOGIC
 jsr InitGame
 jmp StartBank
 ELSE
 ds 6,$ea
 ENDIF
StartBank:
 sta $fff6
 IF LOGIC = 0
 jmp VideoStart
 ELSE
 jmp StartBank
 ENDIF
 IF LOGIC = 0
 include "wall_bridge.inc"
 ENDIF
 IF * > $fff6
 ERR
 ENDIF
 ORG $fffa
 word Reset,Reset,Reset
