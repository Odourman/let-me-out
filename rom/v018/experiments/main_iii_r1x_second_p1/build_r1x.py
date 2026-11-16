#!/usr/bin/env python3
"""R1x isolated coarse position experiment: move the R1w M0 one more
three-cycle BIT FRAMELO later at VBLANK, into second large-female P1.
Preserves all five NPC original source masks and 14-row player/NPC
kernel byte-for-byte, including approved 600-frame R1w timing.
No claim of full game, moving shot logic, or collision identity.
"""
from pathlib import Path
import hashlib,subprocess,sys,json
ROOT=Path(__file__).resolve().parent
BASE=ROOT.parent/"main_iii_r1w_retimed_m0"
subprocess.run([sys.executable,str(BASE/"build_r1w.py")],check=True)
old_rom=(BASE/"r1w_F6.bin").read_bytes()
PIN="dac6340febe7a0a6e94e3e0231c97e8f79731a60a4eeba8903d95018d804141f"
assert hashlib.sha256(old_rom).hexdigest()==PIN,"R1w immutable reference changed"
old=(BASE/"r1w.asm").read_text()
needle=""" BIT FRAMELO
 STA RESM0
 STA WSYNC"""
new=""" BIT FRAMELO
 ; R1x second COARSE shift: additional 3 CPU cycles = +9 CC.
 ; Testing if the existing four shot-row kernels keep M0 enabled.
 BIT FRAMELO
 STA RESM0
 STA WSYNC"""
assert old.count(needle)==1
src=old.replace(needle,new)
for label in ("MaleRows","FemaleRows","SmallMaleRows","SmallFemaleRows","PlayerRows"):
 for suffix in ("","14"):
  key="\n"+label+suffix+":\n"
  assert old.count(key)==src.count(key)==1,key
  assert old.split(key,1)[1].split("\n",1)[0]==src.split(key,1)[1].split("\n",1)[0],key
for suffix in "ABCD":
 key=f"R1oShot{suffix}:\n"
 end=f"R1oLower{suffix}:\n"
 assert old.split(key,1)[1].split(end,1)[0]==src.split(key,1)[1].split(end,1)[0],suffix
(ROOT/"r1x.asm").write_text(src)
subprocess.run(["dasm","r1x.asm","-f3","-or1x_4k.bin","-lr1x.lst","-sr1x.sym"],check=True,cwd=ROOT)
four=(ROOT/"r1x_4k.bin").read_bytes()
assert len(four)==4096,len(four)
rom=four*4
sha=hashlib.sha256(rom).hexdigest()
(ROOT/"r1x_F6.bin").write_bytes(rom)
(ROOT/"ROM_SHA256.txt").write_text(sha+"  r1x_F6.bin\n")
manifest={
 "research_status":"BUILT_UNVERIFIED_R1X",
 "baseline_R1w_sha256":PIN,
 "rom_sha256":sha,"mapper":"F6","region":"NTSC","bytes":16384,
 "expected_M0_gui_x":[268,270,272,274,276,278,280,282],
 "expected_second_large_female_P1_gui_x":280,
 "actual_collision_latch":"CXM0P D7; instrumented background only",
 "source_masks_preserved":True,
 "kernel_behavior":"identical four R1w 14-row shot routines, only VBLANK RESM0 coarse timing changes",
 "acceptance":"600 genuine Stella frames; 8 shot X ×4 NPC X×2 door; full original masks; zero extra missile; real contact only at actual female overlap",
 "limits":"research-only, static frames cycling X. No six NPC, no full-screen projectile, no actual bullet state/collision target-ID."
}
(ROOT/"manifest.json").write_text(json.dumps(manifest,indent=2)+"\n")
print(json.dumps(manifest,indent=2))
