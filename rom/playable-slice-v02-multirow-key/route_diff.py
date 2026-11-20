"""Replay exactly the joystick and frame-step stream from the frozen TOP lure."""
import argparse
import json
from pathlib import Path
from time import monotonic

from capture import BIN, Session, record
from phase import stop_at, symbols
from aperture_audit import TV
from replay import peek

p=argparse.ArgumentParser()
p.add_argument("rom",type=Path)
p.add_argument("input_log",type=Path)
p.add_argument("--trace",action="store_true")
a=p.parse_args()
with Session([str(BIN),"HEADLESS",str(a.rom.resolve())],"top-lure-input-replay",session_limit=600) as s:
    s.receive(monotonic()+30)
    frame=0
    for line in a.input_log.open():
        row=json.loads(line)
        if row["event"]!="tx":
            continue
        command=bytes.fromhex(row["hex"]).decode().rstrip("\x04")
        if not (command.startswith("STICK LEFT ") or command=="STEP FRAME"):
            continue
        if a.trace and frame==386 and command=="STEP FRAME":
            v=symbols(a.rom.with_name("top-video.sym"))
            for label in ("BlankWait","GameBank","VideoBank","Overscan"):
                tv=stop_at(s,v[label])
                record("boundary",label=label,beam=tv,cpu=s.command("CPU").decode(),
                       timer=s.command("RIOT TIMER").decode(),tia=s.command("TIA").decode(),
                       ram=peek(s,range(0x80,0xb4)))
            for _ in range(4):
                old=s.last_prompt
                before=s.command("TV").decode()
                s.command("STEP INSTRUCTION")
                record("overscan_instruction",op=old,before=before,
                       after=s.command("TV").decode(),cpu=s.command("CPU").decode(),
                       timer=s.command("RIOT TIMER").decode())
            break
        s.command(command)
        if command=="STEP FRAME":
            frame+=1
            tv=s.command("TV FRAME").decode()
            top,bottom,lines=map(int,TV.fullmatch(tv).groups())
            if frame>=24 and lines!=262:
                record("first_bad",frame=frame, aperture=[top,bottom],scanlines=lines,
                       beam=s.command("TV").decode(),cpu=s.command("CPU").decode(),
                       tia=s.command("TIA").decode(),timer=s.command("RIOT TIMER").decode(),
                       ram=peek(s,range(0x80,0xb4)))
                break
    else:
        record("route_pass",frame=frame)
