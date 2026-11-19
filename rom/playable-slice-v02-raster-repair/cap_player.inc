CheckCapPlayer:
 lda NY+4
 clc
 adc #4
 cmp PY
 bcc CapPlayerClear
 sbc #10
 cmp PY
 bcc RejectCapPlayer
CapPlayerClear:
 jmp MatchCapSlots
RejectCapPlayer:
 rts
