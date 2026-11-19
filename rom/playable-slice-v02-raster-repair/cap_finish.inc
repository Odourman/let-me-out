MatchCapSlots:
 lda NX+4
 sec
 sbc NX+3
 cmp #20
 bcc RejectCapSlots
 lda NY+3
 clc
 adc #81
 cmp QueueY+2
 bne RejectCapSlots
 ; The bottom edge of SM is the setup row of SF's third lit row.
 lda NY+4
 clc
 adc #85
 cmp QueueY+3
 bcs RejectCapSlots
 jmp InsertCap
RejectCapSlots:
 rts

FinishCapSlot:
 lda NY+4
 clc
 adc #81
 sta CapStart
 adc #2
 sta QueueY+3
 lda #0
 sta QueueX+3
 lda #$0e
 sta QueueColor+3
 lda Mask3+4
 sta QueueFirst+3
 lda Mask2+7
 sta BridgeOld
 lda NX+4
 sec
 sbc #57
 sta BridgeX
 jmp FinishCapPointer
