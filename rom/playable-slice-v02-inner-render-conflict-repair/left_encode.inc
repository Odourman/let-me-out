; The three closest X values use an earlier reset phase.
; Preserve the padding length so the existing coarse loops stay in page.
EncodeNearLeft:
 cmp #$fd
 bcc RejectNearLeftHere
 eor #$ff
 adc #$0b
 jmp EncodeNearLeftShift
