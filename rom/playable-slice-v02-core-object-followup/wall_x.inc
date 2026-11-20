EncodeWallX:
 lda QueueX,x
 sec
 sbc #66
 cmp #16
 bcs EncodeDone
 adc #7
 and #15
 clc
EncodeDone:
 rts
