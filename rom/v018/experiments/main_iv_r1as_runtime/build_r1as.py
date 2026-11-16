#!/usr/bin/env python3
"""R1as RESEARCH: ONE 16 KB F6 NTSC ROM with TWO alternate six-original-mask
nine-raster-scanline kernels selected at runtime every 8 Stella frames.
Prove visible movement of only FEMALE duplicated P1 group while preserving
2M, 2F, SM, SF and full P0 and M0. NOT full six independent free X.
"""
from pathlib import Path
import sys,os,subprocess,hashlib,json
R=Path(__file__).resolve().parent
A=R.parent/"main_iv_r1aq_timing"
B=R.parent/"main_iv_r1ar_x_variants"
subprocess.run([sys.executable,str(A/"build_r1aq.py")],
 env=dict(os.environ,R1AQ_BATCH="0"),check=True)
subprocess.run([sys.executable,str(B/"build_r1ar.py")],
 env=dict(os.environ,R1AR_BATCH="0"),check=True)
PIN_A="09e262958e9452ec3f61c3d93f2eea19ad03cda7ac52767ae72608e2f7b3a94b"
PIN_B="55b5c8b0a85d657a23b00eacc3ce0738ce0defff725e3e630c96c5f0eb59852d"
assert hashlib.sha256((A/"r1aq_F6.bin").read_bytes()).hexdigest()==PIN_A
assert hashlib.sha256((B/"r1ar_F6.bin").read_bytes()).hexdigest()==PIN_B
srcA=(A/"r1aq.asm").read_text()
srcB=(B/"r1ar.asm").read_text()
start="R1acSelect:\n";end="R1acAfterRows:\n"
assert srcA.count(start)==srcB.count(start)==1
assert srcA.count(end)==srcB.count(end)==1
headA,partA=srcA.split(start,1);blockA,tailA=partA.split(end,1)
headB,partB=srcB.split(start,1);blockB,tailB=partB.split(end,1)
assert headA==headB and tailA==tailB,"Only position timings may differ"
old=" JMP R1apNineRows\nR1apNineRows:\n"
assert blockA.startswith(old) and blockB.startswith(old)
blockA=blockA[len(old):].replace("R1apScan","R1asAScan")
blockB=blockB[len(old):].replace("R1apScan","R1asBScan")
assert blockA.count(" STA RESP1\n")==blockB.count(" STA RESP1\n")==36
# Branch selects a DIFFERENT kernel BEFORE first visible WSYNC, never
# branches inside a 9-scanline critical section. White P1 and P0/M0 bytes unchanged.
dispatch=("R1acSelect:\n"
 " LDA FRAMELO\n"
 " AND #$08\n"          # each scene remains visible for 8 consecutive frames
 " BEQ R1asA\n"
 " JMP R1asB\n"
 "R1asA:\n"+blockA+
 " JMP R1acAfterRows\n"
 "R1asB:\n"+blockB+
 " JMP R1acAfterRows\n"
 "R1acAfterRows:\n")
src=headA+dispatch+tailA
for name in ("MaleRows","FemaleRows","SmallMaleRows","SmallFemaleRows","PlayerRows","ShotEnable"):
 mark="\n"+name+":\n"
 assert srcA.count(mark)==src.count(mark)==1
 assert srcA.split(mark,1)[1].split("\n",1)[0]==src.split(mark,1)[1].split("\n",1)[0]
(R/"r1as.asm").write_text(src)
subprocess.run(["dasm","r1as.asm","-f3","-or1as_4k.bin","-lr1as.lst","-sr1as.sym"],cwd=R,check=True)
raw=(R/"r1as_4k.bin").read_bytes()
assert len(raw)==4096
rom=raw*4;sha=hashlib.sha256(rom).hexdigest()
(R/"r1as_F6.bin").write_bytes(rom)
(R/"ROM_SHA256.txt").write_text(sha+"  r1as_F6.bin\n")
meta={
 "status":"BUILT_UNVERIFIED_R1AS_RUNTIME_TWO_ALTERNATE_SIX_MASK_SCENES",
 "parent_A_rom_sha":PIN_A,"parent_B_rom_sha":PIN_B,
 "two_P1_schedules":{"A":[28,40,56,66],"B":[28,42,56,66]},
 "runtime_selector":"FRAMELO bit3; eight-frame hold per scene",
 "frame_correct_required":"600 real Stella frames with exactly two distinct fully intact six-mask layouts and full P0 M0",
 "NUSIZ1_value":3,
 "source_masks":"Original 8x9 bitmap bytes unchanged; both kernels use canonical immediate row bytes",
 "ROM_SHA256":sha,"bytes":16384,
 "mapper":"standard F6 4 copies of one 4KiB data bank",
 "scope":"Research only: two precomputed X states for doubled female P1 group, not all 6 independently positionable, no full R1/R4 or independent Verification"}
(R/"manifest.json").write_text(json.dumps(meta,indent=2)+"\n")
print(json.dumps(meta,indent=2))
