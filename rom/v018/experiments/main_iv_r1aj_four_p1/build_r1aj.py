#!/usr/bin/env python3
"""R1aj research: FOUR DIFFERENT exact original P1 masks same nine scanlines.
M-F-SM-SF, yellow P0 prepositioned clear, one M0 static shot.
No full R1, no production implementation, no independent VERIFICATION.
"""
from pathlib import Path
import subprocess,hashlib,json,os,sys
R=Path(__file__).resolve().parent
P=R.parent/"main_iv_r1ah_three_p1"
subprocess.run([sys.executable,str(P/"build_r1ah.py")],
 env=dict(os.environ,R1AH_BATCH="2"),check=True)
PIN="6915711bb5d44a8603b3857853f7c688a49f32fb4b1f5ba9ccc0461868ce6a2f"
assert hashlib.sha256((P/"r1ah_F6.bin").read_bytes()).hexdigest()==PIN
old=(P/"r1ah.asm").read_text()
assert old.count(" LDX #12\nPlayerDelay:\n")==1
src=old.replace(" LDX #12\nPlayerDelay:\n"," LDX #9\nPlayerDelay:\n",1)
canon=json.loads((R.parents[3]/"design/NPC_REFERENCE_8x9_masks.json").read_text())
sf=[int(x,2) for x in canon["sprites"]["small_female"]]
assert sf==[0,0,60,60,24,126,60,36,0]
assert src.count(" ORG $FFFA\n")==1 and "SmallFemaleRows:" not in src
tab="SmallFemaleRows:\n BYTE "+",".join("$"+format(x,"02X") for x in sf[::-1])+"\n"
src=src.replace(" ORG $FFFA\n",tab+" ORG $FFFA\n",1)
batch=int(os.environ.get("R1AJ_BATCH","0"))
assert batch in (0,1)
modes={"C":(28,38,48),"D":(30,38,50),"E":(28,40,50),"F":(30,40,52)}
timings={}
for mode,(c1,c2,c3) in modes.items():
 c4=c3+10+2*batch
 assert c4+11<=76
 label="R1acRowSync"+mode+":\n"
 end=" BPL R1acRowSync"+mode+"\n"
 assert src.count(label)==src.count(end)==1
 a,tail=src.split(label,1)
 body,b=tail.split(end,1)
 needle=" STA RESP1\n STA GRP1\n DEY\n"
 assert body.count(needle)==1
 replacement=" STA RESP1\n STA GRP1\n LDA SmallFemaleRows,Y\n"
 replacement+=" NOP\n"*batch+" STA RESP1\n STA GRP1\n DEY\n"
 body=body.replace(needle,replacement,1)
 src=a+label+body+end+b
 timings[mode]={"male_RESP1_end":c1,"female_RESP1_end":c2,
     "smallmale_RESP1_end":c3,"smallfemale_RESP1_end":c4,
     "smallfemale_GRP1_end":c4+3,"next_WSYN C_end":c4+11}
for nm in ("MaleRows","FemaleRows","SmallMaleRows","PlayerRows","ShotEnable"):
 mark="\n"+nm+":\n"
 assert old.count(mark)==src.count(mark)==1
 assert src.split(mark,1)[1].split("\n",1)[0]==old.split(mark,1)[1].split("\n",1)[0]
(R/"r1aj.asm").write_text(src)
subprocess.run(["dasm","r1aj.asm","-f3","-or1aj_4k.bin","-lr1aj.lst","-sr1aj.sym"],cwd=R,check=True)
four=(R/"r1aj_4k.bin").read_bytes()
assert len(four)==4096
rom=four*4;sha=hashlib.sha256(rom).hexdigest()
(R/"r1aj_F6.bin").write_bytes(rom)
(R/"ROM_SHA256.txt").write_text(sha+"  r1aj_F6.bin\n")
manifest={
 "status":"BUILT_UNVERIFIED_R1AJ_RESEARCH",
 "batch":batch,"order":"LargeMale,LargeFemale,SmallMale,SmallFemale",
 "mask_order":"M->F",
 "source_sha_R1ah_3mask_PASS":PIN,
 "source_smal lfem_canonical":sf,
 "P0_only_change":"LDX #12 to #9 at initial PlayerDelay",
 "four_P1_cycle_schedules":timings,
 "rom_sha256":sha,"bytes":16384,
 "mapper":"standard F6","video":"NTSC",
 "scope":"isolated research only: not six NPC, R1-R4 or independent Verification"}
(R/"manifest.json").write_text(json.dumps(manifest,indent=2)+"\n")
print(json.dumps(manifest,indent=2))
