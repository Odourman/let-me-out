#!/usr/bin/env python3
"""R1v: add exactly 3 cycles to VBLANK RESM0 reset to move missile coarse X,
preserving the entire 14-row R1u five-NPC raster loop and its fine HMOVE.
In addition, display diagnostic (not gameplay) M0/P1 collision latch bit
on the blank background below the figures, reset to black next frame.
The test must fail closed on a missing projectile, an extra missile copy,
a lost NPC mask pixel EXCEPT exactly the 2 pixels covered by a real bullet,
a non-262 scanline frame, or collision display inconsistent with overlap.
"""
from pathlib import Path
import hashlib,json,subprocess,sys
ROOT=Path(__file__).resolve().parent
BASE=ROOT.parent/"main_iii_r1u_eight_m0_x"
subprocess.run([sys.executable,str(BASE/"build_r1u.py")],check=True)
prior=(BASE/"r1u_F6.bin").read_bytes()
BASE_SHA="ba06c63fd2247a4dfd47b5baa5619271c3ac851859c3ba3ca516bd4c227fc2e7"
assert hashlib.sha256(prior).hexdigest()==BASE_SHA,"R1u baseline changed!"
orig=(BASE/"r1u.asm").read_text()
src=orig
needle="M0Delay:\n DEX\n BNE M0Delay\n STA RESM0\n STA WSYNC"
repl="""M0Delay:
 DEX
 BNE M0Delay
 ; R1v COARSE RESET: 3 CPU cycles = 9 TIA CC = +18 GUI pixels.
 BIT FRAMELO
 STA RESM0
 STA WSYNC"""
assert src.count(needle)==1
src=src.replace(needle,repl)
# Capture M0/P1 D7 collision *after* shot+NPC row, before clearing latch.
needle="""R1gAfterRows:
 LDA #0
 STA GRP0
 STA GRP1
 STA ENAM0"""
repl="""R1gAfterRows:
 ; Diagnostic ONLY. Real CXM0P D7 = M0/P1 collision.
 ; Show the latch value as background tint below sprites.
 ; Read AFTER display band, clear before next frame.
 LDA CXM0P
 AND #$80
 STA COLUBK
 LDA #0
 STA CXCLR
 STA GRP0
 STA GRP1
 STA ENAM0"""
assert src.count(needle)==1
src=src.replace(needle,repl)
# Clear temporary collision background at beginning of each NEXT frame.
needle=""" STA WSYNC
 LDA #0
 STA GRP0
 STA GRP1
 STA ENAM0"""
repl=""" STA WSYNC
 LDA #0
 STA COLUBK
 STA GRP0
 STA GRP1
 STA ENAM0"""
assert src.count(needle)==1
src=src.replace(needle,repl)
# TIA read $00 is *CXM0P* and write $2C is CXCLR. Must use read side only.
needle="RESM0=$12\nGRP0=$1B"
assert src.count(needle)==1
src=src.replace(needle,"RESM0=$12\nCXM0P=$00\nCXCLR=$2C\nGRP0=$1B")
# Source masks and 14-row derived masks cannot change.
for name in ("MaleRows","FemaleRows","SmallMaleRows","SmallFemaleRows","PlayerRows"):
 for suf in ("","14"):
  label="\n"+name+suf+":\n"
  assert orig.count(label)==src.count(label)==1
  assert orig.split(label,1)[1].split("\n",1)[0]==src.split(label,1)[1].split("\n",1)[0]
# All four shot-raster code regions must remain EXACTLY unchanged.
for s in "ABCD":
 start=f"R1oShot{s}:\n";end=f"R1oLower{s}:\n"
 assert src.split(start,1)[1].split(end,1)[0]==orig.split(start,1)[1].split(end,1)[0]
(ROOT/"r1v.asm").write_text(src)
subprocess.run(["dasm","r1v.asm","-f3","-or1v_4k.bin","-lr1v.lst","-sr1v.sym"],cwd=ROOT,check=True)
raw=(ROOT/"r1v_4k.bin").read_bytes()
assert len(raw)==4096
rom=raw*4
sha=hashlib.sha256(rom).hexdigest()
(ROOT/"r1v_F6.bin").write_bytes(rom)
(ROOT/"ROM_SHA256.txt").write_text(sha+"  r1v_F6.bin\n")
info=dict(
 status="BUILT_UNVERIFIED_R1V_COARSE_M0_OVERLAP_COLLISION_DIAG",
 pinned_R1u_SHA256=BASE_SHA,
 ROM_SHA256=sha,ROM_bytes=len(rom),standard_F6_NTSC=True,
 change="3-cycle BIT FRAMELO immediately before VBLANK STA RESM0; +9 TIA color clocks = +18 GUI pixels",
 expected_M0_GUI_X=[250,252,254,256,258,260,262,264],M0_GUI_Y=167,
 NPC_female_one_GUI_X=248, collision_at_y167_when_overlapped=True,
 collision_display="CXM0P D7 -> COLUBK below NPC row, cleared after read and reset to 0 on next VBLANK",
 note="TEST_ONLY not game collision logic; overlap screen rendering must be proved and no extra missile clones",
 limits="five NPC masks only, static P0 X slots, not free-X, not entire room nor full R1, independent verification still pending")
(ROOT/"manifest.json").write_text(json.dumps(info,indent=2)+"\n")
print(json.dumps(info,indent=2))
