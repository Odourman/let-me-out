CapLateDelay:
 ; Reach c70 with the right door color restored. A late HMOVE would
 ; shift the existing P0 anchor eight clocks left without this correction.
 lda DoorColor
 sta COLUPF
 lda #$80
 sta HMP0
 nop
 nop
 bit PX
 nop
CapLateMotion:
 sta HMOVE
CapLateSync:
 sta WSYNC
 jmp CapGlyph
