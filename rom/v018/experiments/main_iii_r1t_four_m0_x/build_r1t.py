#!/usr/bin/env python3
"""R1t: vary M0 fine position on 4 independent 4-frame phases using HMM0.

This is a strictly bounded fine-position proof, NOT full horizontal travel.
All five NPC mask bytes, their four P0 X states, 14 displayed rows, fixed
M0 scanline ENAM0 gating, and 262 NTSC baseline are preserved.
"""
from pathlib import Path
import hashlib,json,subprocess,sys,re
ROOT=Path(__file__).resolve().parent
PARENT=ROOT.parent/"main_iii_r1s_reorder_arm_shot"
subprocess.run([sys.executable,str(PARENT/"build_r1s.py")],check=True)
rom=(PARENT/"r1s_F6.bin").read_bytes()
EXPECTED="33ab04b95ca6f649593e50082bf17275b605caea282e6e044aeb49abf93d1d85"
assert hashlib.sha256(rom).hexdigest()==EXPECTED,"R1s changed – STOP"
old=(PARENT/"r1s.asm").read_text()
original="""R1hSetBall:
 STA RESBL
 STA WSYNC
 ; Shift BALL left by 2CC during blank scanline. Never HMOVE in NPC rows.
R1hHMOVE:
 STA HMOVE"""
modified="""R1hSetBall:
 STA RESBL
 ; Trick 24: ROM lookup, trick 10: HMM0 fine motion.
 ; Bits 2-3 change every four frames, INDEPENDENT of P0 fourth-X
 ; selector bits 4-5 and right-door bit 6.
 LDA FRAMELO
 AND #$0C
 LSR
 LSR
 TAX
 LDA R1tM0Motion,X
 STA HMM0
 STA WSYNC
 ; ALL fine motion is still applied outside visible NPC scanlines.
R1hHMOVE:
 STA HMOVE"""
assert old.count(original)==1
src=old.replace(original,modified)
anchor=" ORG $FFFA\n"
assert src.count(anchor)==1
src=src.replace(anchor,"; Four TIA fine-motion positions: -4CC,-3CC,-2CC,-1CC\nR1tM0Motion:\n BYTE $40,$30,$20,$10\n"+anchor)
for label in ("MaleRows","FemaleRows","SmallMaleRows","SmallFemaleRows","PlayerRows"):
 for suf in ("","14"):
  key=label+suf+":\n"
  assert old.count("\n"+key)==src.count("\n"+key)==1, key
  assert old.split("\n"+key,1)[1].split("\n",1)[0]==src.split("\n"+key,1)[1].split("\n",1)[0],key
for suffix in "ABCD":
 for token in (f"R1oShot{suffix}:\n",f"R1oLower{suffix}:\n"):
  assert src.split(token,1)[1].split("\n",1)[0]==old.split(token,1)[1].split("\n",1)[0]
(ROOT/"r1t.asm").write_text(src)
subprocess.run(["dasm","r1t.asm","-f3","-or1t_4k.bin","-lr1t.lst","-sr1t.sym"],cwd=ROOT,check=True)
base=(ROOT/"r1t_4k.bin").read_bytes()
assert len(base)==4096
built=base*4
sha=hashlib.sha256(built).hexdigest()
(ROOT/"r1t_F6.bin").write_bytes(built)
(ROOT/"ROM_SHA256.txt").write_text(sha+"  r1t_F6.bin\n")
info={
 "status":"BUILT_UNVERIFIED_R1T_M0_HMOVE",
 "r1s_PINNED_SHA256":EXPECTED,
 "rom_SHA256":sha,
 "F6_ntsc_bytes":len(built),
 "HMM0_table":["$40","$30","$20","$10"],
 "expected_GUI_missile_x":[232,234,236,238],
 "M0_GUI_y":167,
 "independent_phase_bits":{"M0":"FRAMELO & $0C","fourth_NPC_P0":"FRAMELO & $30","door":"FRAMELO & $40"},
 "tested_combinations_target":4*4*2,
 "limits":"Fine movement over four positions only. Does not prove continuous projectile across full screen, collision detection or sixth NPC."
}
(ROOT/"build_manifest.json").write_text(json.dumps(info,indent=2)+"\n")
print(json.dumps(info,indent=2))
