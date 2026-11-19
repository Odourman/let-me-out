ParkDoorMissile:
 sta WSYNC
 ldy #14
ParkDoorDelay:
 dey
 bne ParkDoorDelay
 sta RESM1
 lda #$10
 sta HMM1
 sta WSYNC
 sta HMOVE
 sta WSYNC
 sta HMCLR
 rts

DoorCutoutProbe:
 cmp #$43
 beq CutoutExit
 ; This bounded test omits the normal P0/M0 work to isolate M1.
 and #1
 asl
 asl
 asl
 asl
 sta NUSIZ1
 lda (P1Ptr),y
 sta GRP1
 lda #0
 sta COLUP1
 lda #2
 sta ENAM1
CutoutColor:
 lda DoorColor
 sta COLUPF
 iny
 jmp RoomQueueCheck
CutoutExit:
 lda #0
 sta ENAM1
 lda #$0e
 sta COLUP1
 jmp CutoutColor
