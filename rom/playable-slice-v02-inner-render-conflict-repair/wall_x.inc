EncodeWallX:
 lda QueueX,x
 sec
 sbc #66
 cmp #16
 bcs EncodeFarWallX
 adc #7
 and #15
 clc
 rts
EncodeFarWallX:
 jmp EncodeNearLeft
