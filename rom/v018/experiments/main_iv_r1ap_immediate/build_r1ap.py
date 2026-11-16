#!/usr/bin/env python3
"""R1ap RESEARCH: unroll 9 physical rows with approved, precomputed immediate
P1 mask bytes. NUSIZ1=$03, M-M-F-F-SM-SF target. One yellow P0 player
moved clear of the second F for occlusion control, one M0 test shot.
This is fixed-X only; NOT six independently moving sprites or full R1.
"""
from pathlib import Path
import os,sys,subprocess,hashlib,json,re
R=Path(__file__).resolve().parent
P=R.parent/"main_iv_r1aj_four_p1"
subprocess.run([sys.executable,str(P/"build_r1aj.py")],
 env=dict(os.environ,R1AJ_BATCH="0"),check=True)
PIN="ff0f1c64ffff1915cef934f224b3f3d780bc2de6cc52038d62666904c1f0f263"
assert hashlib.sha256((P/"r1aj_F6.bin").read_bytes()).hexdigest()==PIN
old=(P/"r1aj.asm").read_text()
assert old.count(" LDA #$01\n STA NUSIZ1\n")==1
assert old.count(" LDX #9\nPlayerDelay:\n")==1
src=old.replace(" LDA #$01\n STA NUSIZ1\n"," LDA #$03\n STA NUSIZ1\n",1)
src=src.replace(" LDX #9\nPlayerDelay:\n"," LDX #5\nPlayerDelay:\n",1)
def extract(label):
 m=re.search(r"(?m)^"+re.escape(label)+r":\s*\n\s*BYTE ([^\n]+)",old)
 assert m is not None,label
 result=[int(i.strip().removeprefix("$"),16) for i in m.group(1).split(",")]
 assert len(result)==9,(label,result)
 return result
names={
  "M":"MaleRows","F":"FemaleRows","SM":"SmallMaleRows",
  "SF":"SmallFemaleRows","P":"PlayerRows","S":"ShotEnable"
}
masks={k:extract(v) for k,v in names.items()}
assert masks["M"]==[0x3c,0x3c,0x18,0xff,0x18,0x24,0x24,0x42,0x42]
assert masks["F"]==[0x3c,0x3c,0x18,0xff,0x3c,0x7e,0x7e,0x24,0x24]
assert masks["SM"]==[0,0x24,0x18,0x7e,0x18,0x3c,0x3c,0,0]
assert masks["SF"]==[0,0x24,0x3c,0x7e,0x18,0x3c,0x3c,0,0]
assert masks["P"]==[0x3c,0x7e,0x18,0x7e,0x1e,0x3c,0x18,0x24,0x42]
assert masks["S"]==[0,0,0,0,2,0,0,0,0]
start="R1acSelect:\n";end="R1acAfterRows:\n"
assert src.count(start)==src.count(end)==1
pre,rest=src.split(start,1)
discard,post=rest.split(end,1)
lines=["R1acSelect:"," JMP R1apNineRows","R1apNineRows:"," LDX #0"]
for y in range(8,-1,-1):
 lines.extend([
  "R1apScan"+str(8-y)+":",
  " STA WSYNC",
  " STX GRP1",            # clear late duplicates from previous scanline in HBLANK
  " LDX #$"+format(masks["F"][y],"02X"),
  " LDA #$"+format(masks["P"][y],"02X"),
  " STA GRP0",
  " LDA #$"+format(masks["S"][y],"02X"),
  " STA ENAM0",
  " LDA #$"+format(masks["M"][y],"02X"),
  " NOP"," NOP"," NOP"," NOP",
  " STA RESP1",           # c28 male
  " NOP",
  " STA GRP1",
  " NOP"," NOP",
  " STA RESP1",           # c40 female
  " STX GRP1",
  " LDX #0",
  " LDA #$"+format(masks["SM"][y],"02X"),
  " NOP"," NOP"," NOP"," NOP",
  " STA RESP1",           # c58 small male
  " STA GRP1",
  " LDA #$"+format(masks["SF"][y],"02X"),
  " NOP",
  " STA RESP1",           # c68 small female
  " STA GRP1"
 ])
assert lines.count(" STA RESP1")==36
src=pre+"\n".join(lines)+"\n"+end+post
for name in names.values():
 mark="\n"+name+":\n"
 assert old.count(mark)==src.count(mark)==1
 assert old.split(mark,1)[1].split("\n",1)[0]==src.split(mark,1)[1].split("\n",1)[0]
(R/"r1ap.asm").write_text(src)
subprocess.run(["dasm","r1ap.asm","-f3","-or1ap_4k.bin","-lr1ap.lst","-sr1ap.sym"],cwd=R,check=True)
four=(R/"r1ap_4k.bin").read_bytes()
assert len(four)==4096
rom=four*4;sha=hashlib.sha256(rom).hexdigest()
(R/"r1ap_F6.bin").write_bytes(rom)
(R/"ROM_SHA256.txt").write_text(sha+"  r1ap_F6.bin\n")
meta={
 "status":"BUILT_UNVERIFIED_R1AP_IMMEDIATE_UNROLLED_NINE_ROW_HYPOTHESIS",
 "NUSIZ1_value":3,
 "pinned_original_four_P1_ROM_SHA256":PIN,
 "P0_delay":5,"original_P0_delay":9,
 "four_RESP1_cpu_end_cycles":[28,40,58,68],
 "row_late_STA_GRP1_cpu_end":71,
 "next_STA_WSYN C_end":74,
 "expected_source_masks":"M M F F SM SF on same 9 rows, every source mask unchanged",
 "canonical_M_F_SM_SF_and_P_mask_byte_tables":"retained unchanged and immediate loaded from them",
 "one_original_yellow_P0_and_M0":"retained, P0 moved to remove white occlusion",
 "ROM_SHA256":sha,"bytes":16384,
 "mapper":"standard F6 4 identical 4KiB banks","video":"NTSC",
 "limitation":"Research only, no independently free six X, no full R1 or Verification"}
(R/"manifest.json").write_text(json.dumps(meta,indent=2)+"\n")
print(json.dumps(meta,indent=2))
