#!/usr/bin/env python3
"""R1am RESEARCH: gate unwanted late extra copy of last small female P1.
One exact reordering of spare NOP to LDX #0 plus STX GRP1 at row end.
If final 8x9 mask is damaged or 262 lines break, fail closed in Stella.
"""
from pathlib import Path
import os,sys,subprocess,hashlib,json
R=Path(__file__).resolve().parent
P=R.parent/"main_iv_r1al_auto_copy_timing"
script=(P/"build_r1al.py").read_bytes()
sha=hashlib.sha1(b"blob "+str(len(script)).encode()+b"\0"+script).hexdigest()
assert sha=="27589828487ba45a0e5871d1a945b99460f5a116","Pinned R1al builder changed"
subprocess.run([sys.executable,str(P/"build_r1al.py")],check=True)
old=(P/"r1al.asm").read_text()
src=old
for mode in "CDEF":
 label="R1acRowSync"+mode+":\n"
 end=" BPL R1acRowSync"+mode+"\n"
 before,rest=src.split(label,1)
 body,tail=rest.split(end,1)
 needle=" STX GRP1\n LDA SmallMaleRows,Y\n NOP\n STA RESP1\n STA GRP1\n LDA SmallFemaleRows,Y\n STA RESP1\n STA GRP1\n DEY\n"
 replacement=" STX GRP1\n LDX #0\n LDA SmallMaleRows,Y\n STA RESP1\n STA GRP1\n LDA SmallFemaleRows,Y\n STA RESP1\n STA GRP1\n DEY\n STX GRP1\n"
 assert body.count(needle)==1,(mode,body[-400:])
 body=body.replace(needle,replacement,1)
 src=before+label+body+end+tail
for name in ("MaleRows","FemaleRows","SmallMaleRows","SmallFemaleRows","PlayerRows","ShotEnable"):
 mark="\n"+name+":\n"
 assert old.count(mark)==src.count(mark)==1
 assert old.split(mark,1)[1].split("\n",1)[0]==src.split(mark,1)[1].split("\n",1)[0]
(R/"r1am.asm").write_text(src)
subprocess.run(["dasm","r1am.asm","-f3","-or1am_4k.bin","-lr1am.lst","-sr1am.sym"],cwd=R,check=True)
four=(R/"r1am_4k.bin").read_bytes()
assert len(four)==4096
rom=four*4;sha=hashlib.sha256(rom).hexdigest()
(R/"r1am_F6.bin").write_bytes(rom)
(R/"ROM_SHA256.txt").write_text(sha+"  r1am_F6.bin\n")
meta={
 "status":"BUILT_UNVERIFIED_R1AM_TAIL_P1_AUTO_COPY_SUPPRESSION",
 "source_builder_git_blob_SHA":"27589828487ba45a0e5871d1a945b99460f5a116",
 "NUSIZ1_value":3,
 "four_original_source_masks_unchanged":True,
 "four_RESP1_cycles":"28,40,52,62",
 "hypothesis":"LDX #0 after female mask used; STX GRP1 at c70 suppresses last small-female medium ghost while preserving close copy",
 "ROM_SHA256":sha,"bytes":16384,"mapper":"standard F6","video":"NTSC",
 "scope":"research only, no 6-NPC full R1, no independent Verification"}
(R/"manifest.json").write_text(json.dumps(meta,indent=2)+"\n")
print(json.dumps(meta,indent=2))
