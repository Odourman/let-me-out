KeyAssistStart:
 ; On the first switch line GRP1 was already updated by SpecialScanline.
 stx AssistQueue
 lda #0
 sta GRP0
 sta ENAM0
 iny
 lda (P1Ptr),y
 sta BridgeOld
 sta WSYNC
 lda BridgeOld
 sta GRP1
 lda AssistX
 bit AssistX
 jmp KeyAssistPosition   ; 15 cycles replace three coarse iterations

KeyAssistPosition:
 sec
KeyAssistCoarse:
 sbc #15
 bcs KeyAssistCoarse
 eor #7
 asl
 asl
 asl
 asl
 sta HMP0
 sta RESP0
 lda #0
 sta HMP1
 sta WSYNC
 sta HMOVE
 iny
 lda (P1Ptr),y
 sta GRP1
 dey
 dey
 jmp AssistInstallRegisters

FinishKeySelection:
 lda AssistObject
 beq FirstKeySelection
 jmp RejectKeySelection
FirstKeySelection:
 inx
 stx AssistObject
 dex
 jmp NextKeyNpc

ClearKeySelection:
 lda #0
 sta AssistObject
 rts
