AppendBridge:
 sta QueueY,x
 lda QueueLo-1,x
 sta P1Ptr
 lda QueueHi-1,x
 sta P1Ptr+1
 lda (P1Ptr),y
 sta BridgeOld
 lda #0
 sta QueueX,x
 lda #KeyColor
 sta QueueColor,x
 lda #$70
 sta QueueFirst,x
 sec
 lda #<(KeyShape-80)
 sbc KeyY
 sta QueueLo,x
 lda #>(KeyShape-80)
 sbc #0
 sta QueueHi,x
 lda Rendered
 ora #32
 sta Rendered
 inc SortI
 rts
