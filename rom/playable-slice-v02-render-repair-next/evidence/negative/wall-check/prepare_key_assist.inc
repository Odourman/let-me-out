PrepareKeyAssist:
 ; The key uses P1 through logical lines 156-158 while P0 moves.
 ; The frame may reserve P0 for a small upper NPC and the lower player.
 lda KeyState
 cmp #1
 bne KeyAssistRejected
 lda Shot
 beq KeyAssistPlayer
 lda BY
 cmp #159
 bcc KeyAssistRejected
KeyAssistPlayer:
 lda PY
 cmp #159
 bcc KeyAssistRejected
 lda PX
 cmp #42
 bcc KeyAssistRejected
 cmp #124
 bcs KeyAssistRejected
 lda KeyY
 cmp #153
 bne KeyAssistRejected
 lda KeyX
 cmp #44
 bcc KeyAssistRejected
 ldx #4
 jmp SelectKeyNpc
KeyAssistRejected:
 rts



SetProbeRight:
 lda DoorColor
 sta COLUPF
 rts
