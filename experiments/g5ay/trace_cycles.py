"""Measure store completion boundaries of the worst scheduled active line."""
from pathlib import Path
import re
import time
from capture import BIN, Session, Rejected, expect, record

dir = Path("clean1")
symbols = (dir/"bank1.sym").read_text().splitlines()
address = next(line.split()[1] for line in symbols if line.startswith("LineAll_76 "))
rom = (dir/"g5ay_clean1_F6.bin").resolve()
with Session([str(BIN),"HEADLESS",str(rom)],"gopher-cycle-trace") as session:
    session.receive(time.monotonic()+15)
    expect(session,"VERSION REVISION",rb"v0\.57\.2\n2af86eb725739adbf3d9d45cea2ed69eea57da2a\n")
    for _ in range(20):
        session.command("STEP FRAME")
    expect(session,"CARTRIDGE MAPPED",rb"Bank: 1\n")
    expect(session,f"BREAK PC 0x{address}",rb"")
    expect(session,"LIST BREAKS",rb"breakpoints:\n 0: PC->0x"+address.encode()+rb"\n")
    expect(session,"RUN",rb"break on PC->0x"+address.encode()+rb"\n")
    expect(session,"DROP BREAK 0",rb"breakpoint #0 dropped\n")
    for symbol in ("RESP1","GRP1","GRP0","ENAM0"):
        expect(session,f"TRACE {symbol}",rb"")
    session.command("LIST TRACES")
    session.command("STEP SCANLINE")
    tv_pattern=rb"FR=(\d+) SL=(\d+) CL=(-?\d+)\n"
    baseline=tuple(map(int,expect(session,"TV",tv_pattern).groups()))
    if baseline[2]!=-68:
        raise Rejected(f"not at start of line: {baseline}")
    pairs = []
    for _ in range(45):
        result=session.command("STEP INSTRUCTION")
        fr,sl,cl=map(int,expect(session,"TV",tv_pattern).groups())
        if (fr,sl)!=baseline[:2]:
            raise Rejected("raster advanced before obtaining all five stores")
        for event in re.finditer(rb"write 0x([0-9a-f]+) to 0x[0-9a-f]+ \((RESP1|GRP1|GRP0|ENAM0)\)",result):
            cycle,phase=divmod(cl+68,3)
            record("bus_at_instruction_boundary",fr=fr,sl=sl,cl=cl,cycle=cycle,phase=phase,
                   value=event[1].decode(),register=event[2].decode())
            pairs.append((event[2],cycle,phase))
        if sum(register==b"GRP1" for register,_,_ in pairs)==6:
            break
    else:
        raise Rejected("instruction bound reached")
    got=[cycle for register,cycle,phase in pairs if register==b"RESP1" and not phase]
    if got!=[22,31,40,50,59]:
        raise Rejected(f"unexpected RESP1 completion bounds: {got}")
    record("cycle_check",resp1=got,last_grp1=pairs[-1][1])
