"""Instruction/beam trace of one actual key-band room scanline."""
import argparse
from pathlib import Path
from time import monotonic

from capture import BIN, Session, record
from phase import stop_at, symbols
from replay import peek

p=argparse.ArgumentParser()
p.add_argument("rom",type=Path)
p.add_argument("px",type=int,choices=(24,60,104))
a=p.parse_args()
syms=symbols(a.rom.with_name("top-video.sym"))
with Session([str(BIN),"HEADLESS",str(a.rom.resolve())],"r2-key-band") as s:
    s.receive(monotonic()+30)
    for _ in range(24):
        s.command("STEP FRAME")
    values={0xb3:1,0x80:a.px,0x81:151,0x84:0,0x90:0,0xaf:1,0xae:4,0xb0:85,0xb1:153,
            0xa0:255,0xa1:255,0xa2:255,0xa3:255,0xa4:0}
    values.update({0x91+i:v for i,v in enumerate((90,24,60,51 if a.px==60 else 59,85,20,48,96,148,153))})
    for addr,val in values.items():
        s.command(f"POKE 0x{addr:04x} 0x{val:02x}")
    s.command("STEP FRAME")
    addr=syms["RoomSprites"]
    s.command(f"BREAK PC 0x{addr}")
    for _ in range(360):
        s.command("RUN")
        cpu=s.command("CPU").decode().strip()
        if "Y=ea" in cpu:
            break
    else:
        raise AssertionError("target room row did not enter the ordinary raster path")
    s.command("DROP BREAK 0")
    record("objects",px=a.px,p0=s.command("PLAYER 0").decode(),p1=s.command("PLAYER 1").decode())
    for _ in range(34):
        before=s.command("TV").decode().strip()
        op=s.last_prompt
        cpu=s.command("CPU").decode().strip()
        reply=s.command("STEP INSTRUCTION").decode().strip()
        after=s.command("TV").decode().strip()
        record("raster_instruction",px=a.px,before=before,after=after,op=op,cpu=cpu,reply=reply)
        if f"$"+syms["NextRoom"] in op:
            break
