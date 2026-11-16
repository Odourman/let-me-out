#!/usr/bin/env python3
"""Trick #10: four HMP0 values from locally proven R1e static four-mask ROM.

The ONLY intended change is coarse-free fine positioning on P0; P0's automatic
white fourth-NPC copy will move with the yellow player. P1 and M0 are zero.
No claims about independent fourth NPC X or six NPCs.
"""
from pathlib import Path
import subprocess,hashlib,json
ROOT=Path(__file__).resolve().parent
SRC=ROOT.parent/"main_ii_p0_four"/"r1e_four_originals.asm"
BASE=SRC.read_text()
needle="FRAMELO=$80"
assert needle in BASE
src=BASE.replace(needle,needle+"\nHMP0=$20\nHMP1=$21\nHMM0=$22\nHMM1=$23\nHMBL=$24\nHMOVE=$2A")
old=""" INC FRAMELO
 STA WSYNC
 LDA #0
 STA GRP0"""
new=""" INC FRAMELO
 ; Phase selects fine-offset from 0/-1/-3/+3 color clocks.
 LDA FRAMELO
 LSR
 LSR
 LSR
 LSR
 AND #3
 TAX
 LDA P0FineTable,X
 STA HMP0
 ; Explicitly keep P1, missile0, missile1 and ball unmoved.
 LDA #0
 STA HMP1
 STA HMM0
 STA HMM1
 STA HMBL
 STA WSYNC
 LDA #0
 STA GRP0"""
assert old in src
src=src.replace(old,new)
old2=""" STA RESP1
 STA WSYNC
 LDX #34
BlankLines:"""
new2=""" STA RESP1
 STA WSYNC
 ; Proper HMOVE: immediate command during following horizontal blanking.
HMoveStrobe:
 STA HMOVE
 LDX #34
BlankLines:"""
assert old2 in src
src=src.replace(old2,new2)
assert "ShotRows:\n BYTE" in src
src=src.replace("ShotRows:\n BYTE $00,$00,$00,$00,$02,$00,$00,$00,$00",
"ShotRows:\n BYTE $00,$00,$00,$00,$02,$00,$00,$00,$00\nP0FineTable:\n BYTE $00,$F0,$D0,$30")
assert src.count("P0FineTable:")==1
(ROOT/"trick10_hmove.asm").write_text(src)
cmd=["dasm","trick10_hmove.asm","-f3","-otrick10_4k.bin",
     "-ltrick10.lst","-strick10.sym"]
subprocess.run(cmd,cwd=ROOT,check=True)
raw=(ROOT/"trick10_4k.bin").read_bytes()
assert len(raw)==4096
full=raw*4
(ROOT/"trick10_F6.bin").write_bytes(full)
(ROOT/"ROM_SHA256.txt").write_text(
    f'{hashlib.sha256(full).hexdigest()}  trick10_F6.bin\n')
print(json.dumps({"rom_size":len(full),"sha256":hashlib.sha256(full).hexdigest(),
"motion_register_high_nibbles":{"0":"00","1":"F0","2":"D0","3":"30"},
"target":"P0 shifts, original first P0 and white P0 duplicate together; P1 and M0 static"},
indent=2))
