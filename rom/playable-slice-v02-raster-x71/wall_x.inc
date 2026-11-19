EncodeWallX:
 lda QueueX,x
 sec
 sbc #66
 cmp #9
 bcs CheckUpperWallX
 adc #7
 clc
 rts
CheckUpperWallX:
 lda QueueX,x
 sec
 sbc #75
 cmp #7
 rts
