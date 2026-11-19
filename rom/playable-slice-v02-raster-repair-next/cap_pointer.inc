FinishCapPointer:
 sec
 lda #<(Mask3-80)
 sbc NY+4
 sta QueueLo+3
 lda #>(Mask3-80)
 sbc #0
 sta QueueHi+3
 lda Rendered
 ora #16
 sta Rendered
 inc SortI
 rts
