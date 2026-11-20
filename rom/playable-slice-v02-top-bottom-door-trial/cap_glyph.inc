CapGlyph:
 ; A is $80 after HMOVE, clearing the missile enable before it reaches SF.
CapHeadDisable:
 sta ENAM1
 iny
 lda CapPlayerNext
 sta GRP0
 lda #$26
 sta COLUPF
 lda.w CapWallColor
 sta COLUPF
 jmp GlyphP1
