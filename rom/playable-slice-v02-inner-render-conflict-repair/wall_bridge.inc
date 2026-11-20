; One scheduled P1 setup can reuse the late-HMOVE kernel with M1 disabled.
; Use it where the scheduler already keeps the playfield stable.
PlanWallBridge:
 lda Eligible
 cmp Rendered
 bne RejectWallBridge
 ldx SortI
 dex
NextWallSlot:
 bmi RejectWallBridge
 lda QueueY,x
 cmp #90
 bcc PreviousWallSlot
 cmp #248
 bcs PreviousWallSlot
 jsr EncodeWallX
 bcs PreviousWallSlot
 bpl InstallWallBridge
 ; Keep the earliest ordinary wall opportunity when the first P1 slot
 ; is already in or beyond the normal bridge band.
 ldy QueueX
 cpy #66
 bcs PreviousWallSlot
InstallWallBridge:
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
 jsr CacheBridgeColor
 iny
 iny
 lda (P0Ptr),y
 sta CapPlayerFirst
 iny
 lda (P0Ptr),y
 sta CapPlayerNext
 rts
