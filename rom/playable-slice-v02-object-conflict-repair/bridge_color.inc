CacheBridgeColor:
 lda #$26
 cpy #150
 bcc StoreBridgeColor
 cpy #181
 bcs StoreBridgeColor
 lda DoorColor
StoreBridgeColor:
 sta CapWallColor
 rts
