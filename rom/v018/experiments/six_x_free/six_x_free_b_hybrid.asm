; LET ME OUT! v0.18 / SEX_X_FREE R1 diagnostic, 6502 source for DASM.
; USER-AUTHORIZED TEST ONLY. It is NOT a valid full R1 renderer.
; Six logical X coordinates in RIOT $90-$95 with six distinct 32-frame
; paths; all six are independent of NUSIZ pairing (initial X=16,36,56,76,96,116).
; Candidate B hybrid: PF coarse representations of ALL six requested X positions,
; plus P1 displaying one exact ORIGINAL mask at a time, P0 yellow player,
; M0 short vertical shot marker. PF bits are 4 color clocks wide, so mask
; fidelity CANNOT equal the 8x9 source. Quantify in real Stella; NOT R1 PASS.
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
PFPTRLO  = $89
PFPTRHI  = $8A
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
 ; VBLANK: precomputed 54 PF bytes for all six independent X paths.
 ; Eleven fixed WSYNC lines, five byte transfers per line (<=65 cycles).
 LDA FRAMELO
 AND #$1F
 TAX
 LDA PFScenePtrLo,X
 STA PFPTRLO
 LDA PFScenePtrHi,X
 STA PFPTRHI
 LDY #53
 STA WSYNC
 LDA (PFPTRLO),Y
 STA $00A0,Y
 DEY
 LDA (PFPTRLO),Y
 STA $00A0,Y
 DEY
 LDA (PFPTRLO),Y
 STA $00A0,Y
 DEY
 LDA (PFPTRLO),Y
 STA $00A0,Y
 DEY
 LDA (PFPTRLO),Y
 STA $00A0,Y
 DEY
 STA WSYNC
 LDA (PFPTRLO),Y
 STA $00A0,Y
 DEY
 LDA (PFPTRLO),Y
 STA $00A0,Y
 DEY
 LDA (PFPTRLO),Y
 STA $00A0,Y
 DEY
 LDA (PFPTRLO),Y
 STA $00A0,Y
 DEY
 LDA (PFPTRLO),Y
 STA $00A0,Y
 DEY
 STA WSYNC
 LDA (PFPTRLO),Y
 STA $00A0,Y
 DEY
 LDA (PFPTRLO),Y
 STA $00A0,Y
 DEY
 LDA (PFPTRLO),Y
 STA $00A0,Y
 DEY
 LDA (PFPTRLO),Y
 STA $00A0,Y
 DEY
 LDA (PFPTRLO),Y
 STA $00A0,Y
 DEY
 STA WSYNC
 LDA (PFPTRLO),Y
 STA $00A0,Y
 DEY
 LDA (PFPTRLO),Y
 STA $00A0,Y
 DEY
 LDA (PFPTRLO),Y
 STA $00A0,Y
 DEY
 LDA (PFPTRLO),Y
 STA $00A0,Y
 DEY
 LDA (PFPTRLO),Y
 STA $00A0,Y
 DEY
 STA WSYNC
 LDA (PFPTRLO),Y
 STA $00A0,Y
 DEY
 LDA (PFPTRLO),Y
 STA $00A0,Y
 DEY
 LDA (PFPTRLO),Y
 STA $00A0,Y
 DEY
 LDA (PFPTRLO),Y
 STA $00A0,Y
 DEY
 LDA (PFPTRLO),Y
 STA $00A0,Y
 DEY
 STA WSYNC
 LDA (PFPTRLO),Y
 STA $00A0,Y
 DEY
 LDA (PFPTRLO),Y
 STA $00A0,Y
 DEY
 LDA (PFPTRLO),Y
 STA $00A0,Y
 DEY
 LDA (PFPTRLO),Y
 STA $00A0,Y
 DEY
 LDA (PFPTRLO),Y
 STA $00A0,Y
 DEY
 STA WSYNC
 LDA (PFPTRLO),Y
 STA $00A0,Y
 DEY
 LDA (PFPTRLO),Y
 STA $00A0,Y
 DEY
 LDA (PFPTRLO),Y
 STA $00A0,Y
 DEY
 LDA (PFPTRLO),Y
 STA $00A0,Y
 DEY
 LDA (PFPTRLO),Y
 STA $00A0,Y
 DEY
 STA WSYNC
 LDA (PFPTRLO),Y
 STA $00A0,Y
 DEY
 LDA (PFPTRLO),Y
 STA $00A0,Y
 DEY
 LDA (PFPTRLO),Y
 STA $00A0,Y
 DEY
 LDA (PFPTRLO),Y
 STA $00A0,Y
 DEY
 LDA (PFPTRLO),Y
 STA $00A0,Y
 DEY
 STA WSYNC
 LDA (PFPTRLO),Y
 STA $00A0,Y
 DEY
 LDA (PFPTRLO),Y
 STA $00A0,Y
 DEY
 LDA (PFPTRLO),Y
 STA $00A0,Y
 DEY
 LDA (PFPTRLO),Y
 STA $00A0,Y
 DEY
 LDA (PFPTRLO),Y
 STA $00A0,Y
 DEY
 STA WSYNC
 LDA (PFPTRLO),Y
 STA $00A0,Y
 DEY
 LDA (PFPTRLO),Y
 STA $00A0,Y
 DEY
 LDA (PFPTRLO),Y
 STA $00A0,Y
 DEY
 LDA (PFPTRLO),Y
 STA $00A0,Y
 DEY
 LDA (PFPTRLO),Y
 STA $00A0,Y
 DEY
 STA WSYNC
 LDA (PFPTRLO),Y
 STA $00A0,Y
 DEY
 LDA (PFPTRLO),Y
 STA $00A0,Y
 DEY
 LDA (PFPTRLO),Y
 STA $00A0,Y
 DEY
 LDA (PFPTRLO),Y
 STA $00A0,Y
 DEY
 STA WSYNC
 ; One WSYNC before copy, 11 copy WSYNC, 18 blanks = 30 total.
 LDX #18
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
 ; P1 and P0 preloaded one line before visible band. M0 is a
 ; 9-scanline test marker, NOT a full projectile implementation.
 LDY #8
 LDA (NPCPTRLO),Y
 STA GRP1
 LDA PlayerRows,Y
 STA GRP0
 LDA #2
 STA ENAM0
PfSpriteLine:
 STA WSYNC
 ; PF 4-color-clock silhouettes, six separate X (coarse, noncanonical).
 LDA $00A0,Y
 STA PF0
 LDA $00A9,Y
 STA PF1
 LDA $00B2,Y
 STA PF2
 LDA $00BB,Y
 STA PF0
 LDA $00C4,Y
 STA PF1
 LDA $00CD,Y
 STA PF2
 DEY
 BMI PfSpriteDone
 LDA (NPCPTRLO),Y
 STA GRP1
 LDA PlayerRows,Y
 STA GRP0
 JMP PfSpriteLine
PfSpriteDone:
 STA WSYNC
 LDA #0
 STA GRP0
 STA GRP1
 STA ENAM0
 STA PF0
 STA PF1
 STA PF2
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
 ORG $F500
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
 ORG $F560
PFScenePtrLo:
 BYTE <PFScene0,<PFScene1,<PFScene2,<PFScene3,<PFScene4,<PFScene5,<PFScene6,<PFScene7,<PFScene8,<PFScene9,<PFScene10,<PFScene11,<PFScene12,<PFScene13,<PFScene14,<PFScene15,<PFScene16,<PFScene17,<PFScene18,<PFScene19,<PFScene20,<PFScene21,<PFScene22,<PFScene23,<PFScene24,<PFScene25,<PFScene26,<PFScene27,<PFScene28,<PFScene29,<PFScene30,<PFScene31
PFScenePtrHi:
 BYTE >PFScene0,>PFScene1,>PFScene2,>PFScene3,>PFScene4,>PFScene5,>PFScene6,>PFScene7,>PFScene8,>PFScene9,>PFScene10,>PFScene11,>PFScene12,>PFScene13,>PFScene14,>PFScene15,>PFScene16,>PFScene17,>PFScene18,>PFScene19,>PFScene20,>PFScene21,>PFScene22,>PFScene23,>PFScene24,>PFScene25,>PFScene26,>PFScene27,>PFScene28,>PFScene29,>PFScene30,>PFScene31
 ORG $F600
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
 ORG $F700
PFScene0:
 BYTE $00,$00,$00,$00,$00,$00,$00,$00,$00
 BYTE $C6,$C6,$C6,$C6,$C6,$C6,$C6,$C6,$C6
 BYTE $8C,$8C,$8C,$8C,$8C,$8C,$8C,$8C,$8C
 BYTE $10,$10,$10,$10,$10,$10,$10,$10,$10
 BYTE $00,$C6,$C6,$C6,$C6,$C6,$C6,$00,$00
 BYTE $00,$00,$00,$00,$00,$00,$00,$00,$00
PFScene1:
 BYTE $00,$00,$00,$00,$00,$00,$00,$00,$00
 BYTE $C6,$C6,$C6,$C6,$46,$E6,$46,$C6,$C6
 BYTE $8C,$8C,$8C,$8C,$8C,$DC,$88,$8C,$8C
 BYTE $10,$10,$10,$10,$10,$10,$00,$10,$10
 BYTE $00,$C2,$C2,$C7,$C2,$C2,$C2,$00,$00
 BYTE $00,$00,$00,$00,$00,$00,$00,$00,$00
PFScene2:
 BYTE $00,$00,$00,$00,$00,$00,$00,$00,$00
 BYTE $AA,$AA,$44,$44,$44,$EE,$44,$44,$44
 BYTE $8C,$8C,$CC,$CC,$8C,$CC,$8C,$8C,$8C
 BYTE $00,$00,$10,$10,$00,$10,$00,$00,$00
 BYTE $00,$C3,$C3,$C3,$C3,$C3,$C3,$00,$00
 BYTE $00,$00,$00,$00,$00,$00,$00,$00,$00
PFScene3:
 BYTE $00,$00,$00,$00,$00,$00,$00,$00,$00
 BYTE $6A,$6A,$64,$64,$44,$EE,$44,$64,$64
 BYTE $88,$88,$9C,$9C,$88,$DC,$88,$88,$88
 BYTE $10,$10,$10,$10,$10,$10,$00,$10,$10
 BYTE $00,$C1,$41,$C3,$41,$C1,$C1,$00,$00
 BYTE $00,$00,$00,$01,$00,$00,$00,$00,$00
PFScene4:
 BYTE $00,$00,$00,$00,$00,$00,$00,$00,$00
 BYTE $6C,$6C,$6C,$6C,$6C,$6C,$6C,$6C,$6C
 BYTE $8C,$8C,$8C,$8C,$8C,$8C,$8C,$8C,$8C
 BYTE $10,$10,$10,$10,$10,$10,$10,$10,$10
 BYTE $00,$C1,$41,$C1,$41,$C1,$C1,$00,$00
 BYTE $00,$01,$01,$01,$01,$01,$01,$00,$00
PFScene5:
 BYTE $00,$00,$00,$00,$00,$00,$00,$00,$00
 BYTE $6C,$6C,$6C,$6C,$4C,$EC,$4C,$6C,$6C
 BYTE $98,$98,$98,$98,$98,$9C,$08,$98,$98
 BYTE $10,$10,$10,$10,$10,$30,$10,$10,$10
 BYTE $00,$C1,$41,$C3,$41,$C1,$C1,$00,$00
 BYTE $00,$00,$00,$01,$00,$00,$00,$00,$00
PFScene6:
 BYTE $00,$00,$00,$00,$00,$00,$00,$00,$00
 BYTE $B4,$B4,$48,$48,$48,$FC,$48,$48,$48
 BYTE $0C,$0C,$8C,$8C,$0C,$8C,$0C,$0C,$0C
 BYTE $10,$10,$30,$30,$10,$30,$10,$10,$10
 BYTE $00,$43,$43,$E3,$43,$43,$43,$00,$00
 BYTE $00,$00,$00,$00,$00,$00,$00,$00,$00
PFScene7:
 BYTE $00,$00,$00,$00,$00,$00,$00,$00,$00
 BYTE $D4,$D4,$C8,$C8,$48,$FC,$48,$C8,$C8
 BYTE $98,$98,$98,$98,$98,$98,$18,$98,$98
 BYTE $10,$10,$10,$10,$10,$30,$10,$10,$10
 BYTE $00,$42,$42,$E7,$42,$42,$42,$00,$00
 BYTE $00,$00,$00,$00,$00,$00,$00,$00,$00
PFScene8:
 BYTE $00,$00,$00,$00,$00,$00,$00,$00,$00
 BYTE $CC,$CC,$CC,$CC,$CC,$CC,$CC,$CC,$CC
 BYTE $8C,$8C,$8C,$8C,$8C,$8C,$8C,$8C,$8C
 BYTE $10,$10,$10,$10,$10,$10,$10,$10,$10
 BYTE $00,$46,$46,$E6,$46,$46,$46,$00,$00
 BYTE $00,$00,$00,$00,$00,$00,$00,$00,$00
PFScene9:
 BYTE $00,$00,$00,$00,$00,$80,$00,$00,$00
 BYTE $CC,$CC,$CC,$CC,$8C,$CC,$8C,$CC,$CC
 BYTE $98,$98,$D8,$D8,$98,$F8,$90,$98,$98
 BYTE $00,$00,$10,$10,$00,$10,$00,$00,$00
 BYTE $00,$C4,$44,$CE,$44,$C4,$C4,$00,$00
 BYTE $00,$00,$00,$00,$00,$00,$00,$00,$00
PFScene10:
 BYTE $80,$80,$00,$00,$00,$80,$00,$00,$00
 BYTE $4A,$4A,$84,$84,$84,$CE,$84,$84,$84
 BYTE $CC,$CC,$CC,$CC,$CC,$CC,$CC,$CC,$CC
 BYTE $00,$00,$00,$00,$00,$00,$00,$00,$00
 BYTE $00,$CC,$4C,$CC,$4C,$CC,$CC,$00,$00
 BYTE $00,$00,$00,$00,$00,$00,$00,$00,$00
PFScene11:
 BYTE $80,$80,$80,$80,$00,$80,$00,$80,$80
 BYTE $8A,$8A,$84,$84,$84,$CE,$84,$84,$84
 BYTE $98,$98,$D8,$D8,$98,$D8,$98,$98,$98
 BYTE $00,$00,$10,$10,$00,$10,$00,$00,$00
 BYTE $00,$C8,$C8,$DC,$C8,$C8,$C8,$00,$00
 BYTE $00,$00,$00,$00,$00,$00,$00,$00,$00
PFScene12:
 BYTE $80,$80,$80,$80,$80,$80,$80,$80,$80
 BYTE $86,$86,$86,$86,$86,$86,$86,$86,$86
 BYTE $8C,$8C,$8C,$8C,$8C,$8C,$8C,$8C,$8C
 BYTE $10,$10,$10,$10,$10,$10,$10,$10,$10
 BYTE $00,$D8,$D8,$D8,$D8,$D8,$D8,$00,$00
 BYTE $00,$00,$00,$00,$00,$00,$00,$00,$00
PFScene13:
 BYTE $80,$80,$80,$80,$00,$80,$00,$80,$80
 BYTE $86,$86,$86,$86,$86,$C6,$86,$86,$86
 BYTE $18,$18,$98,$98,$18,$9C,$08,$18,$18
 BYTE $10,$10,$30,$30,$10,$30,$10,$10,$10
 BYTE $00,$C8,$88,$DC,$88,$C8,$C8,$00,$00
 BYTE $00,$00,$00,$00,$00,$00,$00,$00,$00
PFScene14:
 BYTE $80,$80,$00,$00,$00,$80,$00,$00,$00
 BYTE $45,$45,$82,$82,$82,$C7,$82,$82,$82
 BYTE $0C,$0C,$0C,$0C,$0C,$0C,$0C,$0C,$0C
 BYTE $30,$30,$30,$30,$30,$30,$30,$30,$30
 BYTE $00,$CC,$8C,$CC,$8C,$CC,$CC,$00,$00
 BYTE $00,$00,$00,$00,$00,$00,$00,$00,$00
PFScene15:
 BYTE $00,$00,$00,$00,$00,$80,$00,$00,$00
 BYTE $C5,$C5,$C2,$C2,$82,$C7,$82,$C2,$C2
 BYTE $08,$08,$9C,$9C,$08,$9C,$08,$08,$08
 BYTE $10,$10,$30,$B0,$10,$30,$10,$10,$10
 BYTE $00,$84,$84,$CE,$84,$84,$84,$00,$00
 BYTE $00,$00,$00,$00,$00,$00,$00,$00,$00
PFScene16:
 BYTE $00,$00,$00,$00,$00,$00,$00,$00,$00
 BYTE $C6,$C6,$C6,$C6,$44,$EE,$44,$C6,$C6
 BYTE $8C,$8C,$8C,$8C,$8C,$DC,$88,$8C,$8C
 BYTE $10,$10,$10,$10,$10,$10,$00,$10,$10
 BYTE $00,$C6,$46,$C6,$44,$C6,$C6,$00,$00
 BYTE $00,$00,$00,$00,$00,$00,$00,$00,$00
PFScene17:
 BYTE $00,$00,$00,$00,$00,$00,$00,$00,$00
 BYTE $A6,$A6,$46,$46,$44,$EE,$44,$46,$46
 BYTE $88,$88,$DC,$DC,$88,$DC,$88,$88,$88
 BYTE $00,$00,$10,$10,$00,$10,$00,$00,$00
 BYTE $00,$C6,$46,$C6,$42,$C6,$C6,$00,$00
 BYTE $00,$00,$00,$00,$00,$00,$00,$00,$00
PFScene18:
 BYTE $00,$00,$00,$00,$00,$00,$00,$00,$00
 BYTE $6C,$6C,$6C,$6C,$44,$EE,$44,$6C,$6C
 BYTE $CC,$CC,$CC,$CC,$CC,$DC,$88,$CC,$CC
 BYTE $00,$00,$00,$00,$00,$10,$00,$00,$00
 BYTE $00,$C3,$43,$C3,$42,$C3,$C3,$00,$00
 BYTE $00,$00,$00,$00,$00,$00,$00,$00,$00
PFScene19:
 BYTE $00,$00,$00,$00,$00,$00,$00,$00,$00
 BYTE $6C,$6C,$6C,$6C,$64,$6E,$64,$6C,$6C
 BYTE $98,$98,$D8,$D8,$98,$DC,$88,$98,$98
 BYTE $00,$00,$10,$10,$00,$10,$00,$00,$00
 BYTE $00,$43,$43,$E3,$41,$43,$43,$00,$00
 BYTE $00,$00,$00,$00,$00,$00,$00,$00,$00
PFScene20:
 BYTE $00,$00,$00,$00,$00,$00,$00,$00,$00
 BYTE $6C,$6C,$6C,$6C,$28,$7C,$28,$6C,$6C
 BYTE $8C,$8C,$8C,$8C,$8C,$DC,$88,$8C,$8C
 BYTE $10,$10,$10,$10,$10,$10,$00,$10,$10
 BYTE $00,$41,$41,$E1,$41,$41,$41,$00,$00
 BYTE $00,$01,$01,$01,$00,$01,$01,$00,$00
PFScene21:
 BYTE $00,$00,$00,$00,$00,$00,$00,$00,$00
 BYTE $6C,$6C,$6C,$6C,$68,$7C,$68,$6C,$6C
 BYTE $98,$98,$98,$98,$98,$98,$98,$98,$98
 BYTE $10,$10,$10,$10,$10,$10,$10,$10,$10
 BYTE $00,$43,$43,$E3,$41,$43,$43,$00,$00
 BYTE $00,$00,$00,$00,$00,$00,$00,$00,$00
PFScene22:
 BYTE $00,$00,$00,$00,$00,$00,$00,$00,$00
 BYTE $78,$78,$78,$78,$48,$FC,$48,$78,$78
 BYTE $8C,$8C,$8C,$8C,$8C,$9C,$08,$8C,$8C
 BYTE $10,$10,$10,$10,$10,$30,$10,$10,$10
 BYTE $00,$63,$43,$63,$42,$63,$63,$00,$00
 BYTE $00,$00,$00,$00,$00,$00,$00,$00,$00
PFScene23:
 BYTE $00,$00,$00,$00,$00,$00,$00,$00,$00
 BYTE $B8,$B8,$58,$58,$48,$FC,$48,$58,$58
 BYTE $98,$98,$98,$98,$98,$B8,$90,$98,$98
 BYTE $10,$10,$10,$10,$10,$10,$10,$10,$10
 BYTE $00,$66,$46,$66,$42,$66,$66,$00,$00
 BYTE $00,$00,$00,$00,$00,$00,$00,$00,$00
PFScene24:
 BYTE $00,$00,$00,$00,$00,$00,$00,$00,$00
 BYTE $CC,$CC,$CC,$CC,$48,$FC,$48,$CC,$CC
 BYTE $8C,$8C,$8C,$8C,$8C,$DC,$88,$8C,$8C
 BYTE $10,$10,$10,$10,$10,$10,$00,$10,$10
 BYTE $00,$66,$46,$66,$44,$66,$66,$00,$00
 BYTE $00,$00,$00,$00,$00,$00,$00,$00,$00
PFScene25:
 BYTE $00,$00,$00,$00,$00,$00,$00,$00,$00
 BYTE $CC,$CC,$CC,$CC,$C8,$DC,$C8,$CC,$CC
 BYTE $D0,$D0,$F8,$F8,$D0,$F8,$90,$D0,$D0
 BYTE $00,$00,$00,$00,$00,$10,$00,$00,$00
 BYTE $00,$4C,$4C,$EC,$44,$4C,$4C,$00,$00
 BYTE $00,$00,$00,$00,$00,$00,$00,$00,$00
PFScene26:
 BYTE $00,$00,$00,$00,$00,$80,$00,$00,$00
 BYTE $CC,$CC,$CC,$CC,$84,$CE,$84,$CC,$CC
 BYTE $CC,$CC,$CC,$CC,$CC,$FC,$48,$CC,$CC
 BYTE $00,$00,$00,$00,$00,$00,$00,$00,$00
 BYTE $00,$4C,$4C,$EC,$48,$4C,$4C,$00,$00
 BYTE $00,$00,$00,$00,$00,$00,$00,$00,$00
PFScene27:
 BYTE $80,$80,$00,$00,$00,$80,$00,$00,$00
 BYTE $4C,$4C,$8C,$8C,$84,$CE,$84,$8C,$8C
 BYTE $D8,$D8,$D8,$D8,$D8,$F8,$90,$D8,$D8
 BYTE $00,$00,$00,$00,$00,$10,$00,$00,$00
 BYTE $00,$D8,$58,$D8,$48,$D8,$D8,$00,$00
 BYTE $00,$00,$00,$00,$00,$00,$00,$00,$00
PFScene28:
 BYTE $80,$80,$80,$80,$00,$80,$00,$80,$80
 BYTE $86,$86,$86,$86,$84,$CE,$84,$86,$86
 BYTE $8C,$8C,$8C,$8C,$8C,$DC,$88,$8C,$8C
 BYTE $10,$10,$10,$10,$10,$10,$00,$10,$10
 BYTE $00,$D8,$58,$D8,$50,$D8,$D8,$00,$00
 BYTE $00,$00,$00,$00,$00,$00,$00,$00,$00
PFScene29:
 BYTE $80,$80,$00,$00,$00,$80,$00,$00,$00
 BYTE $46,$46,$86,$86,$84,$CE,$84,$86,$86
 BYTE $98,$98,$98,$98,$98,$98,$18,$98,$98
 BYTE $10,$10,$10,$10,$10,$30,$10,$10,$10
 BYTE $00,$D8,$D8,$D8,$C8,$D8,$D8,$00,$00
 BYTE $00,$00,$00,$00,$00,$00,$00,$00,$00
PFScene30:
 BYTE $00,$00,$00,$00,$00,$80,$00,$00,$00
 BYTE $C6,$C6,$C6,$C6,$82,$C7,$82,$C6,$C6
 BYTE $0C,$0C,$0C,$0C,$0C,$9C,$08,$0C,$0C
 BYTE $30,$30,$30,$30,$30,$30,$10,$30,$30
 BYTE $00,$CC,$CC,$CC,$C8,$CC,$CC,$00,$00
 BYTE $00,$00,$00,$00,$00,$00,$00,$00,$00
PFScene31:
 BYTE $00,$00,$00,$00,$00,$00,$00,$00,$00
 BYTE $C6,$C6,$C6,$C6,$C2,$C7,$C2,$C6,$C6
 BYTE $98,$98,$98,$98,$98,$9C,$08,$98,$98
 BYTE $10,$10,$10,$10,$10,$30,$10,$10,$10
 BYTE $00,$CC,$8C,$CC,$84,$CC,$CC,$00,$00
 BYTE $00,$00,$00,$00,$00,$00,$00,$00,$00
 ORG $FFFA
 WORD Reset
 WORD Reset
 WORD Reset
