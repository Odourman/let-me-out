; One independent missile supplies a part of F while P1 retains its mask.
; Fixed diagnostic position corresponding to F at X68/Y86.
ParkCrowdMissile:
 lda #68
 ldx #3
 jmp Position
RetriggerPair:
 lda #$20
 sta NUSIZ1
 lda MissileRows-166,y
 sta ENAM1
 lda (P0Ptr),y
 sta GRP0
 lda (P1Ptr),y
 sta GRP1
 iny
 jmp NextRoom
MissileRows:
 byte 2,2,2,2,2,2,2,2,0
