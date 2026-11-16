#!/usr/bin/env python3
"""R1q direct test of preserving C/D fourth-P0 RESP0 cycles by deferring M0 shutdown.

The fifth-NPC R1o baseline is immutable. A/B unmodified. On C and D,
move STY ENAM0 *after* the position strobes, instead of before,
to check Stella's actual duplicate-missile timing without guessing.
This may fail because duplicate M0 appears before the late shutoff.
"""
from pathlib import Path
import sys,subprocess,hashlib,json
ROOT=Path(__file__).resolve().parent
PARENT=ROOT.parent/"main_iii_r1o_single_arm_shot"
subprocess.run([sys.executable,str(PARENT/"build_r1o.py")],check=True)
oldrom=(PARENT/"r1o_F6.bin").read_bytes()
BASE="41a1b55a4d413cca88eccd690d29b6af1a041e4a354e0f4838a832f10fd6c44d"
assert hashlib.sha256(oldrom).hexdigest()==BASE
old=(PARENT/"r1o.asm").read_text()
src=old
c_old=""" STX GRP0
 ; Loading white A (2 cycles) while bitmap already in GRP0.
 STY ENAM0
 LDA #$0E
 STA RESP0
 STA COLUP0
 ; Seven cycles: third P1's original mask; preserves 76-cycle budget.
 STX.w GRP1
 STA RESP1

 DEY
 JMP R1oLowerC"""
c_new=""" STX GRP0
 ; R1q probe: restore c53 RESP0; turn M0 off after positioning.
 LDA #$0E
 STA RESP0
 STY ENAM0
 STA COLUP0
 ; Seven cycles: third P1's original mask; preserves 76-cycle budget.
 STX.w GRP1
 STA RESP1

 DEY
 JMP R1oLowerC"""
assert src.count(c_old)==1
src=src.replace(c_old,c_new)
d_old=""" STX GRP0
 STY ENAM0
 LDA #$0E
 STA COLUP0
 STA RESP0
 ; Seven cycles: third P1's original mask; preserves 76-cycle budget.
 STX.w GRP1
 STA RESP1

 DEY
 JMP R1oLowerD"""
d_new=""" STX GRP0
 ; R1q probe: restore c56 RESP0; turn M0 off after positioning.
 LDA #$0E
 STA COLUP0
 STA RESP0
 STY ENAM0
 ; Seven cycles: third P1's original mask; preserves 76-cycle budget.
 STX.w GRP1
 STA RESP1

 DEY
 JMP R1oLowerD"""
assert src.count(d_old)==1
src=src.replace(d_old,d_new)
for label in ["MaleRows","FemaleRows","SmallMaleRows","SmallFemaleRows","PlayerRows"]:
    for suffix in ["","14"]:
        orig=old.split(label+suffix+":\n",1)[1].split("\n",1)[0]
        new=src.split(label+suffix+":\n",1)[1].split("\n",1)[0]
        assert orig==new
(ROOT/"r1q.asm").write_text(src)
subprocess.run(["dasm","r1q.asm","-f3","-or1q_4k.bin","-lr1q.lst","-sr1q.sym"],check=True,cwd=ROOT)
raw=(ROOT/"r1q_4k.bin").read_bytes()
assert len(raw)==4096
rom=raw*4
sha=hashlib.sha256(rom).hexdigest()
(ROOT/"r1q_F6.bin").write_bytes(rom)
(ROOT/"ROM_SHA256.txt").write_text(sha+"  r1q_F6.bin\n")
(ROOT/"build_manifest.json").write_text(json.dumps({
 "type":"RESEARCH HYPOTHESIS, do not claim success until Stella",
 "rom_SHA256":sha,"source_R1o":BASE,
 "test":"C/D fourth RESP0 original cycles, M0 shutoff after C/D strobe",
 "C_end_cycle_disable":56,"D_end_cycle_disable":59,
 "risk":"M0 automatic duplicate at approx 55 cycles",
 "five_original_NPC_masks":"unchanged",
 "shot_expected":"one yellow at player hand x232, y167",
 "full_R1":"FAIL/BLOCKED"
},indent=2)+"\n")
print(sha)
