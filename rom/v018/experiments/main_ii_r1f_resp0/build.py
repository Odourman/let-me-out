#!/usr/bin/env python3
"""R1f: independent-position P0 double-retrigger experiment; ordinary F6 NTSC.

Source is exactly proven R1e four-original 600 frame kernel.
Replace P0 far-copy dependency by two SAME-SCANLINE medium-copy RESP0
strobes, one for yellow player (before first copy) and the other after
yellow player's pixels finish, for white original small female bitmap.
Two variants differ ONLY by exchanging adjacent STX GRP0 / STA RESP0:
therefore second P0 X moves by 3 CPU cycles = 9 TIA color clocks
while the first RESP0 and all P1 deadlines remain UNCHANGED.

This is an unverified HYPOTHESIS; actual Stella mask fidelity decides.
"""
from pathlib import Path
import subprocess,hashlib,json
ROOT=Path(__file__).resolve().parent
BASE=(ROOT.parent/"main_ii_p0_four"/"r1e_four_originals.asm").read_text()
checks=[
 " LDA #$04\n STA NUSIZ0", " ; Five cycles: first P0 copy remains yellow",
 " NOP\nR1cFirstRESP1:\n STA RESP1",
 " ; Three CPU cycles to preserve all 8 pixels of first P1 mask.\n BIT FRAMELO",
 " LDX #1\nR1cSecondDelay:\n DEX\n BNE R1cSecondDelay",
 "R1cSecondRESP1:\n STA RESP1\n ; Seven cycles: load the fourth ORIGINAL bitmap into P0 after yellow copy.\n LDX SmallFemaleRows,Y\nR1eFourthP0Write:\n STX GRP0"
]
for token in checks:
 assert token in BASE, f"Missing original R1e canonical section: {token}"
S=BASE.replace(" LDA #$04\n STA NUSIZ0"," LDA #$02\n STA NUSIZ0")
S=S.replace(" ; Calibrated P0=GUI-X186 using delay 4; extra VBLANK line restores 262.",
            " ; R1f: P0 reset every visible row at two fixed times; medium NUSIZ0=2.")
S=S.replace(" ; Five cycles: first P0 copy remains yellow on each NPC raster row.",
            " ; First P0 retrigger draws the yellow player via medium-copy decode.")
S=S.replace(" NOP\nR1cFirstRESP1:\n STA RESP1",
            " LDX SmallFemaleRows,Y\nR1cFirstRESP1:\n STA RESP1\nR1fYellowRESP0:\n STA RESP0")
S=S.replace(" ; Three CPU cycles to preserve all 8 pixels of first P1 mask.\n BIT FRAMELO\n",
            " ; Earlier P0 yellow copy is drawn by medium retrigger in this row.\n")
S=S.replace(" LDX #1\nR1cSecondDelay:\n DEX\n BNE R1cSecondDelay",
            " BIT FRAMELO\n BIT FRAMELO\nR1cSecondDelay:")
S=S.replace("R1cSecondRESP1:\n STA RESP1\n ; Seven cycles: load the fourth ORIGINAL bitmap into P0 after yellow copy.\n LDX SmallFemaleRows,Y\nR1eFourthP0Write:\n STX GRP0",
            "R1cSecondRESP1:\n STA RESP1\n ; P0's fourth mask already in X since before first P1 retrigger.\n"
            "R1fSecondP0Window:\nR1eFourthP0Write:\n STX GRP0\nR1fWhiteRESP0:\n STA RESP0")
assert S.count("R1fYellowRESP0:")==1 and S.count("R1fWhiteRESP0:")==1
assert S.count(" LDX SmallFemaleRows,Y")==1
variants={
 "early_white":S.replace("R1fSecondP0Window:\nR1eFourthP0Write:\n STX GRP0\nR1fWhiteRESP0:\n STA RESP0",
                         "R1fSecondP0Window:\nR1fWhiteRESP0:\n STA RESP0\nR1eFourthP0Write:\n STX GRP0"),
 "late_white":S
}
results={}
for variant,asm in variants.items():
    folder=ROOT/variant
    folder.mkdir(parents=True,exist_ok=True)
    (folder/"probe.asm").write_text(asm)
    subprocess.run(["dasm","probe.asm","-f3","-oprobe_4k.bin",
                    "-lprobe.lst","-sprobe.sym"],cwd=folder,check=True)
    one=(folder/"probe_4k.bin").read_bytes()
    assert len(one)==4096
    rom=one*4
    (folder/"probe_F6.bin").write_bytes(rom)
    results[variant]={
        "same_p0_yellow_resp0":"after first P1 RESP1",
        "second_p0_resp0":"before white mask write" if variant=="early_white" else "after white mask write",
        "usual_2x_medium_copy_NUSIZ0":"02",
        "standard_F6_16KB":len(rom),
        "sha256":hashlib.sha256(rom).hexdigest(),
        "expected_second_strobe_delta_cc":-9 if variant=="early_white" else 0
    }
(ROOT/"manifest.json").write_text(json.dumps(results,indent=2)+"\n")
print(json.dumps(results,indent=2))
