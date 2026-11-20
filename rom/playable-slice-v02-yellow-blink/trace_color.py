"""Log the actual queue color stores on a visible-key frame."""
import argparse
from pathlib import Path
from time import monotonic

from capture import BIN, Session, record
from phase import stop_at, symbols

p=argparse.ArgumentParser()
p.add_argument("rom",type=Path)
p.add_argument("edge",choices=("top","bottom"))
a=p.parse_args()
sym=symbols(a.rom.with_name(f"{a.edge}-video.sym"))
with Session([str(BIN),"HEADLESS",str(a.rom.resolve())],"key-color") as s:
    s.receive(monotonic()+30)
    for _ in range(24):
        s.command("STEP FRAME")
    values={0xb3:1,0x80:60,0x81:159,0x84:1,0x85:120,0x86:160,
            0xaf:1,0xb0:85,0xb1:153,0x90:0}
    values.update({0x91+i:v for i,v in enumerate((90,30,60,59,120,20,48,96,148,118))})
    for addr,v in values.items():
        s.command(f"POKE 0x{addr:04x} 0x{v:02x}")
    s.command("STEP FRAME")
    for _ in range(7):
        stop_at(s,sym["GlyphP1"])
        for _ in range(3):
            s.command("STEP INSTRUCTION")
        before=s.command("TV").decode().strip()
        cpu=s.command("CPU").decode().strip()
        prompt=s.last_prompt
        s.command("STEP INSTRUCTION")
        record("colup1",before=before,after=s.command("TV").decode().strip(),
               cpu=cpu,instruction=prompt.decode() if isinstance(prompt,bytes) else prompt)
        if "A=1a" in cpu or "A=1e" in cpu:
            break
    else:
        raise AssertionError("expected floor-key color store")
