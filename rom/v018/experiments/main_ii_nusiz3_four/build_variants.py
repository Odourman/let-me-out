#!/usr/bin/env python3
"""Isolated 6502 diagnostic variants from the locally successful R1c source.

nusiz3_only: three regular P1 original bitmaps; NUSIZ1=$03 automatic copies.
four_mask_probe: fourth different original 8x9 bitmap, no fourth RESP1.
M0 moves to preceding row to save 7 cycles in the 9-NPC-line kernel.
This diagnostic compromise is NOT a proof of full gameplay or free-X R1.
"""
from pathlib import Path
import hashlib, json, subprocess
ROOT=Path(__file__).resolve().parent
SRC=ROOT.parent/"main_ii_three_masks"/"r1c_three_retriggers.asm"
REF=ROOT.parent/"main_ii_three_masks"/"REFERENCE_8x9_MASKS_FROM_MAIN.json"
source=SRC.read_text()
ref=json.loads(REF.read_text())
assert " LDA #$01\n STA NUSIZ1" in source
assert "R1cThirdRESP1:\n STA RESP1\n DEY" in source
assert ref["sprites"]["small_female"]==[
    "00000000","00000000","00111100","00111100",
    "00011000","01111110","00111100","00100100","00000000"]
a=source.replace(" LDA #$01\n STA NUSIZ1"," LDA #$03\n STA NUSIZ1")
b=a.replace(
    "R1cThirdRESP1:\n STA RESP1\n DEY",
    "R1cThirdRESP1:\n STA RESP1\n"
    " ; Attempt fourth original mask on the third reset's medium copy.\n"
    " LDA SmallFemaleRows,Y\nR1dSmallFemaleWrite:\n STA GRP1\n DEY")
b=b.replace(" LDA ShotRows,Y\n STA ENAM0\n","")
b=b.replace(" LDX #12\nP0Delay:"," LDX #5\nP0Delay:")
b=b.replace(" LDX #80\nTopLines:"," LDX #79\nTopLines:")
b=b.replace(
  "TopLines:\n STA WSYNC\n DEX\n BNE TopLines\n LDY #8",
  "TopLines:\n STA WSYNC\n DEX\n BNE TopLines\n"
  " ; One separate M0 shot-line: no 7-cycle M0 update on NPC scanlines.\n"
  " LDA #2\n STA ENAM0\n STA WSYNC\n LDA #0\n STA ENAM0\n LDY #8")
smf=[int(x,2) for x in ref["sprites"]["small_female"]]
b=b.replace(
 "PlayerRows:\n BYTE",
 "SmallFemaleRows:\n BYTE "+",".join("$%02X"%v for v in smf[::-1])+
 "\nPlayerRows:\n BYTE")
assert "R1dSmallFemaleWrite" in b and b.count("SmallFemaleRows:")==1
assert " LDX #79\nTopLines:" in b and " LDA #2\n STA ENAM0\n STA WSYNC" in b
results={}
for name,variant in [
    ("nusiz3_only",a),
    ("four_mask_probe",b)
]:
    folder=ROOT/name
    folder.mkdir(parents=True,exist_ok=True)
    (folder/"probe.asm").write_text(variant)
    subprocess.run(["dasm","probe.asm","-f3","-oprobe_4k.bin",
                    "-lprobe.lst","-sprobe.sym"],cwd=folder,check=True)
    raw=(folder/"probe_4k.bin").read_bytes()
    assert len(raw)==4096
    image=raw*4
    (folder/"probe_F6.bin").write_bytes(image)
    results[name]={"standard_f6_16kb":len(image),
                   "sha256":hashlib.sha256(image).hexdigest()}
(ROOT/"manifest.json").write_text(json.dumps(results,indent=2)+"\n")
print(json.dumps(results,indent=2))
