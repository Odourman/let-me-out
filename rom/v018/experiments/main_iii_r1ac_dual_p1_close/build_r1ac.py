#!/usr/bin/env python3
"""MAIN III research-only R1ac: TWO DIFFERENT original 8x9 P1 masks
on each SAME raster scanline, via two RESP1 close-copy triggers and GRP1.
Four modes c30/42,c32/42,c30/44,c32/44 measure independent fine X.
No change to production or approved gameplay. This is not R1 PASS.
"""
from pathlib import Path
import hashlib,subprocess,re,json
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[3]
BASE=REPO/"rom/v018/experiments/venetian_blinds/vb_9_interleave.asm"
raw=BASE.read_bytes()
# Git blob identity pins the exact previous ROM DEVELOPMENT source.
blob=hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()
PIN="a25c92adb4ca5087eeace674e371be98b273ae5b"
assert blob==PIN,(blob,PIN,"base Venetian source not authorized reference")
s=raw.decode("utf-8")
# NUSIZ1=$01 is essential: it enables P1 CLOSE copy decoding, not merely
# the RESP1 positional counter reset.
assert s.count(" STA COLUBK\n LDA #145\n")==1
s=s.replace(" STA COLUBK\n LDA #145\n",
            " STA COLUBK\n LDA #$01\n STA NUSIZ1\n LDA #145\n",1)
assert s.count("Row00:\n")==1
assert s.count("\n STA WSYNC\n LDA #0\n STA GRP0\n STA GRP1\n STA ENAM0\n LDX #102\nBottomBlank:")==1
a,b=s.split("Row00:\n",1)
old_rows,tail=b.split("\n STA WSYNC\n LDA #0\n STA GRP0\n STA GRP1\n STA ENAM0\n LDX #102\nBottomBlank:",1)
assert "Row08:" in old_rows and old_rows.count(" STA RESP1")==9
# Original raw 8x9 bytes, unmodified source labels.
for name,expected in {
 "MaleRows":"$3C,$3C,$18,$FF,$18,$24,$24,$42,$42",
 "FemaleRows":"$3C,$3C,$18,$FF,$3C,$7E,$7E,$24,$24",
 "PlayerRows":"$3C,$7E,$18,$7E,$1E,$3C,$18,$24,$42"
}.items():
 assert s.count(name+":\n BYTE "+expected)==1,("mask changed",name)
# Source line order is bottom->top because visible kernel uses Y=8..0.
# No change to approved 8x9 bitmap data. Add a separate one-row shot-enable table.
assert "ShotEnable:" not in s
# Keep ROM data clear of four separate ALIGN 256 kernel pages.
assert s.count(" ORG $F300\n")==1
s=s.replace(" ORG $F300\n"," ORG $F800\n",1)
assert "\nMaleRows:\n" in s
s=s.replace("\nMaleRows:\n","\n ALIGN 256\nMaleRows:\n",1)
# Additional control bits have no graphic mask meaning.
s=s.replace("\n ORG $FFFA\n","\nShotEnable:\n BYTE $00,$00,$00,$00,$02,$00,$00,$00,$00\n ORG $FFFA\n",1)
# Need to replace the original rows after the mask insertion, not the old source.
a,b=s.split("Row00:\n",1)
old_rows,tail=b.split("\n STA WSYNC\n LDA #0\n STA GRP0\n STA GRP1\n STA ENAM0\n LDX #102\nBottomBlank:",1)
heads=[
 ("C",30,42,1,3),
 ("D",32,42,2,2),
 ("E",30,44,1,4),
 ("F",32,44,2,3)
]
kernels=[]
timing={}
for key,c1,c2,n1,n2 in heads:
 body=[
 f" ALIGN 256\nR1acKernel{key}:\n LDY #8\nR1acRowSync{key}:\n STA WSYNC",
 " LDA MaleRows,Y",
 " STA GRP1",
 " LDX FemaleRows,Y",
 " LDA PlayerRows,Y",
 " STA GRP0",
 " LDA ShotEnable,Y",
 " STA ENAM0",
 ]+[" NOP"]*n1+[
 " STA RESP1",  # P1 close copy #1
 " BIT FRAMELO", # A/X intact
 ]+[" NOP"]*n2+[
 " STA RESP1",  # P1 close copy #2
 " STX GRP1",  # second ORIGINAL mask
 " DEY",
 f" BPL R1acRowSync{key}",
 " JMP R1acAfterRows"
 ]
 assert 25+2*n1+3==c1
 assert c1+3+2*n2+3==c2
 assert c2+3+2+3+3==c2+11
 timing[key]={"resp1_endcycles":[c1,c2],"close_start_x_model":[3*c1-51,3*c2-51],
              "grp1_female_endcycle":c2+3,"scanline_cpu_to_loop_branch":c2+8,
              "scanline_cpu_including_jmp_entry_to_next_WSYNCH":c2+14}
 kernels.append("\n".join(body)+"\n")
# Branch/dispatch before first WSYNC; adds no extra rows vs old 9-row chain.
dispatcher="""R1acSelect:
 LDA FRAMELO
 AND #$03
 BEQ R1acPickC
 CMP #$01
 BEQ R1acPickD
 CMP #$02
 BEQ R1acPickE
 JMP R1acKernelF
R1acPickC:
 JMP R1acKernelC
R1acPickD:
 JMP R1acKernelD
R1acPickE:
 JMP R1acKernelE
"""
# All four aligned kernels: make placement absolute and BPL within same page.
part=a+dispatcher+"\n".join(kernels)+"R1acAfterRows:\n"
src=part+"\n STA WSYNC\n LDA #0\n STA GRP0\n STA GRP1\n STA ENAM0\n LDX #102\nBottomBlank:"+tail
# Source after ORG FF... still assembled within normal 4 KiB; test with DASM.
(ROOT/"r1ac.asm").write_text(src)
subprocess.run(["dasm","r1ac.asm","-f3","-or1ac_4k.bin","-lr1ac.lst","-sr1ac.sym"],cwd=ROOT,check=True)
four=(ROOT/"r1ac_4k.bin").read_bytes()
assert len(four)==4096,len(four)
rom=four*4
sha=hashlib.sha256(rom).hexdigest()
(ROOT/"r1ac_F6.bin").write_bytes(rom)
(ROOT/"ROM_SHA256.txt").write_text(sha+"  r1ac_F6.bin\n")
manifest={
 "status":"BUILT_UNVERIFIED_R1AC_SAME_Y_TWO_DISTINCT_8X9_P1_ORIGINAL_MASKS",
 "parent_ROM_DEV_blob_sha":PIN,"ROM_SHA256":sha,"bytes":len(rom),
 "format":"16K F6 NTSC, 4 identical banks",
 "purpose":"Isolated R1 two fully different P1 bitmaps on same 9 scanlines, independent two-X toggles",
 "variants":timing,"shot_y":"middle row (Y=4), one row-only M0",
 "original_mask_data":"MaleRows/FemaleRows/PlayerRows unchanged, no 14-row scaling",
 "critical_risk":"second RESP may abort ongoing first copy, late GRP1 may overwrite earlier mask, ghosts/extra main copy",
 "exclusions":"No six NPC; no full game; not integrated R1-R4; no independent verification; no production changes"
}
(ROOT/"manifest.json").write_text(json.dumps(manifest,indent=2)+"\n")
print(json.dumps(manifest,indent=2))
