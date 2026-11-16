#!/usr/bin/env python3
"""R1an research: shift small male/female RESP1 by +2 CPU cycles each so
second large female NUSIZ3 copy fully completes before its counter reset.
Static 8x9 masks original, one P0 player/M0, 76-cycle NTSC budget.
"""
from pathlib import Path
import os,sys,subprocess,hashlib,json
R=Path(__file__).resolve().parent
P=R.parent/"main_iv_r1al_auto_copy_timing"
code=(P/"build_r1al.py").read_bytes()
blob=hashlib.sha1(b"blob "+str(len(code)).encode()+b"\0"+code).hexdigest()
assert blob=="27589828487ba45a0e5871d1a945b99460f5a116"
subprocess.run([sys.executable,str(P/"build_r1al.py")],check=True)
old=(P/"r1al.asm").read_text()
src=old
for mode in "CDEF":
 label="R1acRowSync"+mode+":\n";end=" BPL R1acRowSync"+mode+"\n"
 before,tail=src.split(label,1)
 body,after=tail.split(end,1)
 needle=" LDA SmallMaleRows,Y\n NOP\n STA RESP1\n STA GRP1\n LDA SmallFemaleRows,Y\n STA RESP1\n"
 assert body.count(needle)==1,mode
 body=body.replace(needle," LDA SmallMaleRows,Y\n NOP\n NOP\n STA RESP1\n STA GRP1\n LDA SmallFemaleRows,Y\n STA RESP1\n")
 src=before+label+body+end+after
for name in ("MaleRows","FemaleRows","SmallMaleRows","SmallFemaleRows","PlayerRows","ShotEnable"):
 mark="\n"+name+":\n"
 assert src.count(mark)==old.count(mark)==1
 assert old.split(mark,1)[1].split("\n",1)[0]==src.split(mark,1)[1].split("\n",1)[0]
(R/"r1an.asm").write_text(src)
subprocess.run(["dasm","r1an.asm","-f3","-or1an_4k.bin","-lr1an.lst","-sr1an.sym"],cwd=R,check=True)
four=(R/"r1an_4k.bin").read_bytes();assert len(four)==4096
rom=four*4;sha=hashlib.sha256(rom).hexdigest()
(R/"r1an_F6.bin").write_bytes(rom)
(R/"ROM_SHA256.txt").write_text(sha+"  r1an_F6.bin\n")
meta={"status":"BUILT_UNVERIFIED_R1AN_FEMALE_COPY_FULL_WINDOW",
 "pinned_R1al_builder_git_blob":"27589828487ba45a0e5871d1a945b99460f5a116",
 "NUSIZ1_value":3,"cycles_RESP1":[28,40,54,64],
 "next_WSYN C_deadline":75,
 "source_masks":"all four unique approved 8x9 bitmap rows unchanged",
 "yellow_P0_M0":"unchanged from R1al",
 "ROM_SHA256":sha,"bytes":16384,
 "scope":"Research only, no full R1 or independent Verification"}
(R/"manifest.json").write_text(json.dumps(meta,indent=2)+"\n")
print(json.dumps(meta,indent=2))
