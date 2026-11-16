#!/usr/bin/env python3
"""Calibrate actual TIA RESP0 coarse position from isolated R1c 3-mask source."""
from pathlib import Path
import hashlib,json,subprocess
ROOT=Path(__file__).resolve().parent
source=(ROOT.parent/"main_ii_three_masks"/"r1c_three_retriggers.asm").read_text()
assert " LDX #12\nP0Delay:" in source
delays=[4,6,8,10,12,13,14,15]
manifest={}
for delay in delays:
    folder=ROOT/("delay_%02d"%delay)
    folder.mkdir(parents=True,exist_ok=True)
    asm=source.replace(" LDX #12\nP0Delay:"," LDX #%d\nP0Delay:"%delay)
    (folder/"probe.asm").write_text(asm)
    subprocess.run(["dasm","probe.asm","-f3","-oprobe_4k.bin",
                    "-lprobe.lst","-sprobe.sym"],cwd=folder,check=True)
    data=(folder/"probe_4k.bin").read_bytes()
    assert len(data)==4096
    rom=data*4
    (folder/"probe_F6.bin").write_bytes(rom)
    manifest[str(delay)]={"sha256":hashlib.sha256(rom).hexdigest(),"size":len(rom)}
(ROOT/"rom_manifest.json").write_text(json.dumps(manifest,indent=2)+"\n")
print(json.dumps(manifest,indent=2))
