#!/usr/bin/env python3
"""R1ah experimental third complete original P1 mask on same nine raster rows."""
from pathlib import Path
import hashlib,subprocess,os,sys,json
R=Path(__file__).resolve().parent
P=R.parent/"main_iv_r1ag_mask_order"
subprocess.run([sys.executable,str(P/"build_r1ag.py")],env=dict(os.environ,R1AG_BATCH="2"),check=True)
PIN="4188d0c22a2c9b908de37af1f257e8a4c25799038c938976323204cedd46dbcd"
assert hashlib.sha256((P/"r1ag_F6.bin").read_bytes()).hexdigest()==PIN
old=(P/"r1ag.asm").read_text()
canon=json.loads((R.parents[3]/"design/NPC_REFERENCE_8x9_masks.json").read_text())
sm=[int(x,2) for x in canon["sprites"]["small_male"]]
assert sm==[0,0,60,60,24,126,24,36,0]
assert "SmallMaleRows:" not in old and old.count(" ORG $FFFA\n")==1
table="SmallMaleRows:\n BYTE "+",".join("$"+format(x,"02X") for x in sm[::-1])+"\n"
src=old.replace(" ORG $FFFA\n",table+" ORG $FFFA\n",1)
batch=int(os.environ.get("R1AH_BATCH","0"))
gaps=[18,14,10,20]
assert 0<=batch<4
modes={"C":(28,38),"D":(30,38),"E":(28,40),"F":(30,40)}
timings={}
for mode,(c1,c2) in modes.items():
 c3=c2+gaps[batch]+(c1-28)
 assert c3>=c2+10 and (c3-c2)%2==0 and c3+11<=76
 n1=(c1-28)//2;n2=(c2-c1-8)//2;n3=(c3-c2-10)//2
 label="R1acRowSync"+mode+":\n";end=" BPL R1acRowSync"+mode+"\n"
 assert src.count(label)==src.count(end)==1
 a,tail=src.split(label,1);body,b=tail.split(end,1)
 assert body.count("STA RESP1")==2
 ins=[" STA WSYNC"," LDX FemaleRows,Y"," LDA PlayerRows,Y",
      " STA GRP0"," LDA ShotEnable,Y"," STA ENAM0",
      " LDA MaleRows,Y"," BIT FRAMELO"]
 ins+=[" NOP"]*n1+[" STA RESP1"," NOP"," STA GRP1"]+[" NOP"]*n2
 ins+=[" STA RESP1"," STX GRP1"," LDA SmallMaleRows,Y"]
 ins+=[" NOP"]*n3+[" STA RESP1"," STA GRP1"," DEY"]
 src=a+label+"\n".join(ins)+"\n"+end+b
 timings[mode]={"first_RESP1_end":c1,"second_RESP1_end":c2,
                "third_RESP1_end":c3,"third_GRP1_end":c3+3,
                "next_WSYN C_end":c3+11}
for name in ("MaleRows","FemaleRows","PlayerRows","ShotEnable"):
 mark="\n"+name+":\n"
 assert src.count(mark)==old.count(mark)==1
 assert src.split(mark,1)[1].split("\n",1)[0]==old.split(mark,1)[1].split("\n",1)[0]
(R/"r1ah.asm").write_text(src)
subprocess.run(["dasm","r1ah.asm","-f3","-or1ah_4k.bin","-lr1ah.lst","-sr1ah.sym"],cwd=R,check=True)
four=(R/"r1ah_4k.bin").read_bytes()
assert len(four)==4096
rom=four*4;sha=hashlib.sha256(rom).hexdigest()
(R/"r1ah_F6.bin").write_bytes(rom)
(R/"ROM_SHA256.txt").write_text(sha+"  r1ah_F6.bin\n")
manifest={"status":"BUILT_UNVERIFIED_R1AH_RESEARCH","batch":batch,
 "order":"LargeMale,LargeFemale,SmallMale","mask_order":"M->F",
 "original_small_male_topdown":sm,
 "pinned_R1ag_ROM_SHA256":PIN,
 "cycle_schedule":timings,"ROM_SHA256":sha,
 "size":16384,"mapper":"F6 standard","video":"NTSC",
 "scope":"Research only; not v0.18 full R1, no production or VERIFICATION"}
(R/"manifest.json").write_text(json.dumps(manifest,indent=2)+"\n")
print(json.dumps(manifest,indent=2))
