CapGlyph:
 ; Both P0 and M0 are clear on this line by the scheduling guard.
 lda #$26
 sta COLUPF
 iny
 lda #0
CapHeadDisable:
 sta ENAM1
 sta GRP0
 lda DoorColor
 nop
 sta COLUPF
 jmp GlyphP1
