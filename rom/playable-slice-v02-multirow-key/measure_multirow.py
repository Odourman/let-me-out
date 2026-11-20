"""Measure physical yellow and white pixels and live reset events."""
import argparse
from pathlib import Path
from time import monotonic
from aperture_audit import TV,native_picture
from capture import BIN,Session,record
from phase import stop_at,symbols
from pixels import YELLOW,WHITE,BROWN,colored

p=argparse.ArgumentParser()
p.add_argument("rom",type=Path)
a=p.parse_args()
rom=a.rom.resolve()
syms=symbols(rom.with_suffix(".sym"))
with Session([str(BIN),"HEADLESS",str(rom)],"multirow") as s:
    s.receive(monotonic()+30)
    for _ in range(25):
        s.command("STEP FRAME")
    top,bottom,lines=map(int,TV.fullmatch(s.command("TV FRAME").decode()).groups())
    image=rom.with_suffix(".png")
    s.command(f"SCREENSHOT {image}")
    rgb=native_picture(image,(top,bottom))
    record("raster",lines=lines,aperture=[top,bottom],mapper=s.command("CARTRIDGE MAPPER").decode().strip(),
           brown_band=sorted((x,y) for x,y in colored(rgb,BROWN) if 40<=y<=44),
           yellow=sorted(colored(rgb,YELLOW)),white=sorted(colored(rgb,WHITE)))
    for label in ("FirstResp0","SecondGrp0","SecondResp0","FirstResp1",
                  "SecondGrp4","SecondResp4"):
        if label not in syms:
            continue
        before=stop_at(s,syms[label])
        cpu=s.command("CPU").decode().strip()
        s.command("STEP INSTRUCTION")
        record("write",label=label,before=before,after=s.command("TV").decode().strip(),cpu=cpu)
