PlanSmallOverlap:
 lda Shot
 ora KeyState
 bne RejectCap
 lda Rendered
 cmp #15
 bne RejectCap
 lda Life+3
 and Life+4
 bpl RejectCap
 lda NY+3
 cmp #78
 bcc RejectCap
 cmp #89
 bcs RejectCap
 adc #4               ; C clear after the guard
 cmp NY+4
 bne RejectCap
 jmp CheckCapX
RejectCap:
 rts
