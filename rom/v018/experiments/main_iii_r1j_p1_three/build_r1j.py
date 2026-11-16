#!/usr/bin/env python3
"""R1j-A research-only P1 three-position test. Build from exact verified R1i-A.
P1 large-female second RESP1 occurs at cycle 39, 42, or 45.
P0 small-female fourth copy retains four exact original X modes.
No new TIA writes or CPU cycles are added to the nine-row kernel.
"""
from pathlib import Path
import hashlib, json, re, subprocess, sys

ROOT=Path(__file__).resolve().parent
PARENT=ROOT.parent/"main_iii_r1i_p1shift"
subprocess.run([sys.executable,str(PARENT/"build_r1i.py")],check=True)
verified=(PARENT/"r1i_F6.bin").read_bytes()
SHA_R1I="34a7f515773c6991d0a7abff4d48f6f9d82dadcfb364fb8996d5ccb31539c55c"
assert hashlib.sha256(verified).hexdigest()==SHA_R1I, "R1i parent changed"
base=(PARENT/"r1i.asm").read_text()
start=" LDY #8\n ; R1i P1 female mode is independent FRAMELO bit7."
assert base.count(start)==1
head,post=base.split(start)
assert post.count("R1gRowsA:\n")==1 and post.count("R1gAfterRows:\n")==1
previous_selector,post=post.split("R1gRowsA:\n",1)
rows,tail=post.split("R1gAfterRows:\n",1)
rows="R1gRowsA:\n"+rows
parts={}
for i,suffix in enumerate("ABCDEFGH"):
    marker=f"R1gRows{suffix}:\n"
    following=f"R1gRows{'ABCDEFGH'[i+1]}:\n" if i<7 else ""
    assert rows.count(marker)==1
    part=rows.split(marker,1)[1]
    if following: part=part.split(following,1)[0]
    assert part.count(" STA RESP1\n")==3
    assert part.count(" BIT FRAMELO\n")==2
    parts[suffix]=marker+part

def rename(source,old,new):
    labels=set(re.findall(r"(?m)^([A-Za-z][A-Za-z0-9_]*):\s*$",source))
    assert labels and all(x.endswith(old) for x in labels)
    for label in sorted(labels,key=len,reverse=True):
        source=re.sub(r"\b"+re.escape(label)+r"\b",label[:-1]+new,source)
    return source

middle={}
for old,new in zip("ABCD","IJKL"):
    section=rename(parts[old],old,new)
    needle=("\n BIT FRAMELO\n BIT FRAMELO\n"
            f"R1cSecondDelay{new}:\nR1cSecondRESP1{new}:\n STA RESP1\n")
    replacement=("\n BIT FRAMELO\n"
                 f"R1cSecondRESP1{new}:\n STA RESP1\n"
                 " BIT FRAMELO\n"
                 f"R1cSecondDelay{new}:\n")
    assert section.count(needle)==1
    middle[new]=section.replace(needle,replacement)
    assert middle[new].count(" STA RESP1\n")==3
    assert middle[new].count(" BIT FRAMELO\n")==2

selector=""" LDY #8
 ; Three P1 positions from two low FRAMELO bits: early, middle, late.
 ; P0 four X positions use bits 4-5; door uses bit 6. All are independent.
 LDA FRAMELO
 AND #$0C
 BEQ R1jSelectEarly
 CMP #$04
 BEQ R1jSelectMiddle
 JMP R1jSelectLate
R1jSelectEarly:
 LDA FRAMELO
 AND #$30
 BEQ R1jEarlyE
 CMP #$10
 BEQ R1jEarlyF
 CMP #$20
 BEQ R1jEarlyG
 JMP R1gRowsH
R1jEarlyE:
 JMP R1gRowsE
R1jEarlyF:
 JMP R1gRowsF
R1jEarlyG:
 JMP R1gRowsG
R1jSelectMiddle:
 LDA FRAMELO
 AND #$30
 BEQ R1jMiddleI
 CMP #$10
 BEQ R1jMiddleJ
 CMP #$20
 BEQ R1jMiddleK
 JMP R1gRowsL
R1jMiddleI:
 JMP R1gRowsI
R1jMiddleJ:
 JMP R1gRowsJ
R1jMiddleK:
 JMP R1gRowsK
R1jSelectLate:
 LDA FRAMELO
 AND #$30
 BEQ R1jLateA
 CMP #$10
 BEQ R1jLateB
 CMP #$20
 BEQ R1jLateC
 JMP R1gRowsD
R1jLateA:
 JMP R1gRowsA
R1jLateB:
 JMP R1gRowsB
R1jLateC:
 JMP R1gRowsC
"""
src=(head+selector+"".join(parts[k] for k in "ABCDEFGH")
     +"".join(middle[k] for k in "IJKL")+"R1gAfterRows:\n"+tail)
assert src.count(" ORG $F400")==1
for suffix in "ABCDEFGHIJKL":
    for label in ("R1gRows","R1cSecondRESP1","R1fYellowRESP0","R1fWhiteRESP0"):
        assert src.count(label+suffix+":\n")==1, (label,suffix)
for mask in ("MaleRows","FemaleRows","SmallMaleRows","SmallFemaleRows","PlayerRows"):
    old=base.split(mask+":\n",1)[1].split("\n",1)[0]
    new=src.split(mask+":\n",1)[1].split("\n",1)[0]
    assert old==new, mask

(ROOT/"r1j.asm").write_text(src)
subprocess.run(["dasm","r1j.asm","-f3","-or1j_4k.bin","-lr1j.lst","-sr1j.sym"],cwd=ROOT,check=True)
raw=(ROOT/"r1j_4k.bin").read_bytes()
assert len(raw)==4096, len(raw)
rom=raw*4
(ROOT/"r1j_F6.bin").write_bytes(rom)
sha=hashlib.sha256(rom).hexdigest()
(ROOT/"ROM_SHA256.txt").write_text(sha+"  r1j_F6.bin\n")
manifest={
 "status":"BUILT_UNVERIFIED_R1J",
 "source_verified_R1i_SHA256":SHA_R1I,
 "ROM_bytes":len(rom),"mapper":"standard 16KiB F6",
 "ROM_SHA256":sha,
 "second_P1_RESP1_CPU_cycle":[39,42,45],
 "P1_GUI_X_predictions":[244,262,280],
 "P0_fourth_GUI_X":[330,348,360,378],
 "right_door_states":2,
 "target_combinations":24,
 "limits":"Four original NPC only, 3 discrete P1 X; original P0 + door; no free 160CC X, no full R1"
}
(ROOT/"build_manifest.json").write_text(json.dumps(manifest,indent=2)+"\n")
print(json.dumps(manifest,indent=2))
