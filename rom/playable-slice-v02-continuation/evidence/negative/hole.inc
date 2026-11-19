PositionHole:
 ldy #13
HolePosition:
 dey
 bne HolePosition
 sta RESM1
 rts
HoleLine:
 lda #$26
 sta COLUPF
 lda (P0Ptr),y
 sta GRP0
 lda (P1Ptr),y
 sta GRP1
 lda DoorColor
 sta COLUPF
 lda #0
 sta COLUP1
 lda #2
 sta ENAM1
 iny
 jmp NextRoom
BridgePreSync:
 sta WSYNC
 lda BridgeOld
 sta GRP1
 lda BridgeX
 bit BridgeX
 jmp NpcSetupFirst       ; 15 cycles elapsed, three coarse iterations saved
