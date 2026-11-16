#!/usr/bin/env python3
"""Trick #25 PHA through mirrored 6507 TIA stack page, isolated VBLANK reset.

CONTROL: LDA #$36 / STA COLUPF (3 cycle write).
STACK:   LDA #$36 / LDX #$08 / TXS / PHA writes $0108 mirror of TIA $08
         / LDX #$FF / TXS restores SP before any JSR/RTS.
No user stack/return op while transient SP. Proves only same TIA pixel effect
on our R3 PF door, NOT more scanline bandwidth or source compatibility.
"""
from pathlib import Path
import subprocess,hashlib,json
ROOT=Path(__file__).resolve().parent
BASE=(ROOT.parent/"main_ii_trick07_asym_pf"/"asymmetric_door.asm").read_text()
needle=" LDA #$36\n STA COLUPF\nFrame:"
assert needle in BASE
variants={
 "control_sta":BASE,
 "stack_pha":BASE.replace(needle," LDA #$36\n ; Controlled PHA bus write to mirrored COLUPF $0108.\n"
               " LDX #$08\n TXS\nR25PhaColor:\n PHA\n LDX #$FF\n TXS\nFrame:")
}
manifest={}
for name,source in variants.items():
 folder=ROOT/name
 folder.mkdir(parents=True,exist_ok=True)
 (folder/"probe.asm").write_text(source)
 subprocess.run(["dasm","probe.asm","-f3","-oprobe_4k.bin",
                 "-lprobe.lst","-sprobe.sym"],cwd=folder,check=True)
 raw=(folder/"probe_4k.bin").read_bytes()
 assert len(raw)==4096
 rom=raw*4
 (folder/"probe_F6.bin").write_bytes(rom)
 manifest[name]={"rom_length":len(rom),"sha256":hashlib.sha256(rom).hexdigest()}
(ROOT/"manifest.json").write_text(json.dumps(manifest,indent=2)+"\n")
print(json.dumps(manifest,indent=2))
