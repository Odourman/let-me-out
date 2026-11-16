#!/usr/bin/env python3
"""R1at research: advance FIRST P1 RESP1 by 2 or 4 CPU cycles while holding
male GRP1 end time and ALL female/small P1 reset end times constant.
This isolates male X from female X in the known exact six-mask R1aq ROM.
No game production or independent Verification.
"""
from pathlib import Path
import subprocess,hashlib,os,sys,json,re
R=Path(__file__).resolve().parent
P=R.parent/"main_iv_r1aq_timing"
subprocess.run([sys.executable,str(P/"build_r1aq.py")],
 env=dict(os.environ,R1AQ_BATCH="0"),check=True)
PIN="09e262958e9452ec3f61c3d93f2eea19ad03cda7ac52767ae72608e2f7b3a94b"
assert hashlib.sha256((P/"r1aq_F6.bin").read_bytes()).hexdigest()==PIN
old=(P/"r1aq.asm").read_text()
batch=int(os.environ.get("R1AT_BATCH","0"))
assert batch in (0,1)
pre_nops=3-batch
post_nops=2+batch
pattern=re.compile(r"( LDA #\$[0-9A-F]{2}\n)(?: NOP\n){4}( STA RESP1\n) NOP\n( STA GRP1\n NOP\n NOP\n STA RESP1\n)")
src,n=pattern.subn(
 lambda m:m.group(1)+" NOP\n"*pre_nops+m.group(2)+" NOP\n"*post_nops+m.group(3),old)
assert n==9,("missing first P1 timing per row",n)
assert old.count(" STA RESP1\n")==src.count(" STA RESP1\n")==36
for name in ("MaleRows","FemaleRows","SmallMaleRows","SmallFemaleRows","PlayerRows","ShotEnable"):
 mark="\n"+name+":\n"
 assert old.count(mark)==src.count(mark)==1
 assert old.split(mark,1)[1].split("\n",1)[0]==src.split(mark,1)[1].split("\n",1)[0]
(R/"r1at.asm").write_text(src)
subprocess.run(["dasm","r1at.asm","-f3","-or1at_4k.bin","-lr1at.lst","-sr1at.sym"],cwd=R,check=True)
four=(R/"r1at_4k.bin").read_bytes();assert len(four)==4096
rom=four*4;sha=hashlib.sha256(rom).hexdigest()
(R/"r1at_F6.bin").write_bytes(rom)
(R/"ROM_SHA256.txt").write_text(sha+"  r1at_F6.bin\n")
meta={"status":"BUILT_UNVERIFIED_R1AT_MALE_ONLY_EARLIER_X",
 "baseline_R1aq_ROM_SHA256":PIN,
 "batch":batch,"NUSIZ1_value":3,
 "first_male_RESP1_cycle":26-2*batch,
 "first_male_GRP1_cycle":"unchanged from parent R1aq",
 "female_RESP1_cycle":40,
 "small_male_RESP1_cycle":56,
 "small_female_RESP1_cycle":66,
 "all_four_original_source_masks":"byte-identical",
 "P0_player_and_single_M0_shot":"unchanged",
 "ROM_SHA256":sha,"bytes":16384,"NTSC_scanlines_target":262,
 "scope":"Research only: fixed 6-instance X, no free motion, no full R1, no independent Verification"}
(R/"manifest.json").write_text(json.dumps(meta,indent=2)+"\n")
print(json.dumps(meta,indent=2))
