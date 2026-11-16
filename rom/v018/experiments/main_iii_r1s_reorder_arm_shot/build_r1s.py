#!/usr/bin/env python3
"""R1s: try C/D cycle-preserving instruction reordering for the 14-row five-NPC M0 shot.

Keep the R1o source/ROM pinned. A/B stay unchanged.
C/D: defer STX GRP0 until AFTER required late RESP0 strobe, yet before
the small female's pixels start. Meanwhile shut down missile immediately
after second large-female RESP1 (c45) at CPU c48, before extra M0 copy.
This keeps both c53/c56 RESP0 phases and all 5 original masks if correct.
No added CPU cycles or changed source mask bytes.
"""
from pathlib import Path
import hashlib,json,subprocess,sys
ROOT=Path(__file__).resolve().parent
BASE=ROOT.parent/"main_iii_r1o_single_arm_shot"
subprocess.run([sys.executable,str(BASE/"build_r1o.py")],check=True)
parent=(BASE/"r1o_F6.bin").read_bytes()
EXPECTED="41a1b55a4d413cca88eccd690d29b6af1a041e4a354e0f4838a832f10fd6c44d"
assert hashlib.sha256(parent).hexdigest()==EXPECTED, "R1o base changed"
old=(BASE/"r1o.asm").read_text()
src=old
needle_c=""" STX GRP0
 ; Loading white A (2 cycles) while bitmap already in GRP0.
 STY ENAM0
 LDA #$0E
 STA RESP0
 STA COLUP0
 ; Seven cycles: third P1's original mask; preserves 76-cycle budget."""
replace_c=""" ; R1s C: disable M0 at c48; restore RESP0 at original c53.
 ; The small female does not draw until after delayed GRP0 at c56.
 STY ENAM0
 LDA #$0E
 STA RESP0
 STX GRP0
 STA COLUP0
 ; Seven cycles: third P1's original mask; preserves 76-cycle budget."""
assert src.count(needle_c)==1
src=src.replace(needle_c,replace_c)
needle_d=""" STX GRP0
 STY ENAM0
 LDA #$0E
 STA COLUP0
 STA RESP0
 ; Seven cycles: third P1's original mask; preserves 76-cycle budget."""
replace_d=""" ; R1s D: disable M0 at c48; restore RESP0 at original c56.
 ; The small female does not draw until after delayed GRP0 at c59.
 STY ENAM0
 LDA #$0E
 STA COLUP0
 STA RESP0
 STX GRP0
 ; Seven cycles: third P1's original mask; preserves 76-cycle budget."""
assert src.count(needle_d)==1
src=src.replace(needle_d,replace_d)
for s in "AB":
    assert src.split(f"R1oShot{s}:\n",1)[1].split(f"R1oLower{s}:\n",1)[0]==old.split(f"R1oShot{s}:\n",1)[1].split(f"R1oLower{s}:\n",1)[0],"A/B regression"
for x in ("MaleRows","FemaleRows","SmallMaleRows","SmallFemaleRows","PlayerRows"):
    for suffix in ("","14"):
        assert src.split(x+suffix+":\n",1)[1].split("\n",1)[0]==old.split(x+suffix+":\n",1)[1].split("\n",1)[0],x+suffix
(ROOT/"r1s.asm").write_text(src)
subprocess.run(["dasm","r1s.asm","-f3","-or1s_4k.bin","-lr1s.lst","-sr1s.sym"],check=True,cwd=ROOT)
base4=(ROOT/"r1s_4k.bin").read_bytes()
assert len(base4)==4096
rom=base4*4
sha=hashlib.sha256(rom).hexdigest()
(ROOT/"r1s_F6.bin").write_bytes(rom)
(ROOT/"ROM_SHA256.txt").write_text(sha+"  r1s_F6.bin\n")
manifest={
 "status":"BUILT_UNVERIFIED_R1S",
 "parent_R1o_ROM_SHA256":EXPECTED,"R1s_ROM_SHA256":sha,
 "standard_16K_F6_bytes":len(rom),
 "five_source_original_8x9_masks_and_14_display_rows":"unchanged",
 "shot":{"gui_x":232,"gui_y":167,"required_copy_count":1},
 "C_cycle_strobes":{"ENAM0_off":48,"RESP0":53,"GRP0":56},
 "D_cycle_strobes":{"ENAM0_off":48,"RESP0":56,"GRP0":59},
 "original_P0_fourth_X":[330,348,360,378],
 "test_goal":"ALL 600/600 Stella frames five NPC + one arm-height M0, 4x2 modes",
 "limitations":"STATIC shot; free X, six NPC, collision hit logic and full R1 all still blocked"
}
(ROOT/"build_manifest.json").write_text(json.dumps(manifest,indent=2)+"\n")
print(json.dumps(manifest,indent=2))
