#!/usr/bin/env python3
"""Isolated MAIN IV R1af research: widen P1 RESET cycle-pair sample."""
from pathlib import Path
import os,subprocess,hashlib,json,sys
ROOT=Path(__file__).resolve().parent
PARENT=ROOT.parent/"main_iii_r1ae_later_grp1"
subprocess.run([sys.executable,str(PARENT/"build_r1ae.py")],check=True)
PIN="05606a5fd7426df00941be5621ca46c113df794c4ac3fa0f00f0e15cca66a993"
assert hashlib.sha256((PARENT/"r1ae_F6.bin").read_bytes()).hexdigest()==PIN
old=(PARENT/"r1ae.asm").read_text()
batch=int(os.environ.get("R1AF_BATCH","0"))
assert batch in range(8),batch
pairs=[((28,30),(40,42)),((32,34),(44,46)),
       ((36,38),(48,50)),((40,42),(52,54)),
       ((28,30),(52,54)),((32,34),(48,50)),
       ((36,38),(52,54)),((28,30),(46,48))]
first,second=pairs[batch]
modes={"C":(first[0],second[0]),"D":(first[1],second[0]),
       "E":(first[0],second[1]),"F":(first[1],second[1])}
src=old
schedule={}
for mode,(c1,c2) in modes.items():
    assert c1>=28 and c1%2==0 and c2>=c1+8 and (c2-c1)%2==0
    n1=(c1-28)//2
    n_between=(c2-c1-8)//2
    label=f"R1acRowSync{mode}:\n"
    end=f" BPL R1acRowSync{mode}\n"
    assert src.count(label)==src.count(end)==1
    head,rest=src.split(label,1)
    body,tail=rest.split(end,1)
    assert body.startswith(" STA WSYNC\n") and body.count("STA RESP1")==2
    lines=[" STA WSYNC"," LDX FemaleRows,Y"," LDA PlayerRows,Y",
           " STA GRP0"," LDA ShotEnable,Y"," STA ENAM0",
           " LDA MaleRows,Y"," BIT FRAMELO"]
    lines+=[" NOP"]*n1
    lines+=[" STA RESP1"," NOP"," STA GRP1"]
    lines+=[" NOP"]*n_between
    lines+=[" STA RESP1"," STX GRP1"," DEY"]
    src=head+label+"\n".join(lines)+"\n"+end+tail
    schedule[mode]={"first_RESP1_end_cycle":c1,
      "male_GRP1_end_cycle":c1+5,"second_RESP1_end_cycle":c2,
      "female_GRP1_end_cycle":c2+3,"DEY_end_cycle":c2+5,
      "nops_before_first_RESP1":n1,"nops_between_GRPs":n_between}
for name in ("MaleRows","FemaleRows","PlayerRows","ShotEnable"):
    marker="\n"+name+":\n"
    assert old.count(marker)==src.count(marker)==1
    assert old.split(marker,1)[1].split("\n",1)[0]==src.split(marker,1)[1].split("\n",1)[0]
(ROOT/"r1af.asm").write_text(src)
subprocess.run(["dasm","r1af.asm","-f3","-or1af_4k.bin","-lr1af.lst","-sr1af.sym"],cwd=ROOT,check=True)
four=(ROOT/"r1af_4k.bin").read_bytes()
assert len(four)==4096
rom=four*4
sha=hashlib.sha256(rom).hexdigest()
(ROOT/"r1af_F6.bin").write_bytes(rom)
(ROOT/"ROM_SHA256.txt").write_text(sha+"  r1af_F6.bin\n")
manifest={"status":"BUILT_UNVERIFIED_RESEARCH_R1AF","batch":batch,
 "cycle_pairs":schedule,"pinned_R1ae_ROM_SHA256":PIN,"ROM_SHA256":sha,
 "bytes":16384,"mapper":"F6 four identical banks","video":"NTSC",
 "source_masks":"MaleRows, FemaleRows, PlayerRows, ShotEnable unchanged",
 "goal":"Four pairs x 600 authentic Stella GUI frames; exact 9-row original masks, zero ghosts, full yellow P0, one M0, 262 scanlines",
 "limit":"Research ONLY: not six independent NPC, not R1 PASS, not independent VERIFICATION"}
(ROOT/"manifest.json").write_text(json.dumps(manifest,indent=2)+"\n")
print(json.dumps(manifest,indent=2))
