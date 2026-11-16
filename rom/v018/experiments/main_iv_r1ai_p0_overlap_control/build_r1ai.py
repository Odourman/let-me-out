#!/usr/bin/env python3
"""R1ai research: isolate P0/P1 overlap in the two R1ah failed branches.
Change only initial P0 RESP0 delay X12 -> X9. P1 and all graphics unchanged.
"""
from pathlib import Path
import subprocess,hashlib,json,os,sys
R=Path(__file__).resolve().parent
P=R.parent/"main_iv_r1ah_three_p1"
batch=int(os.environ.get("R1AI_BATCH","0"))
assert batch in (0,1)
original_batch={0:0,1:3}[batch]
pins={
 0:"c2a5b53a5573107ed3c96aa355d88c1183a3f1ce5a90b358e373eb794d0d744a",
 1:"3d15b41f73e51359f0f0e4c915c188beb3be8115ee25309a55f3e7ac8abdcad0"}
subprocess.run([sys.executable,str(P/"build_r1ah.py")],
  env=dict(os.environ,R1AH_BATCH=str(original_batch)),check=True)
original_rom=(P/"r1ah_F6.bin").read_bytes()
assert hashlib.sha256(original_rom).hexdigest()==pins[batch],"Pinned failing R1ah ROM changed"
src=(P/"r1ah.asm").read_text()
needle=" LDX #12\nPlayerDelay:\n"
assert src.count(needle)==1
src=src.replace(needle," LDX #9\nPlayerDelay:\n",1)
# No other data, register timing, sprite table, M0 or code change.
assert src.replace(" LDX #9\nPlayerDelay:\n",needle,1)==(P/"r1ah.asm").read_text()
(R/"r1ai.asm").write_text(src)
subprocess.run(["dasm","r1ai.asm","-f3","-or1ai_4k.bin","-lr1ai.lst","-sr1ai.sym"],cwd=R,check=True)
four=(R/"r1ai_4k.bin").read_bytes()
assert len(four)==4096
rom=four*4
sha=hashlib.sha256(rom).hexdigest()
(R/"r1ai_F6.bin").write_bytes(rom)
(R/"ROM_SHA256.txt").write_text(sha+"  r1ai_F6.bin\n")
d={
 "status":"BUILT_UNVERIFIED_R1AI_ISOLATED_P0_POSITION_CHANGE",
 "batch":batch,"failing_R1ah_batch":original_batch,
 "old_ROM_SHA256":pins[batch],"ROM_SHA256":sha,
 "diff":"ONLY LDX #12 to LDX #9 before initial PlayerDelay/RESP0",
 "P1":"exactly unchanged R1ah three original masks, same RESP1 timings",
 "P0":"same original player mask moved to avoid spatial overlap with third white P1",
 "shot":"same original static M0",
 "mapper":"standard F6 NTSC","size":16384,
 "mask_order":"M->F","goal":"600 authentic Stella images, 3 full white masks, intact yellow P0 and M0, zero ghosts, 262 scanlines",
 "scope":"research ONLY, not R1/R2/R3/R4 PASS, no production or independent VERIFICATION"}
(R/"manifest.json").write_text(json.dumps(d,indent=2)+"\n")
print(json.dumps(d,indent=2))
