CheckCapX:
 lda PY
 cmp #60
 bcc RejectCapX
 lda NX+4
 cmp #72
 bcc RejectCapX
 cmp #79
 bcs RejectCapX
 jmp CheckCapPlayer
RejectCapX:
 rts

InsertCap:
 lda QueueY+3
 sta QueueY+4
 lda QueueX+3
 sta QueueX+4
 lda QueueColor+3
 sta QueueColor+4
 lda QueueLo+3
 sta QueueLo+4
 lda QueueHi+3
 sta QueueHi+4
 lda QueueFirst+3
 sta QueueFirst+4
 jmp FinishCapSlot
