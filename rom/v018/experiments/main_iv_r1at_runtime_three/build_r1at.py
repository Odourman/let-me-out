#!/usr/bin/env python3
"""R1at isolated research-only: ONE standard 16 KB F6/NTSC ROM with
THREE runtime-selected canonical six-original-NPC drawing kernels.
Alternates A (base), B (female group +2 CPU cycles), C (male group +2
CPU cycles after B). Must show 3 distinct source-perfect six-mask
X-position signatures in same real Stella run. NOT free X or full game.
"""
from pathlib import Path
import sys,os,subprocess,hashlib,json
R=Path(__file__).resolve().parent
A=R.parent/"main_iv_r1aq_timing"
P=R.parent/"main_iv_r1ar_x_variants"
subprocess.run([sys.executable,str(A/"build_r1aq.py")],
 env=dict(os.environ,R1AQ_BATCH="0"),check=True)
SHA_A="09e262958e9452ec3f61c3d93f2eea19ad03cda7ac52767ae72608e2f7b3a94b"
assert hashlib.sha256((A/"r1aq_F6.bin").read_bytes()).hexdigest()==SHA_A
srcA=(A/"r1aq.asm").read_text()
subprocess.run([sys.executable,str(P/"build_r1ar.py")],
 env=dict(os.environ,R1AR_BATCH="0"),check=True)
SHA_B="55b5c8b0a85d657a23b00eacc3ce0738ce0defff725e3e630c96c5f0eb59852d"
assert hashlib.sha256((P/"r1ar_F6.bin").read_bytes()).hexdigest()==SHA_B
srcB=(P/"r1ar.asm").read_text()
subprocess.run([sys.executable,str(P/"build_r1ar.py")],
 env=dict(os.environ,R1AR_BATCH="1"),check=True)
SHA_C="b6d454e53769f1ad17c4441f4784c4f2a8936712e61faf500d51f666dae77080"
assert hashlib.sha256((P/"r1ar_F6.bin").read_bytes()).hexdigest()==SHA_C
srcC=(P/"r1ar.asm").read_text()
start="R1acSelect:\n";end="R1acAfterRows:\n"
def part(s,letter):
 assert s.count(start)==s.count(end)==1
 h,b=s.split(start,1)
 body,t=b.split(end,1)
 prefix=" JMP R1apNineRows\nR1apNineRows:\n"
 assert body.startswith(prefix),(letter,body[:80])
 body=body[len(prefix):].replace("R1apScan","R1at"+letter+"Scan")
 assert body.count(" STA RESP1\n")==36,letter
 return h,body,t
headA,kernA,tailA=part(srcA,"A")
headB,kernB,tailB=part(srcB,"B")
headC,kernC,tailC=part(srcC,"C")
assert headA==headB==headC and tailA==tailB==tailC,"Only critical P1 phase NOP schedules may differ"
# Branch outside the nine-row critical region, so no new per-row CPU cycles.
selector=(
 "R1acSelect:\n"
 " LDA FRAMELO\n"
 " AND #$18\n"
 " BEQ R1atJumpA\n"
 " CMP #$08\n"
 " BEQ R1atJumpB\n"
 " CMP #$10\n"
 " BEQ R1atJumpC\n"
 " JMP R1atA\n"
 "R1atJumpA:\n"
 " JMP R1atA\n"
 "R1atJumpB:\n"
 " JMP R1atB\n"
 "R1atJumpC:\n"
 " JMP R1atC\n"
 "R1atA:\n"+kernA+
 " JMP R1acAfterRows\n"
 "R1atB:\n"+kernB+
 " JMP R1acAfterRows\n"
 "R1atC:\n"+kernC+
 " JMP R1acAfterRows\n"
 "R1acAfterRows:\n")
src=headA+selector+tailA
for name in ("MaleRows","FemaleRows","SmallMaleRows","SmallFemaleRows","PlayerRows","ShotEnable"):
 marker="\n"+name+":\n"
 assert srcA.count(marker)==src.count(marker)==1
 assert srcA.split(marker,1)[1].split("\n",1)[0]==src.split(marker,1)[1].split("\n",1)[0]
(R/"r1at.asm").write_text(src)
subprocess.run(["dasm","r1at.asm","-f3","-or1at_4k.bin","-lr1at.lst","-sr1at.sym"],cwd=R,check=True)
raw=(R/"r1at_4k.bin").read_bytes()
assert len(raw)==4096,len(raw)
rom=raw*4
sha=hashlib.sha256(rom).hexdigest()
(R/"r1at_F6.bin").write_bytes(rom)
(R/"ROM_SHA256.txt").write_text(sha+"  r1at_F6.bin\n")
manifest={
 "status":"BUILT_UNVERIFIED_R1AT_THREE_RUNTIME_SIX_MASK_X_LAYOUTS",
 "source_ROM_SHA256":{"A":SHA_A,"B":SHA_B,"C":SHA_C},
 "three_preverified_P1_schedules":{"A":[28,40,56,66],"B":[28,42,56,66],"C":[30,42,56,66]},
 "runtime_selector":"FRAMELO & $18: 0=A, 8=B, 16=C, 24=A, 8 frames per state",
 "NUSIZ1_value":3,
 "source_masks":"Canonical original 8x9 M M F F SM SF; bytes unchanged",
 "full_yellow_player_P0_and_one_static_M0":"unchanged",
 "ROM_SHA256":sha,"bytes":16384,
 "mapper":"standard F6, four identical 4 KB banks",
 "limits":"Three predefined runtime X configurations, no full free X or real independent 6-NPC movement, no new gameplay, no independent Verification"}
(R/"manifest.json").write_text(json.dumps(manifest,indent=2)+"\n")
print(json.dumps(manifest,indent=2))
