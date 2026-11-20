"""Generate one five-row, cycle-accounted 6507 diagnostic band."""
import argparse
import json
import re
from pixels import ROOT
from pathlib import Path
import shutil
import subprocess

p=argparse.ArgumentParser()
p.add_argument("out",type=Path)
p.add_argument("--player",type=int,choices=(24,60,104),required=True)
p.add_argument("--first-cycle",type=int,required=True)
p.add_argument("--second-cycle",type=int,required=True)
p.add_argument("--shift-first",type=int,default=0)
p.add_argument("--indexed",action="store_true")
p.add_argument("--advance-y",action="store_true")
p.add_argument("--planned-map",action="store_true")
p.add_argument("--key-x",type=int,default=85)
p.add_argument("--key-y",type=int,default=153)
p.add_argument("--py",type=int,default=151)
p.add_argument("--sm-y",type=int,default=149)
p.add_argument("--pf-dynamic",action="store_true")
p.add_argument("--p1-key",action="store_true")
p.add_argument("--reset-first",action="store_true")
p.add_argument("--grp-delay",type=int,choices=(0,2,3,4),default=0)
p.add_argument("--sm-x",type=int,default=59)
p.add_argument("--shift-second",type=int,default=0)
p.add_argument("--shot",action="store_true")
p.add_argument("--shot-x",type=int,default=120)
p.add_argument("--release-nusiz",action="store_true")
a=p.parse_args()
out=a.out.resolve()
out.mkdir(parents=True,exist_ok=True)
source=Path(__file__).resolve().with_name("multirow.asm")
shutil.copyfile(source,out/source.name)
player=(0x7e,0x1e,0x3c,0x18,0x24)
key=(0x70,0x50,0x7e,0x24,0x04)
sm=(0x7e,0x18,0x24,0,0)
pf_rows=[(16,0,0)]*6
if a.planned_map:
    grid=next(m["grid"] for m in json.loads(
        (ROOT/"design/OPEN_ROOMS_V019_40x22_CANDIDATES.json").read_text())["maps"]
        if m["id"]=="A_OPEN_01")
    source_text=(ROOT/"rom/playable-slice-v02-key-p0-followup/game.asm").read_text()
    def mask(label):
        contents=re.search(r"^"+label+r":\n +byte ([^\n]+)",source_text,re.M)[1]
        return [int(v.strip().removeprefix("$"),16) for v in contents.split(",")]
    sm_source=[int(v,2) for v in json.loads(
        (ROOT/"design/NPC_REFERENCE_8x9_masks.json").read_text())["sprites"]["small_male"]]
    def at(values,offset):
        return values[offset] if 0<=offset<len(values) else 0
    ys=range(a.key_y+1,a.key_y+6)
    player=tuple(at(mask("PlayerShape"),y-a.py) for y in ys)
    key=tuple(at(mask("KeyShape"),y-a.key_y) for y in ys)
    sm=tuple(at(sm_source,y-a.sm_y) for y in ys)
    def packed(y):
        data=grid[y//8].replace("D","#")
        return tuple(sum(1<<b for c,b in zip(data[lo:hi],bits) if c=="#")
                     for lo,hi,bits in ((0,4,range(4,8)),(4,12,range(7,-1,-1)),(12,20,range(8))))
    pf_rows=[packed(y) for y in (*ys,a.key_y+6)]
    assert a.key_x-85==3*(a.second_cycle-41)
first,second=(key,player) if a.player>85 else (player,key)
rows=[]
shifted_white=[]
for i,(g0,g1,white) in enumerate(zip(first,second,sm)):
    k=[f"Row{i}:"," sta $02"]
    cycles=[0]
    def emit(op,c):
        k.append(f" {op}")
        cycles[0]+=c
    def pad(target):
        delta=target-cycles[0]
        assert delta>=0 and delta!=1,(i,target,cycles)
        if delta%2:
            emit("bit $80",3)
            delta-=3
        for _ in range(delta//2):
            emit("nop",2)
    if a.p1_key:
        if a.shift_first<0:
            white >>= -a.shift_first
        elif a.shift_first>0:
            white = (white<<a.shift_first)&255
        shifted_white.append(white)
        emit(f"lda #{2 if a.shot and i==2 else 0}",2)
        emit("sta $1d",3)
        if a.indexed:
            emit(f"ldy #{i}",2)
            emit("lda ($89),y",5)
            emit("sta $1b",3)
            emit("lda ($d7),y",5)
            emit("sta $1c",3)
        else:
            emit(f"lda #{player[i]}",2)
            emit("sta $1b",3)
            emit("lda #$0e",2)
            emit("sta $07",3)
            emit(f"lda #{white}",2)
            emit("sta $1c",3)
        for op,c in ((f"ldy #{key[i]}",2),("ldx #1",2),("stx $05",3)):
            emit(op,c)
        pad(a.first_cycle)
        k.append(f"FirstResp{i}:")
        emit("sta $11",3)
        emit("ldx #$1e",2)
        pad(a.second_cycle)
        k.append(f"SecondResp{i}:")
        emit("sta $11",3)
        pad(cycles[0]+a.grp_delay)
        k.append(f"SecondGrp{i}:")
        emit("sty $1c",3)
        emit("stx $07",3)
        changes=[(j,new) for j,(old,new) in enumerate(zip(pf_rows[i],pf_rows[i+1])) if old!=new]
        assert len(changes)<=2, (i,changes)
        if len(changes)==2:
            emit(f"ldx #{changes[0][1]}",2)
        pad(55 if cycles[0]==53 else 54)
        emit("lda #0",2)
        emit("sta $05",3)
        if a.indexed:
            emit("lda #$0e",2)
            emit("sta $07",3)
        if len(changes)==2:
            k.append(f"PFWrite{changes[0][0]}Row{i}:")
            emit(f"stx ${13+changes[0][0]:02x}",3)
        if changes:
            j,value=changes[-1]
            emit(f"lda #{value}",2)
            k.append(f"PFWrite{j}Row{i}:")
            emit(f"sta ${13+j:02x}",3)
        if a.advance_y and changes:
            emit("iny",2)
        if a.pf_dynamic:
            for j,address in enumerate(("$0d","$0e","$0f")):
                emit(f"lda Pf{j},x",4)
                emit(f"sta {address}",3)
        elif not a.advance_y:
            assert cycles[0]+3<=76
        rows.extend(k)
        continue
    if a.reset_first:
        emit(f"lda #{white}",2)
        emit("sta $1c",3)
    else:
        emit(f"lda #{2 if a.shot and i==2 else 0}",2)
        emit("sta $1d",3)
    if a.shift_first<0:
        g0 >>= -a.shift_first
    elif a.shift_first>0:
        g0 = (g0<<a.shift_first)&255
    emit(f"lda #{g0}",2)
    emit("sta $1b",3)
    if a.shift_second<0:
        g1 >>= -a.shift_second
    elif a.shift_second>0:
        g1 = (g1<<a.shift_second)&255
    emit(f"ldy #{g1}",2)
    emit("ldx #1",2)
    emit("stx $04",3)
    pad(a.first_cycle)
    k.append(f"FirstResp{i}:")
    emit("sta $10",3)
    if a.reset_first:
        pad(a.second_cycle)
        k.append(f"SecondResp{i}:")
        emit("sta $10",3)
        pad(cycles[0]+a.grp_delay)
        k.append(f"SecondGrp{i}:")
        emit("sty $1b",3)
        emit(f"lda #{2 if a.shot and i==2 else 0}",2)
        emit("sta $1d",3)
    else:
        emit(f"lda #{white}",2)
        emit("sta $1c",3)
        pad(a.second_cycle-3)
        k.append(f"SecondGrp{i}:")
        emit("sty $1b",3)
        k.append(f"SecondResp{i}:")
        emit("sta $10",3)
    if a.release_nusiz:
        pad(max(54 if a.reset_first else 53,cycles[0]))
        emit("lda #0",2)
        emit("sta $04",3)
    assert cycles[0]+3<=76
    rows.extend(k)
rows.append(" sta $02")
(out/"rows.inc").write_text("\n".join(rows)+"\n")
tables = (" ALIGN 256\nPlayerRows:\n byte "+",".join(map(str,player))
          +"\nSmRows:\n byte "+",".join(map(str,shifted_white or sm))
          +"\nPf0:\n ds 31,$10\nPf1:\n ds 31,$00\nPf2:\n ds 31,$00\n")
(out/"tables.inc").write_text(tables)
first_x=a.player if a.p1_key else min(a.player,85)
subprocess.run(["/workspace/.g5ar-env01/bin/dasm","multirow.asm",
                f"-DFIRST_X={first_x}",f"-DSM_X={a.sm_x}",f"-DSHOT_X={a.shot_x}",*(f"-DINIT_PF{i}={v}" for i,v in enumerate(pf_rows[0])),"-f3","-oone.bank","-sprobe.sym",
                "-lprobe.lst"],cwd=out,check=True)
(out/"plan.json").write_text(json.dumps(dict(options=vars(a)|{"out":str(a.out)},
    player=player,key=key,sm=sm,pf=pf_rows),default=str,indent=2)+"\n")
bank=(out/"one.bank").read_bytes()
assert len(bank)==4096
(out/"probe.bin").write_bytes(bank*4)
