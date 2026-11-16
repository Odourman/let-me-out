#!/usr/bin/env python3
"""Trick #05: PF1 dynamic raster sprite in a separate 9-line band.

Four static-offset ROM variants: mask unchanged, shift PF pixels by 1/2
PF bits (each PF bit is 4 TIA color clocks). Entire R1e four-NPC game band
remains unchanged. DOES NOT CLAIM PF is a valid 8x9 humanoid or free same-Y
sprite channel. Observed mirrored right-half copy is part of the test.
"""
from pathlib import Path
import subprocess,hashlib,json
ROOT=Path(__file__).resolve().parent
BASE=(ROOT.parent/"main_ii_p0_four"/"r1e_four_originals.asm").read_text()
assert "COLUBK=$09" in BASE
assert " LDX #79\nTopLines:" in BASE
assert "TopLines:\n STA WSYNC\n DEX\n BNE TopLines\n" in BASE
SRC=BASE.replace("COLUBK=$09","COLUBK=$09\nCOLUPF=$08")
SRC=SRC.replace(" LDA #$0E\n STA COLUP1",
                " LDA #$0E\n STA COLUP1\n LDA #$36\n STA COLUPF")
SRC=SRC.replace(" LDX #79\nTopLines:"," LDX #70\nTopLines:")
source_marker="TopLines:\n STA WSYNC\n DEX\n BNE TopLines\n"
pf_band="""TopLines:
 STA WSYNC
 DEX
 BNE TopLines
 ; Nine source PF rows, one per raster line, Y=8..0.
 LDY #8
PFSpriteBand:
 STA WSYNC
 LDA PFRow,Y
 STA PF1
 DEY
 BPL PFSpriteBand
 LDA #0
 STA PF1
"""
SRC=SRC.replace(source_marker,pf_band)
assert "PFSpriteBand:" in SRC
assert "ShotRows:\n BYTE $00,$00,$00,$00,$02,$00,$00,$00,$00" in SRC
base_rows=[0x00,0x18,0x24,0x3C,0x3C,0x3C,0x24,0x18,0x00] # top to bottom
out={}
for shift in (-2,-1,1,2):
    label={-2:"left2",-1:"left1",1:"right1",2:"right2"}[shift]
    new=[]
    for b in base_rows:
        x=(b>>(-shift)) if shift<0 else ((b<<shift)&255)
        new.append(x)
    source=SRC.replace("ShotRows:\n BYTE $00,$00,$00,$00,$02,$00,$00,$00,$00",
        "ShotRows:\n BYTE $00,$00,$00,$00,$02,$00,$00,$00,$00\n"+
        "PFRow:\n BYTE "+",".join(f"${v:02X}" for v in new[::-1]))
    assert source.count("PFRow:")==1
    path=ROOT/label
    path.mkdir(exist_ok=True,parents=True)
    (path/"probe.asm").write_text(source)
    subprocess.run(["dasm","probe.asm","-f3","-oprobe_4k.bin",
                    "-lprobe.lst","-sprobe.sym"],cwd=path,check=True)
    data=(path/"probe_4k.bin").read_bytes()
    assert len(data)==4096
    rom=data*4
    (path/"probe_F6.bin").write_bytes(rom)
    out[label]={"shift_pf_bits":shift,"pf_bit_width_tia_clocks":4,
                "rom_sha256":hashlib.sha256(rom).hexdigest(),
                "top_down_pf_rows_hex":[f"{v:02X}" for v in new]}
(ROOT/"manifest.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps(out,indent=2))
