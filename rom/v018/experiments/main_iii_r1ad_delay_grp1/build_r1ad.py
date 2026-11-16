#!/usr/bin/env python3
"""R1ad research-only cycle-neutral TIA P1 first-row ghost correction.
R1ac 600-image audit proved 300 exact 9-row two-mask frames, but 300
with 4 extra white pixels on row0 to the LEFT of the first mask. Their
locations are the initial base P1 MAIN copy of MaleRows[8]=$42.
Delay first male GRP1 load from CPU c7 to c1+7 after first RESP1:
 for c1=30 => c37 (intended close starts ~c39)
 for c1=32 => c39 (intended close starts ~c41)
Replace early 7-cycle load+store with 3+2+2 neutral BIT,NOP,NOP;
replace between-RESP BIT+NOPs with new male load+STA and remainder NOPs.
All RESP1 endcycle pairs and Y rows remain exactly unchanged.
"""
from pathlib import Path
import hashlib,subprocess,json,re,sys
ROOT=Path(__file__).resolve().parent
PARENT=ROOT.parent/"main_iii_r1ac_dual_p1_close"
subprocess.run([sys.executable,str(PARENT/"build_r1ac.py")],check=True)
pin="af47683fccff5fa48546de9c81032502ccf2ea7a980de90ed1880812789a7f30"
assert hashlib.sha256((PARENT/"r1ac_F6.bin").read_bytes()).hexdigest()==pin
old=(PARENT/"r1ac.asm").read_text()
s=old
counts={"C":(30,42,3),"D":(32,42,2),"E":(30,44,4),"F":(32,44,3)}
for mode,(c1,c2,n) in counts.items():
 a=f"R1acRowSync{mode}:\n";b=f" BPL R1acRowSync{mode}\n"
 assert s.count(a)==s.count(b)==1
 head,rest=s.split(a,1);part,tail=rest.split(b,1)
 early=""" STA WSYNC
 LDA MaleRows,Y
 STA GRP1
 LDX FemaleRows,Y"""
 late=""" STA WSYNC
 ; Delay male GRP1 until AFTER first RESP1, prevent early main P1 ghost.
 BIT FRAMELO
 NOP
 NOP
 LDX FemaleRows,Y"""
 assert part.count(early)==1,(mode,"early")
 part=part.replace(early,late,1)
 before=" STA RESP1\n BIT FRAMELO\n"+" NOP\n"*n+" STA RESP1\n"
 m=(3+2*n-7)//2
 assert 3+2*n==7+2*m and m>=0
 after=" STA RESP1\n LDA MaleRows,Y\n STA GRP1\n"+" NOP\n"*m+" STA RESP1\n"
 assert part.count(before)==1,(mode,"mid",repr(part))
 part=part.replace(before,after,1)
 s=head+a+part+b+tail
for name in ("MaleRows","FemaleRows","PlayerRows"):
 label=f"\n{name}:\n"
 assert old.count(label)==s.count(label)==1
 assert old.split(label,1)[1].split("\n",1)[0]==s.split(label,1)[1].split("\n",1)[0]
for mode,(c1,c2,n) in counts.items():
 # independent static schedule audit in the actual source text
 a=f"R1acRowSync{mode}:\n";b=f" BPL R1acRowSync{mode}\n"
 p=s.split(a,1)[1].split(b,1)[0].splitlines()
 cycles=0;writes=[];load_end=None
 for line in p:
  ins=line.strip().split(" ;")[0].strip()
  if not ins or ins.startswith(";"):continue
  if ins.startswith("LDA ") and ",Y" in ins: ncy=4
  elif ins.startswith("LDX ") and ",Y" in ins:ncy=4
  elif ins.startswith("BIT "):ncy=3
  elif ins.startswith("STA "):ncy=3
  elif ins=="NOP":ncy=2
  elif ins=="DEY":ncy=2
  else:raise ValueError(("uncosted",mode,ins))
  cycles+=ncy
  if ins=="STA RESP1":writes.append(cycles)
  if ins=="STA GRP1":load_end=cycles
 assert writes==[c1,c2],(mode,writes,c1,c2)
 assert load_end==c1+7,(mode,load_end,c1)
 assert cycles==c2+5,(mode,cycles,c2)
(ROOT/"r1ad.asm").write_text(s)
subprocess.run(["dasm","r1ad.asm","-f3","-or1ad_4k.bin","-lr1ad.lst","-sr1ad.sym"],cwd=ROOT,check=True)
b=(ROOT/"r1ad_4k.bin").read_bytes()
assert len(b)==4096
rom=b*4;sha=hashlib.sha256(rom).hexdigest()
(ROOT/"r1ad_F6.bin").write_bytes(rom)
(ROOT/"ROM_SHA256.txt").write_text(sha+"  r1ad_F6.bin\n")
info={
 "status":"BUILT_UNVERIFIED_R1AD_DELAYED_GRP1_P1_GHOST_REMOVAL_TEST",
 "pinned_R1ac_ROM_sha256":pin,"ROM_sha256":sha,"bytes":16384,
 "independent_P1_X_modes":{k:{"first_resp1_cpu_end":a,"second_resp1_cpu_end":b,"first_male_grp1_cpu_end":a+7} for k,(a,b,_) in counts.items()},
 "specific_hypothesis":"Suppress 4 ghost WHITE pixels at first scanline left of male by not enabling P1 GRP1 bitmap until after first RESP1; no cycle count change.",
 "original_bitmaps":"male/female/player all 9 source bytes exactly unchanged",
 "needs":"600 genuine Stella frames 262 NTSC all source masks exact every 9 rows, independent two-X, full player, one M0, ZERO extra white",
 "limits":"research only; not six NPC; not independent Verification; no production changes"
}
(ROOT/"manifest.json").write_text(json.dumps(info,indent=2)+"\n")
print(json.dumps(info,indent=2))
