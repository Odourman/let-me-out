#!/usr/bin/env python3
"""R1u: broader 8 consecutive GUI X samples x232..246 for one M0.
This is a strict hardware WINDOW LIMIT probe with unchanged R1s NPC source.
No assertion that a shot across the full playfield is solved.
"""
from pathlib import Path
import subprocess,sys,hashlib,json,re
ROOT=Path(__file__).resolve().parent
PARENT=ROOT.parent/"main_iii_r1t_four_m0_x"
subprocess.run([sys.executable,str(PARENT/"build_r1t.py")],check=True)
prior=(PARENT/"r1t_F6.bin").read_bytes()
EXPECTED="db14c067d386c0f4040a6208f8d97b29f5dbe2568c36d5421da8d0491e25743e"
assert hashlib.sha256(prior).hexdigest()==EXPECTED,"R1t research baseline drift"
old=(PARENT/"r1t.asm").read_text()
s=old
a=""" LDA FRAMELO
 AND #$0C
 LSR
 LSR
 TAX
 LDA R1tM0Motion,X"""
b=""" LDA FRAMELO
 AND #$07
 TAX
 LDA R1tM0Motion,X"""
assert s.count(a)==1
s=s.replace(a,b)
table="""R1tM0Motion:
 BYTE $40,$30,$20,$10"""
extended="""R1tM0Motion:
 BYTE $40,$30,$20,$10,$00,$F0,$E0,$D0"""
assert s.count(table)==1
s=s.replace(table,extended)
for name in ("MaleRows","FemaleRows","SmallMaleRows","SmallFemaleRows","PlayerRows"):
 for suf in ("","14"):
  label="\n"+name+suf+":\n"
  assert old.count(label)==s.count(label)==1
  assert old.split(label,1)[1].split("\n",1)[0]==s.split(label,1)[1].split("\n",1)[0]
for suffix in "ABCD":
 for label in (f"R1oShot{suffix}:\n",f"R1oLower{suffix}:\n"):
  assert old.split(label,1)[1].split("\n",1)[0]==s.split(label,1)[1].split("\n",1)[0]
(ROOT/"r1u.asm").write_text(s)
subprocess.run(["dasm","r1u.asm","-f3","-or1u_4k.bin","-lr1u.lst","-sr1u.sym"],cwd=ROOT,check=True)
raw=(ROOT/"r1u_4k.bin").read_bytes()
assert len(raw)==4096
rom=raw*4
sha=hashlib.sha256(rom).hexdigest()
(ROOT/"r1u_F6.bin").write_bytes(rom)
(ROOT/"ROM_SHA256.txt").write_text(sha+"  r1u_F6.bin\n")
manifest={
 "status":"BUILT_UNVERIFIED_R1U_WINDOW_PROBE",
 "baseline_R1t_SHA256":EXPECTED,
 "ROM_SHA256":sha,
 "ROM_bytes":16384,"mapper":"standard F6","video":"NTSC",
 "expected_one_m0_at_gui_y167_with_x":[232,234,236,238,240,242,244,246],
 "motion_bytes":["$40","$30","$20","$10","$00","$F0","$E0","$D0"],
 "frame_bits":"FRAMELO & $07, different every frame; P0 X=FRAMELO&$30; door=FRAMELO&$40",
 "target_combinations":8*4*2,
 "limits":"Research-only fine movement 14 GUI pixels before the first female at x248. No screen-wide shot, collision, six NPC, or verification."
}
(ROOT/"build_manifest.json").write_text(json.dumps(manifest,indent=2)+"\n")
print(json.dumps(manifest,indent=2))
