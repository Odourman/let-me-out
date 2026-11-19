 ALIGN 256
PFData0:
 include "key_bridge.inc"
 ds PFData0+80-*,0
MapColumn0:
 byte 240
 include "prepare_key_assist.inc"
 include "cap_finish.inc"
 ALIGN 256
PFData1:
 include "key_bridge_append.inc"
 include "key_assist_select.inc"
 ds PFData1+80-*,0
MapColumn1:
 byte 255,255,255,255,255,255,255,255,0,0,0,0,0,0,0,0
 byte 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
 byte 8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8
 byte 8,8,8,8,8,8,8,8,15,15,15,15,15,15,15,15
 byte 0
 include "cap_plan.inc"
 ds PFData1+192-*,0
MapColumn1Lower:
 byte 15,15,15,15,15,15,15,15,8
 include "cap_pointer.inc"
 ds PFData1+224-*,0
MapColumn1Bottom:
 byte 0
 include "cap_resp1.inc"
 ds PFData1+248-*,0
MapColumn1End:
 byte 255,255,255,255,255,255,255,255
 ALIGN 256
PFData2:
 include "assist_window.inc"
 include "key_assist_install.inc"
 ds PFData2+80-*,0
MapColumn2:
 byte 255,255,255,255,255,255,255,255,0
 include "cap_late_delay.inc"
 ds PFData2+112-*,0
MapColumn2Middle:
 byte 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
 byte 0,0,0,0,0,0,0,0,3,3,3,3,3,3,3,3
 byte 0
 include "cap_insert.inc"
 ds PFData2+192-*,0
MapColumn2Lower:
 byte 3,3,3,3,3,3,3,3,0
 include "wall_x.inc"
 ds PFData2+224-*,0
MapColumn2Bottom:
 byte 0
 include "cap_glyph.inc"
 ds PFData2+248-*,0
MapColumn2End:
 byte 255,255,255,255,255,255,255,255
 ALIGN 256
RoomFlags:
 include "key_assist_raster.inc"
 ds RoomFlags+80-*,0
MapFlags:
 byte 0,0,0,0,0,0,0,0,8,0,0,0,0,0,0,0
 byte 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
 byte 8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
 byte 0,0,0,0,0,0,0,0,8,0,0,0,0,0,0,0
 byte 8,0,0,0,0,129,0,0,128,128,128,128,128,128,128,128
 byte 128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128
 byte 128,128,128,128,128,128,128,128,129,0,0,0,0,0,0,0
 byte 8,0,0,0,0,0,0,0,8,0,0,0,0,0,0,0
 byte 0,129,0,0,0,0,0,0,129,0,0,0,0,0,0,0
 byte 8,0,0,0,0,0,0,0,0,0,0,0,129,0,0,0
 byte 0,0,0,0,0,0,0,0,120,0,0,0,0,0,0,0
 ds 175,0
Mask0:
 byte 60,60,24,255,24,36,36,66,66
 ds 175,0
Mask1:
 byte 60,60,24,255,60,126,126,36,36
 ds 175,0
Mask2:
 byte 0,0,60,60,24,126,24,36,0
 ds 175,0
Mask3:
 byte 0,0,60,60,24,126,60,36,0
 ds 175,0
