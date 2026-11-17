#!/usr/bin/env python3
"""F9: exactly ONE permitted 16KiB F6/NTSC ROM after separately GREEN G0.
Use pinned archived original F7 ASM, not new R1ba. DO NOT rerun build to
change any phase or bank. All eight RAM modes are IN THE SAME program.
"""
import hashlib,json,re,subprocess
from pathlib import Path
R=Path(__file__).resolve().parent; ROOT=R.parents[3]
g=json.loads((R/"r1_f9_g0_source_only.json").read_text())
assert g["G0"]=="F9_G0_SOURCE_ONLY_FEASIBLE_EIGHT_STATES_NO_ROM"
assert g["F9_eight_nine_row_kernel_source_bytes"]==2670
assert g["F9_source_max_CODE_budget_before_FE00"]==3108
assert g["authoritative_frozen_F8"]=="5c5e603482be7be482eaf8eae5ba317d91087b3d"
parent=ROOT/"seed"
f7=parent/"r1_f7_2x2_independent_RAM_X_ONE_ROM.asm"
original=f7.read_text()
assert hashlib.sha256(f7.read_bytes()).hexdigest()=="2ea6ccbc765bb0472c662bc562c864299e8988dc433c945cf35dae999c79983c"
assert original.count("F7_00_Row00:\n")==1 and original.count("F7AfterRows:\n")==1
pre,rest=original.split("F7_00_Row00:\n",1)
oldkernel,post=rest.split("F7AfterRows:\n",1)
assert oldkernel.count(" STA RESP1\n")+oldkernel.count(" STA RESP1,X\n")==9*2*4
assert "X0_SELECT=$A0\nX1_SELECT=$A1\nF7_SEQ_STEP=$A2\nF7_HOLDCOUNT=$A3" in pre
pre=pre.replace("X1_SELECT=$A1\n","X1_SELECT=$A1\nX2_SELECT=$A4\n",1)
pre=pre.replace(" STA X1_SELECT\n STA F7_SEQ_STEP\n"," STA X1_SELECT\n STA X2_SELECT\n STA F7_SEQ_STEP\n",1)
pre=pre.replace(" CMP #7\n"," CMP #8\n",1)
pre=pre.replace(" LDA F7X0Desired,X\n"," LDA F9X0Desired,X\n",1)
pre=pre.replace(" LDA F7X1Desired,X\n"," LDA F9X1Desired,X\n",1)
pre=pre.replace("F7_KeepX1:\n LDX #28\n",
"""F7_KeepX1:
 LDA F9X2Desired,X
 CMP X2_SELECT
 BEQ F9_KeepX2
 STA X2_SELECT
F9_KeepX2:
 LDX #28
""",1)
assert pre.count(" STA X2_SELECT\n")==2
assert pre.count(" LDA F9X0Desired,X\n")==1 and pre.count(" LDA F9X1Desired,X\n")==1 and pre.count(" LDA F9X2Desired,X\n")==1
assert pre.count(" CMP #8\n")==1 and " CMP #7\n" not in pre
assert pre.count(" ; F7 source-level dispatch:")==1
pre=pre.split(" ; F7 source-level dispatch:",1)[0]
dispatch=""" ; F9 source-level 3 separate RAM bits -> eight unrolled 9-row kernels.
 LDX #0
 LDA X0_SELECT
 BEQ F9_X0Zero
 LDA X1_SELECT
 BEQ F9_X0OneX1Zero
 LDA X2_SELECT
 BEQ F9_Goto110
 JMP F9_111_Row00
F9_Goto110:
 JMP F9_110_Row00
F9_X0OneX1Zero:
 LDA X2_SELECT
 BEQ F9_Goto100
 JMP F9_101_Row00
F9_Goto100:
 JMP F9_100_Row00
F9_X0Zero:
 LDA X1_SELECT
 BEQ F9_X0ZeroX1Zero
 LDA X2_SELECT
 BEQ F9_Goto010
 JMP F9_011_Row00
F9_Goto010:
 JMP F9_010_Row00
F9_X0ZeroX1Zero:
 LDA X2_SELECT
 BEQ F9_Goto000
 JMP F9_001_Row00
F9_Goto000:
 JMP F9_000_Row00
"""
s=json.loads((R/"canon_masks.json").read_text())["sprites"]
masks={k:[int(n,2) for n in s[k]] for k in ("large_male","large_female","small_male")}
M,F,SM=(masks[k] for k in ("large_male","large_female","small_male"))
assert M==[0x3c,0x3c,0x18,0xff,0x18,0x24,0x24,0x42,0x42]
assert F==[0x3c,0x3c,0x18,0xff,0x3c,0x7e,0x7e,0x24,0x24]
assert SM==[0,0,0x3c,0x3c,0x18,0x7e,0x18,0x24,0]
P0=[0x3c,0x7e,0x18,0x7e,0x1e,0x3c,0x18,0x24,0x42]
rows=[]
for bits in ("000","001","010","011","100","101","110","111"):
 x0,x1,x2=map(int,bits)
 for y in range(9):
  q=["F9_"+bits+"_Row"+format(y,"02d")+":"," STA WSYNC",
     " LDA #$"+format(P0[y],"02X")," STA GRP0",
     " LDA #$"+format(2 if y==4 else 0,"02X")," STA ENAM0",
     " LDA #$"+format(M[y],"02X")]
  q+=[" NOP"]*(3+x0)
  q+=[" STA RESP1"," STA GRP1"," LDA #$"+format(F[y],"02X")]
  if x0==0 and x1==0:q+=[" BIT FRAMELO"," STA RESP1"]
  elif x0==0 and x1==1:q+=[" NOP"," NOP"," STA RESP1"]
  elif x0==1 and x1==0:q+=[" STA RESP1,X"]
  else:q+=[" NOP"," STA RESP1"]
  q+=[" STA GRP1"," LDA #$"+format(SM[y],"02X")]
  q+=[" NOP"]*((4 if x1==0 else 3)+x2)
  q+=[" STA RESP1" if x1==0 else " STA RESP1,X"," STA GRP1"]
  if y==8:q+=[" JMP F9AfterRows"]
  rows+=q
post=post.replace(" ORG $F800\n"," ORG $FE00\n",1)
old_data="F7X0Desired:\n BYTE 0,1,0,0,1,0,0\nF7X1Desired:\n BYTE 0,0,0,1,1,1,0\n"
new_data="""F9X0Desired:
 BYTE 0,0,0,0,1,1,1,1
F9X1Desired:
 BYTE 0,0,1,1,1,1,0,0
F9X2Desired:
 BYTE 0,1,1,0,0,1,1,0
"""
assert old_data in post
post=post.replace(old_data,new_data,1)
source=pre+dispatch+"\n".join(rows)+"\nF9AfterRows:\n"+post
assert source.count(" STA RESP1\n")+source.count(" STA RESP1,X\n")==9*3*8
assert source.count(" STA GRP1\n")==9*3*8+3
assert source.count(" ORG $FE00\n")==1 and " ORG $F800\n" not in source
assert source.count(" ORG $FFFA\n")==1
assert len(re.findall(r"(?m)^F9_[01]{3}_Row\d\d:$",source))==72
assert source.count(" STA WSYNC\n")>75
assert source.count(" STA X0_SELECT\n")==2 and source.count(" STA X1_SELECT\n")==2 and source.count(" STA X2_SELECT\n")==2
for bits,expected in g["all_72_rows_SOURCE_ONLY"].items():
 for row in expected["rows"]:
  y=row["y_TOP_DOWN"]
  assert row["M"]==format(M[y],"02X") and row["F"]==format(F[y],"02X") and row["SM"]==format(SM[y],"02X")
  assert row["RESP1_CPU_SOURCE_ONLY"]==[21+2*int(bits[0]),32+int(bits[1]),48+2*int(bits[2])]
  assert row["WSYNC_CPU_SOURCE_ONLY"]==54+2*int(bits[2])+(3 if y==8 else 0)
stem="r1_f9_three_masks_three_binary_ram_x_ONE_ROM"
dest=R/(stem+".asm")
dest.write_text(source)
dist=R/"dist";dist.mkdir(exist_ok=True)
# ONE AND ONLY ONE new build. No rerun/alternative phase if DASM fails.
cmd=["dasm",dest.name,"-f3",f"-odist/{stem}.4k.bin",f"-ldist/{stem}.lst",f"-sdist/{stem}.sym"]
subprocess.run(cmd,cwd=R,check=True)
bank=(dist/(stem+".4k.bin")).read_bytes()
assert len(bank)==4096,(len(bank),"F9_ONE_BUILD_INVALID_4K_STOP")
actual_lst=(dist/(stem+".lst")).read_text()
sym=(dist/(stem+".sym")).read_text()
for bits in ("000","001","010","011","100","101","110","111"):
 for y in range(9):assert "F9_"+bits+"_Row"+format(y,"02d") in sym
assert "F9AfterRows" in sym and "F9X2Desired" in sym
assert "F9_Goto000" in sym and "F9_111_Row00" in sym
rom=bank*4
assert len(rom)==16384
binary=dist/(stem+"_F6.bin");binary.write_bytes(rom)
sha=hashlib.sha256(rom).hexdigest()
info={"status":"F9_ONE_AND_ONLY_ONE_16KiB_F6_ROM_BUILT_STELLA_UNTESTED",
 "ROM_SHA256":sha,"ROM_bytes":len(rom),
 "F6_bank_count":4,"each_bank_bytes":4096,"all_four_bank_contents_identical":True,
 "ASM_SHA256":hashlib.sha256(source.encode()).hexdigest(),
 "original_archived_f7_ASM_SHA256":"2ea6ccbc765bb0472c662bc562c864299e8988dc433c945cf35dae999c79983c",
 "G0":"F9_G0_SOURCE_ONLY_FEASIBLE_EIGHT_STATES_NO_ROM",
 "mask_blob":"058800a4c1904d1ff289e7e61b3902aa111ba16d",
 "registered_corners":{bits:v["preregistered_X_M_F_SM"] if "preregistered_X_M_F_SM" in v else v["preregistered_cropped_X"] for bits,v in g["all_72_rows_SOURCE_ONLY"].items()},
 "RAM":["$A0","$A1","$A4"],"Gray":["000","001","011","010","110","111","101","100","000"],
 "no_second_F9_ROM":True,"full_R1_BLOCKED":True}
(dist/(stem+".json")).write_text(json.dumps(info,indent=2)+"\n")
print("F9_THE_ONLY_ONE_16K_ROM_BUILT",sha)
print("F9_EIGHT_MODES_IN_ONE_ROM_72_G0_ROWS_MATCH",list(info["registered_corners"]))
print("F9_NOT_YET_STELLA_PROVEN")
