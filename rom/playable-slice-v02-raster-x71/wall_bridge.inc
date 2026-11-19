; One scheduled P1 setup can reuse the late-HMOVE kernel with M1 disabled.
; Restrict it to the X63–70 and X72–78 domains within the flat door-band PF.
PlanWallBridge:
 lda Eligible
 cmp Rendered
 bne RejectWallBridge
 ldx SortI
 dex
NextWallSlot:
 bmi RejectWallBridge
 lda QueueY,x
 cmp #155
 bcc PreviousWallSlot
 cmp #181
 bcs PreviousWallSlot
 jsr EncodeWallX
 bcs PreviousWallSlot
 sta BridgeX
 lda #0
 sta QueueX,x
 lda QueueY,x
 sec
 sbc #2
 sta BridgeOld         ; temporarily hold the cache origin during VBLANK
 lda #1                ; select the bridge kernel without arming M1 at a room Y
 sta CapStart
RejectWallBridge:
 rts
PreviousWallSlot:
 dex
 jmp NextWallSlot

CacheCapPlayer:
 ldy CapStart
 cpy #1
 bne FillCapPlayer
 ldy BridgeOld
 lda #0
 sta BridgeOld         ; the vertical sorter has already closed the old mask
FillCapPlayer:
 iny
 iny
 lda (P0Ptr),y
 sta CapPlayerFirst
 iny
 lda (P0Ptr),y
 sta CapPlayerNext
 rts
