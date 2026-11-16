#!/usr/bin/env python3
"""R1az RESEARCH: three independently pixel-verified Y-offset source-mask
nine-scanline kernels built into ONE 16KB standard F6 NTSC ROM.
Selector changes SM/SF Y masks every 8 frames, other four P1 original
NPCs plus yellow P0 and static M0 stay same. Not full arbitrary Y / R4.
"""
from pathlib import Path
import os,sys,hashlib,subprocess,json
R=Path(__file__).resolve().parent
P=R.parent/"main_iv_r1ay_neighbor_y"
PINS=[
 "f3d509e1c46b432bcc33a518647378c1332b4ff2564224a2ff36a62b90356633",
 "1abd8ab43c89ab5f95b446fb9172e0e83c96aff212cb9f7d761150271ffaf71a",
 "b5b75b5027692b8e8055901c79d462423eefa9ba6e0811db5b739e31a9bc7849"
]
profile_y=[(1,-1),(-1,1),(-2,-1)]
sources={}
for i,key in enumerate("ABC"):
 subprocess.run([sys.executable,str(P/"build_r1ay.py")],
  env=dict(os.environ,R1AY_BATCH=str(i)),check=True)
 assert hashlib.sha256((P/"r1ay_F6.bin").read_bytes()).hexdigest()==PINS[i],(i,"original ROM SHA mismatch")
 manifest=json.loads((P/"manifest.json").read_text())
 assert (manifest["small_male_offset"],manifest["small_female_offset"])==profile_y[i]
 sources[key]=(P/"r1ay.asm").read_text()
start="R1acSelect:\n";end="R1acAfterRows:\n"
parts={}
for key,src in sources.items():
 assert src.count(start)==src.count(end)==1
 head,rest=src.split(start,1)
 body,tail=rest.split(end,1)
 prefix=" JMP R1apNineRows\nR1apNineRows:\n"
 assert body.startswith(prefix),(key,body[:80])
 body=body[len(prefix):].replace("R1apScan","R1az"+key+"Scan")
 assert body.count(" STA RESP1\n")==36
 parts[key]=(head,body,tail)
assert len({parts[k][0] for k in parts})==1,"Unexpected different ROM init code"
assert len({parts[k][2] for k in parts})==1,"Unexpected different ROM final tables"
head=parts["A"][0];tail=parts["A"][2]
selector=(
 "R1acSelect:\n"
 " LDA FRAMELO\n"
 " AND #$18\n"
 " BEQ R1azPickA\n"
 " CMP #$08\n"
 " BEQ R1azPickB\n"
 " CMP #$10\n"
 " BEQ R1azPickC\n"
 " JMP R1azKernelA\n"
 "R1azPickA:\n JMP R1azKernelA\n"
 "R1azPickB:\n JMP R1azKernelB\n"
 "R1azPickC:\n JMP R1azKernelC\n"
 "R1azKernelA:\n"+parts["A"][1]+" JMP R1acAfterRows\n"
 "R1azKernelB:\n"+parts["B"][1]+" JMP R1acAfterRows\n"
 "R1azKernelC:\n"+parts["C"][1]+" JMP R1acAfterRows\n"
 "R1acAfterRows:\n")
src=head+selector+tail
for name in ("MaleRows","FemaleRows","SmallMaleRows","SmallFemaleRows","PlayerRows","ShotEnable"):
 anchor="\n"+name+":\n"
 assert src.count(anchor)==sources["A"].count(anchor)==1
 assert src.split(anchor,1)[1].split("\n",1)[0]==sources["A"].split(anchor,1)[1].split("\n",1)[0]
(R/"r1az.asm").write_text(src)
subprocess.run(["dasm","r1az.asm","-f3","-or1az_4k.bin","-lr1az.lst","-sr1az.sym"],cwd=R,check=True)
four=(R/"r1az_4k.bin").read_bytes()
assert len(four)==4096
rom=four*4;sha=hashlib.sha256(rom).hexdigest()
(R/"r1az_F6.bin").write_bytes(rom)
(R/"ROM_SHA256.txt").write_text(sha+"  r1az_F6.bin\n")
meta={
 "status":"BUILT_UNVERIFIED_R1AZ_RUNTIME_THREE_Y_PROFILES",
 "parent_R1AY_ROM_SHA256":dict(zip("ABC",PINS)),
 "y_profiles":profile_y,"NUSIZ1_value":3,
 "runtime_selector":"FRAMELO & $18: A=0 or 24; B=8; C=16, eight-frame hold per profile",
 "source_masks":"four canonical original 8x9 mask byte tables unchanged",
 "per_scanline_P1_register_timings":"all equal 28,40,56,66 across A/B/C",
 "P0_M0":"original complete yellow P0 and one static M0 unaffected",
 "ROM_SHA256":sha,"bytes":16384,
 "mapper":"standard F6 four copies of a 4KiB bank",
 "scope":"research only. No independent arbitrary Y for six NPC, no PF walls/door/key, no full R1/R4 or independent VERIFICATION"}
(R/"manifest.json").write_text(json.dumps(meta,indent=2)+"\n")
print(json.dumps(meta,indent=2))
