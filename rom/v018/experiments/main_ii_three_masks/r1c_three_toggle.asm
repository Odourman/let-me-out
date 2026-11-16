; MAIN II isolated R1c research probe: THREE DIFFERENT ORIGINAL 8x9 NPC masks, same Y.
; EXPLORATORY NTSC/F6. Not full R1. No copied third-party assembler.
; Two cycle-tight kernels alternate small-male X by ~3 color clocks. P0/M0 preserved.
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
THIRD_DELAY=$81
 ORG $F000
Reset:
 SEI
 CLD
 LDX #$FF
 TXS
 LDA #0
 STA FRAMELO
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
 STA THIRD_DELAY
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
 ; bit 4 of 8bit FRAMELO selects two separately assembled same-line
 ; kernels; only the THIRD RESP1 is delayed 1 CPU cycle in late mode.
 LDA FRAMELO
 AND #$10
 BNE UseLate
 JMP R1cEarlyRow
UseLate:
 JMP R1cLateRow
R1cEarlyRow:
 STA WSYNC
 LDA MaleRows,Y
 STA GRP1
 LDA PlayerRows,Y
 STA GRP0
 LDA ShotRows,Y
 STA ENAM0
 ; Save five cycles vs dynamic delay loop: fixed earliest first P1 trigger.
 NOP
R1cEarlyFirstRESP1:
 STA RESP1
 ; Three CPU cycles to preserve all 8 pixels of first P1 mask.
 BIT FRAMELO
 LDA FemaleRows,Y
R1cEarlyFemaleWrite:
 STA GRP1
 LDX #1
R1cEarlySecondDelay:
 DEX
 BNE R1cEarlySecondDelay
R1cEarlySecondRESP1:
 STA RESP1
 ; Three CPU cycles to preserve all 8 pixels of second P1 mask.
 BIT FRAMELO
 LDA SmallMaleRows,Y
R1cEarlySmallMaleWrite:
 STA GRP1
 LDX #1
R1cEarlyThirdDelay:
 DEX
 BNE R1cEarlyThirdDelay
R1cEarlyThirdRESP1:
 STA RESP1
 DEY
 BPL R1cEarlyRow
 STA WSYNC
 JMP SharedTail
R1cLateRow:
 STA WSYNC
 LDA MaleRows,Y
 STA GRP1
 LDA PlayerRows,Y
 STA GRP0
 LDA ShotRows,Y
 STA ENAM0
 ; Save five cycles vs dynamic delay loop: fixed earliest first P1 trigger.
 NOP
R1cLateFirstRESP1:
 STA RESP1
 ; Three CPU cycles to preserve all 8 pixels of first P1 mask.
 BIT FRAMELO
 LDA FemaleRows,Y
R1cLateFemaleWrite:
 STA GRP1
 LDX #1
R1cLateSecondDelay:
 DEX
 BNE R1cLateSecondDelay
R1cLateSecondRESP1:
 STA RESP1
 ; Three CPU cycles to preserve all 8 pixels of second P1 mask.
 BIT FRAMELO
 LDA SmallMaleRows,Y
R1cLateSmallMaleWrite:
 STA GRP1
 LDX THIRD_DELAY
R1cLateThirdDelay:
 DEX
 BNE R1cLateThirdDelay
R1cLateThirdRESP1:
 STA RESP1
 DEY
 BPL R1cLateRow
 STA WSYNC
 JMP SharedTail
SharedTail:
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
; exact original user-approved small_male 8x9, top-to-bottom:
; 00 00 3c 3c 18 7e 18 24 00. Reverse order for LDY #8 downto 0.
SmallMaleRows:
 BYTE $00,$24,$18,$7E,$18,$3C,$3C,$00,$00
; Yellow P0 is a previous unapproved temporary bitmap candidate.
PlayerRows:
 BYTE $42,$24,$18,$3C,$1E,$7E,$18,$7E,$3C
ShotRows:
 BYTE $00,$00,$00,$00,$02,$00,$00,$00,$00
 ORG $FFFA
 WORD Reset
 WORD Reset
 WORD Reset
