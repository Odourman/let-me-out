; LET ME OUT! v0.18 / R3 C02 only / isolated right-door NTSC diagnostic.
; Source map: design/PLANERADE_RUMSKARTOR_V011.json selected C02, exact geometry.
; 16KiB standard F6 = four byte-identical 4KiB banks (no expanded TIA power).
; Frame period: 3 VSYNC + 37 VBLANK + 192 visible + 30 overscan = 262.
; 192 visible: 8 blank + 176 C02 (22*8) + 8 blank.
; Asymmetric PF writes: LEFT0/1/2 then RIGHT0/1/2, CTRLPF=0.
; P1 x~right border: port drawn orange, transparent black round+wedge keyhole.
; Data rows of C02 'D' remain clear PF: orange P1 overlays right-only portal.
; Minimal logical entry check: state flag and test (x,y); no game progression.
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
CTRLPF=$0A
PF0=$0D
PF1=$0E
PF2=$0F
RESP0=$10
RESP1=$11
GRP0=$1B
GRP1=$1C
HMP0=$20
HMP1=$21
HMOVE=$2A
HMCLR=$2B

SCENE_ID=$80
FRAMELO=$81
DOOR_PHASE=$82
DOOR_OPEN=$83
TEST_X=$84
TEST_Y=$85
TEST_PASS=$86
TEST_LEFT=$87
R3_MAGIC=$88
DOOR_VISIBLE=$89

 ORG $F000
Reset:
 SEI
 CLD
 LDX #$FF
 TXS
 LDX #$7F
 LDA #0
ClearRIOT:
 STA $80,X
 DEX
 BPL ClearRIOT
 LDA #$03
 STA SCENE_ID
 LDA #$C3
 STA R3_MAGIC
 LDA #$FF   ; first frame sets FRAMELO=0
 STA FRAMELO
 LDA #0
 STA VSYNC
 STA VBLANK
 STA GRP0
 STA GRP1
 STA PF0
 STA PF1
 STA PF2
 STA NUSIZ0
 STA NUSIZ1
 STA HMP0
 STA HMP1
 STA HMCLR
 STA CTRLPF ; asymmetric playfield
 STA COLUBK ; black background/keyhole
 LDA #$34
 STA COLUPF ; candidate brown NTSC (must inspect in Stella)
 LDA #0
 STA DOOR_PHASE
 STA DOOR_OPEN
Frame:
 LDA #2
 STA VSYNC
 STA WSYNC
 STA WSYNC
 STA WSYNC
 LDA #0
 STA VSYNC
 LDA #2
 STA VBLANK
 ; VBLANK scanline 3: deterministic three-state sequence 0..179.
 ; 0..59 brown locked, 60..119 orange locked, 120..179 opened.
 INC FRAMELO
 LDA FRAMELO
 CMP #180
 BNE PhaseChoice
 LDA #0
 STA FRAMELO
PhaseChoice:
 CMP #60
 BCC StateBrown
 CMP #120
 BCC StateOrange
StateOpen:
 LDA #2
 STA DOOR_PHASE
 LDA #1
 STA DOOR_OPEN
 LDA #0
 STA DOOR_VISIBLE
 STA COLUP1
 JMP StateChosen
StateBrown:
 LDA #0
 STA DOOR_PHASE
 STA DOOR_OPEN
 LDA #$FF
 STA DOOR_VISIBLE
 LDA #$34
 STA COLUP1
 JMP StateChosen
StateOrange:
 LDA #1
 STA DOOR_PHASE
 LDA #0
 STA DOOR_OPEN
 LDA #$FF
 STA DOOR_VISIBLE
 LDA #$3C
 STA COLUP1
StateChosen:
 STA WSYNC
 ; VBLANK scanline 4: set P1 near far right. This is a single
 ; coarse position per frame. Measure exact drawn X in Stella.
 LDX #13    ; #14 overruns one CPU scanline and wraps P1 to x~0
PlaceDoor:
 DEX
 BNE PlaceDoor
 STA RESP1
 STA WSYNC
 ; VBLANK scanline 5: synthetic minimal passage requests; no gameplay.
 STA HMOVE
 LDA FRAMELO
 AND #3
 TAY
 LDA ProbeX,Y
 STA TEST_X
 LDA ProbeY,Y
 STA TEST_Y
 LDA #0
 STA TEST_PASS
 STA TEST_LEFT
 LDA DOOR_OPEN
 BEQ PassageEnd
 LDA TEST_X
 CMP #39
 BNE PassageEnd
 LDA TEST_Y
 CMP #9
 BCC PassageEnd
 CMP #13
 BCS PassageEnd
 LDA #1
 STA TEST_PASS
PassageEnd:
 STA WSYNC
 ; 3 VSYNC + 3 spent VBLANK + 34 fill = 40 -> first visible line.
 LDX #34
BlankFill:
 STA WSYNC
 DEX
 BNE BlankFill
 LDA #0
 STA VBLANK
 ; visible top 8 black lines
 LDY #0
 LDX #8
VisibleTop:
 STA WSYNC
 DEX
 BNE VisibleTop
 ; 176 C02 lines. Each row has separate left/right PF bits.
 ; LDA absolute,Y crosses pages unpredictably: up to 6 extra cycles,
 ; worst 71 incl three indexed page crossings before NEXT WSYNC.
 ; This is STATIC, not a Stella debugger trace.
MapLine:
 STA WSYNC
 LDA LEFT0,Y
 STA PF0
 LDA LEFT1,Y
 STA PF1
 LDA LEFT2,Y
 STA PF2
 NOP
 NOP
 NOP
 NOP
 LDA RIGHT0,Y
 STA PF0
 LDA RIGHT1,Y
 STA PF1
 LDA RIGHT2,Y
 STA PF2
 LDA DOORROWS,Y
 AND DOOR_VISIBLE
 STA GRP1
 INY
 CPY #176
 BNE MapLine
 ; Bottom 8 blank lines incl this first WSYNC
 STA WSYNC
 LDA #0
 STA GRP1
 STA PF0
 STA PF1
 STA PF2
 LDX #7
VisibleBottom:
 STA WSYNC
 DEX
 BNE VisibleBottom
 ; Overscan starts on the next line: 30 WSYNCs.
 LDA #2
 STA VBLANK
 LDX #30
Overscan:
 STA WSYNC
 DEX
 BNE Overscan
 JMP Frame

 ORG $F400
ProbeX:
 BYTE 39,0,39,39
ProbeY:
 BYTE 10,10,8,13
; Every PF byte and P1 bit below is GENERATED from original authorized C02
; 40x22 JSON; no hand-edited level data.
 INCLUDE "dist/r3_tables.inc"
 ORG $FFFA
 WORD Reset
 WORD Reset
 WORD Reset
