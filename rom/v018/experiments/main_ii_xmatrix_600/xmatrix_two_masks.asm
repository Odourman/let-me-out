; MAIN II R1b: two DIFFERENT user-referenced 8x9 masks in same Y band.
; EXPLORATORY NTSC/F6. Not full R1. No copied third-party assembler.
; Eight A/B delay combinations with shortened 2-cycle GRP1 settle. P0 yellow, M0 projectile.
 processor 6502
VSYNC=$00
VBLANK=$01
WSYNC=$02
NUSIZ0=$04
NUSIZ1=$05
COLUP0=$06
COLUP1=$07
COLUBK=$09
PF0=$0D
PF1=$0E
PF2=$0F
RESP0=$10
RESP1=$11
RESM0=$12
GRP0=$1B
GRP1=$1C
ENAM0=$1D
FRAMELO=$80
DELAYA=$81
DELAYB=$82
PHASEIDX=$83
 ORG $F000
Reset:
 SEI
 CLD
 LDX #$FF
 TXS
 LDA #0
 STA FRAMELO
 STA PHASEIDX
 STA VSYNC
 STA VBLANK
 STA GRP0
 STA GRP1
 STA ENAM0
 STA PF0
 STA PF1
 STA PF2
 STA COLUBK
 STA NUSIZ0
 LDA #$01
 STA NUSIZ1
 LDA #$1E
 STA COLUP0
 LDA #$0E
 STA COLUP1
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
 INC FRAMELO
 ; Phase cycles 0..7 at every 16th frame (RAM index survives
 ; 8-bit frame count wrap). Only combinations fitting 76 cycles are used.
 LDA FRAMELO
 AND #$0F
 BNE PhaseReady
 INC PHASEIDX
 LDA PHASEIDX
 CMP #8
 BNE PhaseReady
 LDA #0
 STA PHASEIDX
PhaseReady:
 LDX PHASEIDX
 LDA FirstDelayTable,X
 STA DELAYA
 LDA SecondDelayTable,X
 STA DELAYB
 STA WSYNC
 LDA #0
 STA GRP0
 STA GRP1
 STA ENAM0
 LDX #12
P0Delay:
 DEX
 BNE P0Delay
 STA RESP0
 STA WSYNC
 LDX #8
M0Delay:
 DEX
 BNE M0Delay
 STA RESM0
 STA WSYNC
 ; Place initial main P1 copy farther right so row-0 main-copy ghost
 ; cannot begin before the first same-line RESP1 retrigger.
 LDX #10
P1Delay:
 DEX
 BNE P1Delay
 STA RESP1
 STA WSYNC
 LDX #33
BlankLines:
 STA WSYNC
 DEX
 BNE BlankLines
 LDA #0
 STA VBLANK
 LDX #80
TopLines:
 STA WSYNC
 DEX
 BNE TopLines
 LDY #8
R1bRow:
 STA WSYNC
 LDA MaleRows,Y
 STA GRP1
 LDA PlayerRows,Y
 STA GRP0
 LDA ShotRows,Y
 STA ENAM0
 LDX DELAYA
R1bDelayA:
 DEX
 BNE R1bDelayA
R1bFirstRESP1:
 STA RESP1
 ; Wait until first eight pixels SHOULD be finished before GRP1 changes.
 ; Exactly two cycles after first RESP1 before loading next original mask.
 NOP
 LDA FemaleRows,Y
R1bFemaleWrite:
 STA GRP1
 LDX DELAYB
R1bDelayB:
 DEX
 BNE R1bDelayB
R1bSecondRESP1:
 STA RESP1
 DEY
 BPL R1bRow
 STA WSYNC
 LDA #0
 STA GRP0
 STA GRP1
 STA ENAM0
 LDX #101
BottomLines:
 STA WSYNC
 DEX
 BNE BottomLines
 LDA #2
 STA VBLANK
 LDX #29
Overscan:
 STA WSYNC
 DEX
 BNE Overscan
 STA WSYNC
 JMP Frame
 ORG $F200
; The user-approved original mask data are exactly preserved (Y=8..0).
MaleRows:
 BYTE $42,$42,$24,$24,$18,$FF,$18,$3C,$3C
FemaleRows:
 BYTE $24,$24,$7E,$7E,$3C,$FF,$18,$3C,$3C
; Yellow P0 is a previous unapproved temporary bitmap candidate.
PlayerRows:
 BYTE $42,$24,$18,$3C,$1E,$7E,$18,$7E,$3C
ShotRows:
 BYTE $00,$00,$00,$00,$02,$00,$00,$00,$00
FirstDelayTable:
 BYTE 1,2,3,1,2,3,1,2
SecondDelayTable:
 BYTE 1,1,1,2,2,2,3,3
 ORG $FFFA
 WORD Reset
 WORD Reset
 WORD Reset
