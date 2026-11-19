ParkDoorM1:
 sta WSYNC
 ldy #14
ParkDoorM1Wait:
 dey
 bne ParkDoorM1Wait
 sta RESM1
 lda #$10
 sta NUSIZ1
 rts
DoorStencil:
 lda #$26
 sta COLUPF
 lda (P1Ptr),y
 sta GRP1
 lda DoorColor
 sta COLUPF
 lda #0
 sta COLUP1
 lda #2
 sta ENAM1
 jmp RoomTail
