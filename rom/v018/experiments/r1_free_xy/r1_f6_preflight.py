#!/usr/bin/env python3
"""R1-F6 G0 source-only preflight: NO DASM, ROM, Stella or CI mutations.
Pin the untouched source/canon and PRE-REGISTER two fixed 9-row TIA plans.
The c21 and c23 plans use different RESP1 addressing to preserve second c32.
"""
import hashlib,json
from pathlib import Path
R=Path(__file__).resolve().parent
REPO=R.parents[3]
ORIGINAL=REPO/"rom/v018/experiments/venetian_blinds/vb_9_interleave.asm"
CANON=REPO/"design/NPC_REFERENCE_8x9_masks.json"
assert ORIGINAL.exists() and CANON.exists()
def gitblob(p):
    b=p.read_bytes()
    return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
assert gitblob(ORIGINAL)=="a25c92adb4ca5087eeace674e371be98b273ae5b", "Pinned original F4/F6 skeleton changed"
assert gitblob(CANON)=="058800a4c1904d1ff289e7e61b3902aa111ba16d", "Canon changed"
canon=json.loads(CANON.read_text())
assert canon["width"]==8 and canon["height"]==9
assert [int(row,2) for row in canon["sprites"]["large_male"]]==[0x3c,0x3c,0x18,0xff,0x18,0x24,0x24,0x42,0x42]
assert [int(row,2) for row in canon["sprites"]["large_female"]]==[0x3c,0x3c,0x18,0xff,0x3c,0x7e,0x7e,0x24,0x24]
old=ORIGINAL.read_text()
assert old.count("Row00:\n")==old.count("BottomBlank:")==1
assert old.count(" STA WSYNC\n LDA #0\n STA GRP0\n STA GRP1\n STA ENAM0\n LDX #102\nBottomBlank:")==1
assert all(x in old for x in (" STA HMOVE\n","BlankFill:","TopBlank:","BottomBlank:","Overscan:"," STA GRP0\n"," STA ENAM0\n"))
# No additional TV-standard, palette, Y-scaling, cartridge or mapper changes.
# Original frame skeleton was shown to produce 262 NTSC scanlines in F4;
# no timing result is claimed for the NEW probe until a real Stella frame.
PLAYER=[0x3c,0x7e,0x18,0x7e,0x1e,0x3c,0x18,0x24,0x42]
plans={}
for first in (21,23):
    c=0;trace=[]
    def step(op,n):
        nonlocal_c = None
        return op,n
    def add(op,cycles):
        global c
        c+=cycles;trace.append({"instruction":op,"CPU_end_cycle_STATIC":c,"TIA_CC_nominal":3*c})
    add("LDA #player[y]",2);add("STA GRP0",3)
    add("LDA #one M0 on row04 else #0",2);add("STA ENAM0",3)
    add("LDA #canonical male row y (TOP_DOWN)",2)
    for _ in range(3 if first==21 else 4):add("NOP",2)
    add("STA RESP1 male",3);assert c==first
    add("STA GRP1 male",3)
    add("LDA #canonical female row y (TOP_DOWN)",2)
    if first==21:
        add("BIT FRAMELO",3)
        add("STA RESP1 female",3)
    else:
        # 6502 STA zpg,X with X = $00, four cycles, writes exact same RESP1.
        add("STA RESP1,X female (X=$00)",4)
    assert c==32,(first,c)
    add("STA GRP1 female",3);assert c==35
    next_wsync=c+3
    assert next_wsync==38 and 76-next_wsync==38
    assert trace[-1]["CPU_end_cycle_STATIC"]==35
    first_grp=first+3
    # Source estimates; TIA reset/decode/START/GRP latches are not identical to CPU writes.
    first_start=17+max(0,3*first-68)
    second_start=17+max(0,3*32-68)
    predicted=(9+2*first_start,9+2*second_start)
    assert predicted==((43,99) if first==21 else (45,99))
    assert 3*first_grp < 68+first_start, "male data must be loaded before nominal copy START"
    assert 3*35 < 68+second_start, "female data must be loaded before nominal copy START"
    plans[f"c{first}_c32"]={
      "source_only":True, "mode":first, "first_RESP1_end":first,
      "first_GRP1_end":first_grp, "second_RESP1_end":32, "second_GRP1_end":35,
      "next_WSYNC_end":next_wsync,"cycles_spare_before_76":76-next_wsync,
      "NUSIZ1":1,"X_register_fixed_zero":True,
      "source_row_template":trace,
      "nine_rows":[{
        "y_source_top_down":y,"male_canon_byte":f"{int(canon['sprites']['large_male'][y],2):02X}",
        "female_canon_byte":f"{int(canon['sprites']['large_female'][y],2):02X}",
        "player_byte":f"{PLAYER[y]:02X}", "M0_enable":2 if y==4 else 0,
        "RESP1_end_cycles":[first,32],
        "GRP1_end_cycles":[first_grp,35],"GRP0_end":5,"ENAM0_end":10,
        "next_WSYNC_end":38, "cycle_margin":38
      } for y in range(9)],
      "pixel_X_original_model_prediction_not_measurement":list(predicted)
    }
assert len(plans)==2
pre={
  "G0":"F6_SOURCE_ONLY_FEASIBLE_BOTH_PHASES_9_ROWS",
  "frozen_F5_parent":"953c6c5ef20e83d93474de4c094de784761da257",
  "original_rom_skeleton_blob":"a25c92adb4ca5087eeace674e371be98b273ae5b",
  "locked_NPC_mask_git_blob":"058800a4c1904d1ff289e7e61b3902aa111ba16d",
  "P0_player_preserved":True,"M0_test_shot_preserved":True,
  "PF_mirrored_brown_sidewalls_reset_initialization_preserved":True,
  "HMOVE_init_only_prior_to_visible_9_rows":True,
  "VDEL1_not_activated":True,
  "frame_skeleton_WSYNCS_preserved_F4_known_262_but_new_ROM_not_yet_measured":True,
  "predecessor":"80 TopBlank WSYNC lines; constant LDX #0 outside 9-row band; first source row starts with STA WSYNC",
  "successor":"after row08 next WSYNC c38 then GRP0/GRP1/ENAM0 off and 102 BottomBlank lines; preserve 29 Overscan and 3 VSYNC slots",
  "c21_vs_c23_prior_predictions":[[43,99],[45,99]],
  "P1_START_reset_latch_hypothesis_is_NOT_a_measured_register":True,
  "preflight_allows_ONLY_first_c21_ROM_then_c23_ROM_if_c21_real_pixel_gate_passes":True,
  "plans":plans
}
f=R/"r1_f6_g0_source_only.json";f.write_text(json.dumps(pre,indent=2)+"\n")
print("F6_G0_SOURCE_ONLY_FEASIBLE BOTH c21/c32 and c23/c32: all nine rows 38/76, +38 margin; top-down M/F")
print("F6_PRE_REGISTERED_SCREENSHOT_X c21 (43,99) c23 (45,99), NOT MEASURED")
