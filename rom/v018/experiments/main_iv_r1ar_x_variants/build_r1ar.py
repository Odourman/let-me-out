#!/usr/bin/env python3
"""R1ar RESEARCH: constrained independent 6-mask P1 positions.
Start from exact R1aq six-source 600/600 pass batch0. Explore either
female +2 cycles alone, both M+F +2, or male +2 alone. Exact 8x9 bitmaps
with yellow P0 and M0 unchanged. Not free 160-CC independent X.
"""
from pathlib import Path
import os,subprocess,sys,hashlib,json,re
R=Path(__file__).resolve().parent
P=R.parent/"main_iv_r1aq_timing"
pysrc=(P/"build_r1aq.py").read_bytes()
blob=hashlib.sha1(b"blob "+str(len(pysrc)).encode()+b"\0"+pysrc).hexdigest()
assert blob=="c3cd9f7f893f499957306cd1f2b60316eb13c028"
subprocess.run([sys.executable,str(P/"build_r1aq.py")],
 env=dict(os.environ,R1AQ_BATCH="0"),check=True)
PIN="09e262958e9452ec3f61c3d93f2eea19ad03cda7ac52767ae72608e2f7b3a94b"
assert hashlib.sha256((P/"r1aq_F6.bin").read_bytes()).hexdigest()==PIN
old=(P/"r1aq.asm").read_text()
batch=int(os.environ.get("R1AR_BATCH","0"))
assert batch in (0,1,2)
src=old
# Shift first male by +2 CPU cycles in 1 and 2.
if batch in (1,2):
 pattern=re.compile(r"( LDA #\$[0-9A-F]{2}\n)(?: NOP\n){4}( STA RESP1\n NOP\n STA GRP1\n)")
 src,n=pattern.subn(lambda m:m.group(1)+" NOP\n"*5+m.group(2),src)
 assert n==9,("male first RESP1 site",n)
# Shift second female by +2 independently in batch0; in batch1
# it shifts automatically with male. In batch2 undo the shift of F.
if batch==0:
 before=" STA GRP1\n NOP\n NOP\n STA RESP1\n STX GRP1\n"
 after=" STA GRP1\n NOP\n NOP\n NOP\n STA RESP1\n STX GRP1\n"
 assert src.count(before)==9
 src=src.replace(before,after)
if batch==2:
 before=" STA GRP1\n NOP\n NOP\n STA RESP1\n STX GRP1\n"
 after=" STA GRP1\n NOP\n STA RESP1\n STX GRP1\n"
 assert src.count(before)==9
 src=src.replace(before,after)
# One NOP removed from SM preparation in batch 0/1 to hold SM/SF fixed.
if batch in (0,1):
 pattern=re.compile(r"( LDX #0\n LDA #\$[0-9A-F]{2}\n)(?: NOP\n){3}( STA RESP1\n STA GRP1\n LDA #\$[0-9A-F]{2}\n)")
 src,n=pattern.subn(lambda m:m.group(1)+" NOP\n"*2+m.group(2),src)
 assert n==9,("small male compensation",n)
assert old.count(" STA RESP1\n")==src.count(" STA RESP1\n")==36
for name in ("MaleRows","FemaleRows","SmallMaleRows","SmallFemaleRows","PlayerRows","ShotEnable"):
 mark="\n"+name+":\n"
 assert src.count(mark)==old.count(mark)==1
 assert src.split(mark,1)[1].split("\n",1)[0]==old.split(mark,1)[1].split("\n",1)[0]
(R/"r1ar.asm").write_text(src)
subprocess.run(["dasm","r1ar.asm","-f3","-or1ar_4k.bin","-lr1ar.lst","-sr1ar.sym"],cwd=R,check=True)
four=(R/"r1ar_4k.bin").read_bytes();assert len(four)==4096
rom=four*4;sha=hashlib.sha256(rom).hexdigest()
(R/"r1ar_F6.bin").write_bytes(rom)
(R/"ROM_SHA256.txt").write_text(sha+"  r1ar_F6.bin\n")
timings=[[28,42,56,66],[30,42,56,66],[30,40,56,66]]
meta={"status":"BUILT_UNVERIFIED_R1AR_TWO_LARGE_P1_X_VARIATIONS",
 "R1AQ_source_builder_blob":"c3cd9f7f893f499957306cd1f2b60316eb13c028",
 "R1AQ_600_pass_ROM_SHA256":PIN,
 "batch":batch,"NUSIZ1_value":3,
 "P1_RESP1_cycles":timings[batch],
 "original_8x9_masks":"all byte-identical; exact 2M2F SM SF is audited",
 "yellow_P0_and_M0":"byte-identical from R1aq",
 "ROM_SHA256":sha,"bytes":16384,
 "scope":"research only, no independent free X or full R1, no independent Verification"}
(R/"manifest.json").write_text(json.dumps(meta,indent=2)+"\n")
print(json.dumps(meta,indent=2))
