#!/usr/bin/env python3
"""Generate two scoped, original-assembly near-copy timing experiments.

Read only the already proven ghost-free R1b reference on this branch.
Each output retains both byte-exact reference NPC masks and P0/M0.
"""
from pathlib import Path
import subprocess
import hashlib
import json

HERE=Path(__file__).resolve().parent
BASE=HERE.parent/"main_ii_r1b"/"r1b_two_masks.asm"
src=BASE.read_text()
old=""" LDX #1
R1bPostFirst:
 DEX
 BNE R1bPostFirst
"""
assert src.count(old)==1, "Unexpected source structure - abort"
variants={
  "near60": " BIT $00\n",   # replace six-cycle loop with 3-cycle BIT
  "near51": "",             # eliminate six-cycle loop altogether
}
results={}
for name,replacement in variants.items():
    folder=HERE/name
    folder.mkdir(exist_ok=True)
    asm=folder/"near.asm"
    asm.write_text(src.replace(old,replacement))
    image4=folder/"near_4k.bin"
    sym=folder/"proof.sym"
    listing=folder/"proof.lst"
    subprocess.run(["dasm","near.asm","-f3",f"-o{image4.name}",
                    f"-l{listing.name}",f"-s{sym.name}"],cwd=folder,check=True)
    assert image4.stat().st_size==4096
    four=image4.read_bytes()
    full=folder/"proof_F6.bin"
    full.write_bytes(four*4)
    assert full.stat().st_size==16384
    results[name]={"sha256":hashlib.sha256(full.read_bytes()).hexdigest(),
                   "size":full.stat().st_size,"source":str(asm)}
(HERE/"rom_manifest.json").write_text(json.dumps(results,indent=2)+"\n")
print(json.dumps(results,indent=2))
