"""Capture consecutive frames and account for the shared yellow color by geometry."""
import argparse
from pathlib import Path
import re
from time import monotonic

from audit import GOLD, KEY
from capture import BIN, Session, record
from pixels import PLAYER, WHITE, YELLOW, colored, expected_mask, npc_pixels, picture
from replay import FRAME, peek

p = argparse.ArgumentParser()
p.add_argument("rom", type=Path)
p.add_argument("out", type=Path)
p.add_argument("on", type=int, choices=(0, 6, 8))
p.add_argument("--shot-only",action="store_true")
a = p.parse_args()
a.out.mkdir(parents=True)
cases = ((24,151,False),(60,151,False),(60,159,False),(60,159,True))
for px, py, shot in (cases[-1:] if a.shot_only else cases):
    with Session([str(BIN), "HEADLESS", str(a.rom.resolve())], "blink-fixture") as s:
        s.receive(monotonic()+30)
        for _ in range(24):
            s.command("STEP FRAME")
        values = {0xb3:1,0x80:px,0x81:py,0x84:int(shot),0x85:120,0x86:160,
                  0xaf:1,0xb0:85,0xb1:153,0x90:10 if a.on else 254}
        nx,ny=(90,30,60,59,120),(20,48,96,148,118)
        values.update({0x91+i:v for i,v in enumerate((*nx,*ny))})
        for addr,v in values.items():
            s.command(f"POKE 0x{addr:04x} 0x{v:02x}")
        mask=expected_mask(KEY,85,168)
        player=expected_mask(PLAYER,px,py+15)
        missile={(120,175)} if shot else set()
        for n in range(27):
            clock=peek(s,[0x90])[0]
            s.command("STEP FRAME")
            new_clock,state,rendered=peek(s,[0x90,0xaf,0xec])
            assert state in (1, 0x81)
            total=int(re.search(FRAME,s.command("TV FRAME"))[3])
            name=f"{px}-{py}-{int(shot)}-{n:02}.png"
            target=a.out/name
            s.command(f"SCREENSHOT {target}")
            if n==0:  # initial raster still carries pre-fixture state
                continue
            rgb=picture(target)
            yellow=colored(rgb,YELLOW)
            key_color=yellow if a.on else colored(rgb,GOLD)
            box={xy for xy in key_color if 85<=xy[0]<93 and 168<=xy[1]<177}
            objects,white_extra=npc_pixels(target,nx,ny,[255]*5)
            phase=clock%12 if a.on else clock
            record("blink",px=px,py=py,shot=shot,n=n,clock=clock,next_clock=new_clock,
                   phase=phase,wanted=not a.on or phase<a.on,key=len(box&mask),
                   key_extra=len(box-mask),player_missing=len(player-yellow),
                   yellow_extra=len(yellow-player-missile-(mask if a.on else set())),
                   shot_pixels=len(missile&yellow),objects=objects,white_extra=white_extra,
                   queued=bool(rendered&32),scanlines=total,png=name)
