; LET ME OUT! v0.18 / SEX_X_FREE R1 diagnostic, 6502 source for DASM.
; USER-AUTHORIZED TEST ONLY. It is NOT a valid full R1 renderer.
; Six logical X coordinates in RIOT $90-$95 with six distinct 32-frame
; paths; all six are independent of NUSIZ pairing (initial X=16,36,56,76,96,116).
; First candidate A multiplex: P1 renders exactly one of six NPC per frame
; using ORIGINAL, unmodified 8x9 masks. P0 yellow player; M0 test projectile.
; Expected 1/6 duty cycle on P1: unacceptable until real Stella is measured.
; This NEGATIVE diagnostic must not count as a graphics PASS.
 processor 6502
VSYNC   = $00
VBLANK  = $01
WSYNC   = $02
NUSIZ0  = $04
NUSIZ1  = $05
COLUP0  = $06
COLUP1  = $07
COLUPF  = $08
COLUBK  = $09
CTRLPF  = $0A
PF0     = $0D
PF1     = $0E
PF2     = $0F
RESP0   = $10
RESP1   = $11
RESM0   = $12
GRP0    = $1B
GRP1    = $1C
ENAM0   = $1D
HMP0    = $20
HMP1    = $21
HMM0    = $22
HMOVE   = $2A
HMCLR   = $2B
FRAMELO = $80
FRAMEHI = $81
NPCPHASE = $82
SELID    = $83
SELX     = $84
NPCPTRLO = $85
NPCPTRHI = $86
PLAYERX  = $87
SHOTX    = $88
NPCX0   = $90
NPCX1   = $91
NPCX2   = $92
NPCX3   = $93
NPCX4   = $94
NPCX5   = $95
 ORG $F000
Reset:
 SEI
 CLD
 LDX #$FF
 TXS
 LDX #$1F
 LDA #0
ClearRam:
 STA $80,X
 DEX
 BPL ClearRam
 LDA #$10
 STA NUSIZ0
 LDA #0
 STA NUSIZ1
 STA GRP0
 STA GRP1
 STA ENAM0
 STA PF0
 STA PF1
 STA PF2
 STA CTRLPF
 STA HMCLR
 LDA #$1E
 STA COLUP0
 LDA #$0E
 STA COLUP1
 LDA #0
 STA COLUBK
 LDA #145
 STA PLAYERX
 LDA #154
 STA SHOTX
 LDA #2
 STA VBLANK
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
 ; VBLANK line3: update six separate X bytes, each from a distinct path.
 LDA FRAMELO
 AND #$1F
 TAY
 LDA Path0,Y
 STA NPCX0
 LDA Path1,Y
 STA NPCX1
 LDA Path2,Y
 STA NPCX2
 LDA Path3,Y
 STA NPCX3
 LDA Path4,Y
 STA NPCX4
 LDA Path5,Y
 STA NPCX5
 STA WSYNC
 ; VBLANK line4: choose ONE P1 sprite for THIS frame, never claim six shown.
 LDX NPCPHASE
 STX SELID
 LDA NPCX0,X
 STA SELX
 LDA PtrLo,X
 STA NPCPTRLO
 LDA PtrHi,X
 STA NPCPTRHI
 INC NPCPHASE
 LDA NPCPHASE
 CMP #6
 BCC PhaseReady
 LDA #0
 STA NPCPHASE
PhaseReady:
 STA WSYNC
 ; VBLANK line5: position the permanently visible player P0.
 LDX #12
PositionPlayer:
 DEX
 BNE PositionPlayer
 STA RESP0
 STA WSYNC
 ; VBLANK line6: position M0 test projectile separately from NPCs.
 LDX #14
PositionShot:
 DEX
 BNE PositionShot
 STA RESM0
 STA WSYNC
 ; VBLANK line7: exact coarse+fine X for the selected white P1 NPC.
 LDA SELX
 LDX #1
 JSR SetHorizPos
 STA WSYNC
 ; VBLANK line8: apply fine motion, player/shot HMP=0 by reset.
 STA HMOVE
 ; Correct frame accounting: 30 WSYNC after HMOVE = 262 total lines.
 ; First Stella run measured 263, traced to an extra VBLANK WSYNC.
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
 ; All six logical NPCs share this y band, but A displays 1/6 per frame.
 LDY #8
SpriteLine:
 STA WSYNC
 LDA (NPCPTRLO),Y
 STA GRP1
 LDA PlayerRows,Y
 STA GRP0
 LDA ShotRows,Y
 STA ENAM0
 DEY
 BPL SpriteLine
 STA WSYNC
 LDA #0
 STA GRP0
 STA GRP1
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
 BNE FrameNumberReady
 INC FRAMEHI
FrameNumberReady:
 JMP Frame
; Horizontal fine+coarse placement in VBLANK only.
; Based on standard documented 6502 TIA position idiom; initial frame X
; values are rendered with real RESP1/HMP1/HMOVE, NOT NUSIZ copies.
; A=desired color-clock x coordinate, X=object (1=P1).
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
 ORG $F200
MaleRows:
 BYTE $42,$42,$24,$24,$18,$FF,$18,$3C,$3C
FemaleRows:
 BYTE $24,$24,$7E,$7E,$3C,$FF,$18,$3C,$3C
SmallMaleRows:
 BYTE $00,$24,$18,$7E,$18,$3C,$3C,$00,$00
SmallFemaleRows:
 BYTE $00,$24,$3C,$7E,$18,$3C,$3C,$00,$00
PlayerRows:
 BYTE $42,$24,$18,$3C,$1E,$7E,$18,$7E,$3C
ShotRows:
 BYTE $00,$00,$00,$00,$02,$00,$00,$00,$00
PtrLo:
 BYTE <MaleRows,<MaleRows,<FemaleRows,<FemaleRows,<SmallMaleRows,<SmallFemaleRows
PtrHi:
 BYTE >MaleRows,>MaleRows,>FemaleRows,>FemaleRows,>SmallMaleRows,>SmallFemaleRows
; 6 independently defined deterministic X paths, each table aligned to
; same 256-byte page to avoid absolute-indexed page-cross in VBLANK update.
 ORG $F300
Path0:
 BYTE $10,$11,$12,$13,$14,$13,$12,$11,$10,$0F,$0E,$0D,$0C,$0D,$0E,$0F
 BYTE $11,$12,$13,$14,$15,$14,$13,$12,$11,$10,$0F,$0E,$0D,$0E,$0F,$10
Path1:
 BYTE $24,$24,$22,$22,$20,$20,$1E,$1E,$20,$20,$22,$22,$24,$24,$26,$26
 BYTE $23,$23,$21,$21,$1F,$1F,$1D,$1D,$1F,$1F,$21,$21,$23,$23,$25,$25
Path2:
 BYTE $38,$39,$38,$3A,$38,$3B,$38,$3C,$38,$3D,$38,$3C,$38,$3B,$38,$3A
 BYTE $39,$3A,$39,$3B,$39,$3C,$39,$3D,$39,$3E,$39,$3D,$39,$3C,$39,$3B
Path3:
 BYTE $4C,$4B,$4A,$4B,$4C,$4D,$4E,$4D,$4C,$4A,$48,$4A,$4C,$4E,$50,$4E
 BYTE $4B,$4A,$49,$4A,$4B,$4C,$4D,$4C,$4B,$49,$47,$49,$4B,$4D,$4F,$4D
Path4:
 BYTE $60,$60,$60,$61,$61,$61,$62,$62,$62,$61,$61,$60,$60,$5F,$5F,$5E
 BYTE $61,$61,$61,$62,$62,$62,$63,$63,$63,$62,$62,$61,$61,$60,$60,$5F
Path5:
 BYTE $74,$76,$78,$7A,$7C,$7A,$78,$76,$74,$72,$70,$6E,$6C,$6E,$70,$72
 BYTE $73,$75,$77,$79,$7B,$79,$77,$75,$73,$71,$6F,$6D,$6B,$6D,$6F,$71
 ORG $FFFA
 WORD Reset
 WORD Reset
 WORD Reset
