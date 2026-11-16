#!/usr/bin/env python3
"""R1aa: Berzerk-inspired NUSIZ0 ONE_COPY ONLY after D's small female sprite reset.

From pinned failed R1y: D at c53 STY NUSIZ0 (Y=8: bit2/1/0=0, one copy)
rather than STY ENAM0 (which prematurely kills M0 x288..300).
Then D-end after STA RESP1, DEY:
 STY ENAM0 (same 3 cycles as replaced JMP R1oLowerD),
 fall-through to R1oLowerD/STA WSYNC.
M0 is off BEFORE following line, but NUSIZ0 remains single-copy on
D's lower 8 scanlines. Strict original-mask test determines whether
this is viable; it may remove player/robot copies. Fail honestly.
"""
from pathlib import Path
import subprocess,sys,hashlib,json
ROOT=Path(__file__).resolve().parent
BASE=ROOT.parent/"main_iii_r1y_second_exit"
subprocess.run([sys.executable,str(BASE/"build_r1y.py")],check=True)
parent=(BASE/"r1y_F6.bin").read_bytes()
PIN="aaf9ecf5b6698e1df75e9c0f70c114a913711d1edf99b4ef48ef8f7ad40e02b0"
assert hashlib.sha256(parent).hexdigest()==PIN
old=(BASE/"r1y.asm").read_text()
start="R1oShotD:\n";end="R1oLowerD:\n"
pre,rest=old.split(start,1)
shot,post=rest.split(end,1)
needle=""" LDA #$0E
 STX GRP0
 STY ENAM0
 STA RESP0
 STA COLUP0"""
replace=""" LDA #$0E
 STX GRP0
 ; Berzerk-derived hypothesis: D set ONE_COPY at c53 instead of M0 off.
 STY NUSIZ0
 STA RESP0
 STA COLUP0"""
assert shot.count(needle)==1
shot=shot.replace(needle,replace)
before=" DEY\n JMP R1oLowerD\n"
after=""" ; one-copy prevents M0 NUSIZ0 clones while missile is on.
 DEY
 ; Shut M0 off on time without adding cycles: replaces 3cy JMP,
 ; next label is R1oLowerD and must immediately fall through.
 STY ENAM0
"""
assert shot.count(before)==1
shot=shot.replace(before,after)
src=pre+start+shot+end+post
for nm in ("MaleRows","FemaleRows","SmallMaleRows","SmallFemaleRows","PlayerRows"):
 for suf in ("","14"):
  label="\n"+nm+suf+":\n"
  assert old.split(label,1)[1].split("\n",1)[0]==src.split(label,1)[1].split("\n",1)[0]
for s in "ABC":
 a=f"R1oShot{s}:\n";b=f"R1oLower{s}:\n"
 assert old.split(a,1)[1].split(b,1)[0]==src.split(a,1)[1].split(b,1)[0]
(ROOT/"r1aa.asm").write_text(src)
subprocess.run(["dasm","r1aa.asm","-f3","-or1aa_4k.bin","-lr1aa.lst","-sr1aa.sym"],cwd=ROOT,check=True)
raw=(ROOT/"r1aa_4k.bin").read_bytes()
assert len(raw)==4096
rom=raw*4;sha=hashlib.sha256(rom).hexdigest()
(ROOT/"r1aa_F6.bin").write_bytes(rom)
(ROOT/"ROM_SHA256.txt").write_text(sha+"  r1aa_F6.bin\n")
info=dict(status="BUILT_UNVERIFIED_R1AA_ONECOPY_BERZERK_HYPOTHESIS",pinned_r1y_sha256=PIN,rom_sha256=sha,rom_size=16384,
 change="D special shot: STY NUSIZ0 at c53 (Y=8 ONE_COPY), unchanged STA RESP0 c56, COLUP0 c59; STY ENAM0 at prior JMP slot c71; lower scanlines inherit NUSIZ0=ONE_COPY",
 tested_x=[286,288,290,292,294,296,298,300],tested_NPC_fourth_X=[330,348,360,378],
 required="600 real Stella pixelaudit, five complete original mask instances all 14 rows, single yellow shot y167, zero white/ghost copies, 262 NTSC",
 risk="losing automatic P0 player copy on 8 lower rows because NUSIZ0 is not restored until next VBLANK; must NOT call this solution unless 600 strict PASS",
 limits="research-only no approved game logic, no full-screen shot, no independent Verification")
(ROOT/"manifest.json").write_text(json.dumps(info,indent=2)+"\n")
print(json.dumps(info,indent=2))
