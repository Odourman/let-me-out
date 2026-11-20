; Plan the OFF frame before the planner's initial WSYNC.
BlinkPrepare:
 sta TIM64T
 lda FrameClock
 cmp #BLINK_ON
 bcc BlinkDone
 lda KeyState
 cmp #1
 bne BlinkDone
 ; The renderer treats this sentinel as a non-floor state.
 lda #$81
 sta KeyState
BlinkDone:
 rts

; An even modulus preserves parity, the logic bank's only use of FrameClock.
BlinkFinish:
 inc FrameClock
 lda FrameClock
 cmp #12
 bcc BlinkNextFrame
 lda #0
 sta FrameClock
BlinkNextFrame:
 jmp GameBank
