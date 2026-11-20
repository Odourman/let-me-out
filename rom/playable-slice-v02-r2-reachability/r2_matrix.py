"""Capture consecutive frames and account for the shared yellow color by geometry."""
import argparse
import json
from itertools import product
from pathlib import Path
from time import monotonic

from audit import GOLD, KEY
from capture import BIN, Session, record
from aperture_audit import native_picture, TV
from pixels import ROOT, PLAYER, WHITE, YELLOW, colored, expected_mask, masks_for_project
from replay import peek

p = argparse.ArgumentParser()
p.add_argument("rom", type=Path)
p.add_argument("out", type=Path)
p.add_argument("on", type=int, choices=(0, 6, 8))
a = p.parse_args()
a.out.mkdir(parents=True)
grid=next(m["grid"] for m in json.loads(
    (ROOT/"design/OPEN_ROOMS_V019_40x22_CANDIDATES.json").read_text())["maps"]
          if m["id"]=="A_OPEN_01")
def legal(x,y):
    return all(grid[yy//8][xx//4]=="." for yy in (y,y+8) for xx in (x,x+4,x+7))
def overlap(a,b):
    return abs(a[0]-b[0])<8 and abs(a[1]-b[1])<9
cases = (*product(range(5),((24,151,False),(60,151,False),(60,159,False))),
         (4,(60,159,True)),(4,(104,151,False)))
with Session([str(BIN), "HEADLESS", str(a.rom.resolve())], "r2-fixture", session_limit=900) as s:
    s.receive(monotonic()+30)
    for _ in range(24):
        s.command("STEP FRAME")
    for carrier,(px,py,shot) in cases:
        values = {0xb3:1,0x80:px,0x81:py,0x84:int(shot),0x85:120,0x86:160,
                  0xaf:1,0xb0:85,0xb1:153,0xae:carrier,0x88:1,0x90:10 if a.on else 254}
        pos=[(90,20),(24,48),(60,96),(59,148),(116,120)]
        pos[carrier]=(85,153)
        life=[0 if i==carrier else 255 for i in range(5)]
        nx,ny=zip(*pos)
        alive=[pt for i,pt in enumerate(pos) if life[i]]
        assert all(legal(*pt) for pt in ((px,py),*pos))
        assert not any(overlap(pt,(px,py)) for pt in alive if pt!=(59,148))
        assert not any(overlap(pt,other) for i,pt in enumerate(alive) for other in alive[i+1:])
        # A player already touching a living hunter would immediately lose a life.
        # Preserve that historical case separately and add a legal near-Y SM.
        domain="CONSISTENT_SEEDED"
        if any(overlap(pt,(px,py)) for pt in alive):
            # Keep SM on the key band, but safely left of the player's hitbox.
            pos[3]=(px-9,148)
            assert legal(*pos[3]) and not any(overlap(pos[3],pt) for i,pt in enumerate(pos) if i!=3 and life[i])
            nx,ny=zip(*pos)
        values.update({0xa0+i:v for i,v in enumerate(life)})
        values.update({0x91+i:v for i,v in enumerate((*nx,*ny))})
        for addr,v in values.items():
            s.command(f"POKE 0x{addr:04x} 0x{v:02x}")
        mask=expected_mask(KEY,85,168)
        player=expected_mask(PLAYER,px,py+15)
        missile={(120,175)} if shot else set()
        for n in range(13):
            clock=peek(s,[0x90])[0]
            s.command("STEP FRAME")
            new_clock,state,rendered=peek(s,[0x90,0xaf,0xec])
            assert state in (1, 0x81)
            top,bottom,total=map(int,TV.fullmatch(s.command("TV FRAME").decode()).groups())
            name=f"carrier{carrier}-{px}-{py}-{int(shot)}-{n:02}.png"
            target=a.out/name
            s.command(f"SCREENSHOT {target}")
            if n==0:  # initial raster still carries pre-fixture state
                continue
            rgb=native_picture(target,(top,bottom))
            yellow=colored(rgb,YELLOW)
            key_color=yellow if a.on else colored(rgb,GOLD)
            box={xy for xy in key_color if 85<=xy[0]<93 and 168<=xy[1]<177}
            white=colored(rgb,WHITE)
            masks=masks_for_project()
            expected={i:expected_mask(masks[i],nx[i],ny[i]+15) for i,v in enumerate(life) if v}
            objects=[dict(index=i,visible=len(p&white),expected=len(p)) for i,p in expected.items()]
            white_extra=len(white-set().union(*expected.values()))
            phase=clock%12 if a.on else clock
            record("blink",domain=domain,carrier=carrier,nx=nx,ny=ny,life=life,px=px,py=py,shot=shot,n=n,clock=clock,next_clock=new_clock,
                   phase=phase,wanted=not a.on or phase<a.on,key=len(box&mask),
                   key_extra=len(box-mask),player_missing=len(player-yellow),
                   yellow_extra=len(yellow-player-missile-(mask if a.on else set())),
                   shot_pixels=len(missile&yellow),objects=objects,white_extra=white_extra,
                   queued=bool(rendered&32),scanlines=total,png=name)
