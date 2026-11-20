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



; The mirrored graphics banks share addresses. When M1 is scheduled,
; use the kernel that keeps the player's latch order and manages M1.
SelectDoorKernel:
 lda CapStart
 beq SelectNormalDoor
CapKernelSelected:
 sta $fff9
 rts
SelectNormalDoor:
 lda PY
 cmp #64
 bcc DoorKernelSelected
 cmp #104
 bcs DoorKernelSelected
 sta $fff8
DoorKernelSelected:
 rts

FinishHorizontal:
 lda #0
 sta ENAM1
 sta NUSIZ1
 lda CapStart
 beq FinishMove
 lda #$20
 sta NUSIZ1
 lda NX+4
 ldx #3
 jsr Position
 jsr CacheCapPlayer
FinishMove:
 sta WSYNC
 sta HMOVE
 sta WSYNC
 sta HMCLR
 rts
