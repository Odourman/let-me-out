#!/usr/bin/env python3
"""R1g four orderings of the SAME four P0 register instructions.

The 2 already proven exact R1f positions are the controls. Two new modes
only reorder STX GRP0, LDA #$0E, STA COLUP0, STA RESP0; exactly
11 total CPU cycles per scanline, same P1 deadlines, player unchanged.
Fail closed against actual Stella pixels. No claim full free X.
"""
from pathlib import Path
import subprocess,hashlib,json,sys
ROOT=Path(__file__).resolve().parent
PARENT=ROOT.parent/"main_ii_r1f_resp0"
subprocess.run([sys.executable,str(PARENT/"build.py")],check=True)
e=(PARENT/"early_white"/"probe.asm").read_text()
l=(PARENT/"late_white"/"probe.asm").read_text()
old="""R1fSecondP0Window:
R1eFourthP0Write:
 STX GRP0
R1fWhiteRESP0:
 STA RESP0
 ; Five cycles: whiten only P0 automatic wide-spaced second copy.
 LDA #$0E
R1eFourthColorWrite:
 STA COLUP0"""
c="""R1fSecondP0Window:
R1eFourthP0Write:
 STX GRP0
 ; Loading white A (2 cycles) while bitmap already in GRP0.
 LDA #$0E
R1fWhiteRESP0:
 STA RESP0
R1eFourthColorWrite:
 STA COLUP0"""
d="""R1fSecondP0Window:
R1eFourthP0Write:
 STX GRP0
 LDA #$0E
R1eFourthColorWrite:
 STA COLUP0
R1fWhiteRESP0:
 STA RESP0"""
assert old in l
variants={"pre_mask":e,"post_mask":l,"post_lda":l.replace(old,c),
          "post_color":l.replace(old,d)}
manifest={}
for name,src in variants.items():
    dest=ROOT/name
    dest.mkdir(parents=True,exist_ok=True)
    (dest/"probe.asm").write_text(src)
    subprocess.run(["dasm","probe.asm","-f3","-oprobe_4k.bin",
                    "-lprobe.lst","-sprobe.sym"],cwd=dest,check=True)
    data=(dest/"probe_4k.bin").read_bytes()
    assert len(data)==4096
    full=data*4
    (dest/"probe_F6.bin").write_bytes(full)
    manifest[name]={"rom_bytes":len(full),"sha256":hashlib.sha256(full).hexdigest()}
(ROOT/"manifest.json").write_text(json.dumps(manifest,indent=2)+"\n")
print(json.dumps(manifest,indent=2))
