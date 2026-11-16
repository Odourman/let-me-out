#!/usr/bin/env python3
"""R1-F6 single 6502 F6/NTSC two-mask probe.
One invocation builds EXACTLY ONE of only two authorized phases (21 or 23).
HARD G0 source preflight MUST have succeeded first; no 6-NPC build or R1ba.
"""
from pathlib import Path
import subprocess,hashlib,json,argparse
R=Path(__file__).resolve().parent
ROOT=R.parents[3]
TEMPLATE=ROOT/"rom/v018/experiments/venetian_blinds/vb_9_interleave.asm"
CANON=ROOT/"design/NPC_REFERENCE_8x9_masks.json"
p=argparse.ArgumentParser();p.add_argument("--first",type=int,choices=[21,23],required=True)
args=p.parse_args();phase=args.first
pre=json.loads((R/"r1_f6_g0_source_only.json").read_text())
assert pre["G0"]=="F6_SOURCE_ONLY_FEASIBLE_BOTH_PHASES_9_ROWS"
assert pre["preflight_allows_ONLY_first_c21_ROM_then_c23_ROM_if_c21_real_pixel_gate_passes"]
assert pre["plans"][f"c{phase}_c32"]["first_RESP1_end"]==phase
old=TEMPLATE.read_text()
canon=json.loads(CANON.read_text())["sprites"]
male=[int(row,2) for row in canon["large_male"]]
female=[int(row,2) for row in canon["large_female"]]
assert male==[0x3c,0x3c,0x18,0xff,0x18,0x24,0x24,0x42,0x42]
assert female==[0x3c,0x3c,0x18,0xff,0x3c,0x7e,0x7e,0x24,0x24]
player=[0x3c,0x7e,0x18,0x7e,0x1e,0x3c,0x18,0x24,0x42]
anchor="Row00:\n"
end="\n STA WSYNC\n LDA #0\n STA GRP0\n STA GRP1\n STA ENAM0\n LDX #102\nBottomBlank:"
assert old.count(anchor)==old.count(end)==1
head,other=old.split(anchor,1)
oldrows,tail=other.split(end,1)
assert oldrows.count(" STA RESP1\n")==9
assert head.count("COLUBK=$09\n")==1 and head.count(" STA COLUBK\n LDA #145\n")==1
head=head.replace("COLUBK=$09\n","COLUBK=$09\nCOLUPF=$08\nCTRLPF=$0A\n",1)
head=head.replace(" STA COLUBK\n LDA #145\n",
  " STA COLUBK\n LDA #$26\n STA COLUPF\n LDA #1\n STA CTRLPF\n LDA #$F0\n STA PF0\n LDA #1\n STA NUSIZ1\n LDA #145\n",1)
assert " LDA #1\n STA NUSIZ1\n" in head
assert " STA HMOVE\n" in head and "TopBlank:\n" in head and "BlankFill:\n" in head
assert " STA VDEL1" not in head
# X=0 for zero-page indexed $11 RESP1 phase23 store; no X changes in the raster.
head += (" ; R1-F6 G0 approved isolated correct TOP-DOWN 2-mask HBLANK/START experiment.\n"
         " ; DO NOT use older R1ba reversed row order.\n"
         " LDX #0\n")
rows=[]
for y in range(9):
    q=[f"R1F6Row{y:02d}:",
       " STA WSYNC",
       " LDA #$%02X" % player[y]," STA GRP0",
       " LDA #$%02X" % (2 if y==4 else 0)," STA ENAM0",
       " LDA #$%02X" % male[y]]
    q+=[" NOP"]*(3 if phase==21 else 4)
    q+=[" STA RESP1"," STA GRP1"," LDA #$%02X" % female[y]]
    if phase==21:q+=[" BIT FRAMELO"," STA RESP1"]
    else:q+=[" STA RESP1,X"] # zero page $11, four cycles; X stays 0.
    q+=[" STA GRP1"]
    p0=pre["plans"][f"c{phase}_c32"]["nine_rows"][y]
    assert (p0["male_canon_byte"],p0["female_canon_byte"])==(f"{male[y]:02X}",f"{female[y]:02X}")
    assert q.count(" STA RESP1")+q.count(" STA RESP1,X")==2
    assert q.count(" STA GRP1")==2
    rows+=q
source=head+"\n".join(rows)+"\n"+end.lstrip("\n")+tail.replace(" ORG $F300\n"," ORG $F800\n",1)
assert source.count(" STA RESP1\n")+source.count(" STA RESP1,X\n")==18
assert source.count(" STA GRP1\n")==9*2+3 # Reset,VBlank,BottomBlank + 18 visible
assert source.count(" STA NUSIZ1\n")==2
assert source.count(" STA HMOVE\n")==1
assert source.count(" STA PF0\n")==2
assert source.count(" STA COLUPF\n")==1
assert " ORG $F800\n" in source and " ORG $F300\n" not in source
for y in range(9):
    a=source.index(f"R1F6Row{y:02d}:")
    b=source.index(f"R1F6Row{y+1:02d}:") if y<8 else source.index(" STA WSYNC\n LDA #0\n STA GRP0\n STA GRP1\n STA ENAM0\n LDX #102\nBottomBlank:")
    r=source[a:b]
    assert r.count(" STA GRP1\n")==2 and r.count(" STA RESP1\n")+r.count(" STA RESP1,X\n")==2
    assert " LDA #$%02X" % male[y] in r and " LDA #$%02X" % female[y] in r
    assert not any(op in r for op in (" DEX\n"," BNE "," BEQ "," TAX\n"," INX\n"))
stem=f"r1_f6_two_correct_masks_C{phase:02d}_C32"
src=R/f"{stem}.asm"
src.write_text(source)
dist=R/"dist";dist.mkdir(exist_ok=True)
subprocess.run(["dasm",src.name,"-f3",
    f"-odist/{stem}.4k.bin",f"-ldist/{stem}.lst",f"-sdist/{stem}.sym"],cwd=R,check=True)
bank=(dist/f"{stem}.4k.bin").read_bytes()
assert len(bank)==4096
rom=bank*4;assert len(rom)==16384
romp=dist/f"{stem}_F6.bin";romp.write_bytes(rom)
lst=(dist/f"{stem}.lst").read_text()
assert lst.count("RESP1")>=18
if phase==23:
    assert len([line for line in lst.splitlines() if "95 11" in line and "RESP1,X" in line])==9
else:
    assert len([line for line in lst.splitlines() if "BIT FRAMELO" in line])==9
manifest={
 "status":"BUILT_BUT_NOT_YET_STELLA_PASSED","source_preflight":"SOURCE_ONLY_FEASIBLE_BOTH",
 "F6_phase_first_RESP1":phase,"second_RESP1":32,"first_GRP1":phase+3,"second_GRP1":35,
 "nine_source_rows":9,"first_mask":"large_male TOP_DOWN","second_mask":"large_female TOP_DOWN",
 "source_canon_git_blob":"058800a4c1904d1ff289e7e61b3902aa111ba16d",
 "P0_yellow_original":True,"M0_one_static_shot":True,
 "NUSIZ1":1,"PF0":240,"CTRLPF":1,"COLUPF":38,
 "source_only_next_WSYNC_end":38,"source_only_cycle_margin":38,
 "ROM_file":str(romp.relative_to(R)),"size":len(rom),"bank_size":len(bank),
 "four_bank_copies_identical":all(rom[i*4096:(i+1)*4096]==bank for i in range(4)),
 "ROM_sha256":hashlib.sha256(rom).hexdigest(),
 "ASM_sha256":hashlib.sha256(source.encode()).hexdigest(),
 "preregistered_crop_X_prediction":[43,99] if phase==21 else [45,99],
 "physical_pixel_result":"UNKNOWN_UNTIL_REAL_STELLA",
 "no_runtime_independent_X":True}
(dist/f"{stem}.json").write_text(json.dumps(manifest,indent=2)+"\n")
print("F6_ONE_ALLOWED_ROM_BUILT",phase,"size",len(rom),"SHA256",manifest["ROM_sha256"])
print("F6_ROW_CYCLE_SOURCE_ONLY first",phase,"GRP",phase+3,"second",32,"GRP 35","next WSYNC 38","margin 38")
