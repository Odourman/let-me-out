#!/usr/bin/env python3
"""R1ba isolated research: mirrored brown PF side walls plus three runtime Y profiles, retaining EXACT
three alternating 6-original-Android R1at nine-row raster kernels, full
yellow P0 player and one static M0. No R1 PASS, no cutover, no Verification.
"""
from pathlib import Path
import hashlib,sys,subprocess,json,re
R=Path(__file__).resolve().parent
P=R.parent/"main_iv_r1at_runtime_three"
source=(P/"build_r1at.py").read_bytes()
blob=hashlib.sha1(b"blob "+str(len(source)).encode()+b"\0"+source).hexdigest()
assert blob=="db04b19994969bcb52ce50c294a698bb0ddb6924"
subprocess.run([sys.executable,str(P/"build_r1at.py")],check=True)
PIN="486dca4b574d9a394075788bc974232d3b7452282f282e46c7dd3fca454d2c0a"
assert hashlib.sha256((P/"r1at_F6.bin").read_bytes()).hexdigest()==PIN
old=(P/"r1at.asm").read_text()
assert old.count("COLUBK=$09\n")==1 and "COLUPF=$08" not in old and "CTRLPF=$0A" not in old
assert old.count(" STA COLUBK\n")==1
src=old.replace("COLUBK=$09\n","COLUBK=$09\nCOLUPF=$08\nCTRLPF=$0A\n",1)
mode=0 # proven reflected brown PF mode only
assert mode in (0,1,2)
# Mode 0: reflected, brown and sprites on top. Mode 1: PF disabled control.
# Mode 2: non-reflected negative control (right edge should NOT be a wall).
pfval=[0xF0,0x00,0xF0][mode]
ctrl=[0x01,0x01,0x00][mode]
# Wide four-PF-bit side bands to remain visible even if rightmost small
# original 8x9 NPC crosses the last 16 displayed color clocks.
addition=(" LDA #$26\n STA COLUPF\n"
          " LDA #$"+format(ctrl,"02X")+"\n STA CTRLPF\n"
          " LDA #$"+format(pfval,"02X")+"\n STA PF0\n")
src=src.replace(" STA COLUBK\n",
                " STA COLUBK\n"+addition,1)
# No changes to source sprite masks or critical 9-row four P1 RESP schedule:
for name in ("MaleRows","FemaleRows","SmallMaleRows","SmallFemaleRows","PlayerRows","ShotEnable"):
 mark="\n"+name+":\n"
 assert src.count(mark)==old.count(mark)==1
 assert old.split(mark,1)[1].split("\n",1)[0]==src.split(mark,1)[1].split("\n",1)[0]
section=lambda z:z.split("R1acSelect:\n",1)[1].split("R1acAfterRows:\n",1)[0]
assert section(old)==section(src)
assert src.count(" STA RESP1\n")==old.count(" STA RESP1\n")
# Source-exact Y offsets from preverified R1ay profiles, paired with
# R1at runtime X layouts A/B/C. Do not add any raster instruction.
canon=json.loads((R.parents[3]/"design/NPC_REFERENCE_8x9_masks.json").read_text())
SM=[int(x,2) for x in canon["sprites"]["small_male"]]
SF=[int(x,2) for x in canon["sprites"]["small_female"]]
assert SM==[0,0,60,60,24,126,24,36,0]
assert SF==[0,0,60,60,24,126,60,36,0]
profiles={"A":(1,-1),"B":(-1,1),"C":(-2,-1)}
pSM=re.compile(r"( LDX #0\n LDA #)\$([0-9A-F]{2})(\n(?: NOP\n){2,3} STA RESP1\n STA GRP1\n)")
pSF=re.compile(r"( STA GRP1\n LDA #)\$([0-9A-F]{2})(\n NOP\n STA RESP1\n STA GRP1\n)")
def shift_body(z,regex,arr,dy):
 n=[0]
 def sub(m):
  y=n[0];n[0]+=1
  assert y<9 and int(m.group(2),16)==arr[y],("source drift",y,m.group(2),arr[y])
  srcy=y-dy
  b=arr[srcy] if 0<=srcy<9 else 0
  return m.group(1)+"$"+format(b,"02X")+m.group(3)
 s,k=regex.subn(sub,z)
 assert k==9,("not 9 original bitmap immediates",k,dy)
 assert all(0<=y+dy<9 for y,b in enumerate(arr) if b),"original mask would clip"
 return s
for letter,(sm_dy,sf_dy) in profiles.items():
 lbl="R1at"+letter+":\n"
 boundary=" JMP R1acAfterRows\n"
 assert src.count(lbl)==1,letter
 pre,rest=src.split(lbl,1)
 body,tail=rest.split(boundary,1)
 assert body.count(" STA RESP1\n")==36,letter
 body=shift_body(body,pSM,SM,sm_dy)
 body=shift_body(body,pSF,SF,sf_dy)
 src=pre+lbl+body+boundary+tail
assert src.count(" STA RESP1\n")==old.count(" STA RESP1\n")
assert src.count(" STA GRP1\n")==old.count(" STA GRP1\n")

(R/"r1ba.asm").write_text(src)
subprocess.run(["dasm","r1ba.asm","-f3","-or1ba_4k.bin","-lr1ba.lst","-sr1ba.sym"],cwd=R,check=True)
four=(R/"r1ba_4k.bin").read_bytes()
assert len(four)==4096
rom=four*4;sha=hashlib.sha256(rom).hexdigest()
(R/"r1ba_F6.bin").write_bytes(rom)
(R/"ROM_SHA256.txt").write_text(sha+"  r1ba_F6.bin\n")
meta={"status":"BUILT_UNVERIFIED_R1BA_INTEGRATED_X_Y_BROWN_PF_RESEARCH",
 "source_builder_git_blob":"db04b19994969bcb52ce50c294a698bb0ddb6924",
 "pinned_successful_three_runtime_ROM_SHA256":PIN,
 "mode":mode,"NUSIZ1_value":3,"PF0":pfval,"PF1":0,"PF2":0,
 "CTRLPF":ctrl,"COLUPF":0x26,
 "brown_wall_hypothesis":mode==0,
 "y_profiles":[list(profiles[k]) for k in "ABC"],
 "X_profiles":"R1at A/B/C, each paired with one Y profile",
 "source_masks":"all six 8x9 original silhouettes unchanged",
 "P0_M0":"full original player and one M0 unchanged",
 "critical_nine_scanline_P1_instructions":"same opcode cycle schedule; only source-immediate row bitmap bytes vary by Y",
 "ROM_SHA256":sha,"bytes":16384,
 "mapper":"standard F6 4 identical 4K banks", "video":"NTSC",
 "limits":"RESEARCH mirrored brown band only, not asymmetric right door or R1 full scene; no independent Verification"}
(R/"manifest.json").write_text(json.dumps(meta,indent=2)+"\n")
print(json.dumps(meta,indent=2))
