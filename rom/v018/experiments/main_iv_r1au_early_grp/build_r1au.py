#!/usr/bin/env python3
"""R1au research: restore first large male FULL original 8x9 source mask after
independent earlier P1 RESP1 by advancing first GRP1 by 2 or 4 CPU cycles.
Keep the SECOND female RESP1, small male/female RESP1, P0 and M0 unchanged.
Fail-closed 600 genuine Stella frames per candidate. No full R1/Verification.
"""
from pathlib import Path
import hashlib,subprocess,sys,os,re,json
R=Path(__file__).resolve().parent
P=R.parent/"main_iv_r1at_male_early"
base=(P/"build_r1at.py").read_bytes()
blob=hashlib.sha1(b"blob "+str(len(base)).encode()+b"\0"+base).hexdigest()
assert blob=="94aa43107b7ca41247ef4b6ca21a3f28de8e73ca"
variant=int(os.environ.get("R1AU_VARIANT","0"))
assert variant in (0,1,2)
parent_batch,shift=[(0,1),(1,1),(1,2)][variant]
subprocess.run([sys.executable,str(P/"build_r1at.py")],
 env=dict(os.environ,R1AT_BATCH=str(parent_batch)),check=True)
ROM_PINS=[
 "14b2329201be324742339e3be880d0d511cd93c473d2dca4bc95feacc7520079",
 "298e9ce16a5b73b24d516d567e4a66e521edde7aab45c07a7a047a9762e26749"
]
assert hashlib.sha256((P/"r1at_F6.bin").read_bytes()).hexdigest()==ROM_PINS[parent_batch]
old=(P/"r1at.asm").read_text()
pre=3-parent_batch
post=2+parent_batch
assert post>shift
pattern=re.compile(r"( LDA #\$[0-9A-F]{2}\n)(?: NOP\n){"+str(pre)+r"}( STA RESP1\n)(?: NOP\n){"+str(post)+r"}( STA GRP1\n)(?: NOP\n){2}( STA RESP1\n)")
src,n=pattern.subn(lambda m:m.group(1)+" NOP\n"*pre+m.group(2)+
        " NOP\n"*(post-shift)+m.group(3)+" NOP\n"*(2+shift)+m.group(4),old)
assert n==9,("not nine identical first-mask timing sequences",n)
assert src.count(" STA RESP1\n")==old.count(" STA RESP1\n")==36
for label in ("MaleRows","FemaleRows","SmallMaleRows","SmallFemaleRows","PlayerRows","ShotEnable"):
 mark="\n"+label+":\n"
 assert src.count(mark)==old.count(mark)==1
 assert src.split(mark,1)[1].split("\n",1)[0]==old.split(mark,1)[1].split("\n",1)[0]
(R/"r1au.asm").write_text(src)
subprocess.run(["dasm","r1au.asm","-f3","-or1au_4k.bin","-lr1au.lst","-sr1au.sym"],cwd=R,check=True)
four=(R/"r1au_4k.bin").read_bytes()
assert len(four)==4096
rom=four*4;sha=hashlib.sha256(rom).hexdigest()
(R/"r1au_F6.bin").write_bytes(rom)
(R/"ROM_SHA256.txt").write_text(sha+"  r1au_F6.bin\n")
meta={
 "status":"BUILT_UNVERIFIED_R1AU_EARLY_MALE_GRP1_RESEARCH",
 "NUSIZ1_value":3,
 "R1at_parent_builder_git_blob_SHA":"94aa43107b7ca41247ef4b6ca21a3f28de8e73ca",
 "variant":variant,"parent_batch":parent_batch,
 "original_R1at_failed_ROM_SHA256":ROM_PINS[parent_batch],
 "first_male_RESP1_cpu":26-2*parent_batch,
 "first_male_GRP1_shift_earlier_cpu":2*shift,
 "female_RESP1_cpu_unchanged":40,
 "small_male_RESP1_cpu_unchanged":56,
 "small_female_RESP1_cpu_unchanged":66,
 "source_masks":"all canonical nine-row source bytes unchanged",
 "P0_and_M0":"unchanged",
 "ROM_SHA256":sha,"bytes":16384,"mapper":"F6 standard 16KiB NTSC",
 "limits":"research only, no independent six X or full R1/VERIFICATION"
}
(R/"manifest.json").write_text(json.dumps(meta,indent=2)+"\n")
print(json.dumps(meta,indent=2))
