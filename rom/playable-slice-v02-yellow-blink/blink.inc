; Use the spare clocks before the planner's initial WSYNC. The timer
; remains at its original beam position. The even modulus preserves
; parity, the logic bank's only use of FrameClock.
BlinkPrepare:
 lda FrameClock
 cmp #12
 bcc BlinkPhase
 lda #0
 sta FrameClock
BlinkPhase:
 cmp #BLINK_ON
 bcc BlinkPlan
 lda KeyState
 cmp #1
 bne BlinkPlan
 ; Scheduler-only sentinel, restored immediately after Schedule.
 lda #$81
 sta KeyState
BlinkPlan:
 sta WSYNC
 jsr PlanFrame
 jmp PositionFrame
