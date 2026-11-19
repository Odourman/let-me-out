ScheduleAssist:
 lda KeyState
 cmp #1
 beq AssistRejectLocal
 lda #129
 ldx PY
 cpx #61
 bcs AssistLower
 lda #69
 bne AssistSetSplit
AssistLower:
 cpx #135
 bcs AssistSetSplit
 lda #136
 cpx #110
 bcc AssistSetSplit
 lda #104
AssistSetSplit:
 sta SplitY
 sec
 sbc #8
 sta SplitLow
 adc #13
 sta SplitHigh
 ldx #4
AssistCheckStrip:
 lda Life,x
 beq AssistContinueLocal
 lda NY,x
 cmp SplitLow
 bcc AssistContinueLocal
 cmp SplitHigh
 bcc AssistRejectLocal
AssistContinueLocal:
 jmp AssistNextStrip
AssistRejectLocal:
 rts
