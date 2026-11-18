"""Read real Gopher instruction-boundary timing at diagnostic labels."""
import json
from pathlib import Path
import sys
import time

from capture import BIN, Session, expect, record

name = sys.argv[1]
stem = Path("roms") / name
symbols = {a:int(b,16) for line in stem.with_suffix(".sym").read_text().splitlines()
           if len(parts:=line.split())>=2 and len(b:=parts[1])==4
           and all(c in "0123456789abcdef" for c in b) and (a:=parts[0])}
with Session([str(BIN),"HEADLESS",str(stem.with_suffix(".bin").resolve())],"gopher-timing") as session:
    session.receive(time.monotonic()+15)
    expect(session,"VERSION REVISION",rb"v0\.57\.2\n2af86eb725739adbf3d9d45cea2ed69eea57da2a\n")
    session.command("STEP FRAME")
    for label in ("VisibleStart","BandEntry","BandExit","Frame","VisibleStart"):
        address = f"{symbols[label]:04x}"
        expect(session,f"BREAK PC 0x{address}",rb"")
        expect(session,"RUN",rb"break on PC->0x"+address.encode()+rb"\n")
        tv = expect(session,"TV",rb"FR=(\d+) SL=(\d+) CL=(-?\d+)\n")
        record("landmark",label=label,fr=int(tv[1]),sl=int(tv[2]),cl=int(tv[3]))
        expect(session,"DROP BREAK 0",rb"breakpoint #0 dropped\n")
