#!/usr/bin/env python3
"""R1h: four-original-R1g 600-pass kernel + BALL left wall + PF0 right door.

The ball replaces the LEFT reflected PF0 wall (4 TIA CC); PF0 D4 supplies
RIGHT wall when closed, or zero when open. Door state toggles every 64 frames
in VBLANK; fourth NPC chooses one of four 16-frame X via existing R1g.
ZERO new instructions inside ANY of four proven 76-cycle NPC row kernels.
BALL horizontal RESPBL timing calibrated from real Stella X11 not guessed.

In this calibration harness, 0..7 NOPs after WSYNC yield eight candidate
RESBL offsets. Each candidate is a distinct 16KB standard-F6 ROM; a single
dynamic multi-mode production candidate must be built only after calibration.
No change to original approved NPC reference masks.
"""
from pathlib import Path
import json,hashlib,subprocess,sys
ROOT=Path(__file__).resolve().parent
PARENT=ROOT.parent/"main_ii_r1g_dynamic"
subprocess.run([sys.executable,str(PARENT/"build_dynamic.py")],check=True)
BASE=(PARENT/"r1g_four_dynamic.asm").read_text()
assert BASE.count(" STA RESP1\n STA WSYNC\n LDX #34\nBlankLines:")==1
assert BASE.count(" STA COLUP1\nFrame:")==1
assert BASE.count(" STA PF0")==1
assert BASE.count(" STA COLUP0")==4*2+1 or BASE.count(" STA COLUP0")>=5
source=BASE.replace("COLUP1=$07","COLUP1=$07\nCOLUPF=$08\nCTRLPF=$0A")
source=source.replace("RESP1=$11","RESP1=$11\nRESBL=$14")
source=source.replace("ENAM0=$1D","ENAM0=$1D\nENABL=$1F")
source=source.replace(" STA COLUP1\nFrame:",
""" STA COLUP1
 ; REFLECT PF and 4 color-clock BALL width, brown independent outer wall.
 LDA #$21
 STA CTRLPF
 LDA #$36
 STA COLUPF
 LDA #2
 STA ENABL
Frame:""")
old=" STA RESP1\n STA WSYNC\n LDX #34\nBlankLines:"
assert old in source
out={}
for count in range(0,8):
    # Keep additional placement scanline budget neutral by reducing BlankLines 34->33.
    placement=(" NOP\n"*count)
    new=""" STA RESP1
 STA WSYNC
 ; Dedicated VBLANK test line to position 4CC BALL near LEFT visible x0.
"""+placement+"""R1hSetBall:
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
    src=source.replace(old,new)
    # Four bitmaps remain byte-identical to main; four P1/P0 critical loops unchanged.
    assert src.count("R1gRowsA:")==1
    path=ROOT/f"delay_{count}"
    path.mkdir(parents=True,exist_ok=True)
    (path/"probe.asm").write_text(src)
    subprocess.run(["dasm","probe.asm","-f3","-oprobe_4k.bin",
                    "-lprobe.lst","-sprobe.sym"],cwd=path,check=True)
    blob=(path/"probe_4k.bin").read_bytes()
    assert len(blob)==4096
    rom=blob*4
    (path/"probe_F6.bin").write_bytes(rom)
    out[f"delay_{count}"]={
      "ball_NOP_count_after_WSYNC":count,
      "sha256":hashlib.sha256(rom).hexdigest(),
      "ROM_bytes":len(rom),
      "door_toggle":"FRAMELO & $40",
      "fourth_npc_X_select":"FRAMELO & $30"}
(ROOT/"manifest.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps(out,indent=2))
