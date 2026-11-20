"""Compare the same WSYNC at the old door-band rows in three real ROMs."""
from pathlib import Path
import re
from time import monotonic

from capture import BIN,Session,record
from phase import symbols

root=Path.cwd()
base=root.parent/"playable-slice-v02-object-conflict-repair"
cases=[
 ("right",base/"let-me-out-v02-object-conflict-repair.bin",base/"video.sym"),
 *((edge,root/f"let-me-out-v02-door-{edge}.bin",root/f"{edge}-video.sym")
   for edge in ("top","bottom")),
]
for label,rom,sym in cases:
    with Session([str(BIN),"HEADLESS",str(rom)],label) as s:
        s.receive(monotonic()+15)
        for _ in range(24):
            s.command("STEP FRAME")
        address=symbols(sym)["NextRoom"]
        s.command(f"BREAK PC 0x{address}")
        for _ in range(176):
            s.command("RUN")
            tv=s.command("TV").decode().strip()
            line=int(re.search(r"SL=(\d+)",tv)[1])
            if line in (138,139,140):
                record("mid_band",case=label,tv=tv,cpu=s.command("CPU").decode().strip())
            if line==140:
                break
        else:
            raise AssertionError("target raster row was not reached")
