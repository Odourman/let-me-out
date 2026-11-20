"""Controller, ROM geometry and native RGB tests for the isolated variants."""
import argparse
from collections import deque
from itertools import groupby
import json
import re
from pathlib import Path
from time import monotonic

from capture import BIN,Session,record
from pixels import ROOT,YELLOW,colored,expected_mask,picture
from audit import KEY
from replay import FRAME,peek
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


def monitor_blink(s,out,on,policy):
    for i in range(95):
        px,clock=peek(s,[0x80,0x90])
        phase=clock%12
        if px==77:
            inp(s,"RIGHT" if (phase<on)==(policy=="on") else "NORIGHT")
        s.command("STEP FRAME")
        state,x,y=peek(s,[0xaf,0xb0,0xb1])
        state &= 0x7f
        stamp=s.command("TV FRAME")
        from aperture_audit import native_picture, TV
        top,bottom,lines=map(int,TV.fullmatch(stamp.decode()).groups())
        assert lines==262
        name=f"cold-blink-{i:03}.png"
        target=out/name
        s.command(f"SCREENSHOT {target}")
        yellow=colored(native_picture(target,(top,bottom)),YELLOW)
        mask=expected_mask(KEY,x,y+15)
        actors=peek(s,[0xae,0x81,0x84,*range(0x91,0x9b),*range(0xa0,0xa5)])
        record("cold_blink",domain="REAL_COLD",carrier=actors[0],py=actors[1],shot=actors[2],
               nx=actors[3:8],ny=actors[8:13],life=actors[13:],key_x=x,key_y=y,frame=i,phase=phase,wanted=phase<on,state=state,
               expected_pickup=policy,key=len(mask&yellow),px_before=px,lines=lines,png=name)
        if state==2:
            assert (phase<on)==(policy=="on"), (phase,policy)
            return
    raise AssertionError("no pickup in the selected phase")


def route(s,out,edge,blink=0,pickup="on",visit=None,lure=False):
    assert peek(s,[0xae])[0]==4
    inp(s,"DOWN")
    snap(s,72,"south-corridor",out)
    inp(s,"NODOWN","RIGHT","FIRE")
    snap(s,1,"first-fire",out)
    for _ in range(110):
        s.command("STEP FRAME")
        if peek(s,[0xaf])[0]&0x7f==1:
            break
    assert peek(s,[0xaf])[0]&0x7f==1 and peek(s,[0xac])==[3]
    snap(s,1,"key-floor",out)
    inp(s,"NOFIRE","NORIGHT","DOWN")
    assert snap(s,5,"align",out)[:2]==[12,159]
    if visit is not None:
        if lure:
            controller(s,"RIGHT")
            assert snap(s,48,"lure-x",out)[:2]==[60,159]
            controller(s,None)
            for _ in range(20):
                if peek(s,[0x99])[0]>=148:
                    break
                s.command("STEP FRAME")
            assert 148<=peek(s,[0x99])[0]<151 and peek(s,[0xac])==[3]
            controller(s,"LEFT")
            assert snap(s,36,"lure-retreat",out)[:2]==[24,159]
            if visit==60:
                controller(s,None)
                for _ in range(200):
                    if peek(s,[0x94])[0]<=47:
                        break
                    s.command("STEP FRAME")
                assert peek(s,[0x94])[0]<=47 and peek(s,[0xac])==[3]
                controller(s,"RIGHT")
                assert snap(s,36,"visit-x",out)[:2]==[60,159]
        else:
            controller(s,"RIGHT")
            assert snap(s,visit-12,"visit-x",out)[:2]==[visit,159]
        controller(s,"UP")
        assert snap(s,8,"visit-y",out)[:2]==[visit,151]
        controller(s,None)
        for index in range(24):
            clock=peek(s,[0x90])[0]
            state=snap(s,1,f"visit-frame-{index:02}",out)
            assert state[:2]==[visit,151]
            life=peek(s,range(0xa0,0xa5))
            carrier,key_state,x,y=peek(s,[0xae,0xaf,0xb0,0xb1])
            assert life[carrier]==0 and key_state&0x7f==1
            assert sum(value==255 for value in life)==4 and peek(s,[0xac])==[3]
            # A freeze is never used. The four NPCs keep moving during the visit.
            from aperture_audit import TV,native_picture
            top,bottom,_=map(int,TV.fullmatch(s.command("TV FRAME").decode()).groups())
            img=native_picture(out/f"visit-frame-{index:02}.png",(top,bottom))
            key=expected_mask(KEY,x,y+15)
            record("real_visit",domain="REAL_COLD",px=visit,py=151,phase=clock%12,
                   wanted=clock%12<blink,carrier=carrier,life=life,key_x=x,key_y=y,
                   nx=peek(s,range(0x91,0x96)),ny=peek(s,range(0x96,0x9b)),
                   key=len(key&colored(img,YELLOW)))
        controller(s,"DOWN")
        assert snap(s,8,"visit-return",out)[:2]==[visit,159]
    inp(s,"NODOWN","RIGHT")
    if blink:
        monitor_blink(s,out,blink,pickup)
    else:
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
    for x in (64,88):
        setup(s,x,y,*points,0)
        controller(s,direction)
        assert snap(s,8,f"locked-rim-{x}",out)[:2]==[x,y]
        assert peek(s,[0xb2,0xb3])==[0,0]
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
    parser.add_argument("--blink",type=int,choices=(0,6,8),default=0)
    parser.add_argument("--pickup",choices=("on","off"),default="on")
    parser.add_argument("--visit",type=int,choices=(24,60))
    parser.add_argument("--lure",action="store_true")
    args=parser.parse_args()
    args.out.mkdir(parents=True,exist_ok=False)
    with Session([str(BIN),"HEADLESS",str(args.rom.resolve())],args.edge) as s:
        s.receive(monotonic()+30)
        for _ in range(24):
            s.command("STEP FRAME")
        if args.cold:
            route(s,args.out.resolve(),args.edge,args.blink,args.pickup,args.visit,args.lure)
        else:
            fixture(s,args.out.resolve(),args.edge)
    record("result",edge=args.edge,mode="joystick cold" if args.cold else "fixture",status="PASS")


if __name__=="__main__":
    main()
