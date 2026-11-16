#!/usr/bin/env python3
"""R1z: cycle-neutral D-only ENAM0 shutoff/collision-window experiment.

Pinned to R1y failing exact 16 KiB ROM. D's STA COLUP0 moves from c59
to c53, while STY ENAM0 moves c53->c59 and STA RESP0 remains c56.
This is JUST A HYPOTHESIS; an early COLUP0 may recolor M0 white and
the test MUST reject it if so. Other 3 shot kernels untouched.
Inspired by Berzerk's independent scanline missile scheduling, not
a claim to have copied Berzerk's timing or source.
"""
from pathlib import Path
import hashlib,subprocess,json,sys
ROOT=Path(__file__).resolve().parent
BASE=ROOT.parent/"main_iii_r1y_second_exit"
subprocess.run([sys.executable,str(BASE/"build_r1y.py")],check=True)
pin="aaf9ecf5b6698e1df75e9c0f70c114a913711d1edf99b4ef48ef8f7ad40e02b0"
rom=(BASE/"r1y_F6.bin").read_bytes()
assert hashlib.sha256(rom).hexdigest()==pin,"R1y source changed: stop"
old=(BASE/"r1y.asm").read_text()
start="R1oShotD:\n"; end="R1oLowerD:\n"
assert old.count(start)==old.count(end)==1
pre,rest=old.split(start,1)
shot,post=rest.split(end,1)
needle=""" ; R1w D: M0 off c53, original RESP0 c56 and late white at c59.
 LDA #$0E
 STX GRP0
 STY ENAM0
 STA RESP0
 STA COLUP0"""
replace=""" ; R1z test D: COLUP0 white at c53, RESP0 unchanged c56, M0 off c59.
 ; This MAY recolor M0 white. Strict Stella audit must reject that.
 LDA #$0E
 STX GRP0
 STA COLUP0
 STA RESP0
 STY ENAM0"""
assert shot.count(needle)==1
shot=shot.replace(needle,replace)
src=pre+start+shot+end+post
for name in ("MaleRows","FemaleRows","SmallMaleRows","SmallFemaleRows","PlayerRows"):
 for suf in ("","14"):
  label="\n"+name+suf+":\n"
  assert old.count(label)==src.count(label)==1
  assert old.split(label,1)[1].split("\n",1)[0]==src.split(label,1)[1].split("\n",1)[0]
for c in "ABC":
 a=f"R1oShot{c}:\n";b=f"R1oLower{c}:\n"
 assert old.split(a,1)[1].split(b,1)[0]==src.split(a,1)[1].split(b,1)[0]
(ROOT/"r1z.asm").write_text(src)
subprocess.run(["dasm","r1z.asm","-f3","-or1z_4k.bin","-lr1z.lst","-sr1z.sym"],check=True,cwd=ROOT)
raw=(ROOT/"r1z_4k.bin").read_bytes()
assert len(raw)==4096
final=raw*4
sha=hashlib.sha256(final).hexdigest()
(ROOT/"r1z_F6.bin").write_bytes(final)
(ROOT/"ROM_SHA256.txt").write_text(sha+"  r1z_F6.bin\n")
m=dict(status="BUILT_UNVERIFIED_R1Z_D_LATE_OFF",pinned_R1y_SHA256=pin,
ROM_SHA256=sha,bytes=16384,
D_M0_off_end_cycle=59,D_colup0_white_end_cycle=53,
D_fourth_RESP0_end_cycle=56,
expected_shot_x=[286,288,290,292,294,296,298,300],
expected_full_mask_source_bytes_unchanged=True,
test="600 real Stella frames 64 states all five 14row NPC, exactly ONE yellow M0 at y167, true CXM0P latch, no ghost/white missile",
risk="early white COLUP0 may recolor live M0. A FAIL is honest outcome, not R1 approval.",
limits="Not full room, not actual bullet state, not 6 free-X NPC, not independent verification")
(ROOT/"manifest.json").write_text(json.dumps(m,indent=2)+"\n")
print(json.dumps(m,indent=2))
