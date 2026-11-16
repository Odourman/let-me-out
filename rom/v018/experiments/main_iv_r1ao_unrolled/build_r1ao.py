#!/usr/bin/env python3
"""R1ao RESEARCH: unrolled 9-row raster kernel, fixed X P1 under NUSIZ1=3.
Four source-distinct 8x9 masks M,F,SM,SF, allow extra M/F auto-clones;
clear P1 after last sprite to suppress tail ghosts without BPL cycles.
NO independent X, no gameplay, no production modifications.
"""
from pathlib import Path
import os,sys,subprocess,hashlib,json
R=Path(__file__).resolve().parent
P=R.parent/"main_iv_r1aj_four_p1"
subprocess.run([sys.executable,str(P/"build_r1aj.py")],
 env=dict(os.environ,R1AJ_BATCH="0"),check=True)
PIN="ff0f1c64ffff1915cef934f224b3f3d780bc2de6cc52038d62666904c1f0f263"
assert hashlib.sha256((P/"r1aj_F6.bin").read_bytes()).hexdigest()==PIN
old=(P/"r1aj.asm").read_text()
assert old.count(" LDA #$01\n STA NUSIZ1\n")==1
src=old.replace(" LDA #$01\n STA NUSIZ1\n"," LDA #$03\n STA NUSIZ1\n",1)
start="R1acSelect:\n";end="R1acAfterRows:\n"
assert src.count(start)==src.count(end)==1
before,rest=src.split(start,1)
discard,after=rest.split(end,1)
# At c28 first P1 close, c40 second, c54 third and c64 fourth:
# c28 RESP1 M, c40 F, c54 SM, c64 SF.
# No loop branch means 3 CPU cycles saved. STX GRP1 c72
# disables subsequent late unwanted close/medium copies.
row=[
 " STA WSYNC",
 " LDX FemaleRows,Y",
 " LDA PlayerRows,Y",
 " STA GRP0",
 " LDA ShotEnable,Y",
 " STA ENAM0",
 " LDA MaleRows,Y",
 " BIT FRAMELO",
 " STA RESP1",
 " NOP",
 " STA GRP1",
 " NOP",
 " NOP",
 " STA RESP1",
 " STX GRP1",
 " LDX #0",
 " LDA SmallMaleRows,Y",
 " NOP",
 " STA RESP1",
 " STA GRP1",
 " LDA SmallFemaleRows,Y",
 " STA RESP1",
 " STA GRP1",
 " DEY",
 " STX GRP1"
]
seq=["R1acSelect:"," JMP R1aoRows","R1aoRows:"," LDY #8"]
for k in range(9):
 seq.append("R1aoLine"+str(k)+":")
 seq+=row
assert seq.count(" STA RESP1")==36
# Last output executed c72 and R1acAfterRows starts STA WSYNC c75.
src=before+"\n".join(seq)+"\n"+end+after
for name in ("MaleRows","FemaleRows","SmallMaleRows","SmallFemaleRows","PlayerRows","ShotEnable"):
 mark="\n"+name+":\n"
 assert old.count(mark)==src.count(mark)==1
 assert old.split(mark,1)[1].split("\n",1)[0]==src.split(mark,1)[1].split("\n",1)[0]
(R/"r1ao.asm").write_text(src)
subprocess.run(["dasm","r1ao.asm","-f3","-or1ao_4k.bin","-lr1ao.lst","-sr1ao.sym"],cwd=R,check=True)
four=(R/"r1ao_4k.bin").read_bytes()
assert len(four)==4096
rom=four*4
sha=hashlib.sha256(rom).hexdigest()
(R/"r1ao_F6.bin").write_bytes(rom)
(R/"ROM_SHA256.txt").write_text(sha+"  r1ao_F6.bin\n")
manifest={
 "status":"BUILT_UNVERIFIED_R1AO_UNROLLED_NINE_ROW_RESEARCH",
 "pinned_R1aj_four_original_PASS_ROM_SHA256":PIN,
 "NUSIZ1_value":3,
 "four_P1_RESP1_per_scanline":[28,40,54,64],
 "P1_late_zero_GR P1_end_cycle":72,
 "next_WSYN C_cpu_end":75,
 "nine_rows":"unrolled, original 9 row source data tables byte-for-byte unchanged",
 "P0_yellow_player_and_M0_static_shot":"unchanged",
 "ROM_SHA256":sha,"bytes":16384,
 "mapper":"standard 16K F6 (4 copies of 4K source)","video":"NTSC",
 "limitations":"No motion, collision, walls/door/key, no independent verification, no full six-free-X R1"}
(R/"manifest.json").write_text(json.dumps(manifest,indent=2)+"\n")
print(json.dumps(manifest,indent=2))
