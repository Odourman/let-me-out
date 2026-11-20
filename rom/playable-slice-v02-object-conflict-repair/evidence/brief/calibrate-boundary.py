"""Capture stable fixtures to distinguish TIA placement from frame-readback delay."""
from argparse import ArgumentParser
from pathlib import Path
import json
import re
from time import monotonic

from capture import BIN,Session,record
from pixels import picture,colored,expected_mask,PLAYER,YELLOW,WHITE

MALE=(0x3c,0x3c,0x18,0xff,0x18,0x24,0x24,0x42,0x42)

def run(rom,out):
    out.mkdir(parents=True,exist_ok=False)
    with Session([str(BIN),"HEADLESS",str(rom.resolve())],"slice-calibration") as s:
        s.receive(monotonic()+30)
        for _ in range(24):s.command("STEP FRAME")
        s.command("POKE 0x00b3 0x01")  # freeze simulation, continue normal renderer
        for i in range(5): s.command(f"POKE 0x{0xa0+i:04x} 0x00")
        s.command("POKE 0x0081 0x2c")
        for channel,addr,old,rgb,ys in (
            ("P0",0x80,PLAYER,YELLOW,59),("P1",0x91,MALE,WHITE,105)):
            if channel=="P1":
                s.command("POKE 0x00a0 0xff")
                s.command("POKE 0x0096 0x5a")
            for x in (4,12,17,24,32,47,64,73,79,92,117,148):
                s.command(f"POKE 0x{addr:04x} 0x{x:02x}")
                for _ in range(3):s.command("STEP FRAME")
                image=out/f"{channel}-{x}.png"
                s.command(f"SCREENSHOT {image}")
                points=colored(picture(image),rgb)
                dist,obs=min((len(expected_mask(old,v,ys)^points),v)
                             for v in range(max(0,x-8),min(x+9,160)))
                record("fit",channel=channel,requested=x,observed=obs,difference=dist,count=len(points))


def missile_door(rom,out):
    out.mkdir(parents=True,exist_ok=False)
    with Session([str(BIN),"HEADLESS",str(rom.resolve())],"door-missile") as s:
        s.receive(monotonic()+30)
        for _ in range(24):
            s.command("STEP FRAME")
        fixture={0xb3:1,0xb1:0,0x81:44,0x84:1,0x86:90,0x91:105,0x96:90,
                 **{0xa0+i:255 if i==0 else 0 for i in range(5)}}
        for address,value in fixture.items():
            s.command(f"POKE 0x{address:04x} 0x{value:02x}")
        for x in (12,24,32,47,56,64,79,92,117,148):
            s.command(f"POKE 0x0085 0x{x:02x}")
            for _ in range(3):
                s.command("STEP FRAME")
            image=out/f"m0-{x}.png"
            s.command(f"SCREENSHOT {image}")
            yellow=colored(picture(image),YELLOW)
            points={(px,py) for px,py in yellow if py>=100}
            record("missile",x=x,expected=[x,105],actual=sorted(points),
                   correct=points=={(x,105)})


def wall_domain(rom,out):
    """Check the wall-only handoff over its horizontal and vertical range."""
    from audit import BROWN, ROOT
    from replay import FRAME

    walls=next(m["grid"] for m in json.loads(
        (ROOT/"design/OPEN_ROOMS_V019_40x22_CANDIDATES.json").read_text())["maps"]
               if m["id"]=="A_OPEN_01")
    expected={(x,y+15) for y in range(176) for x in range(160)
              if walls[y//8][x//4]=="#"}
    out.mkdir(parents=True,exist_ok=False)
    with Session([str(BIN),"HEADLESS",str(rom.resolve())],"wall-domain") as s:
        s.receive(monotonic()+30)
        for _ in range(24):
            s.command("STEP FRAME")
        settings={0xb3:1,0x80:12,0x81:44,**{0xa0+i:0 for i in range(1,5)}}
        for address,value in settings.items():
            s.command(f"POKE 0x{address:04x} 0x{value:02x}")
        for y in (71,72,73,102,103,104):
            s.command(f"POKE 0x0096 0x{y:02x}")
            for x in (*range(63,72),*range(72,79)):
                s.command(f"POKE 0x0091 0x{x:02x}")
                for _ in range(3):
                    s.command("STEP FRAME")
                target=out/f"wall-{x}-{y}.png"
                s.command(f"SCREENSHOT {target}")
                pixels=picture(target)
                white=colored(pixels,WHITE)
                brown=colored(pixels,BROWN)
                mask=expected_mask(MALE,x,y+15)
                scanlines=int(re.search(FRAME,s.command("TV FRAME"))[3])
                record("wall_domain",x=x,y=y,scanlines=scanlines,
                       npc_missing=len(mask-white),npc_extra=len(white-mask),
                       wall_missing=len(expected-brown),wall_extra=len(brown-expected))

if __name__=="__main__":
    p=ArgumentParser()
    p.add_argument("rom",type=Path)
    p.add_argument("out",type=Path)
    modes=p.add_mutually_exclusive_group()
    modes.add_argument("--door-missile",action="store_true")
    modes.add_argument("--wall-domain",action="store_true")
    a=p.parse_args()
    method=wall_domain if a.wall_domain else missile_door if a.door_missile else run
    method(a.rom,a.out.resolve())
