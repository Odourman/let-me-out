"""Capture stable fixtures to distinguish TIA placement from frame-readback delay."""
from argparse import ArgumentParser
from pathlib import Path
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

if __name__=="__main__":
    p=ArgumentParser()
    p.add_argument("rom",type=Path)
    p.add_argument("out",type=Path)
    a=p.parse_args()
    run(a.rom,a.out.resolve())
