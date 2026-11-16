#!/usr/bin/env python3
"""R1ab: Berzerk one-copy on D shot ONLY; restore 2-copy exactly at line edge.

Pinned to R1aa 600-frame FAIL source.
 At end of special shot row:
    DEY           at ~c68
    STY ENAM0     at ~c71
    LDA #$02      at ~c73
    STA NUSIZ0    at ~c76 (horizontal next scanline boundary)
 First lower D row is unrolled to OMIT STA WSYNC: it starts right at c76.
 Its remaining identical instructions render Y=7; thereafter BPL-like
 3-cycle JMP to original R1oLowerD with WSYNC for Y=6..0.
 Mask source bytes, P1/P0 reset phases of all other rows unchanged.
 These are timing hypotheses, not claims; 600 actual Stella images decide.
"""
from pathlib import Path
import subprocess,sys,hashlib,json
ROOT=Path(__file__).resolve().parent
BASE=ROOT.parent/"main_iii_r1aa_onecopy_d"
subprocess.run([sys.executable,str(BASE/"build_r1aa.py")],check=True)
PIN="9a1a464252c3f0da3d6aecc85fc21514e1cb43c3c35f258548e4919837c84778"
assert hashlib.sha256((BASE/"r1aa_F6.bin").read_bytes()).hexdigest()==PIN,"R1aa baseline moved"
original=(BASE/"r1aa.asm").read_text()
start="R1oShotD:\n"; lower_tag="R1oLowerD:\n"; after_tag="R1gAfterRows:\n"
assert original.count(start)==original.count(lower_tag)==original.count(after_tag)==1
head,rest=original.split(start,1)
shot,tail=rest.split(lower_tag,1)
lower,after=tail.split(after_tag,1)
assert shot.count(" STY ENAM0\n")==1
assert shot.rstrip().endswith("STY ENAM0")
shot+=" LDA #$02\n STA NUSIZ0\n"
assert lower.startswith(" STA WSYNC\n")
assert lower.count("\n DEY\n BPL R1oLowerD\n")==1
first=lower[ len(" STA WSYNC\n"):].split("\n DEY\n BPL R1oLowerD\n",1)[0]
assert first.startswith(" LDA MaleRows14,Y")
first+="\n DEY\n JMP R1oLowerD\n"
out=head+start+shot+"R1abFirstLowerD:\n"+first+lower_tag+lower+after_tag+after
for nm in ("MaleRows","FemaleRows","SmallMaleRows","SmallFemaleRows","PlayerRows"):
 for suff in ("","14"):
  key="\n"+nm+suff+":\n"
  assert original.count(key)==out.count(key)==1
  assert original.split(key,1)[1].split("\n",1)[0]==out.split(key,1)[1].split("\n",1)[0]
for s in "ABC":
 a=f"R1oShot{s}:\n";b=f"R1oLower{s}:\n"
 assert original.split(a,1)[1].split(b,1)[0]==out.split(a,1)[1].split(b,1)[0]
(ROOT/"r1ab.asm").write_text(out)
subprocess.run(["dasm","r1ab.asm","-f3","-or1ab_4k.bin","-lr1ab.lst","-sr1ab.sym"],cwd=ROOT,check=True)
raw=(ROOT/"r1ab_4k.bin").read_bytes()
assert len(raw)==4096
rom=raw*4
sha=hashlib.sha256(rom).hexdigest()
(ROOT/"r1ab_F6.bin").write_bytes(rom)
(ROOT/"ROM_SHA256.txt").write_text(sha+"  r1ab_F6.bin\n")
meta=dict(status="BUILT_UNVERIFIED_R1AB_NUSIZ_RESTORE_AT_LINE_EDGE",baseline_R1aa_sha256=PIN,ROM_sha256=sha,ROM_bytes=len(rom),
 sequence="D NUSIZ0 ONE_COPY c53; M0 off c71; LDA #2 c73; STA NUSIZ0 c76; unrolled next row omits STA WSYNC",
 candidate_source="30 tricks #14 #15 #24 and Berzerk one-copy gameplay, NOT Berzerk copied instructions",
 verification_goals="600 authentic Stella frames: five complete original 14-row NPC, four P0 X, 8 M0 X=286..300, 2 doors, zero ghost, exact CXM0P D7",
 current_known_risk="Changing NUSIZ0 at c53 may itself remove P0 small-female copy on shot row, even if immediately restored on next row",
 no_implementation_or_verification_authority=True)
(ROOT/"manifest.json").write_text(json.dumps(meta,indent=2)+"\n")
print(json.dumps(meta,indent=2))
