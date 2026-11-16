#!/usr/bin/env python3
"""R1n VISUAL HEIGHT RESEARCH. Derive two experiment ROMs from the exact R1k
five-NPC bitmap proof, preserving original nine source mask bytes byte-for-byte.
This is row repetition only, not approved modification to R1's original 8x9
sprite or claim that 14/15 rows meet R1 acceptance.
"""
from pathlib import Path
import hashlib,json,subprocess,re,sys
ROOT=Path(__file__).resolve().parent
BASE=ROOT.parent/"main_iii_r1k_fifth_female"
subprocess.run([sys.executable,str(BASE/"build_r1k.py")],check=True)
oldrom=(BASE/"r1k_F6.bin").read_bytes()
BASE_SHA="99c2cc160713899a8662508a4eeafec956b3d9b4825668e66b135404ec79f2a7"
assert hashlib.sha256(oldrom).hexdigest()==BASE_SHA,"R1k changed: stop"
old=(BASE/"r1k.asm").read_text()

LABELS=("MaleRows","FemaleRows","SmallMaleRows","SmallFemaleRows","PlayerRows")
def bytes_from_source(source,label):
    match=re.search(rf"(?m)^{label}:\s*\n\s+BYTE ([^\n]+)$",source)
    if not match:raise ValueError(f"Missing original bitmap {label}")
    vals=[int(v.strip().replace("$","0x"),16) for v in match.group(1).split(",")]
    assert len(vals)==9
    return vals[::-1] # Atari displayed top-to-bottom with Y8...0

originals={label:bytes_from_source(old,label) for label in LABELS}
for height in (14,15):
    source=old
    assert source.count(" LDY #8\n")==1
    source=source.replace(" LDY #8\n",f" LDY #{height-1}\n")
    derived={}
    for label in LABELS:
        newlabel=f"{label}{height}"
        assert source.count(" "+label+",Y\n")==4,(label,source.count(" "+label+",Y\n"))
        source=source.replace(" "+label+",Y\n"," "+newlabel+",Y\n")
        displayed=[originals[label][i*9//height] for i in range(height)]
        derived[label]=displayed
    original_doorbottom=""" LDX #10
R1hDoorBottom:
 STA WSYNC
 DEX
 BNE R1hDoorBottom
 LDA #$10
 STA PF0
 LDX #91
BottomLines:"""
    assert source.count(original_doorbottom)==1
    adjusted=f""" LDX #{10-(height-9)}
R1hDoorBottom:
 STA WSYNC
 DEX
 BNE R1hDoorBottom
 LDA #$10
 STA PF0
 LDX #91
BottomLines:"""
    source=source.replace(original_doorbottom,adjusted)
    appendix="\n; RESEARCH-ONLY derived display rows from original 8x9 byte tables.\n"
    for label in LABELS:
        appendix+=f"{label}{height}:\n BYTE "+",".join(f"{chr(36)}{b:02X}" for b in derived[label][::-1])+"\n"
    anchor=" ORG $FFFA\n"
    assert source.count(anchor)==1
    source=source.replace(anchor,appendix+anchor)
    for label in LABELS:
        assert bytes_from_source(source,label)==originals[label],f"Original mask changed: {label}"
    newlabel_match=re.findall(rf"(?m)^{LABELS[0]}{height}:\n BYTE ([^\n]+)$",source)
    assert len(newlabel_match)==1
    asm=f"r1n_{height}.asm"
    (ROOT/asm).write_text(source)
    subprocess.run(["dasm",asm,"-f3",f"-or1n_{height}_4k.bin",f"-lr1n_{height}.lst",f"-sr1n_{height}.sym"],cwd=ROOT,check=True)
    raw=(ROOT/f"r1n_{height}_4k.bin").read_bytes()
    assert len(raw)==4096,len(raw)
    rom=raw*4
    sha=hashlib.sha256(rom).hexdigest()
    (ROOT/f"r1n_{height}_F6.bin").write_bytes(rom)
    (ROOT/f"ROM_{height}_SHA256.txt").write_text(sha+f"  r1n_{height}_F6.bin\n")
    manifest=dict(status="BUILT_UNVERIFIED_HEIGHT_RESEARCH",height=height,
        exact_original_9byte_bitmaps_preserved=True,rendered_repeat_rows=height,
        map_top_to_bottom=[i*9//height for i in range(height)],
        fifth_original_NPC_R1k_base_SHA256=BASE_SHA,ROM_sha256=sha,
        F6_bytes=16384,door_gap_rows=32,
        LIMITS="Stretched VISUAL presentation only, original approved sprites are 8x9. Not full R1, not Verification; missile diagnostic still ABOVE player head.")
    (ROOT/f"manifest_{height}.json").write_text(json.dumps(manifest,indent=2)+"\n")
    print(json.dumps(manifest,indent=2))
