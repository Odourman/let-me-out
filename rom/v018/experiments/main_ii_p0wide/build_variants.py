#!/usr/bin/env python3
"""Research R1e: P0 two wide-spaced automatic copies with same-Y P1 triple masks.

control: NUSIZ0=$04, preserve R1c static three masks and original M0.
recolor: replace P1's 7-cycle second-delay with 7-cycle COLUP0 white write;
         restore yellow COLUP0 on each line at original 7-cycle M0 update.
M0 is deliberately moved to ONE adjacent raster line: this variant does NOT
meet the full integrated P0/M0/NPC gameplay burden. All NPC originals unchanged.
"""
from pathlib import Path
import hashlib, json, subprocess
ROOT=Path(__file__).resolve().parent
source=(ROOT.parent/"main_ii_three_masks"/"r1c_three_retriggers.asm").read_text()
assert source.count(" LDA #0\n STA NUSIZ0")==0
assert " STA NUSIZ0\n LDA #$01\n STA NUSIZ1" in source
assert " LDA ShotRows,Y\n STA ENAM0" in source
assert " LDX #1\nR1cSecondDelay:\n DEX\n BNE R1cSecondDelay" in source
control=source.replace(
    " STA NUSIZ0\n LDA #$01\n STA NUSIZ1",
    " STA NUSIZ0\n LDA #$01\n STA NUSIZ1")
# NUSIZ0 shares A=0 before STA; set A=4 immediately before its write.
control=control.replace(" STA NUSIZ0\n LDA #$01", " LDA #$04\n STA NUSIZ0\n LDA #$01")
assert " LDA #$04\n STA NUSIZ0" in control
recolor=control.replace(
    " LDA ShotRows,Y\n STA ENAM0",
    " ; Equivalent seven cycles; yellow reset before first P0 copy.\n"
    " LDA #$1E\n STA COLUP0\n NOP")
recolor=recolor.replace(
    " LDX #1\nR1cSecondDelay:\n DEX\n BNE R1cSecondDelay",
    " ; Equivalent seven cycles; recolor P0 before its wide copy.\n"
    " LDA #$0E\n STA COLUP0\n NOP\nR1cSecondDelay:")
recolor=recolor.replace(
    " LDX #80\nTopLines:", " LDX #79\nTopLines:")
recolor=recolor.replace(
    "TopLines:\n STA WSYNC\n DEX\n BNE TopLines\n LDY #8",
    "TopLines:\n STA WSYNC\n DEX\n BNE TopLines\n"
    " ; Test M0 one scanline BEFORE NPCs to free the same-Y kernel slot.\n"
    " LDA #2\n STA ENAM0\n STA WSYNC\n"
    " LDA #0\n STA ENAM0\n LDY #8")
assert " LDA #$0E\n STA COLUP0\n NOP" in recolor
assert " LDA #$1E\n STA COLUP0\n NOP" in recolor
assert " LDX #79\nTopLines:" in recolor
result={}
for name,text in (("p0wide_control",control),("p0wide_recolor",recolor)):
    folder=ROOT/name
    folder.mkdir(exist_ok=True,parents=True)
    (folder/"probe.asm").write_text(text)
    subprocess.run(["dasm","probe.asm","-f3","-oprobe_4k.bin",
                    "-lprobe.lst","-sprobe.sym"],cwd=folder,check=True)
    raw=(folder/"probe_4k.bin").read_bytes()
    assert len(raw)==4096
    rom=raw*4
    (folder/"probe_F6.bin").write_bytes(rom)
    result[name]={"size":len(rom),"sha256":hashlib.sha256(rom).hexdigest()}
(ROOT/"rom_manifest.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result,indent=2))
