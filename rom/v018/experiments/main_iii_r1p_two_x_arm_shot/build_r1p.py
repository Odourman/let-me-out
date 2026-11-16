#!/usr/bin/env python3
"""R1p: scope-reduced fully auditable research probe.

R1o currently proves five original NPC + one M0 shot at the hand in
fourth-small-NPC positions A/B only, while C/D lose a single exact row.
This experiment deliberately selects A/B only and tests 600/600 frames;
it does NOT claim that all four P0 positions work, or full R1.
"""
from pathlib import Path
import hashlib,subprocess,sys,json
ROOT=Path(__file__).resolve().parent
BASE=ROOT.parent/"main_iii_r1o_single_arm_shot"
subprocess.run([sys.executable,str(BASE/"build_r1o.py")],check=True)
parent_rom=(BASE/"r1o_F6.bin").read_bytes()
EXPECTED="41a1b55a4d413cca88eccd690d29b6af1a041e4a354e0f4838a832f10fd6c44d"
assert hashlib.sha256(parent_rom).hexdigest()==EXPECTED, "R1o base changed"
src=(BASE/"r1o.asm").read_text()
start=src.index(" LDY #4\n ; Select independent fourth-NPC X once per frame")
end=src.index("R1gRowsA:\n",start)
assert src[start:end].count(" JMP R1gRowsC\n")==1
oldselect=src[start:end]
selector=""" LDY #4
 ; R1p STRICTLY REDUCED two proven P0 positions A/B, plus door bit6.
 LDA FRAMELO
 AND #$10
 BEQ R1pChooseA
 JMP R1gRowsB
R1pChooseA:
 JMP R1gRowsA
"""
src=src[:start]+selector+src[end:]
assert "R1gRowsC:\n" in src and "R1gRowsD:\n" in src
# C/D remain in source for exact audit context but cannot be selected.
assert src.split("R1gRowsA:\n",1)[1]==(BASE/"r1o.asm").read_text().split("R1gRowsA:\n",1)[1]
(ROOT/"r1p.asm").write_text(src)
subprocess.run(["dasm","r1p.asm","-f3","-or1p_4k.bin","-lr1p.lst","-sr1p.sym"],cwd=ROOT,check=True)
raw=(ROOT/"r1p_4k.bin").read_bytes()
assert len(raw)==4096
rom=raw*4
sha=hashlib.sha256(rom).hexdigest()
(ROOT/"r1p_F6.bin").write_bytes(rom)
(ROOT/"ROM_SHA256.txt").write_text(sha+"  r1p_F6.bin\n")
info={
 "status":"BUILT_UNVERIFIED_R1P_TWO_X_ONLY",
 "baseline_R1o_SHA256":EXPECTED,"ROM_SHA256":sha,"F6_bytes":len(rom),
 "fourth_P0_GUI_X_exact":[330,348],
 "intentionally_NOT_supported_P0_GUI_X":[360,378],
 "target_states":"2 P0 fourth X times 2 right-door states = 4",
 "five_NPC":"two large female, large male, small male, small female, full 14 display rows",
 "projectile":"one static M0 GUI x232 y167 from yellow player's arm, no extra shot/clones",
 "limits":"Research-only 2/4 P0-X positions, static shot, no six NPC/full R1/free 160CC independent X; separate independent VERIFICATION needed."
}
(ROOT/"build_manifest.json").write_text(json.dumps(info,indent=2)+"\n")
print(json.dumps(info,indent=2))
