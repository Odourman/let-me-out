#!/usr/bin/env python3
"""R1au RESEARCH: use the exact proven six-Android three-layout runtime
R1at ROM; change ONLY the pre-WSYNC selector's 4th 8-frame slot
from A to B, yielding A->B->C->B->A (one large pair moves each switch).
All nine 8x9 mask scanline kernels remain byte-for-byte identical.
"""
from pathlib import Path
import sys,subprocess,hashlib,json
R=Path(__file__).resolve().parent
P=R.parent/"main_iv_r1at_runtime_three"
subprocess.run([sys.executable,str(P/"build_r1at.py")],check=True)
PIN="486dca4b574d9a394075788bc974232d3b7452282f282e46c7dd3fca454d2c0a"
assert hashlib.sha256((P/"r1at_F6.bin").read_bytes()).hexdigest()==PIN,"Not approved source-perfect R1at three-runtime reference"
old=(P/"r1at.asm").read_text()
needle=" CMP #$10\n BEQ R1atJumpC\n JMP R1atA\nR1atJumpA:\n"
replacement=" CMP #$10\n BEQ R1atJumpC\n JMP R1atB\nR1atJumpA:\n"
assert old.count(needle)==1,"Unexpected dispatch sequence; do not touch raster code"
src=old.replace(needle,replacement,1)
assert src.replace(replacement,needle,1)==old,"More than one source change"
for name in ("MaleRows","FemaleRows","SmallMaleRows","SmallFemaleRows","PlayerRows","ShotEnable"):
 marker="\n"+name+":\n"
 assert old.count(marker)==src.count(marker)==1
 assert old.split(marker,1)[1].split("\n",1)[0]==src.split(marker,1)[1].split("\n",1)[0]
(R/"r1au.asm").write_text(src)
subprocess.run(["dasm","r1au.asm","-f3","-or1au_4k.bin","-lr1au.lst","-sr1au.sym"],cwd=R,check=True)
four=(R/"r1au_4k.bin").read_bytes()
assert len(four)==4096
rom=four*4
sha=hashlib.sha256(rom).hexdigest()
(R/"r1au_F6.bin").write_bytes(rom)
(R/"ROM_SHA256.txt").write_text(sha+"  r1au_F6.bin\n")
meta={
 "status":"BUILT_UNVERIFIED_R1AU_ONE_PAIR_MOVES_PER_TRANSITION",
 "pinned_source_R1at_ROM_SHA256":PIN,
 "only_change":"Before nine WSYNC: 4th 8-frame selector slot JMP R1atA to JMP R1atB",
 "source_original_8x9_masks":"All six original Android instances and original P0/M0 bytes unchanged",
 "three_preverified_P1_schedules":{"A":[28,40,56,66],"B":[28,42,56,66],"C":[30,42,56,66]},
 "runtime_sequence_every_eight_frames":"A,B,C,B; repeat, so one large pair changes per boundary",
 "NUSIZ1":3,
 "ROM_SHA256":sha,"bytes":16384,"mapper":"standard F6 four identical banks",
 "limits":"RESEARCH: three X layouts, NUSIZ duplicate pairs fixed relative spacing, no six independent X or full R1/R4, no independent VERIFICATION"}
(R/"manifest.json").write_text(json.dumps(meta,indent=2)+"\n")
print(json.dumps(meta,indent=2))
