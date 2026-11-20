"""Trace actual TIA write sites and the wall-collision stack in each ROM."""
import argparse
import re
from pathlib import Path
from time import monotonic

from capture import BIN,Session,record
from phase import stop_at,symbols


def main():
    p=argparse.ArgumentParser()
    p.add_argument("edge",choices=("top","bottom"))
    p.add_argument("--open",action="store_true")
    a=p.parse_args()
    rom=Path(f"let-me-out-v02-brown-door-{a.edge}.bin").resolve()
    video=symbols(rom.with_name(f"{a.edge}-video.sym"))
    logic=symbols(rom.with_name(f"{a.edge}-logic.sym"))
    with Session([str(BIN),"HEADLESS",str(rom)],a.edge) as s:
        s.receive(monotonic()+15)
        for _ in range(24):
            s.command("STEP FRAME")
        if a.open:
            s.command("POKE 0x00af 0x02")
            s.command("POKE 0x00b2 0x01")
            s.command("STEP FRAME")
        for label in ("DoorMaskWrite","DoorPlayerWrite","NextRoom"):
            beam=stop_at(s,video[label])
            record("tia_write",instruction={"DoorMaskWrite":"STA PF2","DoorPlayerWrite":"STA GRP0","NextRoom":"STA WSYNC"}[label],label=label,tv=beam,
                   cpu=s.command("CPU").decode().strip())
        if a.edge=="bottom":
            beam=stop_at(s,video["LastBorderLine"])
            record("tia_write",instruction="STA WSYNC",label="LastBorderLine",
                   tv=beam,cpu=s.command("CPU").decode().strip())
        for label in ("Frame","BlankWait","Top","Room","Bottom","GameBank","Overscan","Frame"):
            beam=stop_at(s,video[label])
            record("phase",label=label,tv=beam,frame=s.command("TV FRAME").decode().strip())
        s.command("STICK LEFT RIGHT")
        for _ in range(16):
            beam=stop_at(s,logic["HitPoint"])
            if int(re.search(r"SL=(\d+)",beam)[1])>=228:
                record("stack",tv=beam,cpu=s.command("CPU").decode().strip())
                break
        else:
            raise AssertionError("wall-collision stack sample unreachable")


if __name__=="__main__":
    main()
