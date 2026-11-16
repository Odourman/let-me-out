#!/usr/bin/env python3
"""R1ae MAIN III isolated research: remove last TWO white ghost pixels.

Pinned R1ad real-Stella baseline 487/600 exact, 113/600 fail due exactly
white x67–68 on FIRST NPC raster row when first male P1 X=87.
No original bitmap bits missing, player and shot 600/600, four P1-X
pairs independently varying. R1ad loads male GRP1 at c33/35.
R1ae relocates exactly one NOP (2 cycles) BEFORE first STA GRP1:
male first GRP1 c35/37; keeps RESP1 c30/32 and c42/44 unchanged.
No extra CPU cycles; no format/mask/canon changes.
"""
from pathlib import Path
import subprocess,hashlib,json
ROOT=Path(__file__).resolve().parent
PARENT=ROOT.parent/"main_iii_r1ad_delay_grp1"
subprocess.run(["/usr/bin/python3",str(PARENT/"build_r1ad.py")],check=True)
pin="38d910cc9980c9f6d8f57303df02f3cd87c0fe8ab32dbb19041786a9406a14f1"
assert hashlib.sha256((PARENT/"r1ad_F6.bin").read_bytes()).hexdigest()==pin,"R1ad tested ROM mismatch"
old=(PARENT/"r1ad.asm").read_text()
src=old
modes={"C":(30,42),"D":(32,42),"E":(30,44),"F":(32,44)}
for mode,(c1,c2) in modes.items():
 label=f"R1acRowSync{mode}:\n";end=f" BPL R1acRowSync{mode}\n"
 assert src.count(label)==src.count(end)==1
 a,rest=src.split(label,1)
 mid,b=rest.split(end,1)
 oldsegment=" STA RESP1\n STA GRP1\n NOP\n"
 newsegment=" STA RESP1\n NOP\n STA GRP1\n"
 assert mid.count(oldsegment)==1,("unexpected_first_resp_grp",mode)
 mid=mid.replace(oldsegment,newsegment,1)
 src=a+label+mid+end+b
# Source masks fully retained, including PlayerRows and diagnostic shot.
for label in ("MaleRows","FemaleRows","PlayerRows","ShotEnable"):
 key="\n"+label+":\n"
 assert old.count(key)==src.count(key)==1
 assert old.split(key,1)[1].split("\n",1)[0]==src.split(key,1)[1].split("\n",1)[0]
timings={}
for mode,(first,second) in modes.items():
 a=f"R1acRowSync{mode}:\n";b=f" BPL R1acRowSync{mode}\n"
 body=src.split(a,1)[1].split(b,1)[0].splitlines()
 clock=0;resets=[];male_grp=[]
 for t in body:
  t=t.strip()
  if not t or t.startswith(";") or t=="STA WSYNC":continue
  if t in ("NOP","DEY"):cy=2
  elif t.startswith(("STA ","STX ","BIT ")):cy=3
  elif t.startswith(("LDA ","LDX ")) and t.endswith(",Y"):cy=4
  else:raise ValueError(("unknown instruction",mode,t))
  clock+=cy
  if t=="STA RESP1":resets.append(clock)
  if t=="STA GRP1":male_grp.append(clock)
 assert resets==[first,second] and male_grp==[first+5],(mode,resets,male_grp)
 assert clock==second+5
 timings[mode]={"RESP1_end_cycles":resets,"male_GRP1_end_cycle":male_grp[0],"female_GRP1_end_cycle":second+3}
(ROOT/"r1ae.asm").write_text(src)
subprocess.run(["dasm","r1ae.asm","-f3","-or1ae_4k.bin","-lr1ae.lst","-sr1ae.sym"],cwd=ROOT,check=True)
four=(ROOT/"r1ae_4k.bin").read_bytes()
assert len(four)==4096
rom=four*4
sha=hashlib.sha256(rom).hexdigest()
(ROOT/"r1ae_F6.bin").write_bytes(rom)
(ROOT/"ROM_SHA256.txt").write_text(sha+"  r1ae_F6.bin\n")
d={
 "status":"BUILT_UNVERIFIED_R1AE_CYCLE_NEUTRAL_LATE_MALE_GRP1",
 "R1ad_parent_exact_sha256":pin,"ROM_SHA256":sha,"bytes":16384,"mapper":"standard F6","video":"NTSC",
 "source_masks":"original male/female/player 9-row bytes unchanged",
 "register_deadlines":timings,
 "hypothesis":"moving first GRP1 2 CPU cycles later from c33/35 to c35/37 kills 113 remaining 2-white-pixel ghost frames, without damaging first P1 bitmap",
 "goals":"600 consecutive real Stella frames, 262 lines, TWO distinct complete original masks, independent four P1-X pairs, one yellow P0 and one M0, 0 ghost",
 "limits":"strictly isolated research experiment; not all 6 NPC, not v0.18 R1, no independent Verification, no main or PR7 changes"
}
(ROOT/"manifest.json").write_text(json.dumps(d,indent=2)+"\n")
print(json.dumps(d,indent=2))
