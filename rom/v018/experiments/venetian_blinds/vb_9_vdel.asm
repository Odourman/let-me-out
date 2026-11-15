; LET ME OUT! NTSC v0.18 VENETIAN BLINDS – MINIMAL 2-NPC INTERLEAVE
; ORIGINAL authored code. VDEL1 enabled – phase delayed probe.
; NOT authorized as graphics redesign. No copied third-party listing.
; User-authorized R1 feasibility only. Not 6-NPC PASS.
; P0=9-row yellow player, M0=shot; P1 alternates ORIGINAL male/female rows
; within SAME frame (no six-frame cycling), with separate delay/X tables.
; 9 scanlines, even male rows/odd female rows, masked missing rows NOT accepted.
; CPU row: STA WSYNC; LDA #bitmap (2); STA GRP1 (3); LDX delay (3);
; delay loop=5*n-1; STA RESP1(3); LDA #p0 (2); STA GRP0(3);
; LDA #shot(2); STA ENAM0(3); before next WSYNC <= 76 for n<=9.
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
HMP0=$20
HMP1=$21
VDEL1=$26
HMOVE=$2A
HMCLR=$2B
FRAMELO=$80
MALE_DELAY=$81
FEMALE_DELAY=$82
MALE_REQ_X=$90
FEMALE_REQ_X=$91
PLAYER_REQ_X=$92
SHOT_REQ_X=$93
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
 STA NUSIZ0
 STA NUSIZ1
 STA PF0
 STA PF1
 STA PF2
 STA HMP0
 STA HMP1
 STA HMCLR
 LDA #1
 STA VDEL1 ; technical diagnostic: delay P1 GRP latch, NOT a graphics compromise
 LDA #$1E
 STA COLUP0
 LDA #$0E
 STA COLUP1
 LDA #0
 STA COLUBK
 LDA #145
 STA PLAYER_REQ_X
 LDA #154
 STA SHOT_REQ_X
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
 ; Vblank scanline3: independent delays based on separate tables.
 LDA FRAMELO
 AND #$0F
 TAX
 LDA MaleDelayTable,X
 STA MALE_DELAY
 LDA FemaleDelayTable,X
 STA FEMALE_DELAY
 LDA MaleXTable,X
 STA MALE_REQ_X
 LDA FemaleXTable,X
 STA FEMALE_REQ_X
 STA WSYNC
 ; Vblank scanline4 (extra stable slot for exact 262-line skeleton).
 LDA #0
 STA GRP0
 STA GRP1
 STA ENAM0
 STA WSYNC
 ; Vblank scanline5: fixed P0 position independent of P1 test.
 LDX #12
PlayerDelay:
 DEX
 BNE PlayerDelay
 STA RESP0
 STA WSYNC
 ; Vblank scanline6: independent M0 shot position.
 LDX #14
MissileDelay:
 DEX
 BNE MissileDelay
 STA RESM0
 STA WSYNC
 ; Vblank scanline7: coarse/fine initial P1 position.
 LDA MALE_REQ_X
 LDX #1
 JSR SetHorizPos
 STA WSYNC
 ; Vblank scanline8: HMOVE only when blanked.
 STA HMOVE
 LDX #30
BlankFill:
 STA WSYNC
 DEX
 BNE BlankFill
 LDA #0
 STA VBLANK
 LDX #80
TopBlank:
 STA WSYNC
 DEX
 BNE TopBlank
 ; Preload sprite and player bitmaps; 9/18 visible scanlines below.
Row00:
 STA WSYNC
 LDA #$3C
 STA GRP1
 LDX MALE_DELAY
Delay00:
 DEX
 BNE Delay00
 STA RESP1
 LDA #$3C
 STA GRP0
 LDA #$00
 STA ENAM0
Row01:
 STA WSYNC
 LDA #$3C
 STA GRP1
 LDX FEMALE_DELAY
Delay01:
 DEX
 BNE Delay01
 STA RESP1
 LDA #$7E
 STA GRP0
 LDA #$00
 STA ENAM0
Row02:
 STA WSYNC
 LDA #$18
 STA GRP1
 LDX MALE_DELAY
Delay02:
 DEX
 BNE Delay02
 STA RESP1
 LDA #$18
 STA GRP0
 LDA #$00
 STA ENAM0
Row03:
 STA WSYNC
 LDA #$FF
 STA GRP1
 LDX FEMALE_DELAY
Delay03:
 DEX
 BNE Delay03
 STA RESP1
 LDA #$7E
 STA GRP0
 LDA #$00
 STA ENAM0
Row04:
 STA WSYNC
 LDA #$18
 STA GRP1
 LDX MALE_DELAY
Delay04:
 DEX
 BNE Delay04
 STA RESP1
 LDA #$1E
 STA GRP0
 LDA #$02
 STA ENAM0
Row05:
 STA WSYNC
 LDA #$7E
 STA GRP1
 LDX FEMALE_DELAY
Delay05:
 DEX
 BNE Delay05
 STA RESP1
 LDA #$3C
 STA GRP0
 LDA #$00
 STA ENAM0
Row06:
 STA WSYNC
 LDA #$24
 STA GRP1
 LDX MALE_DELAY
Delay06:
 DEX
 BNE Delay06
 STA RESP1
 LDA #$18
 STA GRP0
 LDA #$00
 STA ENAM0
Row07:
 STA WSYNC
 LDA #$24
 STA GRP1
 LDX FEMALE_DELAY
Delay07:
 DEX
 BNE Delay07
 STA RESP1
 LDA #$24
 STA GRP0
 LDA #$00
 STA ENAM0
Row08:
 STA WSYNC
 LDA #$42
 STA GRP1
 LDX MALE_DELAY
Delay08:
 DEX
 BNE Delay08
 STA RESP1
 LDA #$42
 STA GRP0
 LDA #$00
 STA ENAM0
 STA WSYNC
 LDA #0
 STA GRP0
 STA GRP1
 STA GRP0  ; VDEL1: second GRP0 write flushes delayed GRP1 latch to zero
 STA ENAM0
 LDX #102
BottomBlank:
 STA WSYNC
 DEX
 BNE BottomBlank
 LDA #2
 STA VBLANK
 LDX #29
Overscan:
 STA WSYNC
 DEX
 BNE Overscan
 STA WSYNC
 INC FRAMELO
 JMP Frame
 ; Position helper for initial P1 only (not for individual visible lines).
SetHorizPos:
 STA WSYNC
 BIT $00
 SEC
Subtract15:
 SBC #15
 BCS Subtract15
 EOR #7
 ASL
 ASL
 ASL
 ASL
 STA RESP0,X
 STA HMP0,X
 RTS
 ORG $F300
MaleDelayTable:
 BYTE $04,$04,$05,$04,$05,$05,$05,$04,$04,$05,$05,$04,$05,$04,$04,$05
FemaleDelayTable:
 BYTE $08,$09,$08,$08,$09,$09,$08,$09,$08,$09,$09,$09,$08,$08,$09,$08
; Delays are coarse measured candidates; X entries are requested/nominal
; and MUST be compared with observed Stella pixel X, not assumed accurate.
MaleXTable:
 BYTE $18,$18,$27,$18,$27,$27,$27,$18,$18,$27,$27,$18,$27,$18,$18,$27
FemaleXTable:
 BYTE $54,$63,$54,$54,$63,$63,$54,$63,$54,$63,$63,$63,$54,$54,$63,$54
; Unmodified reference sprite masks:
MaleRows:
 BYTE $3C,$3C,$18,$FF,$18,$24,$24,$42,$42
FemaleRows:
 BYTE $3C,$3C,$18,$FF,$3C,$7E,$7E,$24,$24
PlayerRows:
 BYTE $3C,$7E,$18,$7E,$1E,$3C,$18,$24,$42
 ORG $FFFA
 WORD Reset
 WORD Reset
 WORD Reset
