#!/usr/bin/env python3
"""MAIN IV R1ag RESEARCH: independent P1 mask order reversal / close copy tests.
No production, no six-NPC, no R1 or independent Verification approval.
"""
from pathlib import Path
import hashlib,subprocess,os,sys,json
ROOT=Path(__file__).resolve().parent
PARENT=ROOT.parent/"main_iv_r1af_xmatrix"
env=dict(os.environ,R1AF_BATCH="0")
subprocess.run([sys.executable,str(PARENT/"build_r1af.py")],env=env,check=True)
PIN="bac51f2686459a506debcf410a530ef4c68c23417e0bf7a4f64452ade6e1e11d"
assert hashlib.sha256((PARENT/"r1af_F6.bin").read_bytes()).hexdigest()==PIN, "Wrong pinned R1af batch-0 ROM"
old=(PARENT/"r1af.asm").read_text()
batch=int(os.environ.get("R1AG_BATCH","0"))
assert batch in range(6)
# c2 >= c1+8 is required by current two-RESP timing.
# Control pair, four close / near-pairs, and distant reverse-order.
jobs=[
 ("F->M",(28,30),(40,42),"reverse_medium_control"),
 ("F->M",(28,30),(38,40),"reverse_close_8cpu_pair"),
 ("M->F",(28,30),(38,40),"normal_close_8cpu_pair"),
 ("F->M",(36,38),(46,48),"reverse_late_close_8cpu_pair"),
 ("M->F",(36,38),(46,48),"normal_late_close_8cpu_pair"),
 ("F->M",(28,30),(52,54),"reverse_wide_pair"),
]
order,first,second,tag=jobs[batch]
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
    assert src.count(label)==1 and src.count(end)==1
    head,rest=src.split(label,1)
    body,tail=rest.split(end,1)
    assert body.startswith(" STA WSYNC\n") and body.count("STA RESP1")==2
    first_source="FemaleRows" if order=="F->M" else "MaleRows"
    second_source="MaleRows" if order=="F->M" else "FemaleRows"
    lines=[" STA WSYNC",f" LDX {second_source},Y"," LDA PlayerRows,Y",
           " STA GRP0"," LDA ShotEnable,Y"," STA ENAM0",
           f" LDA {first_source},Y"," BIT FRAMELO"]
    lines+=[" NOP"]*n1
    lines+=[" STA RESP1"," NOP"," STA GRP1"]
    lines+=[" NOP"]*n_between
    lines+=[" STA RESP1"," STX GRP1"," DEY"]
    src=head+label+"\n".join(lines)+"\n"+end+tail
    schedule[mode]={"first_RESP1_end_cycle":c1,
      "first_mask_GRP1_end_cycle":c1+5,"second_RESP1_end_cycle":c2,
      "second_mask_GRP1_end_cycle":c2+3,"last_DEY_end_cycle":c2+5,
      "separation_in_6507_cycles":c2-c1,
      "separation_in_TIA_color_clocks":3*(c2-c1)}
for name in ("MaleRows","FemaleRows","PlayerRows","ShotEnable"):
    marker="\n"+name+":\n"
    assert src.count(marker)==old.count(marker)==1
    assert old.split(marker,1)[1].split("\n",1)[0]==src.split(marker,1)[1].split("\n",1)[0]
(ROOT/"r1ag.asm").write_text(src)
subprocess.run(["dasm","r1ag.asm","-f3","-or1ag_4k.bin","-lr1ag.lst","-sr1ag.sym"],cwd=ROOT,check=True)
four=(ROOT/"r1ag_4k.bin").read_bytes()
assert len(four)==4096
rom=four*4
sha=hashlib.sha256(rom).hexdigest()
(ROOT/"r1ag_F6.bin").write_bytes(rom)
(ROOT/"ROM_SHA256.txt").write_text(sha+"  r1ag_F6.bin\n")
manifest={
 "status":"BUILT_UNVERIFIED_RESEARCH_R1AG",
 "batch":batch,"hypothesis":tag,"mask_order":order,
 "four_mode_register_schedule":schedule,
 "pinned_R1af_batch0_SHA256":PIN,"actual_ROM_SHA256":sha,
 "bytes":16384,"mapper":"standard F6, four identical banks","video":"NTSC",
 "original_nine_row_mask_bytes":"UNCHANGED",
 "goal":"600 genuine consecutive Stella screenshots; full two original 8x9 P1 masks in expected order; no extra/missing white, one full yellow P0 and one yellow M0, 262 scanlines",
 "boundary":"Research only; no R1 full scene, no close overlap below 8 CPU cycles, no verification"
}
(ROOT/"manifest.json").write_text(json.dumps(manifest,indent=2)+"\n")
print(json.dumps(manifest,indent=2))
