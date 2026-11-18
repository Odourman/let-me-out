"""Trace each frame stage across admitted and rejected live RAM switches."""
import argparse,re,time
from pathlib import Path
from capture import Session,BIN,expect,record
from replay import SCENES,TV,VERSION,FRAME

def pin(s,pc):
    expect(s,f"BREAK PC 0x{pc}",rb"")
    answer=s.command("RUN").decode()
    assert f"break on PC->0x{pc}" in answer,answer
    expect(s,"DROP BREAK 0",rb"breakpoint #0 dropped\n")
    loc=expect(s,"TV",TV)
    return dict(frame=int(loc[1]),scanline=int(loc[2]),cl=int(loc[3]),
                wsync=len(re.findall(r"\(WSYNC\)",answer)),
                edges=[line for line in answer.splitlines() if any(
                    item in line for item in ("(VSYNC)","(VBLANK)","(NUSIZ0)","(ENAM0)"))])

def trace(rom):
    syms={p[0]:p[1] for l in rom.with_suffix(".sym").read_text().splitlines()
          if len(p:=l.split())>=2}
    with Session([str(BIN),"HEADLESS",str(rom.resolve())],"timing-g5be2") as s:
        s.receive(time.monotonic()+15)
        expect(s,"VERSION REVISION",VERSION)
        for _ in range(3):
            s.command("STEP FRAME")
        for register in ("VSYNC","VBLANK","WSYNC","NUSIZ0","ENAM0","GRP0","GRP1","RESP0","RESP1","COLUP0","VDELP0","VDELP1"):
            expect(s,f"TRACE {register}",rb"")
        loc=pin(s,syms["Frame"])
        for index in (0,3,1,4,2,5,6,7,0,8,1,2):
            label,x,y,admitted=SCENES[index]
            for addr,value in zip(range(0x81,0x8b),x+y):
                s.command(f"POKE 0x{addr:04x} 0x{value:02x}")
            record("phase",fixture=label,phase="Frame",**loc)
            stages=("SyncOff","Visible","Lead","Prepare")
            if admitted:
                stages+=("LeaveBand",)
            for stage in (*stages,"EndShot","Overscan","Frame"):
                loc=pin(s,syms[stage])
                if stage=="Frame":
                    top,bottom,total=map(int,expect(s,"TV FRAME",FRAME).groups())
                    record("frame_total",fixture=label,top=top,bottom=bottom,total=total)
                    record("phase",fixture=label,phase="NextFrame",**loc)
                else:
                    record("phase",fixture=label,phase=stage,**loc)

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("rom",type=Path)
    trace(p.parse_args().rom)
