#!/usr/bin/env python3
"""R1h integrated 4CC BL left wall + PF0 only right door + four-state R1g.

Source from eight-WYSIWYG Stella calibrated R1g kernel, delay0: BALL normally
starts GUI x108; HMBL $20 and HMOVE at start of blanking is intended to move
it -2 TIA CC, to x104. This is a HYPOTHESIS pending actual Stella evidence.

Asymmetric PF right edge closes everywhere except 32 door-band scanlines.
Open/closed toggles via FRAMELO bit6. Four original NPC mask ROW KERNELS
are UNCHANGED from 600-frame proven R1g. BALL consumes hardware BL.
"""
from pathlib import Path
import json,hashlib,subprocess,sys
ROOT=Path(__file__).resolve().parent
PARENT=ROOT.parent/"main_ii_r1h_ball_wall"
subprocess.run([sys.executable,str(PARENT/"calibrate_build.py")],check=True)
BASE=(PARENT/"delay_0"/"probe.asm").read_text()
assert BASE.count("R1gRowsA:")==1 and BASE.count("R1gRowsD:")==1
assert BASE.count("R1hSetBall:")==1
old="""R1hSetBall:
 STA RESBL
 ; Toggle right edge only every 64 frames. PF0 changes OUTSIDE NPC scanlines.
 LDA FRAMELO
 AND #$40
 BEQ R1hRightLocked
 LDA #0
 JMP R1hWritePF0
R1hRightLocked:
 LDA #$10
R1hWritePF0:
 STA PF0
 STA WSYNC
 LDX #33
BlankLines:"""
new="""R1hSetBall:
 STA RESBL
 STA WSYNC
 ; Shift BALL left by 2CC during blank scanline. Never HMOVE in NPC rows.
R1hHMOVE:
 STA HMOVE
 LDA #$10
 STA PF0
 LDX #33
BlankLines:"""
assert BASE.count(old)==1
src=BASE.replace(old,new)
src=src.replace("RESBL=$14","RESBL=$14\nHMP0=$20\nHMP1=$21\nHMM0=$22\nHMM1=$23\nHMBL=$24\nHMOVE=$2A")
oldreset=""" LDA #2
 STA ENABL
Frame:"""
newreset=""" LDA #2
 STA ENABL
 ; Explicit zero on four other motion registers, only BALL moves -2 CC.
 LDA #0
 STA HMP0
 STA HMP1
 STA HMM0
 STA HMM1
 LDA #$20
 STA HMBL
Frame:"""
assert src.count(oldreset)==1
src=src.replace(oldreset,newreset)
oldtop=""" LDX #79
TopLines:
 STA WSYNC
 DEX
 BNE TopLines
 ; R1f:"""
newtop=""" LDX #67
TopLines:
 STA WSYNC
 DEX
 BNE TopLines
 ; New 32 scanline doorway band: 12 rows before M0, 1 M0 + 9 NPC,
 ; 10 rows after NPC. LEFT BL wall stays on through entire scene.
 STA WSYNC
 LDA FRAMELO
 AND #$40
 BEQ R1hDoorLocked
 LDA #0
 JMP R1hBeginDoor
R1hDoorLocked:
 LDA #$10
R1hBeginDoor:
 STA PF0
 LDX #11
R1hDoorTop:
 STA WSYNC
 DEX
 BNE R1hDoorTop
 ; R1f:"""
assert src.count(oldtop)==1
src=src.replace(oldtop,newtop)
# MUST clear A before the original shot-line STA NUSIZ0. With door locked,
# A=$10 otherwise widens M0 from 1 to 2 color clocks (actual Stella FAIL).
shotline="R1hDoorTop:\\n STA WSYNC\\n DEX\\n BNE R1hDoorTop\\n ; R1f:"
assert src.count(shotline.replace("\\\\n","\\n"))==1
src=src.replace(shotline.replace("\\\\n","\\n"),shotline.replace("\\\\n","\\n").replace(" ; R1f:"," LDA #0\\n ; R1f:"))
oldend="""R1gAfterRows:
 LDA #0
 STA GRP0
 STA GRP1
 STA ENAM0
 LDX #101
BottomLines:"""
newend="""R1gAfterRows:
 LDA #0
 STA GRP0
 STA GRP1
 STA ENAM0
 ; 10 physical rows after NPC, then restore closed right wall.
 LDX #10
R1hDoorBottom:
 STA WSYNC
 DEX
 BNE R1hDoorBottom
 LDA #$10
 STA PF0
 LDX #91
BottomLines:"""
assert src.count(oldend)==1
src=src.replace(oldend,newend)
assert src.count("R1hHMOVE:")==1
assert src.count("R1hDoorTop:")==1
assert src.count("R1hDoorBottom:")==1
# Confirm the exact four cycle-critical row source bodies have NOT CHANGED.
a=BASE.split("R1gRowsA:\n")[1].split("R1gAfterRows:\n")[0]
b=src.split("R1gRowsA:\n")[1].split("R1gAfterRows:\n")[0]
assert a==b, "Change to critical 4-NPC cycle kernel is forbidden"
(ROOT/"r1h_integrated.asm").write_text(src)
subprocess.run(["dasm","r1h_integrated.asm","-f3","-or1h_4k.bin",
                "-lr1h.lst","-sr1h.sym"],cwd=ROOT,check=True)
raw=(ROOT/"r1h_4k.bin").read_bytes()
assert len(raw)==4096
rom=raw*4
(ROOT/"r1h_F6.bin").write_bytes(rom)
sha=hashlib.sha256(rom).hexdigest()
(ROOT/"ROM_SHA256.txt").write_text(sha+"  r1h_F6.bin\n")
info={"ROM_bytes":len(rom),"sha256":sha,
      "original_R1g_four_critical_mask_kernels_byte_source_identical":True,
      "BALL_left_4cc":"RESBL in blank + HMBL $20, HMOVE at blank cycle0",
      "PF_right_door":"32 rows opening selected by FRAMELO bit6, outside four critical NPC row loops",
      "fourth_NPC_X":"four independent 16-frame slots selected by FRAMELO & $30",
      "limits":"not yet proven in Stella; BALL resource consumed, no door orange/keyhole"}
(ROOT/"build_manifest.json").write_text(json.dumps(info,indent=2)+"\n")
print(json.dumps(info,indent=2))
