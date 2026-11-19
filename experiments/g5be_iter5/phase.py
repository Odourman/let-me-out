"""Measure VBLANK stage lines and CPU beam phase across cache layouts."""
import argparse
from pathlib import Path
import time

from beam import sym
from capture import BIN, Session, expect, record
from replay import UNIFIED, NEGATIVE, FRAME, VERSION, set_scene
from trace import stop_at


def run(rom, fixture):
    syms=sym(rom.parent/f"{rom.stem}-bank0.sym")
    scenario=next(scene for scene in (*UNIFIED,*NEGATIVE) if scene[0]==fixture)
    _, x,y,_=scenario
    bank=(46,43,49,52).index(sorted(x)[1]) if sorted(x)[1] in (46,43,49,52) else 0
    syms=sym(rom.parent/f"{rom.stem}-bank{bank}.sym")
    with Session([str(BIN),"HEADLESS",str(rom.resolve())],"phase") as session:
        session.receive(time.monotonic()+15)
        expect(session,"VERSION REVISION",VERSION)
        for _ in range(20):
            session.command("STEP FRAME")
        set_scene(session,x,y)
        rows=int(syms["ROWS"],16)
        tail=("FarTail","LeaveLong") if fixture in ("original-far-y","far-y") and int(syms["SEGMENTED"],16) else ()
        stages=("Frame","SetupDynamic", *("PreparePointers","PeakStack")*5,
                *("CacheRow",)*rows, "TailBlank","Visible",*tail,"Overscan","Frame")
        for stage in stages:
            beam,_=stop_at(session,syms[stage])
            record("phase",stage=stage,beam=beam,fixture=scenario[0])
        span=list(map(int,expect(session,"TV FRAME",FRAME).groups()))
        record("frame_total",top=span[0],bottom=span[1],scanlines=span[2])


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("rom",type=Path)
    p.add_argument("--fixture", default="unified-control")
    a=p.parse_args()
    run(a.rom,a.fixture)
