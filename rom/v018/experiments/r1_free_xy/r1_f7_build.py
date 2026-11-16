#!/usr/bin/env python3
"""R1-F7: ONE AND ONLY ONE new 16KB F6/NTSC two-RAM-X-bit diagnostic ROM.
Four unrolled source-locked 9-row kernels in one 4 KiB program bank.
G0 SOURCE ONLY must already be independently green (GHA #43966545190).
No other geometric phase, no R1ba, no third NPC, no variable Y.
"""
import json,hashlib,re,subprocess
from pathlib import Path
R=Path(__file__).resolve().parent; ROOT=R.parents[3]
G0=json.loads((R/"r1_f7_g0_source_only.json").read_text())
assert G0["G0"]=="F7_SOURCE_ONLY_FEASIBLE_FOUR_RUNTIME_PHASES"
assert G0["frozen_F6_base"]=="e45455e09e1d796e576b0012d96e5d817d6210c4"
assert G0["locked_NPC_mask_blob"]=="058800a4c1904d1ff289e7e61b3902aa111ba16d"
assert G0["two_selectors"]["X0_SELECT"]["addr"]=="$A0"
assert G0["two_selectors"]["X1_SELECT"]["addr"]=="$A1"
assert G0["seven_step_16frame_sequence"]["pairs"]==["00","10","00","01","11","01","00"]
old=(ROOT/"rom/v018/experiments/venetian_blinds/vb_9_interleave.asm").read_text()
source_ref=json.loads((R/"canon_masks.json").read_text())["sprites"]
male=[int(v,2) for v in source_ref["large_male"]]
female=[int(v,2) for v in source_ref["large_female"]]
player=[0x3C,0x7E,0x18,0x7E,0x1E,0x3C,0x18,0x24,0x42]
assert male==[0x3C,0x3C,0x18,0xFF,0x18,0x24,0x24,0x42,0x42]
assert female==[0x3C,0x3C,0x18,0xFF,0x3C,0x7E,0x7E,0x24,0x24]
anchor="Row00:\n"
ending="\n STA WSYNC\n LDA #0\n STA GRP0\n STA GRP1\n STA ENAM0\n LDX #102\nBottomBlank:"
assert old.count(anchor)==old.count(ending)==1
head,remain=old.split(anchor,1)
old_visible,tail=remain.split(ending,1)
assert old_visible.count(" STA RESP1\n")==9
# Define two independently writable RAM bytes + phase controller, no aliasing.
head=head.replace("FRAMELO=$80\n",
   "FRAMELO=$80\nX0_SELECT=$A0\nX1_SELECT=$A1\nF7_SEQ_STEP=$A2\nF7_HOLDCOUNT=$A3\n",1)
assert "X0_SELECT=$A0\nX1_SELECT=$A1\n" in head
head=head.replace(" STA FRAMELO\n STA VSYNC\n",
""" STA FRAMELO
 STA X0_SELECT
 STA X1_SELECT
 STA F7_SEQ_STEP
 LDA #16
 STA F7_HOLDCOUNT
 LDA #0
 STA VSYNC
""",1)
head=head.replace("COLUBK=$09\n","COLUBK=$09\nCOLUPF=$08\nCTRLPF=$0A\n",1)
head=head.replace(" STA COLUBK\n LDA #145\n",
""" STA COLUBK
 LDA #$26
 STA COLUPF
 LDA #1
 STA CTRLPF
 LDA #$F0
 STA PF0
 LDA #1
 STA NUSIZ1
 LDA #145
""",1)
assert " STA HMOVE\n LDX #30\nBlankFill:" in head
# Preserve EXACT original 30 blank WSYNC slots: two dedicated to source-only
# source-registered updates, then 28 original. Only one selector value can change
# at any state transition (seven-step table), each selector own STA and RAM byte.
head=head.replace(" STA HMOVE\n LDX #30\nBlankFill:",
""" STA HMOVE
 ; F7: two of the EXISTING 30 VBLANK WSYNC slots used as the two
 ; independent selector update stages; no extra scanline is allocated.
 STA WSYNC
 DEC F7_HOLDCOUNT
 BNE F7_NoNewStep
 LDA #16
 STA F7_HOLDCOUNT
 INC F7_SEQ_STEP
 LDA F7_SEQ_STEP
 CMP #7
 BNE F7_NoNewStep
 LDA #0
 STA F7_SEQ_STEP
F7_NoNewStep:
 STA WSYNC
 ; Independently update separate RAM bytes only when that byte changes.
 ; e.g. 00->10 changes only X0; 00->01 changes only X1.
 LDX F7_SEQ_STEP
 LDA F7X0Desired,X
 CMP X0_SELECT
 BEQ F7_KeepX0
 STA X0_SELECT
F7_KeepX0:
 LDA F7X1Desired,X
 CMP X1_SELECT
 BEQ F7_KeepX1
 STA X1_SELECT
F7_KeepX1:
 LDX #28
BlankFill:""",1)
assert " LDX #28\nBlankFill:" in head
# Preselect one of FOUR unrolled 9-row kernels only after top-blank but before
# the first visible WSYNC. Every branch READS both independent RAM selector
# bytes; no carry between them or table of four linked X formations.
assert head.endswith(" DEX\n BNE TopBlank\n ")==False  # a trailing whitespace is not required
assert "TopBlank:\n STA WSYNC\n DEX\n BNE TopBlank\n" in head
head += """ ; F7 source-level dispatch: two actual different mutable RAM values.
 LDX #0
 LDA X0_SELECT
 BEQ F7_SelectX0Zero
 LDA X1_SELECT
 BEQ F7_Goto10
 JMP F7_11_Row00
F7_Goto10:
 JMP F7_10_Row00
F7_SelectX0Zero:
 LDA X1_SELECT
 BEQ F7_Goto00
 JMP F7_01_Row00
F7_Goto00:
 JMP F7_00_Row00
"""
# Guarantee branch targets into the immediate few bytes near dispatch (never
# an out-of-range 6502 branch into far-away 9-row copies).
rows=[]
for state,first,second in (("00",21,32),("10",23,32),("01",21,33),("11",23,33)):
    plan=G0["plans"][f"c{first}_c{second}"]
    for y in range(9):
        q=[f"F7_{state}_Row{y:02d}:",
           " STA WSYNC",
           " LDA #$%02X"%player[y]," STA GRP0",
           " LDA #$%02X"%(2 if y==4 else 0)," STA ENAM0",
           " LDA #$%02X"%male[y]]
        q+=[" NOP"]*(3 if first==21 else 4)
        q+=[" STA RESP1"," STA GRP1"," LDA #$%02X"%female[y]]
        if first==21 and second==32:
            q+=[" BIT FRAMELO"," STA RESP1"]
        elif first==21 and second==33:
            q+=[" NOP"," NOP"," STA RESP1"]
        elif first==23 and second==32:
            q+=[" STA RESP1,X"] # SAME TIA REG $11; X fixed zero; 4 CPU cycles
        elif first==23 and second==33:
            q+=[" NOP"," STA RESP1"]
        else:raise AssertionError(state)
        q+=[" STA GRP1"]
        if y==8:q+=[" JMP F7AfterRows"]
        assert plan["nine_rows"][y]["male_byte"]==f"{male[y]:02X}"
        assert plan["nine_rows"][y]["female_byte"]==f"{female[y]:02X}"
        assert plan["nine_rows"][y]["first_RESP1_cycle"]==first
        assert plan["nine_rows"][y]["second_RESP1_cycle"]==second
        assert plan["nine_rows"][y]["next_WSYNC_source_end_cycle"]==(41 if second==32 else 42) if y==8 else plan["nine_rows"][y]["next_WSYNC_source_end_cycle"]==(38 if second==32 else 39)
        rows+=q
source=head+"\n".join(rows)+"\nF7AfterRows:\n"+ending.lstrip("\n")+tail
# Extend data table, no reinitialization/mapper change
assert source.count(" ORG $F300\n")==1
source=source.replace(" ORG $F300\n"," ORG $F800\n",1)
assert source.count(" ORG $FFFA\n")==1
source=source.replace(" ORG $FFFA\n",
""" ; Each desired bit is independently compared against its OWN RAM byte.
F7X0Desired:
 BYTE 0,1,0,0,1,0,0
F7X1Desired:
 BYTE 0,0,0,1,1,1,0
 ORG $FFFA
""",1)
assert source.count(" STA RESP1\n")+source.count(" STA RESP1,X\n")==9*2*4
assert source.count(" STA GRP1\n")==9*2*4+3
assert source.count(" STA NUSIZ1\n")==2
assert source.count(" STA HMOVE\n")==1
assert source.count(" STA COLUPF\n")==1 and source.count(" STA CTRLPF\n")==1
assert source.count(" STA WSYNC\n")==9*4+2+source[:source.index("F7_00_Row00:")].count(" STA WSYNC\n")-2 + source[source.index("F7AfterRows:"):].count(" STA WSYNC\n") # tautology count expression carefully; not timing proof
assert source.count(" STA X0_SELECT\n")==2 and source.count(" STA X1_SELECT\n")==2
assert " LDA X0_SELECT\n BEQ " in source and " LDA X1_SELECT\n BEQ " in source
assert all(f"F7_{s}_Row{y:02d}:" in source for s in ("00","10","01","11") for y in range(9))
stem="r1_f7_2x2_independent_RAM_X_ONE_ROM"
src=R/(stem+".asm");src.write_text(source)
dist=R/"dist";dist.mkdir(exist_ok=True)
cmd=["dasm",src.name,"-f3",f"-odist/{stem}.4k.bin",f"-ldist/{stem}.lst",f"-sdist/{stem}.sym"]
subprocess.run(cmd,cwd=R,check=True)
bank=(dist/(stem+".4k.bin")).read_bytes()
assert len(bank)==4096,(len(bank),"not exactly 4K bank")
rom=bank*4
assert len(rom)==16384
romfile=dist/(stem+"_F6.bin");romfile.write_bytes(rom)
lst=(dist/(stem+".lst")).read_text()
assert all(f"F7_{s}_Row{y:02d}" in lst for s in ("00","10","01","11") for y in range(9))
assert len([ln for ln in lst.splitlines() if "95 11" in ln and "RESP1,X" in ln])==9
assert all(rom[4096*i:4096*(i+1)]==bank for i in range(4))
info={"classification":"R1_F7_ONE_NEW_F6_ROM_COMPILED_NOT_YET_STELLA_PROVEN",
  "ROM_bytes":len(rom),"each_bank_bytes":len(bank),
  "ROM_sha256":hashlib.sha256(rom).hexdigest(),
  "ASM_sha256":hashlib.sha256(source.encode()).hexdigest(),
  "four_banks_identical":True,
  "source_based_preflight":"F7_SOURCE_ONLY_FEASIBLE_FOUR_RUNTIME_PHASES",
  "four_schedules":[["00",21,32],["10",23,32],["01",21,33],["11",23,33]],
  "two_actual_separate_RAM_bytes":["X0_SELECT=$A0","X1_SELECT=$A1"],
  "seven_step_independent_update":"00->10->00->01->11->01->00 (16 frames each)",
  "canonical_mask_blob":"058800a4c1904d1ff289e7e61b3902aa111ba16d",
  "prior_screen_X_predictions":{"00":[39,99],"10":[45,99],"01":[39,105],"11":[45,105]},
  "WILL_NOT_BUILD_SECOND_ROM":True,
  "NO_R1_ACCEPTANCE":True,
  "build_command":"cd rom/v018/experiments/r1_free_xy && python3 r1_f7_preflight.py && python3 r1_f7_build.py"}
(dist/(stem+".json")).write_text(json.dumps(info,indent=2)+"\n")
print("F7_THE_ONE_AND_ONLY_16KB_ROM",info["ROM_sha256"])
print("F7_G0_FOUR_SCHEDULES_VERIFIED",info["four_schedules"],"selectors",info["two_actual_separate_RAM_bytes"])
print("F7_UNRUN_STELLA_NO_INDEPENDENCE_CLAIM")
