; Let Me Out! v0.18 scoped sprite multiplex FEASIBILITY proof (NOT R1).
; Author-written 6502, original approved NPC 8x9 bitmaps are unchanged.
; Experimental variant B: two NUSIZ1 copies, different GRP1 data between them.
; F6 cart assembled from this identical 4096-byte bank repeated x4.
; Test configuration: P0=yellow 9px-tall player, P1=male + female retrigger,
; M0=test projectile. NUSIZ1=2 (32px) or 4 (64px), P1 positioned in VBLANK.
; IMPORTANT: fixed NUSIZ separations are a diagnostic limitation, NOT approved R1.
; 76 cycles/line; exact kernel cycle analysis in README.md.
 processor 6502
VSYNC   = $00
VBLANK  = $01
WSYNC   = $02
NUSIZ0  = $04
NUSIZ1  = $05
COLUP0  = $06
COLUP1  = $07
COLUBK  = $09
CTRLPF  = $0A
PF0     = $0D
PF1     = $0E
PF2     = $0F
RESP0   = $10
RESP1   = $11
RESM0   = $12
ENAM0   = $1D
GRP0    = $1B
GRP1    = $1C
FRAMELO = $80
DELAY   = $81
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
 STA CTRLPF
 STA NUSIZ1
 LDA #$10       ; 2 color-clock missile width, single P0 copy
 STA NUSIZ0
 LDA #$1E       ; NTSC yellow player
 STA COLUP0
 LDA #$0E       ; white NPCs
 STA COLUP1
 LDA #0
 STA COLUBK
Frame:
 LDA #2
 STA VSYNC
 STA WSYNC      ; VSYNC scanline 0
 STA WSYNC      ; VSYNC scanline 1
 STA WSYNC      ; VSYNC scanline 2
 LDA #0
 STA VSYNC
 LDA #2
 STA VBLANK
 INC FRAMELO
 LDA FRAMELO
 AND #$40
 BEQ Near
 LDA #6
 STA DELAY
 LDA #4        ; two copies 64 color clocks apart
 JMP SetSize
Near:
 LDA #4
 STA DELAY
 LDA #2        ; two copies 32 color clocks apart
SetSize:
 STA NUSIZ1
 LDA #0
 STA GRP0
 STA GRP1
 STA ENAM0
 STA WSYNC      ; VBLANK line 3, setup
 ; Position P0 approximately mid-screen once per frame.
 LDX #12
PlayerDelay:
 DEX
 BNE PlayerDelay
 STA RESP0
 STA WSYNC      ; VBLANK line 4
 ; Position M0 at right edge for one scanline test projectile.
 LDX #13
MissileDelay:
 DEX
 BNE MissileDelay
 STA RESM0
 STA WSYNC      ; VBLANK line 5
 ; Set P1 coarse position in VBLANK, near X=35.
 LDX #6
NpcPositionDelay:
 DEX
 BNE NpcPositionDelay
 STA RESP1
 STA WSYNC      ; VBLANK line 6
 ; Remaining VBLANK 33 lines -> scanline 40
 LDX #33
VerticalBlank:
 STA WSYNC
 DEX
 BNE VerticalBlank
 ; NTSC visible scanlines 40..231 inclusive.
 LDA #0
 STA VBLANK
 LDX #80
TopBlank:
 STA WSYNC
 DEX
 BNE TopBlank
 ; 9 humanoid rows at one common raster height band
 LDY #8
SpriteLine:
 STA WSYNC
 LDA MaleRows,Y       ; 4 cycles (same ROM page, no crossings)
 STA GRP1             ; 3 -> c7
 LDA PlayerRows,Y     ; 4
 STA GRP0             ; 3 -> c14
 ; P1 is prepositioned; first NUSIZ copy uses MaleRows.
 LDX DELAY            ; 3 -> c17
SecondXDelay:
 DEX
 BNE SecondXDelay    ; 4/6 iterations, (5*N-1) cycles
 LDA FemaleRows,Y     ; 4
 STA GRP1             ; 3
 ; The later NUSIZ copy sees FemaleRows when its beam position arrives.
 LDA ShotRows,Y       ; 4
 STA ENAM0            ; 3
 DEY                  ; 2
 BPL SpriteLine       ; 3 taken / 2 not taken
 ; Worst taken-loop body = 65 cycles with DELAY=6.
 STA WSYNC            ; finish last drawing line
 LDA #0
 STA GRP0
 STA GRP1
 STA ENAM0
 LDX #102
BottomBlank:
 STA WSYNC
 DEX
 BNE BottomBlank
 ; Scanline 232 begins. 30 scanlines overscan.
 LDA #2
 STA VBLANK
 LDX #29
Overscan:
 STA WSYNC
 DEX
 BNE Overscan
 STA WSYNC
 JMP Frame
 ; Original masks, bottom-to-top because Y=8 down to zero.
 ORG $F200
MaleRows:
 BYTE $42,$42,$24,$24,$18,$FF,$18,$3C,$3C
FemaleRows:
 BYTE $24,$24,$7E,$7E,$3C,$FF,$18,$3C,$3C
 ; Unapproved temporary PLAYER candidate for measurement, not canonical pixel art.
 ; Yellow 8x9; top hat (3C,7E), arm/weapon stroke, body and legs.
PlayerRows:
 BYTE $42,$24,$18,$3C,$1E,$7E,$18,$7E,$3C
ShotRows:
 BYTE $00,$00,$00,$00,$02,$00,$00,$00,$00
 ORG $FFFA
 WORD Reset
 WORD Reset
 WORD Reset
