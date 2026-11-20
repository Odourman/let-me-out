"""Report real P0/SM pixels from the isolated F6 re-trigger experiments."""
import argparse
from pathlib import Path
from time import monotonic

from aperture_audit import TV, native_picture
from capture import BIN, Session, record
from phase import stop_at, symbols
from pixels import YELLOW, WHITE, colored

p=argparse.ArgumentParser()
p.add_argument("rom",type=Path)
p.add_argument("image",type=Path)
a=p.parse_args()
sym=symbols(a.rom.with_suffix(".sym"))
with Session([str(BIN),"HEADLESS",str(a.rom.resolve())],"p0-line") as s:
    s.receive(monotonic()+30)
    for _ in range(25):
        s.command("STEP FRAME")
    top,bottom,total=map(int,TV.fullmatch(s.command("TV FRAME").decode()).groups())
    s.command(f"SCREENSHOT {a.image.resolve()}")
    rgb=native_picture(a.image,(top,bottom))
    record("p0_pixels",name=a.rom.stem,scanlines=total,aperture=(top,bottom),
           yellow=sorted(colored(rgb,YELLOW)),white=sorted(colored(rgb,WHITE)))
    for label in ("SecondResp","SecondGrp"):
        before=stop_at(s,sym[label])
        cpu=s.command("CPU").decode().strip()
        s.command("STEP INSTRUCTION")
        record("p0_write",label=label,before=before,cpu=cpu,
               after=s.command("TV").decode().strip())
