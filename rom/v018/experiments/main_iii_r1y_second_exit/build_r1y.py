#!/usr/bin/env python3
"""R1y: another VBLANK +3 CPU cycles shift from verified R1x.
Tests 8 M0 X 286..300 across and beyond second female P1.
The 14 scanline five-NPC kernel and all four variants are unchanged.
No assertion of acceptance before actual Stella 600-frame evidence.
"""
from pathlib import Path
import hashlib,subprocess,json,sys
ROOT=Path(__file__).resolve().parent
BASE=ROOT.parent/"main_iii_r1x_second_p1"
subprocess.run([sys.executable,str(BASE/"build_r1x.py")],check=True)
pin="15b65be5d2baf810576f58dc9fbe6d9a8b62b540d50b04ff2fa7a1dec6fab613"
rom=(BASE/"r1x_F6.bin").read_bytes()
assert hashlib.sha256(rom).hexdigest()==pin,"R1x fixed reference drift"
old=(BASE/"r1x.asm").read_text()
anchor=""" BIT FRAMELO
 STA RESM0
 STA WSYNC"""
assert old.count(anchor)==1
src=old.replace(anchor,""" BIT FRAMELO
 ; R1y another additional 3 cycles before RESM0 (+9 TIA color clocks)
 BIT FRAMELO
 STA RESM0
 STA WSYNC""")
for name in ("MaleRows","FemaleRows","SmallMaleRows","SmallFemaleRows","PlayerRows"):
 for suf in ("","14"):
  key="\n"+name+suf+":\n"
  assert old.count(key)==src.count(key)==1
  assert old.split(key,1)[1].split("\n",1)[0]==src.split(key,1)[1].split("\n",1)[0]
for suffix in "ABCD":
 a=f"R1oShot{suffix}:\n"; b=f"R1oLower{suffix}:\n"
 assert old.split(a,1)[1].split(b,1)[0]==src.split(a,1)[1].split(b,1)[0]
(ROOT/"r1y.asm").write_text(src)
subprocess.run(["dasm","r1y.asm","-f3","-or1y_4k.bin","-lr1y.lst","-sr1y.sym"],cwd=ROOT,check=True)
b=(ROOT/"r1y_4k.bin").read_bytes()
assert len(b)==4096
out=b*4
sha=hashlib.sha256(out).hexdigest()
(ROOT/"r1y_F6.bin").write_bytes(out)
(ROOT/"ROM_SHA256.txt").write_text(sha+"  r1y_F6.bin\n")
d=dict(status="BUILT_UNVERIFIED_R1Y_COARSE_SHOT_WINDOW",R1x_reference_sha256=pin,
 ROM_sha256=sha,standard_F6_NTSC_bytes=16384,
 expected_M0_GUI_X=[286,288,290,292,294,296,298,300],
 M0_GUI_Y=167,expected_second_P1_contact_gui_interval=[280,295],
 source_8x9_masks_identical=True,
 same_visible_14_scanline_five_NPC_kernel=True,
 limits="Research only; no full 160-CC horizontal travel, no bullet RAM, no sixth NPC, no hit target identity, no independent Verification")
(ROOT/"manifest.json").write_text(json.dumps(d,indent=2)+"\n")
print(json.dumps(d,indent=2))
