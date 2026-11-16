#!/usr/bin/env python3
"""R1m research: vertical M0 projectile in same nine-row band as five NPCs.

The previous R1k proved five original NPC at same Y but fired M0 at y160,
two lines ABOVE the y162 top of the yellow provisional player.
This experiment maps the unused 3-cycle BIT instruction to STX ENAM0:
X already holds the canonical small-female mask; its D1 is set on one
single row (Y=3, GUI y167). M0 is then enabled one scanline at waist/lower-arm
level without adding cycles or changing any original NPC bitmaps.

This is a diagnosis, not a claim that GUI y167 exactly matches visible gun arm.
"""
from pathlib import Path
import json,hashlib,subprocess,sys
ROOT=Path(__file__).resolve().parent
BASE=ROOT.parent/"main_iii_r1k_fifth_female"
subprocess.run([sys.executable,str(BASE/"build_r1k.py")],check=True)
old_rom=(BASE/"r1k_F6.bin").read_bytes()
EXPECTED="99c2cc160713899a8662508a4eeafec956b3d9b4825668e66b135404ec79f2a7"
assert hashlib.sha256(old_rom).hexdigest()==EXPECTED,"r1k baseline drift"
old=(BASE/"r1k.asm").read_text()
new=old
for suffix in "ABCD":
    needle=f"R1kAdditionalFemaleRESP1{suffix}:\n STA RESP1\n BIT FRAMELO\nR1cSecondDelay{suffix}:\n"
    repl=f"R1kAdditionalFemaleRESP1{suffix}:\n STA RESP1\n ; R1m: X=canonical SmallFemaleRows,Y. D1=1 on one row (Y=3) only.\n STX ENAM0\nR1cSecondDelay{suffix}:\n"
    assert new.count(needle)==1,suffix
    new=new.replace(needle,repl)
    assert new.count(f" STX ENAM0\nR1cSecondDelay{suffix}:\n")==1
# Disable the separate missile line above the player while retaining its
# 3-cycle STA and the calibrated 262-line/door top geometry.
old_shot=""" LDA #2
 STA ENAM0
 STA WSYNC
 LDA #0
 STA ENAM0
 LDA #$02
 STA NUSIZ0"""
new_shot=""" LDA #0
 STA ENAM0
 STA WSYNC
 LDA #0
 STA ENAM0
 LDA #$02
 STA NUSIZ0"""
assert new.count(old_shot)==1
new=new.replace(old_shot,new_shot)
# Canon sprite table and provisional player held bit-for-bit.
for label in ("MaleRows","FemaleRows","SmallMaleRows","SmallFemaleRows","PlayerRows"):
    assert old.split(label+":\n",1)[1].split("\n",1)[0]==new.split(label+":\n",1)[1].split("\n",1)[0],label
# X=0x7E only at top-down row 5, bit1=1; all other rows zero.
small_female=[0,0,0x3c,0x3c,0x18,0x7e,0x3c,0x24,0]
assert [i for i,x in enumerate(small_female) if x&2]==[5]
(ROOT/"r1m.asm").write_text(new)
subprocess.run(["dasm","r1m.asm","-f3","-or1m_4k.bin","-lr1m.lst","-sr1m.sym"],cwd=ROOT,check=True)
raw=(ROOT/"r1m_4k.bin").read_bytes()
assert len(raw)==4096
rom=raw*4
(ROOT/"r1m_F6.bin").write_bytes(rom)
sha=hashlib.sha256(rom).hexdigest()
(ROOT/"ROM_SHA256.txt").write_text(sha+"  r1m_F6.bin\n")
manifest={"status":"BUILT_UNVERIFIED_R1M",
    "R1k_base_sha256":EXPECTED,"ROM_sha256":sha,"ROM_bytes":16384,
    "original_NPC_masks_and_provisional_player":"bit-exact",
    "shot_expected_stella_gui_y":167,
    "shot_old_stella_gui_y":160,
    "shot_x_stella_gui":240,
    "technique":"Replace R1k one BIT FRAMELO (3 cycles) with STX ENAM0 (3 cycles), X=SmallFemaleRows,Y; D1 only on row5",
    "important_limit":"Shot y167 is lower than provisional player's arm row y165; test not automatically accepted as correct arm pose"}
(ROOT/"build_manifest.json").write_text(json.dumps(manifest,indent=2)+"\n")
print(json.dumps(manifest,indent=2))
