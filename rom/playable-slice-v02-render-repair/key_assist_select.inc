; All other live sprites must end ahead of the key's setup. A single
; small mask can finish before logical line 156 on the upper P0 band.
SelectKeyNpc:
 lda Life,x
 beq NextKeyNpc
 lda NY,x
 cmp #144
 bcc NextKeyNpc
 cmp #149
 bcs RejectKeySelection
 cpx #3
 bcc RejectKeySelection
 lda Life,x
 bpl RejectKeySelection
 jmp FinishKeySelection
NextKeyNpc:
 dex
 bpl SelectKeyNpc
 rts
RejectKeySelection:
 jmp ClearKeySelection
