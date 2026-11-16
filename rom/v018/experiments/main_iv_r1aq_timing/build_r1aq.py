#!/usr/bin/env python3
"""R1aq isolated research: shift last two independent P1 sprites earlier,
leave all source-perfect M,M,F,F,SM original pixels and yellow P0/M0
unchanged; only remove NOP from late small-male timing block per row.
Two variants c3/c4 (56,66) and (54,64). No full R1 nor VERIFICATION.
"""
from pathlib import Path
import os,subprocess,sys,hashlib,json,re
R=Path(__file__).resolve().parent
P=R.parent/"main_iv_r1ap_immediate"
srcpy=(P/"build_r1ap.py").read_bytes()
blob=hashlib.sha1(b"blob "+str(len(srcpy)).encode()+b"\0"+srcpy).hexdigest()
assert blob=="f7beaed477a9559e170e2878df726fd46bb5f7cf"
subprocess.run([sys.executable,str(P/"build_r1ap.py")],check=True)
PIN="e485027d8dd59fe2f6d159d1e9048b0707c528cb0411baa1f7448595bdd0ad18"
assert hashlib.sha256((P/"r1ap_F6.bin").read_bytes()).hexdigest()==PIN
old=(P/"r1ap.asm").read_text()
batch=int(os.environ.get("R1AQ_BATCH","0"))
assert batch in (0,1)
reduce=1+batch
pattern=re.compile(r"( LDA #\$[0-9A-F]{2}\n)(?: NOP\n){4}( STA RESP1\n STA GRP1\n LDA #\$[0-9A-F]{2}\n NOP\n STA RESP1\n STA GRP1\n)")
src,n=pattern.subn(lambda m:m.group(1)+" NOP\n"*(4-reduce)+m.group(2),old)
assert n==9,("Original SM->SF raster sequence not found",n)
assert src.count(" STA RESP1\n")==old.count(" STA RESP1\n")==36
for name in ("MaleRows","FemaleRows","SmallMaleRows","SmallFemaleRows","PlayerRows","ShotEnable"):
 mark="\n"+name+":\n"
 assert old.count(mark)==src.count(mark)==1
 assert old.split(mark,1)[1].split("\n",1)[0]==src.split(mark,1)[1].split("\n",1)[0]
(R/"r1aq.asm").write_text(src)
subprocess.run(["dasm","r1aq.asm","-f3","-or1aq_4k.bin","-lr1aq.lst","-sr1aq.sym"],cwd=R,check=True)
four=(R/"r1aq_4k.bin").read_bytes()
assert len(four)==4096
rom=four*4;sha=hashlib.sha256(rom).hexdigest()
(R/"r1aq_F6.bin").write_bytes(rom)
(R/"ROM_SHA256.txt").write_text(sha+"  r1aq_F6.bin\n")
c3,c4=(58-2*reduce,68-2*reduce)
meta={"status":"BUILT_UNVERIFIED_R1AQ_SIX_STATIC_8X9_MASK_TIMING_REFINEMENT",
 "batch":batch,"pinned_R1ap_source_git_blob":"f7beaed477a9559e170e2878df726fd46bb5f7cf",
 "pinned_R1ap_ROM_SHA256":PIN,
 "NUSIZ1_value":3,"P0_player_delay":5,
 "P1_RESP1_cpu_end_cycles":[28,40,c3,c4],
 "four_original_source_masks_unchanged":True,
 "shot_and_P0_sources_unchanged":True,
 "ROM_SHA256":sha,"bytes":16384,
 "scope":"Research-only 6 static P1 sprite proof, no free X or full R1, no independent Verification"}
(R/"manifest.json").write_text(json.dumps(meta,indent=2)+"\n")
print(json.dumps(meta,indent=2))
