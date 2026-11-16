#!/usr/bin/env python3
"""R1o research: isolate the shot on one of 14 rows, 5 original NPCs.
Original R1n14 ROM SHA is pinned. Top 5 + arm row + lower 8 regular
rows are cycle-neutrally split at pre-visible row-loop boundaries.
Shot-only raster uses original FemaleRows14,Y A bit1 to ENABLE M0,
and Y=8 bit1=0 to DISABLE M0 before automatic medium-size copy.
At this row SmallFemaleRows14,Y == SmallMaleRows14,Y == $3C,
so TXA replaces 4-cycle LDA ...Y (2 cycles) to recover time.
M0 is nudged left by four TIA color clocks via HMM0=$40 during blank HMOVE.
This is a hardware hypothesis, not guaranteed to work before Stella.
"""
from pathlib import Path
import hashlib,json,re,subprocess,sys
ROOT=Path(__file__).resolve().parent
BASE=ROOT.parent/"main_iii_r1n_height"
subprocess.run([sys.executable,str(BASE/"build_r1n.py")],check=True)
base_rom=(BASE/"r1n_14_F6.bin").read_bytes()
BASE_SHA="eb52e6baf37a396acbbf424a7ba937d78ef662cce7a47aff0cda9d9c6cf25558"
assert hashlib.sha256(base_rom).hexdigest()==BASE_SHA,"R1n14 base changed: stop"
base=(BASE/"r1n_14.asm").read_text()
def parse_mask(label):
    m=re.search(rf"(?m)^{label}:\s*\n\s*BYTE ([^\n]+)$",base)
    assert m,label
    return [int(v.strip().replace("$","0x"),16) for v in m.group(1).split(",")][::-1]
names=("MaleRows","FemaleRows","SmallMaleRows","SmallFemaleRows","PlayerRows")
original={s:parse_mask(s) for s in names}
assert len(original["FemaleRows"])==9
masks14={s:parse_mask(s+"14") for s in names}
assert all(len(v)==14 for v in masks14.values())
assert masks14["FemaleRows"][5]&2 and masks14["FemaleRows"][5]==0xFF
assert masks14["SmallFemaleRows"][5]==masks14["SmallMaleRows"][5]==0x3c
assert 8&2==0,"Y=8 can STY ENAM0 off"

old=' LDA #2\n STA ENAM0\n STA WSYNC\n LDA #0\n STA ENAM0'
assert base.count(old)==1
src=base.replace(old,' LDA #0\n STA ENAM0\n STA WSYNC\n LDA #0\n STA ENAM0')
hmm=' STA HMM1\n LDA #$20\n STA HMBL'
assert src.count(hmm)==1
src=src.replace(hmm,' STA HMM1\n ; R1o: shot from hand x232, instead of old x240.\n LDA #$40\n STA HMM0\n LDA #$20\n STA HMBL')
assert src.count(" LDY #13\n")==1
src=src.replace(" LDY #13\n"," LDY #4\n")
head,blocks=src.split("R1gRowsA:\n",1)
assert blocks.count("R1gAfterRows:\n")==1
rowzone,tail=blocks.split("R1gAfterRows:\n",1)
rowzone="R1gRowsA:\n"+rowzone

def strip_debug_labels(body):
    body=re.sub(r"(?m)^R1(?:c|f|e|k)[A-Za-z0-9_]+:\n","",body)
    assert not re.search(r"(?m)^R1(?:c|f|e|k)[A-Za-z0-9_]+:",body)
    return body

new_parts=[]
for i,suffix in enumerate("ABCD"):
    mark=f"R1gRows{suffix}:\n"
    assert rowzone.count(mark)==1
    part=rowzone.split(mark,1)[1]
    if i<3:part=part.split(f"R1gRows{'ABCD'[i+1]}:\n",1)[0]
    part=strip_debug_labels(part)
    assert part.startswith(" STA WSYNC\n"),suffix
    tail_loop=f" DEY\n BPL R1gRows{suffix}\n STA WSYNC\n JMP R1gAfterRows\n"
    assert part.count(tail_loop)==1,suffix
    main=part.split(tail_loop)[0]
    assert main.count(" LDA MaleRows14,Y\n")==1
    # first five TOP image rows read from short tables with Y=4..0.
    top=main
    for label in names:
        needle=f" {label}14,Y\n"
        assert top.count(needle)==1,(suffix,needle)
        top=top.replace(needle,f" R1oTop{label}5,Y\n")
    top+=f" DEY\n BPL R1gRows{suffix}\n LDY #8\n"

    shot=main
    # Original GRP1 large-female Y5 is $FF, its D1 enables M0 on shot row.
    # The R1k padding BIT was 3c; replacing by STA ENAM0 stays at 3c.
    needle=" STA RESP1\n BIT FRAMELO\n STA RESP1\n"
    assert shot.count(needle)==1,suffix
    shot=shot.replace(needle," STA RESP1\n STA ENAM0\n STA RESP1\n")
    # We must disable the duplicate before it begins 32 TIA CC after primary.
    if suffix=="C":
        needle=" LDA #$0E\n STA RESP0\n STA COLUP0\n"
        assert shot.count(needle)==1,(suffix,shot[-300:])
        shot=shot.replace(needle," STY ENAM0\n LDA #$0E\n STA RESP0\n STA COLUP0\n")
    else:
        assert shot.count(" LDA #$0E\n STA COLUP0\n")==1,(suffix,shot[-300:])
        shot=shot.replace(" LDA #$0E\n STA COLUP0\n"," STY ENAM0\n LDA #$0E\n STA COLUP0\n")
    # R1n14 white small-male and small-female pixels are identical on Y8:
    # TXA exactly matches original LDA SmallMaleRows14,Y, saving two cycles.
    assert shot.count(" LDA SmallMaleRows14,Y\n STA GRP1\n")==1
    shot=shot.replace(" LDA SmallMaleRows14,Y\n STA GRP1\n"," STX.w GRP1\n")
    # Some kernels use alternative color order; with those variants the
    # insertion will need equivalent repositioning before the white copy.
    shot+=f" DEY\n JMP R1oLower{suffix}\n"

    bottom=main+f" DEY\n BPL R1oLower{suffix}\n STA WSYNC\n JMP R1gAfterRows\n"
    new_parts.append(f"R1gRows{suffix}:\n"+top+f"R1oShot{suffix}:\n"+shot+
                     f"R1oLower{suffix}:\n"+bottom)

src=head+"".join(new_parts)+"R1gAfterRows:\n"+tail
append="\n; R1o temporary top-five display lookup tables, original tables remain intact.\n"
for label in names:
    five=masks14[label][:5]
    append+="R1oTop"+label+"5:\n BYTE "+",".join("$"+f"{x:02X}" for x in five[::-1])+"\n"
assert src.count(" ORG $FFFA\n")==1
src=src.replace(" ORG $FFFA\n",append+" ORG $FFFA\n")
for label in names:
    assert parse_mask(label)==original[label]
    assert src.split(label+":\n",1)[1].split("\n",1)[0] == base.split(label+":\n",1)[1].split("\n",1)[0]
    assert src.split(label+"14:\n",1)[1].split("\n",1)[0] == base.split(label+"14:\n",1)[1].split("\n",1)[0]
for suff in "ABCD":
    assert src.count("R1oShot"+suff+":\n")==1
    assert src.count("R1oLower"+suff+":\n")==1

(ROOT/"r1o.asm").write_text(src)
subprocess.run(["dasm","r1o.asm","-f3","-or1o_4k.bin","-lr1o.lst","-sr1o.sym"],cwd=ROOT,check=True)
raw=(ROOT/"r1o_4k.bin").read_bytes()
assert len(raw)==4096,len(raw)
rom=raw*4
(ROOT/"r1o_F6.bin").write_bytes(rom)
sha=hashlib.sha256(rom).hexdigest()
(ROOT/"ROM_SHA256.txt").write_text(sha+"  r1o_F6.bin\n")
manifest={
 "status":"BUILT_UNVERIFIED_R1O",
 "base_R1n14_rom_SHA256":BASE_SHA,
 "rom_SHA256":sha,"size":len(rom),
 "standard_F6":True,"display_rows":14,
 "shot_gui_y":167,"shot_expected_gui_x":232,
 "enable":"STA ENAM0 with A=FemaleRows14,Y=$FF only on special shot row",
 "disable":"STY ENAM0 with Y=8 only on special shot row, before extra M0",
 "smallmale_reuse":"TXA loads $3C exact same as SmallMaleRows14,Y=8; saves 2 cycles",
 "five_original_NPC_masks_unchanged":True,
 "limitations":"Not free X, six NPC, dynamic shot, full R1, or independent Verification; timing must be proven on actual Stella pixels."
}
(ROOT/"build_manifest.json").write_text(json.dumps(manifest,indent=2)+"\n")
print(json.dumps(manifest,indent=2))
