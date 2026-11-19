"""Correlate physical beam position with program stages and deepest wall check."""
import argparse
from pathlib import Path
import re
from time import monotonic

from capture import BIN,Session,record


def symbols(path):
    return {parts[0]:parts[1] for line in path.read_text().splitlines()
            if len(parts:=line.split())>=2 and re.fullmatch(r"[0-9a-f]{4}",parts[1])}


def stop_at(s, addr):
    s.command(f"BREAK PC 0x{addr}")
    reply=s.command("RUN")
    assert f"break on PC->0x{addr}".encode() in reply
    s.command("DROP BREAK 0")
    return s.command("TV").decode().strip()


def measure(s, video, logic, max_x):
    for _ in range(24):
        s.command("STEP FRAME")
    if max_x:
        for i in range(5):
            s.command(f"POKE 0x{0xa0+i:04x} 0x{'ff' if i==0 else '00'}")
        for addr,value in ((0x91,148),(0x96,90),(0xb3,1)):
            s.command(f"POKE 0x{addr:04x} 0x{value:02x}")
        for _ in range(2):
            s.command("STEP FRAME")
        for label in ("NpcSetupFirst","NpcSetupSync","GlyphStart"):
            record("phase",label=label,tv=stop_at(s,video[label]))
            if label != "NpcSetupSync":
                s.command("STEP INSTRUCTION")
                record("phase",label=label+"-executed",tv=s.command("TV").decode().strip())
        return
    for label in ("Frame","BlankWait","Top","Room","RoomEnd","Bottom","GameBank","Overscan","Frame"):
        record("phase",label=label,tv=stop_at(s,video[label]),frame=s.command("TV FRAME").decode().strip())
    s.command("STICK LEFT RIGHT")
    record("stack",tv=stop_at(s,logic["HitPoint"]),cpu=s.command("CPU").decode().strip())


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("rom",type=Path)
    p.add_argument('--max-x',action='store_true')
    a=p.parse_args()
    a.rom=a.rom.resolve()
    with Session([str(BIN),"HEADLESS",str(a.rom)],"slice-phase") as s:
        s.receive(monotonic()+30)
        measure(s,symbols(a.rom.with_name("video.sym")),symbols(a.rom.with_name("logic.sym")),a.max_x)
