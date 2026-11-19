"""Measure CPU debugger beam positions and hardware-correlated writes in one row."""
import argparse
from pathlib import Path
import time

from capture import BIN, Session, expect, record
from replay import SCENES, LEFT, TV, VERSION, set_scene
from trace import stop_at


def sym(path):
    return {p[0]:p[1] for line in path.read_text().splitlines()
            if len(p:=line.split())>=2}


def display(s):
    return list(map(int,expect(s,"TV",TV).groups()))


def run(rom, frozen, stack_only, baseline):
    scenarios = SCENES[:1] if baseline else LEFT
    paths = [rom.with_suffix(".sym")] if frozen else [
        rom.parent/f"{rom.stem}-bank{i}.sym" for i in range(4)]
    symbols = [sym(path) for path in paths]
    with Session([str(BIN),"HEADLESS",str(rom.resolve())], "beam") as s:
        s.receive(time.monotonic()+15)
        expect(s,"VERSION REVISION",VERSION)
        for _ in range(20):
            s.command("STEP FRAME")
        if not frozen:
            stop_at(s,symbols[0]["PeakStack"])
            record("stack",readout=s.command("CPU").decode())
        if stack_only:
            return
        for register in ("GRP0","GRP1","RESP1"):
            expect(s,f"TRACE {register}",rb"")
        for label,x,y,_ in scenarios:
            set_scene(s,x,y)
            s.command("STEP FRAME")
            bank = 0 if frozen or baseline else (46,43,49,52).index(sorted(x)[1])
            sy = symbols[bank]
            current,_=stop_at(s,sy[f"Dynamic{x[2]}Y76"])
            first=current
            n=0
            while current[1]==first[1]:
                output=s.command("STEP INSTRUCTION").decode()
                after=display(s)
                if "(TIA)" in output:
                    state=s.command("PLAYER 1").decode()
                    record("write",label=label,x=x,y=y,bank=bank,before=current,
                           after=after,answer=output,player1=state,cpu=s.command("CPU").decode())
                current=after
                n+=1
                assert n<=48
            assert current[0]==first[0] and current[1]==first[1]+1 and current[2]==first[2]
            record("row",label=label,start=first,end=current,instructions=n)


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("rom",type=Path)
    p.add_argument("--frozen",action="store_true")
    p.add_argument("--stack-only",action="store_true")
    p.add_argument("--baseline",action="store_true")
    a=p.parse_args()
    run(a.rom,a.frozen,a.stack_only,a.baseline)
