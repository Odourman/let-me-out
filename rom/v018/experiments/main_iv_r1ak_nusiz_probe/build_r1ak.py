#!/usr/bin/env python3
"""R1ak research-only: change NUSIZ1 ONLY, pin proven four-original-P1 ROM.
Measure exactly how many full original 8x9 masks survive and if autonomous
copies form useful fifth/sixth NPC. Not R1, not production or VERIFICATION.
"""
from pathlib import Path
import subprocess,hashlib,os,sys,json
R=Path(__file__).resolve().parent
P=R.parent/"main_iv_r1aj_four_p1"
subprocess.run([sys.executable,str(P/"build_r1aj.py")],env=dict(os.environ,R1AJ_BATCH="0"),check=True)
PIN="ff0f1c64ffff1915cef934f224b3f3d780bc2de6cc52038d62666904c1f0f263"
assert hashlib.sha256((P/"r1aj_F6.bin").read_bytes()).hexdigest()==PIN
src=(P/"r1aj.asm").read_text()
mode=int(os.environ.get("R1AK_MODE","3"))
assert mode in (0,1,2,3,4,6)
needle=" LDA #$01\n STA NUSIZ1\n"
assert src.count(needle)==1,"Cannot unambiguously locate P1 copies register"
replacement=" LDA #$"+format(mode,"02X")+"\n STA NUSIZ1\n"
src=src.replace(needle,replacement,1)
assert src.replace(replacement,needle,1)==(P/"r1aj.asm").read_text(),"Unexpected changed source"
(R/"r1ak.asm").write_text(src)
subprocess.run(["dasm","r1ak.asm","-f3","-or1ak_4k.bin","-lr1ak.lst","-sr1ak.sym"],cwd=R,check=True)
four=(R/"r1ak_4k.bin").read_bytes()
assert len(four)==4096
rom=four*4
sha=hashlib.sha256(rom).hexdigest()
(R/"r1ak_F6.bin").write_bytes(rom)
(R/"ROM_SHA256.txt").write_text(sha+"  r1ak_F6.bin\n")
d={"status":"BUILT_UNVERIFIED_R1AK_NUSIZ_PROBE",
   "pinned_R1aj_600_PASS_ROM_SHA256":PIN,
   "NUSIZ1_value":mode,
   "only_source_change":"NUSIZ1 immediate value $01 to $"+format(mode,"02X"),
   "ROM_SHA256":sha,"ROM_bytes":16384,
   "all_four_canonical_original_masks":"unchanged",
   "P0_and_M0_and_4_RESP1_cycle_schedule":"unchanged",
   "goal":"Count exact full white masks M,F,SM,SF plus possible duplicate M,F without any ghosts or extra pixels across 600 true Stella X11 frames",
   "limit":"Research only; no free X, no six NPC implementation, no independent Verification"}
(R/"manifest.json").write_text(json.dumps(d,indent=2)+"\n")
print(json.dumps(d,indent=2))
