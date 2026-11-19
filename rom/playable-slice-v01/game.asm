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

NPCCount=5
NX=$91
NY=$96
NDir=$9b
Life=$a0               ; 255 active, 1..8 death, zero removed
Actor=$a5
Quota=$a6
TryDir=$a7
Retry=$a8
Death=$a9
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
QueueFirst=$e5        ; seven first-line bytes; populated while blanked
AudioTicks=$df
Blocked=$e0     ; five retry flags, persistent across NPC update slots
AUDC0=$15
AUDF0=$17
AUDV0=$19

 MAC DrawLine
 SUBROUTINE
 lda (P0Ptr),y
 sta GRP0
 lda #0
 cpy BLine
 bne .NoShot
 lda #2
.NoShot:
 sta ENAM0
 lda (P1Ptr),y
 sta GRP1
 lda PFData1,y
 sta PF1
 lda PFData2,y
 sta PF2
 lda PFData0,y
 sta PF0
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
 lda #44
 sta TIM64T
 ; Horizontal setup uses P0 and M0's independent reset/fine-motion registers.
 lda PX
 sec
 sbc #3
 ldx #0
 jsr Position
 lda BX
 sec
 sbc #3
 bcs MissileXReady
 lda #0
MissileXReady:
 ldx #2
 jsr Position
 sta WSYNC
 sta HMOVE
 sta WSYNC
 sta HMCLR

 jsr Schedule
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
 sta BLine
 lda #0
 sta PF0
 sta PF1
 sta PF2
 sta GRP0
 sta ENAM0
BlankWait:
 lda INTIM
 bne BlankWait
 sta WSYNC
 sta VBLANK
 ldy #80
 ldx #8
Top:
 sta WSYNC
 dex
 bne Top
 jmp Room
NextRoom:
 sta WSYNC
Room:
 DrawLine
 iny
 beq RoomEnd
 tya
 cmp QueueY,x
 bne NextRoom
 ; This line is a horizontal P1 transition. Existing map/P0 registers
 ; are held until the subsequent glyph line.
 lda QueueX,x
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
 iny
 lda (P0Ptr),y
 sta GRP0
 lda #0
 cpy BLine
 bne FirstNoShot
 lda #2
FirstNoShot:
 sta ENAM0
 lda QueueFirst,x
 sta GRP1
 lda QueueColor,x
 sta COLUP1
 lda QueueLo,x
 sta P1Ptr
 lda QueueHi,x
 sta P1Ptr+1
 inx
 iny
 bne NextRoom
RoomEnd:
 sta WSYNC
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
 inc FrameClock
 jmp GameBank
Overscan:
 lda INTIM
 bne Overscan
 jmp Frame

; A is pixel X, X is 0 for P0 and 2 for M0.
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
 lda #<(PlayerShape-255)
 sta P1Ptr
 lda #>(PlayerShape-255)
 sta P1Ptr+1
 lda #2
 sta OrderEnd
 lda #0
 sta SortI
 sta Omitted
PlanNext:
 lda #255
 sta SortJ
 sta Actor
 ldx #4
FindNext:
 lda Life,x
 beq SkipPlan
 lda NY,x
 cmp OrderEnd
 bcc SkipPlan
 cmp SortJ
 bcs SkipPlan
 sta SortJ
 stx Actor
SkipPlan:
 dex
 bpl FindNext
 lda KeyState
 cmp #1
 bne Planned
 lda KeyY
 cmp OrderEnd
 bcc Planned
 cmp SortJ
 bcs Planned
 sta SortJ
 lda #5
 sta Actor
Planned:
 ldx SortI
 ldy Actor
 bmi EndPlan
 ; Move the setup two rows earlier at a tile boundary so its two lines
 ; can keep the preceding PF bytes. The actual bitmap origin stays fixed.
 lda SortJ
 and #7
 cmp #2
 lda SortJ
 bcs NormalSetup
 sec
 sbc #2
NormalSetup:
 clc
 adc #79
 sta QueueY,x
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
 lda #$1a
 sta QueueColor,x
 lda #5
SetShape:
 tay
 sec
 lda ShapeLo,y
 sbc SortJ
 sta QueueLo,x
 lda ShapeHi,y
 sbc #0
 sta QueueHi,x
 lda SortJ
 and #7
 cmp #2
 bcc FirstIsBlank
 lda FirstBits,y
 jmp FirstReady
FirstIsBlank:
 lda #0
FirstReady:
 sta QueueFirst,x
 lda SortJ
 clc
 adc #13
 sta OrderEnd
 inc SortI
 jmp PlanNext
EndPlan:
 lda #0
 sta QueueY,x
 lda KeyState
 cmp #1
 bne NoKeyCount
 inc Omitted
NoKeyCount:
 ldx #4
CountAlive:
 lda Life,x
 beq SkipCount
 inc Omitted
SkipCount:
 dex
 bpl CountAlive
 lda Omitted
 sec
 sbc SortI
 sta Omitted
 rts
Shapes:
 byte 0,0,1,2,3
ShapeLo:
 byte <(Mask0-80),<(Mask1-80),<(Mask2-80),<(Mask3-80),<(DeathShape-80),<(KeyShape-80)
ShapeHi:
 byte >(Mask0-80),>(Mask1-80),>(Mask2-80),>(Mask3-80),>(DeathShape-80),>(KeyShape-80)
FirstBits:
 byte $3c,$3c,0,0,0,0
 ds 175,0
PlayerShape:
 byte $3c,$7e,$18,$7e,$1e,$3c,$18,$24,$42
 ds 175,0
 include "video.inc"
 ds 175,0
DeathShape:
 byte $00,$42,$24,$18,$a5,$18,$24,$42,$00
 ds 175,0
KeyShape:
 byte $00,$70,$50,$7e,$24,$04,$00,$00,$00
 ds 175,0
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
 ORG $fffa
 word Reset,Reset,Reset
