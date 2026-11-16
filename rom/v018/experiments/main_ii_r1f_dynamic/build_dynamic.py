#!/usr/bin/env python3
"""Reproduce the successful R1f pair, then interleave two PRECOMPILED row kernels.

Selects early/late second RESP0 once per frame via FRAMELO bit4.
Every raster row uses one unbranched cycle-critical 6502 kernel. The selection
branch is BEFORE the first NPC scanline, never inside the bitmap deadlines.
No ROM self-modification, and no additional per-row cycles or mapper change.

One extra STA WSYNC at each specialized loop's END is the original bottom
separator, moved into the branch bodies; a JMP executes AFTER that WSYNC,
in otherwise unused first bottom-line time. 262 NTSC still requires Stella.
"""
from pathlib import Path
import hashlib,json,re,subprocess,sys
ROOT=Path(__file__).resolve().parent
PARENT=ROOT.parent/"main_ii_r1f_resp0"
subprocess.run([sys.executable,str(PARENT/"build.py")],check=True)
early=(PARENT/"early_white"/"probe.asm").read_text()
late=(PARENT/"late_white"/"probe.asm").read_text()
start=" LDY #8\nR1cRow:\n"
end=" DEY\n BPL R1cRow\n STA WSYNC\n LDA #0\n STA GRP0"
assert early.count(start)==late.count(start)==1
assert early.count(end)==late.count(end)==1
e_head,e_mid=early.split(start)
l_head,l_mid=late.split(start)
assert e_head==l_head, "R1f controls differ in setup"
ebody,e_tail=e_mid.split(end)
lbody,l_tail=l_mid.split(end)
assert e_tail==l_tail, "R1f controls differ after row kernel"
def specialized(body,suffix):
    labels=set(re.findall(r"^([A-Za-z][A-Za-z0-9_]*):\s*$",body,re.M))
    for label in sorted(labels,key=len,reverse=True):
        body=re.sub(r"\b"+re.escape(label)+r"\b",label+suffix,body)
    label="R1fEarlyRows" if suffix=="E" else "R1fLateRows"
    return (
        label+":\n"+body+
        "\n DEY\n BPL "+label+
        "\n STA WSYNC\n JMP R1fAfterRows\n")
selector=""" LDY #8
 ; Two independent P0 positions selected once PER FRAME during non-critical time.
 LDA FRAMELO
 AND #$10
 BEQ R1fEarlyRows
 JMP R1fLateRows
"""
combined=(e_head+selector+
          specialized(ebody,"E")+specialized(lbody,"L")+
          "R1fAfterRows:\n LDA #0\n STA GRP0"+e_tail)
assert combined.count("R1fYellowRESP0E:")==1
assert combined.count("R1fYellowRESP0L:")==1
assert combined.count("R1fWhiteRESP0E:")==1
assert combined.count("R1fWhiteRESP0L:")==1
assert combined.count("R1fAfterRows:")==1
(ROOT/"r1f_dynamic.asm").write_text(combined)
subprocess.run(["dasm","r1f_dynamic.asm","-f3",
                "-or1f_4k.bin","-lr1f.lst","-sr1f.sym"],cwd=ROOT,check=True)
raw=(ROOT/"r1f_4k.bin").read_bytes()
assert len(raw)==4096
full=raw*4
(ROOT/"r1f_F6.bin").write_bytes(full)
sha=hashlib.sha256(full).hexdigest()
(ROOT/"ROM_SHA256.txt").write_text(sha+"  r1f_F6.bin\n")
result={
 "description":"frame-switched precompiled early/late second RESP0, no branch within scanline",
 "NTSC_F6_bytes":len(full),"sha256":sha,
 "sources":[str(PARENT/"early_white"/"probe.asm"),
            str(PARENT/"late_white"/"probe.asm")],
 "frame_toggle":"FRAMELO & $10",
 "unverified":"600 actual Stella consecutive frames still required"
}
(ROOT/"build_manifest.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result,indent=2))
