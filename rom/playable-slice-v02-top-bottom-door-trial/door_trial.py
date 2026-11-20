"""Controller, ROM geometry and native RGB tests for the isolated variants."""
import argparse
from collections import deque
from itertools import groupby
import json
from pathlib import Path
from time import monotonic

from capture import BIN,Session,record
from pixels import ROOT,picture
from replay import peek
from scenarios import inp,monitor_key,score,setup,snap

ORANGE=(255,185,86)
BROWN=(199,107,33)
BLACK=(6,6,6)


def controller(s,direction):
    inp(s,"NOLEFT","NORIGHT","NOUP","NODOWN")
    if direction:
        inp(s,direction)


def rgb(out,name,edge):
    image=picture(out/f"{name}.png")
    rows=range(15,23) if edge=="top" else range(183,191)
    result={}
    for y in rows:
        result[y]={str(color):[x for x in range(160) if image[y*160+x]==color]
                   for color in (ORANGE,BROWN,BLACK)}
    record("door_rgb",name=name,fields=result,
           other_orange=sum(pixel==ORANGE for i,pixel in enumerate(image) if i//160 not in rows))


def walk(s,out,edge):
    grid=next(m["grid"] for m in json.loads((ROOT/"design/OPEN_ROOMS_V019_40x22_CANDIDATES.json").read_text())["maps"]
              if m["id"]=="A_OPEN_01")
    x,y=peek(s,[0x80,0x81])
    start=(x,y)
    target=(74,8 if edge=="top" else 159)
    dirs={"RIGHT":(1,0),"LEFT":(-1,0),"UP":(0,-1),"DOWN":(0,1)}
    frontier=deque([start])
    paths={start:()}
    while frontier:
        x,y=frontier.popleft()
        if (x,y)==target:
            break
        for name,(dx,dy) in dirs.items():
            nx,ny=x+dx,y+dy
            if ((nx,ny) not in paths and 0<=nx<=152 and 0<=ny<=159
                and all(grid[py//8][px//4]=="." for py in (ny,ny+8)
                        for px in (nx,nx+4,nx+7))):
                paths[nx,ny]=(*paths[x,y],name)
                frontier.append((nx,ny))
    x,y=start
    for i,(direction,steps) in enumerate(groupby(paths[target])):
        count=len(list(steps))
        controller(s,direction)
        dx,dy=dirs[direction]
        x,y=x+count*dx,y+count*dy
        assert snap(s,count,f"route-{i:02}",out)[:2]==[x,y]
    assert peek(s,[0xac])==[3]


def passage(s,out,edge,expected):
    direction="UP" if edge=="top" else "DOWN"
    controller(s,direction)
    snap(s,1,"unlock",out)
    assert peek(s,[0xb2,0xb3])==[1,0]
    controller(s,None)
    snap(s,4,"open",out)
    rgb(out,"open",edge)
    controller(s,direction)
    snap(s,8 if edge=="top" else 9,"exit",out)
    assert peek(s,[0xb2,0xb3,0xac])==[1,1,3] and score(s)==expected


def route(s,out,edge):
    assert peek(s,[0xae])[0]==4
    inp(s,"DOWN")
    snap(s,72,"south-corridor",out)
    inp(s,"NODOWN","RIGHT","FIRE")
    snap(s,1,"first-fire",out)
    for _ in range(110):
        s.command("STEP FRAME")
        if peek(s,[0xaf])[0]==1:
            break
    assert peek(s,[0xaf,0xac])==[1,3]
    snap(s,1,"key-floor",out)
    inp(s,"NOFIRE","NORIGHT","DOWN")
    assert snap(s,5,"align",out)[:2]==[12,159]
    inp(s,"NODOWN","RIGHT")
    monitor_key(s,out)
    assert score(s)==50
    walk(s,out,edge)
    passage(s,out,edge,210)


def fixture(s,out,edge):
    y=8 if edge=="top" else 159
    direction="UP" if edge=="top" else "DOWN"
    points=((20,40,60,96,124),(20,45,70,115,148))
    setup(s,74,y,*points,0)
    controller(s,direction)
    assert snap(s,12,"locked",out)[:2]==[74,y]
    assert peek(s,[0xaf,0xb2,0xb3])==[0,0,0]
    rgb(out,"locked",edge)
    s.command("POKE 0x00af 0x02")
    for label,x,other_y,move in (("old-right",148,80,"RIGHT"),
                                  ("wrong-x",20,y,direction),
                                  ("opposite-edge",74,159 if edge=="top" else 8,
                                   "DOWN" if edge=="top" else "UP")):
        setup(s,x,other_y,*points,0)
        controller(s,move)
        assert snap(s,12,label,out)[:2]==[x,other_y]
        assert peek(s,[0xb2,0xb3])==[0,0]
    setup(s,74,y,*points,0)
    passage(s,out,edge,175)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("rom",type=Path)
    parser.add_argument("out",type=Path)
    parser.add_argument("edge",choices=("top","bottom"))
    parser.add_argument("--cold",action="store_true")
    args=parser.parse_args()
    args.out.mkdir(parents=True,exist_ok=False)
    with Session([str(BIN),"HEADLESS",str(args.rom.resolve())],args.edge) as s:
        s.receive(monotonic()+30)
        for _ in range(24):
            s.command("STEP FRAME")
        (route if args.cold else fixture)(s,args.out.resolve(),args.edge)
    record("result",edge=args.edge,mode="joystick cold" if args.cold else "fixture",status="PASS")


if __name__=="__main__":
    main()
