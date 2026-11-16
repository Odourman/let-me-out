#!/usr/bin/env python3
"""R1al research ONLY: rearrange four P1 RESP1 strobes to try retaining
extra male and female auto copies under NUSIZ1=3, while keeping both
small-original masks, full yellow player P0 and one M0 static shot.
This is a fixed-X feasibility test, not an R1 implementation.
"""
from pathlib import Path
import os,sys,subprocess,hashlib,json
R=Path(__file__).resolve().parent
P=R.parent/"main_iv_r1aj_four_p1"
subprocess.run([sys.executable,str(P/"build_r1aj.py")],env=dict(os.environ,R1AJ_BATCH="0"),check=True)
PIN="ff0f1c64ffff1915cef934f224b3f3d780bc2de6cc52038d62666904c1f0f263"
assert hashlib.sha256((P/"r1aj_F6.bin").read_bytes()).hexdigest()==PIN
original=(P/"r1aj.asm").read_text()
assert original.count(" LDA #$01\n STA NUSIZ1\n")==1
src=original.replace(" LDA #$01\n STA NUSIZ1\n"," LDA #$03\n STA NUSIZ1\n",1)
# One exact byte sequence in all 4 mode loops, so every frame gets same 4-RESP schedule.
c1,c2,c3,c4=(28,40,52,62)
schedule={}
for mode in "CDEF":
 label="R1acRowSync"+mode+":\n"
 end=" BPL R1acRowSync"+mode+"\n"
 assert src.count(label)==src.count(end)==1
 before,rest=src.split(label,1)
 old,after=rest.split(end,1)
 assert old.startswith(" STA WSYNC\n") and old.count("STA RESP1")==4,(mode,old[:400])
 lines=[
  " STA WSYNC",
  " LDX FemaleRows,Y",
  " LDA PlayerRows,Y",
  " STA GRP0",
  " LDA ShotEnable,Y",
  " STA ENAM0",
  " LDA MaleRows,Y",
  " BIT FRAMELO",
  " STA RESP1",
  " NOP",
  " STA GRP1",
  " NOP",
  " NOP",
  " STA RESP1",
  " STX GRP1",
  " LDA SmallMaleRows,Y",
  " NOP",
  " STA RESP1",
  " STA GRP1",
  " LDA SmallFemaleRows,Y",
  " STA RESP1",
  " STA GRP1",
  " DEY"
 ]
 src=before+label+"\n".join(lines)+"\n"+end+after
 schedule[mode]={"first_male_RESP1_cycle":c1,"second_female_RESP1_cycle":c2,
                 "third_small_male_RESP1_cycle":c3,"fourth_small_female_RESP1_cycle":c4,
                 "estimated_next_WSYN C_deadline":c4+11,
                 "NUSIZ1":3,"target":"auto-copy extra M and F at +33 color clocks"}
for name in ("MaleRows","FemaleRows","SmallMaleRows","SmallFemaleRows","PlayerRows","ShotEnable"):
 mark="\n"+name+":\n"
 assert original.count(mark)==src.count(mark)==1
 assert original.split(mark,1)[1].split("\n",1)[0]==src.split(mark,1)[1].split("\n",1)[0]
(R/"r1al.asm").write_text(src)
subprocess.run(["dasm","r1al.asm","-f3","-or1al_4k.bin","-lr1al.lst","-sr1al.sym"],cwd=R,check=True)
four=(R/"r1al_4k.bin").read_bytes();assert len(four)==4096
rom=four*4;sha=hashlib.sha256(rom).hexdigest()
(R/"r1al_F6.bin").write_bytes(rom)
(R/"ROM_SHA256.txt").write_text(sha+"  r1al_F6.bin\n")
manifest={
 "status":"BUILT_UNVERIFIED_R1AL_SIX_SOURCE_PERFECT_P1_HYPOTHESIS",
 "pinned_R1aj_four_source_original_mask_SHA256":PIN,
 "NUSIZ1_value":3,
 "four_original_P1_mask_bytes":"unaltered",
 "player_P0_M0":"unaltered",
 "timing":schedule,"ROM_SHA256":sha,"bytes":16384,
 "format":"F6 16KB NTSC with identical banks",
 "limits":"RESEARCH ONLY: no free X and no independent VERIFICATION"}
(R/"manifest.json").write_text(json.dumps(manifest,indent=2)+"\n")
print(json.dumps(manifest,indent=2))
