InitGame:
 lda #3
 sta Lives
 lda INTIM
 eor #$6d
 bne InitialSeed
 lda #$6d
InitialSeed:
 sta RandomState
InitRoom:
 lda #0
 sta Hunt
 sta Shot
 sta Pressed
 sta RoomDone
 sta KeyState
 sta Unlocked
 sta Quota
 lda #12
 sta PX
 lda #82
 sta PY
 lda #8
 sta Aim
 jsr Random
 sec
SpawnModulo:
 sbc #7
 bcs SpawnModulo
 adc #7
 tay
 ldx #0
SpawnLoop:
 lda SpawnX,y
 sta NX,x
 lda SpawnY,y
 sta NY,x
 lda SpawnDir,y
 sta NDir,x
 lda #0
 sta Blocked,x
 lda #255
 sta Life,x
 iny
 cpy #7
 bcc SpawnNext
 ldy #0
SpawnNext:
 inx
 cpx #5
 bcc SpawnLoop
 jsr Random
 sec
CarrierModulo:
 sbc #5
 bcs CarrierModulo
 adc #5
 sta Carrier
 rts

Random:
 lda RandomState
 lsr
 bcc NoRandomTap
 eor #$b8
NoRandomTap:
 sta RandomState
 rts

LogicUpdate:
 jsr Random
 lda SWCHB
 lsr
 bcs NotReset
 lda #0
 sta Points
 sta PointsHi
 lda #3
 sta Lives
 jsr InitRoom
 jmp VideoBank
NotReset:
 lda Lives
 beq SkipUpdate
 lda RoomDone
 bne SkipUpdate
 lda AudioTicks
 beq VolumeReady
 dec AudioTicks
 bne VolumeReady
 lda #0
 sta AUDV0
VolumeReady:
 jsr DeathTicks
 jsr Gameplay
 lda RoomDone
 bne SkipUpdate
 jsr KeyPickup
 jsr MoveNPC
 jsr Touch
SkipUpdate:
 jmp VideoBank

Gameplay:
 ; Convert active-low direction to R L D U bits.
 lda SWCHA
 eor #$ff
 lsr
 lsr
 lsr
 lsr
 tax
 lda Dx,x
 ora Dy,x
 beq KeepAim
 stx Aim
KeepAim:
 lda INPT4
 bmi Released
 lda Pressed
 bne StepShot
 inc Pressed
 lda Shot
 bne StepShot
 inc Shot
 lda #1
 sta Hunt
 lda Aim
 sta Direction
 lda PX
 clc
 adc #3
 sta BX
 lda PY
 clc
 adc #4
 sta BY
 jmp StepShot
Released:
 lda #0
 sta Pressed
 stx Tmp
 lda Dx,x
 beq MoveY
NormalX:
 clc
 adc PX
 sta TX
 lda PY
 sta TY
 jsr HitBox
 bcs MoveY
 lda TX
 sta PX
MoveY:
 ldx Tmp
 lda Dy,x
 beq StepShot
 IF TOP_DOOR
 bpl MoveOrdinaryY
 ELSE
 bmi MoveOrdinaryY
 ENDIF
 jsr VerticalDoor
 bcs DoneGameplay
 ldx Tmp
 lda Dy,x
MoveOrdinaryY:
 clc
 adc PY
 sta TY
 lda PX
 sta TX
 jsr HitBox
 bcs StepShot
 lda TY
 sta PY
StepShot:
 lda Shot
 beq DoneGameplay
 ldx Direction
 lda BX
 clc
 adc Dx,x
 sta BX
 lda BY
 clc
 adc Dy,x
 sta BY
 tay
 lda BX
 jsr HitPoint
 bcs ShotHitWall
 jmp ShotTarget
ShotHitWall:
 lda #0
 sta Shot
DoneGameplay:
 rts

 ; The 8-pixel box must fit in the single X64..95 aperture.
VerticalDoor:
 lda PX
 cmp #64
 bcc OrdinaryDoorWall
 cmp #89
 bcs OrdinaryDoorWall
 lda PY
 IF TOP_DOOR
 cmp #9
 bcs OrdinaryDoorWall
 ELSE
 cmp #159
 bcc OrdinaryDoorWall
 ENDIF
 lda KeyState
 cmp #2
 bne OrdinaryDoorWall
 lda Unlocked
 bne CrossDoor
 inc Unlocked
 sec
 rts
CrossDoor:
 IF TOP_DOOR
 dec PY
 bne DoorHandled
 ELSE
 inc PY
 lda PY
 cmp #168
 bcc DoorHandled
 ENDIF
 inc RoomDone
 lda #100
 jsr AddScore
 ldx #4
Survivors:
 lda Life,x
 bpl NextSurvivor
 lda #15
 jsr AddScore
NextSurvivor:
 dex
 bpl Survivors
DoorHandled:
 sec
 rts
OrdinaryDoorWall:
 clc
 rts

KeyPickup:
 lda KeyState
 cmp #1
 bne NoPickup
 lda PX
 sec
 sbc KeyX
 clc
 adc #7
 cmp #15
 bcs NoPickup
 lda PY
 sec
 sbc KeyY
 clc
 adc #8
 cmp #17
 bcs NoPickup
 inc KeyState
 lda #50
 jsr AddScore
 lda #4
 sta AUDC0
 lda #12
 sta AUDF0
 lda #8
 sta AUDV0
 sta AudioTicks
NoPickup:
 rts

AddScore:
 clc
 adc Points
 sta Points
 bcc ScoreDone
 inc PointsHi
ScoreDone:
 rts

ShotTarget:
 ldx #4
TargetLoop:
 lda Life,x
 bpl NextTarget
 lda BX
 sec
 sbc NX,x
 cmp #8
 bcs NextTarget
 lda BY
 sec
 sbc NY,x
 cmp #9
 bcs NextTarget
 lda #8
 sta Life,x
 lda #0
 sta Shot
 sec
 lda Points
 sbc #30
 tay
 lda PointsHi
 sbc #0
 bcc ZeroPoints
 sta PointsHi
 sty Points
 rts
ZeroPoints:
 lda #0
 sta Points
 sta PointsHi
 rts
NextTarget:
 dex
 bpl TargetLoop
 rts

DeathTicks:
 ldx #4
DeathLoop:
 lda Life,x
 bmi DeathNext
 beq DeathNext
 dec Life,x
 bne DeathNext
 cpx Carrier
 bne DeathNext
 lda NX,x
 sta KeyX
 lda NY,x
 sta KeyY
 lda #1
 sta KeyState
DeathNext:
 dex
 bpl DeathLoop
 rts

; One actor budget per update. Patrol and hunt use the same four cardinal
; steps and the same full-box wall and inter-actor collision.
MoveNPC:
 lda FrameClock
 and #1
 beq UpdateNpc
 rts
UpdateNpc:
 ldx Quota
 stx Actor
 inc Quota
 lda Quota
 cmp #5
 bcc QuotaValid
 lda #0
 sta Quota
QuotaValid:
 lda Life,x
 bmi NpcAlive
 rts
NpcAlive:
 lda NDir,x
 sta TryDir
 lda Hunt
 beq StartAttempts
 lda Blocked,x
 bne StartAttempts
 lda PX
 sec
 sbc NX,x
 bcc HuntLeft
 sta Sound
 lda #0
 beq HuntCompare
HuntLeft:
 eor #255
 clc
 adc #1
 sta Sound
 lda #2
HuntCompare:
 sta TryDir

 lda PY
 sec
 sbc NY,x
 bcc HuntUp
 cmp Sound
 bcc StartAttempts
 lda #1
 bne HuntChoice
HuntUp:
 eor #255
 clc
 adc #1
 cmp Sound
 bcc StartAttempts
 lda #3
HuntChoice:
 sta TryDir
StartAttempts:
 lda #2
 sta Retry
TryMove:
 ldx Actor
 ldy TryDir
 lda NX,x
 clc
 adc CardinalX,y
 sta TX
 lda NY,x
 clc
 adc CardinalY,y
 sta TY
 jsr HitBox
 bcs TryAnother
 ldx #4
NpcOverlapLoop:
 cpx Actor
 beq NpcOverlapNext
 lda Life,x
 bpl NpcOverlapNext
 jsr Overlap
 bcs TryAnother
NpcOverlapNext:
 dex
 bpl NpcOverlapLoop
 ldx Actor
 lda TX
 sta NX,x
 lda TY
 sta NY,x
 lda TryDir
 sta NDir,x
 lda #0
 sta Blocked,x
NpcDone:
 rts
TryAnother:
 inc TryDir
 lda TryDir
 and #3
 sta TryDir
 dec Retry
 bne TryMove
 ldx Actor
 lda TryDir
 sta NDir,x
 lda #1
 sta Blocked,x
 rts

; AABB result carry=1 if candidate overlaps the indexed live actor.
Overlap:
 lda TX
 sec
 sbc NX,x
 clc
 adc #7
 cmp #15
 bcs NoOverlap
 lda TY
 sec
 sbc NY,x
 clc
 adc #8
 cmp #17
 bcs NoOverlap
 sec
 rts
NoOverlap:
 clc
 rts

Touch:
 lda Hunt
 beq TouchDone
 lda PX
 sta TX
 lda PY
 sta TY
 ldx #4
TouchLoop:
 lda Life,x
 bpl TouchNext
 jsr Overlap
 bcc TouchNext
 dec Lives
 beq TouchDone
 jsr InitRoom
 rts
TouchNext:
 dex
 bpl TouchLoop
TouchDone:
 rts

CardinalX:
 byte 1,0,255,0
CardinalY:
 byte 0,1,0,255

; Six points cover the 8x9 box in this 4x8 tile grid.
HitBox:
 ldy TY
 jsr HitEdge
 bcs BoxDone
 lda TY
 clc
 adc #8
 tay
HitEdge:
 lda TX
 jsr HitPoint
 bcs BoxDone
 lda TX
 clc
 adc #4
 jsr HitPoint
 bcs BoxDone
 lda TX
 clc
 adc #7
 jmp HitPoint
BoxDone:
 rts

; A=x, Y=y. Carry indicates solid. Preserve Y.
HitPoint:
 cmp #160
 bcs Wall
 cpy #176
 bcs Wall
 tax
 lda ColumnByte,x
 clc
 adc RowOffset,y
 sta Tile
 lda ColumnMask,x
 ldx Tile
 and Collision,x
 beq Open
Wall:
 sec
 rts
Open:
 clc
 rts

Dx:
 byte 0,0,0,0,255,255,255,255,1,1,1,1,0,0,0,0
Dy:
 byte 0,255,1,0,0,255,1,0,0,255,1,0,0,255,1,0

 include "collision.inc"
