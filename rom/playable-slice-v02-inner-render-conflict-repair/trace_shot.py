"""Read beam timestamps before the fast zero write in the shot fixture."""
import argparse
from pathlib import Path
from time import monotonic

from capture import BIN,Session,record
from phase import symbols


p=argparse.ArgumentParser()
p.add_argument("edge",choices=("top","bottom"))
edge=p.parse_args().edge
rom=Path(f"let-me-out-v02-brown-door-{edge}.bin").resolve()
video=symbols(Path(f"{edge}-video.sym"))
with Session([str(BIN),"HEADLESS",str(rom)],edge) as session:
    session.receive(monotonic()+30)
    for _ in range(24):
        session.command("STEP FRAME")
    values={0xb3:1,0x81:44,0x84:1,0x85:12,0x86:90,0x91:105,0x96:90,
            **{0xa0+i:255 if i==0 else 0 for i in range(5)}}
    for address,value in values.items():
        session.command(f"POKE 0x{address:04x} 0x{value:02x}")
    for _ in range(3):
        session.command("STEP FRAME")
    session.command(f'BREAK PC 0x{video["RoomSprites"]}')
    for _ in range(176):
        session.command("RUN")
        cpu=session.command("CPU").decode().strip()
        if any(f"Y={y:02x}" in cpu.lower().replace("y=","Y=") for y in (169,170,171)):
            tv=session.command("TV").decode().strip()
            record("shot_write",target="ENAM0",cpu=cpu,tv=tv)
        if "Y=ab" in cpu.lower().replace("y=","Y="):
            break
