"""Correlate the two discarded object's writes with Gopher beam coordinates."""
from pathlib import Path
import sys
from time import monotonic

from capture import BIN,Session,record
from phase import stop_at,symbols

kind=sys.argv[1]
table=symbols(Path("top-video.sym"))
rom=Path("let-me-out-v02-brown-door-top.bin").resolve()
if kind=="ball-key":
    coords=(90,30,60,59,120,20,48,96,148,118)
    values={0x80:24,0x81:151,0xb3:1,0xaf:1,0xb0:85,0xb1:153}
    labels=("BallWidth","BallEnable","BallGold","BallBrown")
else:
    coords=(20,44,68,92,116,86,86,86,86,86)
    values={0x80:24,0x81:159,0xb3:1}
    labels=("LeftMask","LeftReset","RightMask","RightReset")
values.update({0x91+i:value for i,value in enumerate(coords)})
with Session([str(BIN),"HEADLESS",str(rom)],kind) as s:
    s.receive(monotonic()+30)
    for _ in range(24):
        s.command("STEP FRAME")
    for address,value in values.items():
        s.command(f"POKE 0x{address:04x} 0x{value:02x}")
    for _ in range(3):
        s.command("STEP FRAME")
    for label in labels:
        stamp=stop_at(s,table[label])
        record("probe_write",label=label,tv=stamp,cpu=s.command("CPU").decode().strip())
