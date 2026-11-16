#!/usr/bin/env python3
"""R1w: Retimes M0 shutoff without adding cycles to any four NPC-X kernels.

Move only active shot-row writes after R1v RESM0 +9CC coarse positioning:
  A/B M0 off c54 -> c56, white P0 c59 UNCHANGED
  C   M0 off c48 -> c56, RESP0 c53 and white c59 UNCHANGED
  D   M0 off c48 -> c53, RESP0 c56, white c53 -> c59
Each kernel retains identical total 6502 cycles and fourth-P0 RESP0 times.
Strict 600-Stella-frame test decides, not these comments.
"""
from pathlib import Path
import hashlib,json,subprocess,sys
ROOT=Path(__file__).resolve().parent
BASE=ROOT.parent/"main_iii_r1v_resm0_overlap"
subprocess.run([sys.executable,str(BASE/"build_r1v.py")],check=True)
rom=(BASE/"r1v_F6.bin").read_bytes()
PIN="0110ae7cdf33aee5af75b008c2cdd091bffc3abce85dc3b43a0bcc3f07c3ffe3"
assert hashlib.sha256(rom).hexdigest()==PIN,"R1v base changed"
old=(BASE/"r1v.asm").read_text()
src=old
# Replace ONLY the one-row M0 shot kernel segment, not top/bottom rows.
for s in "ABCD":
 start=f"R1oShot{s}:\n";end=f"R1oLower{s}:\n"
 assert src.count(start)==src.count(end)==1
 head,rest=src.split(start,1)
 shot,tail=rest.split(end,1)
 if s in "AB":
  before=""" STY ENAM0
 LDA #$0E
 STA COLUP0"""
  after=""" LDA #$0E
 STY ENAM0
 STA COLUP0"""
 elif s=="C":
  before=""" ; R1s C: disable M0 at c48; restore RESP0 at original c53.
 ; The small female does not draw until after delayed GRP0 at c56.
 STY ENAM0
 LDA #$0E
 STA RESP0
 STX GRP0
 STA COLUP0"""
  after=""" ; R1w C: restore RESP0 at c53 and move M0 off to c56.
 STX GRP0
 LDA #$0E
 STA RESP0
 STY ENAM0
 STA COLUP0"""
 else:
  before=""" ; R1s D: disable M0 at c48; restore RESP0 at original c56.
 ; The small female does not draw until after delayed GRP0 at c59.
 STY ENAM0
 LDA #$0E
 STA COLUP0
 STA RESP0
 STX GRP0"""
  after=""" ; R1w D: M0 off c53, original RESP0 c56 and late white at c59.
 LDA #$0E
 STX GRP0
 STY ENAM0
 STA RESP0
 STA COLUP0"""
 assert shot.count(before)==1,(s,shot)
 shot=shot.replace(before,after)
 src=head+start+shot+end+tail
for name in ("MaleRows","FemaleRows","SmallMaleRows","SmallFemaleRows","PlayerRows"):
 for suf in ("","14"):
  label="\n"+name+suf+":\n"
  assert old.count(label)==src.count(label)==1
  assert old.split(label,1)[1].split("\n",1)[0]==src.split(label,1)[1].split("\n",1)[0]
# Only shot rows changed; all top and lower 13 rows should be byte-identical.
for s in "ABCD":
 for label in (f"R1gRows{s}:\n",f"R1oLower{s}:\n"):
  before=old.split(label,1)[1].split("\n",1)[0]
  after=src.split(label,1)[1].split("\n",1)[0]
  assert before==after
(ROOT/"r1w.asm").write_text(src)
subprocess.run(["dasm","r1w.asm","-f3","-or1w_4k.bin","-lr1w.lst","-sr1w.sym"],check=True,cwd=ROOT)
base=(ROOT/"r1w_4k.bin").read_bytes()
assert len(base)==4096
built=base*4
sha=hashlib.sha256(built).hexdigest()
(ROOT/"r1w_F6.bin").write_bytes(built)
(ROOT/"ROM_SHA256.txt").write_text(sha+"  r1w_F6.bin\n")
manifest=dict(status="BUILT_UNVERIFIED_R1W",parent_R1v_ROM_sha256=PIN,
ROM_sha256=sha,bytes=16384,
M0_expected_gui_x=[250,252,254,256,258,260,262,264],
M0_gui_y=167,original_masks_and_latches="source unchanged",
kernel_off_endcycles={"A":56,"B":56,"C":56,"D":53},
critical_resp0_endcycles={"C":53,"D":56},
goal="all 600 real Stella images no cloned missile; all five original NPCs; real CXM0P collision only when first female overlaps; all 64 modes",
limits="research only, no shot across room, no firebutton, no gameplay, five NPCs, no independent verification")
(ROOT/"manifest.json").write_text(json.dumps(manifest,indent=2)+"\n")
print(json.dumps(manifest,indent=2))
