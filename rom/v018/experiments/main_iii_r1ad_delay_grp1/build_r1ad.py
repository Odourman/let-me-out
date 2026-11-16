#!/usr/bin/env python3
"""R1ad research-only: eliminate four first-row stray white P1 pixels.

Measured R1ac images: 300/600 exact, 300/600 have exactly four white
ghost pixels on top (row0), LEFT of intentional male. All 600 original
P1 mask pixels are PRESENT, and the two P1 X coordinates vary separately.

Potential cause: GRP1 first male pattern written c7 activates the initial
P1 main copy before first RESP1 close reset. Instead, keep GRP1=0 until
AFTER first RESP1 at c30/c32, writing male bitmap at c33/c35. The P1
first close pixels start near CPU c37/c39 (from ACTUAL Stella x87/x99).
This leaves ~4 CPU cycles for GRP1=1 TIA-CC delay.

Cycle-neutral restructuring:
 original c0..25: LDA male; STA GRP1; LDX female; LDA player;
                 STA GRP0; LDA shot; STA ENAM0
 revised  c0..25: LDX female; LDA player; STA GRP0; LDA shot;
                 STA ENAM0; LDA male; BIT FRAMELO
 BOTH exactly 25 cycles.
 original after first RESP1: BIT FRAMELO (3), NOP ... second RESP1
 revised:                   STA GRP1 (3), NOP ... second RESP1
 Maintains four exact CPU reset pairs (30,42),(32,42),(30,44),(32,44).
 Only horizontal graphics enable phase is altered. No mask bytes change.
"""
from pathlib import Path
import hashlib,subprocess,json
ROOT=Path(__file__).resolve().parent
PARENT=ROOT.parent/"main_iii_r1ac_dual_p1_close"
subprocess.run(["/usr/bin/python3",str(PARENT/"build_r1ac.py")],check=True)
pin="af47683fccff5fa48546de9c81032502ccf2ea7a980de90ed1880812789a7f30"
assert hashlib.sha256((PARENT/"r1ac_F6.bin").read_bytes()).hexdigest()==pin, "Wrong R1ac baseline"
old=(PARENT/"r1ac.asm").read_text()
s=old
heads={"C":(30,42,1,3),"D":(32,42,2,2),"E":(30,44,1,4),"F":(32,44,2,3)}
for k,(a,b,n1,n2) in heads.items():
 label=f"R1acRowSync{k}:\n";end=f" BPL R1acRowSync{k}\n"
 assert s.count(label)==1 and s.count(end)==1
 pre,rest=s.split(label,1);body,tail=rest.split(end,1)
 old_start=""" STA WSYNC
 LDA MaleRows,Y
 STA GRP1
 LDX FemaleRows,Y
 LDA PlayerRows,Y
 STA GRP0
 LDA ShotEnable,Y
 STA ENAM0
"""
 new_start=""" STA WSYNC
 LDX FemaleRows,Y
 LDA PlayerRows,Y
 STA GRP0
 LDA ShotEnable,Y
 STA ENAM0
 ; First male GRP1 byte delayed until just after RESP1.
 LDA MaleRows,Y
 BIT FRAMELO
"""
 assert body.count(old_start)==1,("start",k)
 body=body.replace(old_start,new_start)
 first=" STA RESP1\n BIT FRAMELO\n"
 second=" STA RESP1\n STA GRP1\n"
 assert body.count(first)==1,("middle",k)
 body=body.replace(first,second,1)
 s=pre+label+body+end+tail
for nm in ("MaleRows","FemaleRows","PlayerRows"):
 lab=f"\n{nm}:\n"
 assert old.count(lab)==s.count(lab)==1
 assert old.split(lab,1)[1].split("\n",1)[0]==s.split(lab,1)[1].split("\n",1)[0]
timing={}
for k,(c1,c2,n1,n2) in heads.items():
 a=f"R1acRowSync{k}:\n";b=f" BPL R1acRowSync{k}\n"
 ins=s.split(a,1)[1].split(b,1)[0].splitlines()
 clk=0;resp=[];grp=[]
 for line in ins:
  line=line.strip()
  if not line or line.startswith(";"):continue
  if line in ("NOP","DEY"):cy=2
  elif line.startswith("BIT ") or line.startswith("STA ") or line.startswith("STX "):cy=3
  elif line.startswith("LDA ") and line.endswith(",Y"):cy=4
  elif line.startswith("LDX ") and line.endswith(",Y"):cy=4
  else:raise ValueError(("cycle_unknown",k,line))
  clk+=cy
  if line=="STA RESP1":resp.append(clk)
  if line=="STA GRP1":grp.append(clk)
 assert resp==[c1,c2] and grp==[c1+3] and clk==c2+5,(k,resp,grp,clk)
 timing[k]={"resp_end_cycles":resp,"first_grp1_male_end_cycle":grp[0],
  "second_grp1_female_end_cycle":c2+3}
(ROOT/"r1ad.asm").write_text(s)
subprocess.run(["dasm","r1ad.asm","-f3","-or1ad_4k.bin","-lr1ad.lst","-sr1ad.sym"],cwd=ROOT,check=True)
four=(ROOT/"r1ad_4k.bin").read_bytes()
assert len(four)==4096
rom=four*4
sha=hashlib.sha256(rom).hexdigest()
(ROOT/"r1ad_F6.bin").write_bytes(rom)
(ROOT/"ROM_SHA256.txt").write_text(sha+"  r1ad_F6.bin\n")
manifest={
 "status":"BUILT_UNVERIFIED_R1AD_FIRST_GRP1_DELAYED_AFTER_RESP1",
 "pinned_R1ac_rom_sha256":pin,"ROM_SHA256":sha,"bytes":16384,
 "architecture":"original two 9-row full P1 mask close retriggers + yellow P0 player + one M0; 4 independent positional pairs",
 "timetable":timing,
 "novelty":"defer FIRST male GRP1 c7 to c33/c35 using 6502 cycle-neutral reorder; second female GRP1 unchanged",
 "hypothesis":"remove exact 4 first-row ghost pixels on 300 R1ac frames; no P1 mask byte may be omitted",
 "expected_strict_result":"600 real Stella images, 262 lines, two full different male/female masks every original row, no ghost, one yellow shot",
 "limitations":"research-only; no six NPC, no full gameplay, no independent Verification, no changes to production"
}
(ROOT/"manifest.json").write_text(json.dumps(manifest,indent=2)+"\n")
print(json.dumps(manifest,indent=2))
