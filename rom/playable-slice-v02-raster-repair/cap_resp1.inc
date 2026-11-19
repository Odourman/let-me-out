CapPositionSF:
 sec
CapPositionSFCoarse:
 sbc #15
 bcs CapPositionSFCoarse
 eor #15
 asl
 asl
 asl
 asl
 sta HMP1
CapSFReset:
 sta RESP1
 jmp CapLateDelay
