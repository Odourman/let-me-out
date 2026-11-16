#!/usr/bin/env python3
"""R1k research-only possible fifth NPC: original large-female P1 bitmap
is retriggered twice on the same raster line at c39 and c45 (18 TIA CC).
One existing 3-cycle BIT padding becomes STA RESP1 (also 3 cycles).
Strictly preserve original R1h four NPC masks, player, M0, BL and PF.
"""
from pathlib import Path
import hashlib,json,subprocess,sys

ROOT=Path(__file__).resolve().parent
BASE=ROOT.parent/"main_ii_r1h_integrated"
subprocess.run([sys.executable,str(BASE/"build_integrated.py")],check=True)
old_rom=(BASE/"r1h_F6.bin").read_bytes()
BASE_SHA="2a6fc522b139eaebbec6731df8cab1f1c9297f2266ed44a38a9cc2f29b453a39"
assert hashlib.sha256(old_rom).hexdigest()==BASE_SHA, "R1h drift"
old=(BASE/"r1h_integrated.asm").read_text()
new=old
for suffix in "ABCD":
    needle=(f"\n BIT FRAMELO\n BIT FRAMELO\nR1cSecondDelay{suffix}:\n"
            f"R1cSecondRESP1{suffix}:\n STA RESP1\n")
    replacement=(f"\nR1kAdditionalFemaleRESP1{suffix}:\n STA RESP1\n BIT FRAMELO\n"
                 f"R1cSecondDelay{suffix}:\nR1cSecondRESP1{suffix}:\n STA RESP1\n")
    assert new.count(needle)==1, f"source layout drift in {suffix}"
    new=new.replace(needle,replacement)
    assert new.count(f"R1kAdditionalFemaleRESP1{suffix}:\n")==1
assert new.count(" ORG $F400")==1
for mask in ("MaleRows","FemaleRows","SmallMaleRows","SmallFemaleRows","PlayerRows"):
    assert old.split(mask+":\n",1)[1].split("\n",1)[0]==new.split(mask+":\n",1)[1].split("\n",1)[0],mask
for suffix in "ABCD":
    old_body=old.split(f"R1gRows{suffix}:\n",1)[1].split(
        f"R1gRows{'ABCD'[('ABCD'.index(suffix)+1)]}:\n" if suffix!="D" else "R1gAfterRows:\n",1)[0]
    new_body=new.split(f"R1gRows{suffix}:\n",1)[1].split(
        f"R1gRows{'ABCD'[('ABCD'.index(suffix)+1)]}:\n" if suffix!="D" else "R1gAfterRows:\n",1)[0]
    assert new_body.count(" STA RESP1\n")==old_body.count(" STA RESP1\n")+1
    assert new_body.count(" BIT FRAMELO\n")==old_body.count(" BIT FRAMELO\n")-1

(ROOT/"r1k.asm").write_text(new)
subprocess.run(["dasm","r1k.asm","-f3","-or1k_4k.bin","-lr1k.lst","-sr1k.sym"],cwd=ROOT,check=True)
raw=(ROOT/"r1k_4k.bin").read_bytes()
assert len(raw)==4096
rom=raw*4
(ROOT/"r1k_F6.bin").write_bytes(rom)
sha=hashlib.sha256(rom).hexdigest()
(ROOT/"ROM_SHA256.txt").write_text(sha+"  r1k_F6.bin\n")
manifest={
 "status":"BUILT_UNVERIFIED_R1K",
 "rom_bytes":len(rom),"ROM_SHA256":sha,
 "base_R1h_SHA256":BASE_SHA,
 "P1_large_female_retrigger_end_cycles":[39,45],
 "hypothesized_original_large_female_gui_x":[244,280],
 "fifth_NPC":"additional original large-female mask only if BOTH exact bitmaps pass 600 real Stella frames",
 "original_fourth_P0_positions":[330,348,360,378],
 "test_conditions":"fourth P0 4 x door 2, original 4 masks+additional fifth female, yellow player and prior-row M0",
 "limits":"18 CC hardware retrigger effects unknown; NOT a result until Stella pixels confirm"
}
(ROOT/"build_manifest.json").write_text(json.dumps(manifest,indent=2)+"\n")
print(json.dumps(manifest,indent=2))
