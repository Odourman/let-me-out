"""Compare 600 consecutive native Gopher frames to the frozen RGB record."""
import argparse
from pathlib import Path
from time import monotonic

from aperture_audit import TV, native_picture
from capture import BIN, Session, record
from scenarios import inp

p=argparse.ArgumentParser()
p.add_argument("rom",type=Path)
p.add_argument("out",type=Path)
p.add_argument("reference",type=Path)
a=p.parse_args()
a.out.mkdir(parents=True,exist_ok=False)
actions=(("RIGHT","NODOWN"),("NORIGHT","DOWN","FIRE"),("NOFIRE",),
         ("NODOWN","LEFT"),("NOLEFT","UP"),("RIGHT","NOUP"))
with Session([str(BIN),"HEADLESS",str(a.rom.resolve())],"paired-soak",session_limit=900) as s:
    s.receive(monotonic()+30)
    for _ in range(24):
        s.command("STEP FRAME")
    for i in range(600):
        if i%100==0:
            inp(s,*actions[i//100])
        s.command("STEP FRAME")
        top,bottom,lines=map(int,TV.fullmatch(s.command("TV FRAME").decode()).groups())
        name=f"frame-{i+1:03}.png"
        image=a.out/name
        s.command(f"SCREENSHOT {image}")
        base=a.reference/name
        equal=image.read_bytes()==base.read_bytes() or (
            native_picture(image,(top,bottom))==native_picture(base,(29,242)))
        record("paired",frame=i+1,scanlines=lines,aperture=[top,bottom],rgb_equal=equal)
        assert lines==262 and equal, (i+1,lines,equal)
