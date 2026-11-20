; Only the final P1 actor can bridge into a newly ready floor key. The
; candidate must have no lit overlap and RESP1 must clear its right edge.
BridgeFloorKey:
 lda KeyState
 cmp #1
 bne BridgeReject
 lda Rendered
 and #32
 bne BridgeReject
 ldx SortI
 beq BridgeReject
 ldy KeyY
 lda AllowedSetup,y
 cmp KeyY
 bne BridgeReject
 clc
 adc #4
 cmp OrderEnd
 bcc BridgeReject
 lda KeyX
 cmp #42
 bcc BridgeReject
 clc
 adc #3
 sec
 sbc QueueX-1,x
 cmp #20
 bcc BridgeReject
 lda QueueX-1,x
 cmp #23
 bcc BridgeReject
 lda KeyX
 sec
 sbc #42
 sta BridgeX
 tya
 clc
 adc #80
 tay
 cmp QueueY-1,x
 beq BridgeReject
 jmp AppendBridge
BridgeReject:
 rts
