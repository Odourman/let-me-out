CapGlyph:
 ; A is $80 after HMOVE, clearing the missile enable before it reaches SF.
CapHeadDisable:
 sta ENAM1
 iny
 lda CapPlayerNext
 sta GRP0
 lda #$26
 sta COLUPF
 lda #$3c             ; this path is admitted only before a key has fallen
 sta COLUPF
 nop
 jmp GlyphP1
