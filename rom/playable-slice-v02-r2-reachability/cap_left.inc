; X60-62: position P1 four CPU cycles earlier than the regular bridge.
; Rejoin at the same phase so HMOVE and WSYNC keep their existing slots.
CapLeftPosition:
 nop
 nop
 nop
 sta HMP1
CapLeftReset:
 sta RESP1
 nop
 nop
 jmp CapLateDelay
