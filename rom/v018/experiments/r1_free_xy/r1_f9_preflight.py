#!/usr/bin/env python3
"""F9 G0 SOURCE ONLY: frozen F7 ASM/LST/SYM, 72 rows, no DASM/ROM/Stella.
This script MUST pass before the one permitted F9 compilation.
"""
from pathlib import Path
import hashlib,json,re
R=Path(__file__).resolve().parent
ROOT=R.parents[3]
parent=ROOT/"seed"
expected={"asm":"2ea6ccbc765bb0472c662bc562c864299e8988dc433c945cf35dae999c79983c",
 "lst":"5b18b0f5a808b1c38e9b587542dae1b25132a0e92d4f1cd7273156b1b40bf481",
 "sym":"158e8b7a69a15b2ddf4b60c727d4c8c6d41f51ce8103303cfe6ef71c3c383b83",
 "ROM":"ede93075c3c2c88b6cca226f52958fbbcb9117a068edca01d4d83ff30e4677df"}
paths={"asm":parent/"r1_f7_2x2_independent_RAM_X_ONE_ROM.asm",
 "lst":parent/"dist/r1_f7_2x2_independent_RAM_X_ONE_ROM.lst",
 "sym":parent/"dist/r1_f7_2x2_independent_RAM_X_ONE_ROM.sym",
 "ROM":parent/"dist/r1_f7_2x2_independent_RAM_X_ONE_ROM_F6.bin"}
for name,p in paths.items():
 assert p.exists() and hashlib.sha256(p.read_bytes()).hexdigest()==expected[name],("F9_G0_UNFROZEN_F7",name)
assert len(paths["ROM"].read_bytes())==16384
b=(R/"canon_masks.json").read_bytes()
gitblob=hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
assert gitblob=="058800a4c1904d1ff289e7e61b3902aa111ba16d"
sp=json.loads(b)["sprites"]
M=[int(x,2) for x in sp["large_male"]]
F=[int(x,2) for x in sp["large_female"]]
SM=[int(x,2) for x in sp["small_male"]]
assert M==[0x3C,0x3C,0x18,0xFF,0x18,0x24,0x24,0x42,0x42]
assert F==[0x3C,0x3C,0x18,0xFF,0x3C,0x7E,0x7E,0x24,0x24]
assert SM==[0,0,0x3C,0x3C,0x18,0x7E,0x18,0x24,0]
asm=paths["asm"].read_text();sym=paths["sym"].read_text();lst=paths["lst"].read_text()
assert "X0_SELECT=$A0\nX1_SELECT=$A1\nF7_SEQ_STEP=$A2\nF7_HOLDCOUNT=$A3" in asm
assert all("F7_"+q+"_Row"+format(y,"02d")+":" in asm for q in ("00","10","01","11") for y in range(9))
assert " ORG $F800\n" in asm and " ORG $FFFA\n" in asm
names=("F7_00_Row00","F7_10_Row00","F7_01_Row00","F7_11_Row00","F7AfterRows")
addr=[int(re.search(r"(?m)^"+n+r"\s+([0-9a-fA-F]{4})\b",sym).group(1),16) for n in names]
assert addr==[0xF0FF,0xF1F5,0xF2E2,0xF3D8,0xF4CE]
assert all(n in lst for n in names)
actual_f7_kernel_sizes=[b-a for a,b in zip(addr,addr[1:])]
assert actual_f7_kernel_sizes==[246,237,246,246] and sum(actual_f7_kernel_sizes)==975
gray=("000","001","011","010","110","111","101","100","000")
assert len(set(gray))==8 and all(sum(a!=b for a,b in zip(u,v))==1 for u,v in zip(gray,gray[1:]))
player=(0x3C,0x7E,0x18,0x7E,0x1E,0x3C,0x18,0x24,0x42)
plans={};grand=0
for bits in ("000","001","010","011","100","101","110","111"):
 x0,x1,x2=map(int,bits)
 first,second,third=21+2*x0,32+x1,48+2*x2
 rows=[]
 for y in range(9):
  instr=[]
  def add(op,cycles,size):
   instr.append({"op":op,"cycles":cycles,"bytes":size})
  add("LDA #P0",2,2);add("STA GRP0",3,2);add("LDA #M0",2,2);add("STA ENAM0",3,2)
  add("LDA #M",2,2)
  for _ in range(3+x0):add("NOP_M",2,1)
  add("STA RESP1 M",3,2);add("STA GRP1 M",3,2);add("LDA #F",2,2)
  if x0==0 and x1==0:add("BIT FRAMELO",3,2);add("STA RESP1 F",3,2)
  elif x0==0 and x1==1:add("NOP_F",2,1);add("NOP_F",2,1);add("STA RESP1 F",3,2)
  elif x0==1 and x1==0:add("STA RESP1,X F",4,2)
  else:add("NOP_F",2,1);add("STA RESP1 F",3,2)
  add("STA GRP1 F",3,2);add("LDA #SM",2,2)
  for _ in range((4 if x1==0 else 3)+x2):add("NOP_SM",2,1)
  add("STA RESP1 SM" if x1==0 else "STA RESP1,X SM",3 if x1==0 else 4,2)
  add("STA GRP1 SM",3,2)
  if y==8:add("JMP F9AfterRows",3,3)
  add("STA WSYNC",3,2)
  timing={};c=0
  for op in instr:
   c+=op["cycles"]
   if op["op"].startswith("STA RESP1") or op["op"].startswith("STA GRP1"):timing[op["op"]]=c
  assert timing["STA RESP1 M"]==first and timing["STA GRP1 M"]==first+3
  assert timing["STA GRP1 F"]==second+3
  assert timing["STA RESP1 F" if x0==0 or x1==1 else "STA RESP1,X F"]==second
  assert timing["STA RESP1 SM" if x1==0 else "STA RESP1,X SM"]==third
  assert timing["STA GRP1 SM"]==third+3
  assert c==54+2*x2+(3 if y==8 else 0) and c<76,(bits,y,c)
  assert (third+3)*3>=153>123 and (third+3)*3<(161 if x2==0 else 167)
  sizes=sum(q["bytes"] for q in instr);grand+=sizes
  rows.append({"y_TOP_DOWN":y,"M":format(M[y],"02X"),"F":format(F[y],"02X"),
   "SM":format(SM[y],"02X"),"P0":format(player[y],"02X"),"M0":2 if y==4 else 0,
   "RESP1_CPU_SOURCE_ONLY":[first,second,third],"GRP1_CPU_SOURCE_ONLY":[first+3,second+3,third+3],
   "WSYNC_CPU_SOURCE_ONLY":c,"remaining_CPU_cycles":76-c,"code_bytes":sizes,
   "instructions_SOURCE_ONLY":instr})
 plans[bits]={"rows":rows,"preregistered_cropped_X":[39+6*x0,99+6*x1,195+12*x2]}
assert len(plans)==8 and all(len(q["rows"])==9 for q in plans.values())
assert grand==2670,(grand,"F8 byte hypothesis contradicted")
assert 2670+310+128==3108<3584
assert 105-14+24==115 and 0xFE00+115<=0xFFFA
assert 3108+115+6<4096
assert 3+3*(4+3+2+3)+2==41<76
result={"G0":"F9_G0_SOURCE_ONLY_FEASIBLE_EIGHT_STATES_NO_ROM",
 "authoritative_frozen_F8":"5c5e603482be7be482eaf8eae5ba317d91087b3d",
 "real_frozen_F7_SHA256":expected,"original_mask_blob":gitblob,
 "real_f7_ASM_LST_SYM_address_start":[format(x,"04X") for x in addr],
 "real_F7_kernel_bytes":actual_f7_kernel_sizes,
 "F9_eight_nine_row_kernel_source_bytes":grand,
 "old_F7_other_executable_bytes":310,"new_RAM_dispatch_init_reserve_UNPROVEN":128,
 "F9_source_max_CODE_budget_before_FE00":3108,
 "F9_source_DATA_budget_after_FE00":115,"one_F6_bank_max_bytes":4096,
 "extra_RAM":"X2_SELECT=$A4","old_RAM":["X0_SELECT=$A0","X1_SELECT=$A1"],
 "GRAY_9_steps_16_frames_each":list(gray),
 "blankline_update_worst_source_CPU_cycles":41,
 "NO_EXTRA_NTSC_SCANLINE":True,
 "all_72_rows_SOURCE_ONLY":plans,
 "HARDWARE_P1_START_GRPLATCH_WRAP_NOT_MEASURED":True,
 "ONE_ROM_NOT_BUILT":True,"FULL_R1_BLOCKED_NOT_ACCEPTED":True}
(R/"r1_f9_g0_source_only.json").write_text(json.dumps(result,indent=2)+"\n")
print(result["G0"],"ROW_COUNT",72,"ROW_BYTES",grand,"PROGRAM_UPPER_BOUND",3108,"NO_ROM")
