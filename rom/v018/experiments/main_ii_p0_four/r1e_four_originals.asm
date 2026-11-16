; MAIN II R1e isolated four ORIGINAL masks: P1 three plus P0 white wide copy.
; EXPLORATORY NTSC/F6. Not full R1. No copied third-party assembler.
; Static four-distinct-mask feasibility. M0 on preceding row, no free-X proof.
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
 LDA #$04
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
 STA WSYNC
 LDA #0
 STA GRP0
 STA GRP1
 STA ENAM0
 LDX #15
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
 LDX #79
TopLines:
 STA WSYNC
 DEX
 BNE TopLines
 ; Missile line: NUSIZ0=0 prevents a second M0 shot, restores P0 wide.
 ; 79 top lines plus this one = 80.
 STA NUSIZ0
 LDA #$1E
 STA COLUP0
 LDA #2
 STA ENAM0
 STA WSYNC
 LDA #0
 STA ENAM0
 LDA #$04
 STA NUSIZ0
 LDY #8
R1cRow:
 STA WSYNC
 LDA MaleRows,Y
 STA GRP1
 LDA PlayerRows,Y
 STA GRP0
 ; Five cycles: first P0 copy remains yellow on each NPC raster row.
 LDA #$1E
 STA COLUP0
 ; Save five cycles vs dynamic delay loop: fixed earliest first P1 trigger.
 NOP
R1cFirstRESP1:
 STA RESP1
 ; Three CPU cycles to preserve all 8 pixels of first P1 mask.
 BIT FRAMELO
 LDA FemaleRows,Y
R1cFemaleWrite:
 STA GRP1
 LDX #1
R1cSecondDelay:
 DEX
 BNE R1cSecondDelay
R1cSecondRESP1:
 STA RESP1
 ; Seven cycles: load the fourth ORIGINAL bitmap into P0 after yellow copy.
 LDX SmallFemaleRows,Y
R1eFourthP0Write:
 STX GRP0
 ; Five cycles: whiten only P0 automatic wide-spaced second copy.
 LDA #$0E
R1eFourthColorWrite:
 STA COLUP0
 ; Seven cycles: third P1's original mask; preserves 76-cycle budget.
 LDA SmallMaleRows,Y
R1cSmallMaleWrite:
 STA GRP1
R1cThirdRESP1:
 STA RESP1
 DEY
 BPL R1cRow
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
; exact original user-approved small_male 8x9, top-to-bottom:
; 00 00 3c 3c 18 7e 18 24 00. Reverse order for LDY #8 downto 0.
SmallMaleRows:
 BYTE $00,$24,$18,$7E,$18,$3C,$3C,$00,$00
; Yellow P0 is a previous unapproved temporary bitmap candidate.
SmallFemaleRows:
 BYTE $00,$24,$3C,$7E,$18,$3C,$3C,$00,$00
PlayerRows:
 BYTE $42,$24,$18,$3C,$1E,$7E,$18,$7E,$3C
ShotRows:
 BYTE $00,$00,$00,$00,$02,$00,$00,$00,$00
 ORG $FFFA
 WORD Reset
 WORD Reset
 WORD Reset
