CapPositionSF:
 bmi CapLeftJump
 ; BridgeX is 0-15. Compute (14 - BridgeX) modulo 16 in the old phase.
 clc
 eor #15
 sbc #0
 asl
 asl
 asl
 asl
 sta HMP1
CapSFReset:
 sta RESP1
 jmp CapLateDelay
CapLeftJump:
 jmp CapLeftPosition
