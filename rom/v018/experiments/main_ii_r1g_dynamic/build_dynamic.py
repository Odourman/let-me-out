#!/usr/bin/env python3
"""R1g: four proven static per-row kernels assembled into ONE dynamically cycling ROM.

No new operations are inserted WITHIN any of the four 76-cycle-critical
raster loops. FRAMELO bits 4-5 select 1 of four loops before the row band.
The design must survive actual 600 consecutive Stella frames with four masks,
player and missile. Dynamic four X has NOT been claimed prior to that test.
"""
from pathlib import Path
import hashlib,json,re,subprocess,sys
ROOT=Path(__file__).resolve().parent
PARENT=ROOT.parent/"main_ii_r1g_four_positions"
subprocess.run([sys.executable,str(PARENT/"build.py")],check=True)
NAMES=["pre_mask","post_mask","post_lda","post_color"]
sources=[(PARENT/name/"probe.asm").read_text() for name in NAMES]
start=" LDY #8\nR1cRow:\n"
end=" DEY\n BPL R1cRow\n STA WSYNC\n LDA #0\n STA GRP0"
sections=[]
for name,src in zip(NAMES,sources):
    assert src.count(start)==1 and src.count(end)==1
    head,rest=src.split(start)
    body,tail=rest.split(end)
    sections.append((head,body,tail))
assert all(head==sections[0][0] and tail==sections[0][2] for head,body,tail in sections), "unexpected control differences beyond row"
head=sections[0][0]
tail=sections[0][2]
# Four branch targets can be >127 bytes from selector: jump stubs avoid BEQ range.
selector=""" LDY #8
 ; Select independent fourth-NPC X once per frame, OUTSIDE visible row loops.
 LDA FRAMELO
 AND #$30
 BEQ R1gChooseA
 CMP #$10
 BEQ R1gChooseB
 CMP #$20
 BEQ R1gChooseC
 JMP R1gRowsD
R1gChooseA:
 JMP R1gRowsA
R1gChooseB:
 JMP R1gRowsB
R1gChooseC:
 JMP R1gRowsC
"""
def specialized(body,suffix):
    labels=set(re.findall(r"^([A-Za-z][A-Za-z0-9_]*):\s*$",body,re.M))
    for label in sorted(labels,key=len,reverse=True):
        body=re.sub(r"\b"+re.escape(label)+r"\b",label+suffix,body)
    root="R1gRows"+suffix
    return root+":\n"+body+"\n DEY\n BPL "+root+"\n STA WSYNC\n JMP R1gAfterRows\n"
combined=head+selector+"".join(specialized(body,chr(65+i)) for i,(head,body,tail) in enumerate(sections))+"R1gAfterRows:\n LDA #0\n STA GRP0"+tail
# Leave room for four specialized loops beyond $F200; relocate read-only tables.
assert combined.count(" ORG $F200")==1
combined=combined.replace(" ORG $F200"," ORG $F400")
for suffix in "ABCD":
    assert combined.count("R1fYellowRESP0"+suffix+":")==1
    assert combined.count("R1fWhiteRESP0"+suffix+":")==1
assert combined.count("R1gAfterRows:")==1
(ROOT/"r1g_four_dynamic.asm").write_text(combined)
subprocess.run(["dasm","r1g_four_dynamic.asm","-f3","-or1g_4k.bin",
                "-lr1g.lst","-sr1g.sym"],cwd=ROOT,check=True)
raw=(ROOT/"r1g_4k.bin").read_bytes()
assert len(raw)==4096
rom=raw*4
(ROOT/"r1g_F6.bin").write_bytes(rom)
sha=hashlib.sha256(rom).hexdigest()
(ROOT/"ROM_SHA256.txt").write_text(sha+"  r1g_F6.bin\n")
summary={"standard_F6_bytes":len(rom),"sha256":sha,
 "four_cycle_equal_specialized_row_kernels":NAMES,
 "dynamic_selection":"FRAMELO & $30, four 16-frame modes",
 "next_gate":"600 consecutive authentic Stella frames must be PASS"}
(ROOT/"build_manifest.json").write_text(json.dumps(summary,indent=2)+"\n")
print(json.dumps(summary,indent=2))
