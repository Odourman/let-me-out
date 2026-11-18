"""Anchor real TIA register writes to TV at every active scanline."""
from collections import defaultdict
from pathlib import Path
import re
import sys
import time

from capture import BIN, Session, Rejected, expect, record
from runtime_capture import VERSION, TV, peek
from stimuli import BASE_X, BASE_Y, soak

mode = sys.argv[1]
stem = Path("roms",mode)
symbols = {parts[0]:parts[1] for ln in stem.with_suffix(".sym").read_text().splitlines()
           if len(parts:=ln.split())>=2}
x,y = soak()[-1][1:3] if mode=="union" else (BASE_X,BASE_Y)
rom = stem.with_suffix(".bin").resolve()
with Session([str(BIN),"HEADLESS",str(rom)],"gopher-timing") as session:
    session.receive(time.monotonic()+15)
    expect(session,"VERSION REVISION",VERSION)
    for _ in range(3):
        session.command("STEP FRAME")
    for addr,value in zip(range(0x81,0x8b),x+y):
        session.command(f"POKE 0x{addr:04x} 0x{value:02x}")
    assert peek(session,list(range(0x81,0x8b)))==x+y
    address = symbols["BandEntry"]
    expect(session,f"BREAK PC 0x{address}",rb"")
    expect(session,"RUN",rb"break on PC->0x"+address.encode()+rb"\n")
    expect(session,"DROP BREAK 0",rb"breakpoint #0 dropped\n")
    emitted=[]
    for start in range(0xb8,0xf8,8):
        emitted.extend(peek(session,range(start,start+8)))
    record("ram_kernel",hex=bytes(emitted).hex(),x=x,y=y)
    if mode=="union":
        bitmap=[]
        for start in range(0xa0,0xb8,8):
            bitmap.extend(peek(session,range(start,start+8)))
        record("ram_or_bitmap",hex=bytes(bitmap).hex())
    for register in ("RESP1","GRP1","GRP0","ENAM0"):
        expect(session,f"TRACE {register}",rb"")
    first = expect(session,"TV",TV)
    fr_start,sl_before = int(first[1]),int(first[2])
    lead = session.command("STEP SCANLINE")
    if b"write 0x02 to 0x001d (ENAM0)" not in lead:
        raise Rejected("active M0 write missing before band")
    start = expect(session,"TV",TV)
    first_line=int(start[2])
    if first_line!=sl_before+1 or int(start[3])!=-68:
        raise Rejected("not at active band origin")
    raster=defaultdict(list)
    for _ in range(1600):
        out=session.command("STEP INSTRUCTION")
        fr,sl,cl=map(int,expect(session,"TV",TV).groups())
        if fr!=fr_start:
            raise Rejected("stepped to wrong frame")
        if sl>=first_line+24:
            break
        for event in re.finditer(rb"write 0x([0-9a-f]+) to 0x[0-9a-f]+ \((RESP1|GRP1|GRP0|ENAM0)\)",out):
            cyc,phase=divmod(cl+68,3)
            register=event[2].decode()
            raster[sl].append((register,cyc,event[1].decode()))
            record("bus_boundary",fr=fr,sl=sl,cl=cl,cycle=cyc,phase=phase,register=register,value=event[1].decode())
    else:
        raise Rejected("instruction bound exhausted")
    for sl in range(first_line,first_line+24):
        entries = raster[sl]
        if len(entries)!=(11 if mode=="wide" else 9):
            raise Rejected(f"incomplete bus event series line {sl}: {entries!r}")
        record("raster_timing",line=sl,visible_y=64+sl-first_line,
               resp=[c for r,c,v in entries if r=="RESP1"],
               grp=[c for r,c,v in entries if r=="GRP1"],last_cycle=entries[-1][1])
    record("timing_done",first=first_line,last=first_line+23,max_cycle=max(e[-1][1] for e in raster.values()))
