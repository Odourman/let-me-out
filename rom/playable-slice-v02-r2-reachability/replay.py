"""Real joystick inputs, frame stepping, RIOT readback and native captures in Gopher."""
import argparse
from pathlib import Path
import re
from time import monotonic

from capture import BIN, Session, record

BASE = (0x80,0x81,0x82,0x83,0x84,0x85,0x86,0x87,0x88)
FRAME = rb"top: (\d+), bottom: (\d+), total: (\d+)"


def peek(s, addresses):
    addresses=list(addresses)
    values=[]
    for i in range(0,len(addresses),16):
        response=s.command("PEEK "+" ".join(f"0x{a:04x}" for a in addresses[i:i+16]))
        values.extend(int(v,16) for v in re.findall(rb" = 0x([0-9a-f]+)",response))
    assert len(values)==len(addresses)
    return values


def frames(s, count, name, folder):
    totals=[]
    for _ in range(count):
        s.command("STEP FRAME")
        match=re.search(FRAME,s.command("TV FRAME"))
        assert match
        totals.append(int(match[3]))
    state=peek(s,BASE)
    objects=peek(s,[*range(0x91,0xa5),*range(0xaa,0xb4),0xdc])
    record("check",label=name,count=count,scanlines=sorted(set(totals)),state=state,
           npc_x=objects[:5],npc_y=objects[5:10],life=objects[15:20],
           score=objects[20]+256*objects[21],lives=objects[22],carrier=objects[24],
           key=objects[25],key_position=objects[26:28],unlocked=objects[28],
           room_done=objects[29],omitted=objects[30])
    s.command(f"SCREENSHOT {folder/name}.png")
    return state, totals


def play(s, folder):
    for _ in range(20):
        s.command("STEP FRAME")
    stages=(
        ("spawn",(),1),
        ("right",("RIGHT",),12),
        ("diagonal",("UP",),8),
        ("frozen-aim",("NORIGHT","NOUP","DOWN","FIRE"),6),
        ("button-held",(),55),
        ("release",("NODOWN","NOFIRE"),1),
        ("fire-again",("FIRE",),2),
        ("wall-left",("NOFIRE","LEFT"),45),
        ("wall-stop",(),12),
    )
    checks={}
    for name,inputs,count in stages:
        for direction in inputs:
            s.command(f"STICK LEFT {direction}")
        checks[name]=frames(s,count,name,folder)
    assert checks["right"][0][:2]==[24,82]
    assert checks["diagonal"][0][:2]==[32,74]
    assert checks["frozen-aim"][0][:2]==checks["button-held"][0][:2]==[32,74]
    assert checks["frozen-aim"][0][4]==1 and checks["frozen-aim"][0][8]==1
    assert checks["button-held"][0][4]==0 and checks["fire-again"][0][4]==1
    assert checks["wall-left"][0][0]==checks["wall-stop"][0][0]==4
    assert all(set(totals)=={262} for _,totals in checks.values())
    return checks


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("rom",type=Path)
    p.add_argument("out",type=Path)
    a=p.parse_args()
    a.out.mkdir(parents=True,exist_ok=False)
    with Session([str(BIN),"HEADLESS",str(a.rom.resolve())],"playable-v02") as s:
        s.receive(monotonic()+30)
        for cmd in ("VERSION REVISION","CARTRIDGE MAPPER"):
            s.command(cmd)
        play(s,a.out.resolve())
