; The final P1 actor can hand off to a floor key after its last live row.
; When P0's right edge is left of that actor, allow the shorter handoff.
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
 tya
 cmp AllowedSetup,y
 bne BridgeReject
 lda PX
 adc #10              ; equality above set C, QueueX encodes X+3
 cmp QueueX-1,x
 lda #2
 bcs BridgeMargin
 lda #4
BridgeMargin:
 clc
 adc KeyY
 cmp OrderEnd
 bcc BridgeReject
 lda KeyX
 sbc #42              ; the successful order check set C
 bcc BridgeReject
 sta BridgeX
 adc #44              ; recover KeyX+3 with carry set
 sec
 sbc QueueX-1,x
 cmp #20
 bcc BridgeReject
 lda QueueX-1,x
 cmp #23
 bcc BridgeReject
 tya
 clc
 adc #80
 tay
 cmp QueueY-1,x
 beq BridgeReject
 jmp AppendBridge
BridgeReject:
 rts
