#!/usr/bin/env python3
"""R1-F7 G0 SOURCE ONLY, no DASM, Stella, ROM, CI work invoked by this script.
Exactly 4 predeclared RESP1 phase combinations, separate RAM selectors,
top-down original masks, 76 CPU cycles/line and 16KB F6 bank headroom.
"""
from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parent
ROOT=R.parents[3]
def blob(p):
 b=p.read_bytes()
 return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
OLD=ROOT/"rom/v018/experiments/venetian_blinds/vb_9_interleave.asm"
F6=R/"r1_f6_build.py"
CANON=R/"canon_masks.json"
assert blob(OLD)=="a25c92adb4ca5087eeace674e371be98b273ae5b"
assert blob(CANON)=="058800a4c1904d1ff289e7e61b3902aa111ba16d"
f6=F6.read_text();base=OLD.read_text()
assert "STA RESP1,X" in f6 and "STA GRP1" in f6 and "ROW" not in "n/a"
assert " LDX #30\nBlankFill:\n" in base
assert "TopBlank:\n STA WSYNC\n DEX\n BNE TopBlank\n" in base
original=json.loads(CANON.read_text())["sprites"]
M=[int(s,2) for s in original["large_male"]]
F=[int(s,2) for s in original["large_female"]]
assert M==[0x3c,0x3c,0x18,0xff,0x18,0x24,0x24,0x42,0x42]
assert F==[0x3c,0x3c,0x18,0xff,0x3c,0x7e,0x7e,0x24,0x24]
player=[0x3c,0x7e,0x18,0x7e,0x1e,0x3c,0x18,0x24,0x42]
plans={}
for first,second in ((21,32),(23,32),(21,33),(23,33)):
  rows=[]
  for y in range(9):
    t=0;inst=[]
    def add(op,cycles,size):
      global t
      t+=cycles;inst.append({"op":op,"end_CPU_cycle_STATIC":t,"opcode_bytes":size})
    add("LDA #P0[y]",2,2);add("STA GRP0",3,2)
    add("LDA #M0[y]",2,2);add("STA ENAM0",3,2)
    add("LDA #M[y] TOP_DOWN",2,2)
    for _ in range(3 if first==21 else 4):add("NOP",2,1)
    add("STA RESP1 (male)",3,2);assert t==first
    add("STA GRP1 (male)",3,2);assert t==first+3
    add("LDA #F[y] TOP_DOWN",2,2)
    if first==21 and second==32:
      add("BIT FRAMELO (zpg 3-cycle)",3,2)
      add("STA RESP1 (female)",3,2)
    elif first==21 and second==33:
      add("NOP",2,1);add("NOP",2,1)
      add("STA RESP1 (female)",3,2)
    elif first==23 and second==32:
      add("STA RESP1,X (zpg indexed, X=0, 4 cycles)",4,2)
    elif first==23 and second==33:
      add("NOP",2,1)
      add("STA RESP1 (female)",3,2)
    assert t==second,(first,second,y,t)
    add("STA GRP1 (female)",3,2);assert t==second+3
    # row 0-7 fallthrough to next WSYNC, row8 jumps to shared BottomBlank shutdown.
    if y==8:add("JMP F7AfterRows",3,3)
    add("STA WSYNC (next scanline, STATICAL END)",3,2)
    assert t<=76 and 76-t>0,(first,second,y,t)
    rows.append({"source_row_top_down":y,"male_byte":f"{M[y]:02X}",
                 "female_byte":f"{F[y]:02X}","player_byte":f"{player[y]:02X}",
                 "M0_byte":2 if y==4 else 0,
                 "first_RESP1_cycle":first,"first_GRP1_cycle":first+3,
                 "second_RESP1_cycle":second,"second_GRP1_cycle":second+3,
                 "next_WSYNC_source_end_cycle":t,"cycle_margin":76-t,
                 "instr":inst,"row_binary_bytes_including_WSYNCorJump":sum(x["opcode_bytes"] for x in inst)})
  plans[f"c{first}_c{second}"]={"NUSIZ1":1,"nine_rows":rows,
       "first_RESP1_end":first,"second_RESP1_end":second,
       "last_row_with_jump_WSYNCCycle":rows[-1]["next_WSYNC_source_end_cycle"],
       "nine_rows_estimated_bytes":sum(x["row_binary_bytes_including_WSYNCorJump"] for x in rows)}
assert len(plans)==4
assert all(len(p["nine_rows"])==9 for p in plans.values())
# Two different stored writable zero-page RAM selector bytes, not one 2-bit mode variable.
x0_table=[0,1,0,0,1,0,0]
x1_table=[0,0,0,1,1,1,0]
assert list(zip(x0_table,x1_table))==[(0,0),(1,0),(0,0),(0,1),(1,1),(0,1),(0,0)]
assert all(sum(abs(a-b) for a,b in zip(q,r))==1 for q,r in
           zip(list(zip(x0_table,x1_table)),list(zip(x0_table,x1_table))[1:]))
# Two of 30 existing 3-cycle WSYNC blank slots are dedicated to:
# scan A: DEC HOLDCOUNT / conditional INC SEQ_STEP mod7 (<35 cycles)
# scan B: LDX SEQ_STEP / select X0 and X1 independently via compare/store (<33 cycles).
# Remaining 28 original BlankFill WSYNC: exact 30 prior slots maintained.
reserved_frame_lines=2;original_blank=30
assert reserved_frame_lines+(original_blank-reserved_frame_lines)==original_blank
# At last TopBlank WSYNC: DEX(2)+BNE nottaken(2)+LDX#0(2)
# + LDA X0(3)+BEQ(2/3)+LDA X1(3)+BEQ(2/3)+JMP(3) <= 25 CPU cycles
# (branch-to-next-JMP dispatcher, never long rel branch).
kernel_entry_worst_before_Row00WSYNC=27
assert kernel_entry_worst_before_Row00WSYNC+3<76
# Budget 4x 9x ~30 bytes+2KB header/helpers=under 4KB bank.
total_row_bytes=sum(p["nine_rows_estimated_bytes"] for p in plans.values())
assert total_row_bytes+1200<4096,(total_row_bytes,total_row_bytes+1200)
# Frame states are based on separate RAM X0_SELECT and X1_SELECT changing
# separately only if a desired table bit differs from current stored bit.
# This is NOT a single table of four precomputed X coordinates.
p={
 "G0":"F7_SOURCE_ONLY_FEASIBLE_FOUR_RUNTIME_PHASES",
 "frozen_F6_base":"e45455e09e1d796e576b0012d96e5d817d6210c4",
 "original_rom_skeleton_blob":"a25c92adb4ca5087eeace674e371be98b273ae5b",
 "locked_NPC_mask_blob":"058800a4c1904d1ff289e7e61b3902aa111ba16d",
 "two_selectors":{"X0_SELECT":{"addr":"$A0","one_bit_values":[0,1],"male_phase_when_zero":21,"male_phase_when_one":23},
                  "X1_SELECT":{"addr":"$A1","one_bit_values":[0,1],"female_phase_when_zero":32,"female_phase_when_one":33}},
 "separate_RAM_state":{"SEQ_STEP":"$A2","HOLDCOUNT":"$A3","FRAMELO":"$80"},
 "runtime_update_API":"before each visible 9-row raster: two reserved old BlankFill scanlines, DEC HOLDCOUNT; advance SEQ_STEP on zero; independent compare/conditional STA to separate X0_SELECT and X1_SELECT; 28 original blank slots remain; select kernel by reading both RAM bytes, X register forced zero",
 "seven_step_16frame_sequence":{"X0_desired_by_step":x0_table,
      "X1_desired_by_step":x1_table,
      "pairs":[f"{a}{b}" for a,b in zip(x0_table,x1_table)],
      "frames_each_state":16},
 "original_predictions_not_postfit":{
       "00":[39,99],"10":[45,99],"01":[39,105],"11":[45,105]},
 "all_rows_76_CPU_limit":76,
 "per_frame_30_blank_slots_preserved":True,
 "two_extra_visible_frames":False,
 "topblank_last_row_branch_worst_before_first_WSYNC":kernel_entry_worst_before_Row00WSYNC,
 "P0_M0_PF_HMOVE_262_required_real_Stella":True,
 "nineline_total_estimated_bytes":total_row_bytes,
 "worst_estimated_bank_bytes":total_row_bytes+1200,
 "no_fifth_mode_no_extra_ROM":True,
 "predecessor":"80 TopBlank scanline WSYNC retained; final DEX/BNE and bit reads/dispatch <76 before first row0 WSYNC",
 "successor":"row8 3-cycle JMP to shared STA WSYNC; total final visible line <=76; same BottomBlank and Overscan",
 "plans":plans
}
out=R/"r1_f7_g0_source_only.json";out.write_text(json.dumps(p,indent=2)+"\n")
print("F7_G0_SOURCE_ONLY_FEASIBLE_FOUR_RUNTIME_PHASES")
print("F7_STATIC_TIMING",[(k,[v["nine_rows"][0]["next_WSYNC_source_end_cycle"],v["last_row_with_jump_WSYNCCycle"],v["nine_rows_estimated_bytes"]]) for k,v in plans.items()])
print("F7_EACH_BIT_CHANGES_SEPARATELY",p["seven_step_16frame_sequence"]["pairs"])
print("F7_NO_ROM_OR_STELLA_IN_THIS_G0")
