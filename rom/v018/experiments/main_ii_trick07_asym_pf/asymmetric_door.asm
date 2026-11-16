; MAIN II isolated Atari 2600 trick #07: asymmetric PF left wall vs right door.
; OWN ORIGINAL diagnostic code. NTSC 262, ordinary F6 16KB.
; Not the game ROM. No P0/P1 NPC here: R3 PF-only primitive.
; PF0 D4 = leftmost logical map x0; reflect CTRLPF=$01 makes it
; also the rightmost logical map x39 unless PF0 is CHANGED mid-scanline.
; Alternates frame every 16 frames: brown right wall vs open right door.
 processor 6502
VSYNC=$00
VBLANK=$01
WSYNC=$02
COLUPF=$08
COLUBK=$09
CTRLPF=$0A
PF0=$0D
PF1=$0E
PF2=$0F
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
 STA PF0
 STA PF1
 STA PF2
 STA COLUBK
 LDA #$01
 STA CTRLPF
 LDA #$36
 STA COLUPF
Frame:
 INC FRAMELO
 LDA #2
 STA VSYNC
 STA WSYNC
 STA WSYNC
 STA WSYNC
 LDA #0
 STA VSYNC
 LDA #2
 STA VBLANK
 LDX #37
BlankLines:
 STA WSYNC
 DEX
 BNE BlankLines
 LDA #0
 STA VBLANK
 LDX #72
TopLines:
 STA WSYNC
 DEX
 BNE TopLines
 LDY #47
WallDoorRows:
 STA WSYNC
 ; Start every row with a CLOSED LEFT wall PF0 D4.
 LDA #$10
 STA PF0
 ; Delay update until left PF0 region is behind the beam.
 BIT FRAMELO
 BIT FRAMELO
 BIT FRAMELO
 BIT FRAMELO
 BIT FRAMELO
 BIT FRAMELO
 BIT FRAMELO
 BIT FRAMELO
 BIT FRAMELO
 BIT FRAMELO
 ; mode 0: BOTH left and right PF0 D4 intact.
 ; mode 1: midline update right PF0 from table; x39 open in door.
 LDA FRAMELO
 AND #$10
 BEQ R3RightWall
 LDA OpenDoorRightRows,Y
 JMP R3WriteRightPF0
R3RightWall:
 LDA #$10
R3WriteRightPF0:
 STA PF0
 DEY
 BPL WallDoorRows
 STA WSYNC
 LDA #0
 STA PF0
 LDX #71
BottomLines:
 STA WSYNC
 DEX
 BNE BottomLines
 LDA #2
 STA VBLANK
 LDX #30
Overscan:
 STA WSYNC
 DEX
 BNE Overscan
 JMP Frame
 ORG $F300
; 48 physical PF rows: 8 outer closed, 32 door rows, 8 outer closed.
; Table reversed (Y47 -> 0), but symmetric, so scan direction irrelevant.
OpenDoorRightRows:
 BYTE $10,$10,$10,$10,$10,$10,$10,$10
 BYTE $00,$00,$00,$00,$00,$00,$00,$00
 BYTE $00,$00,$00,$00,$00,$00,$00,$00
 BYTE $00,$00,$00,$00,$00,$00,$00,$00
 BYTE $00,$00,$00,$00,$00,$00,$00,$00
 BYTE $10,$10,$10,$10,$10,$10,$10,$10
 ORG $FFFA
 WORD Reset
 WORD Reset
 WORD Reset
