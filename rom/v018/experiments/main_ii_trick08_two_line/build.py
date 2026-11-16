#!/usr/bin/env python3
"""Trick #08 control versus a two-physical-rasterlines-per-bitmap-row variant.

Source: unchanged successful R1e 600-frame four-original 8x9 mask kernel.
The negative variant deliberately adds one STA WSYNC per original NPC line
and compensates the overall 262-line frame count by subtracting nine from
BottomLines. This is NOT assumed to preserve the 9-raster-row design.
"""
from pathlib import Path
import hashlib,subprocess,json
ROOT=Path(__file__).resolve().parent
BASE=(ROOT.parent/"main_ii_p0_four"/"r1e_four_originals.asm").read_text()
assert "R1cThirdRESP1:\n STA RESP1\n DEY\n BPL R1cRow" in BASE
assert " LDX #101\nBottomLines:" in BASE
variant=BASE.replace(
  "R1cThirdRESP1:\n STA RESP1\n DEY\n BPL R1cRow",
  "R1cThirdRESP1:\n STA RESP1\n"
  " ; New WSYNC forces every source bitmap row to occupy two scanlines.\n"
  " ; No original bytes are modified. The extra line may expose P1 ghost.\n"
  " STA WSYNC\n DEY\n BPL R1cRow")
variant=variant.replace(" LDX #101\nBottomLines:"," LDX #92\nBottomLines:")
assert " LDX #92\nBottomLines:" in variant
results={}
for label,src in [("control_one_line",BASE),("two_line_naive",variant)]:
    dir=ROOT/label
    dir.mkdir(parents=True,exist_ok=True)
    (dir/"probe.asm").write_text(src)
    subprocess.run(["dasm","probe.asm","-f3","-oprobe_4k.bin",
                    "-lprobe.lst","-sprobe.sym"],cwd=dir,check=True)
    raw=(dir/"probe_4k.bin").read_bytes()
    assert len(raw)==4096
    full=raw*4
    (dir/"probe_F6.bin").write_bytes(full)
    results[label]={"size":len(full),"sha256":hashlib.sha256(full).hexdigest()}
(ROOT/"rom_manifest.json").write_text(json.dumps(results,indent=2)+"\n")
print(json.dumps(results,indent=2))
