; Diagnostic only. Active shot is outside this probe's matrix.
ParkKeyObjects:
 lda #86
 ldx #2
 jsr Position
 lda #86
 ldx #4
 jmp Position
BallKeyRow:
 lda (P0Ptr),y
 sta GRP0
 lda (P1Ptr),y
 sta GRP1
 lda #$11
 sta CTRLPF
 lda #$10
 sta NUSIZ0
 lda #2
BallEnable:
 sta $1f
 sta ENAM0
 lda #$1a
BallGold:
 sta COLUPF
MissileGold:
 sta COLUP0
 nop
 lda #0
 sta $1f
 sta ENAM0
 sta NUSIZ0
 lda #$26
BallBrown:
 sta COLUPF
 lda #$1e
 sta COLUP0
 iny
 jmp NextRoom
