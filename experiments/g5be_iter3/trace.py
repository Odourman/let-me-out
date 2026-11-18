"""Collect actual TIA bus writes between the starts of adjacent physical rows."""
import argparse
import time
from pathlib import Path

from capture import BIN, Session, expect, record
from replay import FRAME, SCENES, TV, VERSION, set_scene


def stop_at(s, addr):
    expect(s,f"BREAK PC 0x{addr}",rb"")
    result=s.command("RUN").decode()
    assert f"break on PC->0x{addr}" in result, result
    expect(s,"DROP BREAK 0",rb"breakpoint #0 dropped\n")
    position=expect(s,"TV",TV)
    return list(map(int,position.groups())), result.splitlines()


def trace(rom):
    symbols = {p[0]:p[1] for l in rom.with_suffix(".sym").read_text().splitlines()
               if len(p:=l.split())>=2}
    with Session([str(BIN), "HEADLESS", str(rom.resolve())], "g5be3-bus") as s:
        s.receive(time.monotonic()+15)
        expect(s,"VERSION REVISION",VERSION)
        for _ in range(20):
            s.command("STEP FRAME")
        for register in ("RESP0","RESP1","GRP0","GRP1","COLUP0","ENAM0","NUSIZ0"):
            expect(s,f"TRACE {register}",rb"")
        for label,xs,ys,_ in SCENES:
            x=xs[2]
            row=f"Dynamic{x}Y"
            if row+"76" not in symbols:
                record("schedule_absent", label=label, x=xs,y=ys)
                continue
            set_scene(s,xs,ys)
            s.command("STEP FRAME")
            total=list(map(int,expect(s,"TV FRAME",FRAME).groups()))
            start,_=stop_at(s,symbols[row+"76"])
            end,writes=stop_at(s,symbols[row+"77"])
            assert start[0]==end[0] and end[1]==start[1]+1, (start,end)
            record("row_bus",label=label,x=xs,y=ys,frame_total=total,
                   start=start,end=end,writes=[v for v in writes if "(TIA)" in v])
            s.command("STEP FRAME")


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("rom",type=Path)
    trace(p.parse_args().rom)
