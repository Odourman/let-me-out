#!/usr/bin/env python3
"""R1ay: source-perfect 6 original 8x9 androids with two small masks
staggered on adjacent scanlines. ONLY change row-immediate mask bytes,
not P1 reset/write timing, P0 or M0. Static isolated NTSC proof, not R1.
"""
from pathlib import Path
import os,sys,subprocess,re,hashlib,json
R=Path(__file__).resolve().parent
P=R.parent/"main_iv_r1aq_timing"
raw=(P/"build_r1aq.py").read_bytes()
blob=hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()
assert blob=="c3cd9f7f893f499957306cd1f2b60316eb13c028"
subprocess.run([sys.executable,str(P/"build_r1aq.py")],
 env=dict(os.environ,R1AQ_BATCH="0"),check=True)
PIN="09e262958e9452ec3f61c3d93f2eea19ad03cda7ac52767ae72608e2f7b3a94b"
assert hashlib.sha256((P/"r1aq_F6.bin").read_bytes()).hexdigest()==PIN
old=(P/"r1aq.asm").read_text()
canon=json.loads((R.parents[3]/"design/NPC_REFERENCE_8x9_masks.json").read_text())
sm=[int(x,2) for x in canon["sprites"]["small_male"]]
sf=[int(x,2) for x in canon["sprites"]["small_female"]]
assert sm==[0,0,60,60,24,126,24,36,0]
assert sf==[0,0,60,60,24,126,60,36,0]
batch=int(os.environ.get("R1AY_BATCH","0"))
shifts=[(1,-1),(-1,1),(-2,-1)]
assert 0<=batch<len(shifts)
sm_dy,sf_dy=shifts[batch]
for bits,dy in ((sm,sm_dy),(sf,sf_dy)):
 assert all(0<=y+dy<9 for y,b in enumerate(bits) if b)
def shift_row(bits,y,dy):
 k=y-dy
 return bits[k] if 0<=k<9 else 0
# Exactly one unique SM and one SF immediate per each of nine physical
# display rows. Exact source original bitmap remains in label tables.
patSM=re.compile(r"( LDX #0\n LDA #)\$([0-9A-F]{2})(\n(?: NOP\n){3} STA RESP1\n STA GRP1\n)")
patSF=re.compile(r"( STA GRP1\n LDA #)\$([0-9A-F]{2})(\n NOP\n STA RESP1\n STA GRP1\n)")
def replace_rows(src,pat,bits,dy):
 line=0
 def replacement(m):
  nonlocal line
  assert line<9 and int(m.group(2),16)==bits[line],(line,m.group(2),bits[line])
  value=shift_row(bits,line,dy)
  line+=1
  return m.group(1)+"$"+format(value,"02X")+m.group(3)
 new,n=pat.subn(replacement,src)
 assert n==9,(n,pat.pattern[:100])
 return new
src=replace_rows(old,patSM,sm,sm_dy)
src=replace_rows(src,patSF,sf,sf_dy)
assert src.count(" STA RESP1\n")==old.count(" STA RESP1\n")==36
assert src.count(" STA GRP1\n")==old.count(" STA GRP1\n")
for name in ("MaleRows","FemaleRows","SmallMaleRows","SmallFemaleRows","PlayerRows","ShotEnable"):
 anchor="\n"+name+":\n"
 assert src.count(anchor)==old.count(anchor)==1
 assert old.split(anchor,1)[1].split("\n",1)[0]==src.split(anchor,1)[1].split("\n",1)[0]
(R/"r1ay.asm").write_text(src)
subprocess.run(["dasm","r1ay.asm","-f3","-or1ay_4k.bin","-lr1ay.lst","-sr1ay.sym"],cwd=R,check=True)
raw=(R/"r1ay_4k.bin").read_bytes()
assert len(raw)==4096
rom=raw*4;sha=hashlib.sha256(rom).hexdigest()
(R/"r1ay_F6.bin").write_bytes(rom)
(R/"ROM_SHA256.txt").write_text(sha+"  r1ay_F6.bin\n")
meta={
 "status":"BUILT_UNVERIFIED_R1AY_SIX_STAGGERED_CANONICAL_MASKS",
 "batch":batch,"small_male_offset":sm_dy,"small_female_offset":sf_dy,
 "pinned_R1aq_600_PASS_SHA256":PIN,"source_builder_git_blob":"c3cd9f7f893f499957306cd1f2b60316eb13c028",
 "four_source_8x9_mask_tables":"byte-identical originals",
 "only_change":"source-immediate bitmap values selected on 9 physical raster rows with zero padding",
 "all_P1_register_TIMING":"unchanged parent 28 40 56 66",
 "full_yellow_P0_and_one_M0":"unchanged",
 "ROM_SHA256":sha,"bytes":16384,"NTSC_frame_lines":262,
 "mapper":"standard F6, 4 repeated 4096 byte banks",
 "scope":"Research static Y neighbor offsets, not dynamic Y motion or full R1/R4, no independent Verification"}
(R/"manifest.json").write_text(json.dumps(meta,indent=2)+"\n")
print(json.dumps(meta,indent=2))
