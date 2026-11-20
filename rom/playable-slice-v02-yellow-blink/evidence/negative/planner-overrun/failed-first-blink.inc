; Phase is normalized before planning. Subtracting a multiple of 12
; leaves parity, the logic bank's only use of FrameClock, unchanged.
BlinkPrepare:
 lda FrameClock
 cmp #12
 bcc BlinkPhase
 sbc #12
 sta FrameClock
BlinkPhase:
 cmp #BLINK_ON
 bcc BlinkDone
 lda KeyState
 cmp #1
 bne BlinkDone
 ; Renderer-only sentinel. Schedule and bridge reject it as a floor key.
 lda #$81
 sta KeyState
BlinkDone:
 rts
BlinkRestore:
 lda KeyState
 and #$7f
 sta KeyState
 rts
