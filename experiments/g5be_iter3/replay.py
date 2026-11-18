"""Exercise independent coordinate writes against one resident F6 binary."""
import argparse
import re
import time
from pathlib import Path

from capture import BIN, Session, expect, record

VERSION = rb"v0\.57\.2\n2af86eb725739adbf3d9d45cea2ed69eea57da2a\n"
FRAME = rb"top: (\d+), bottom: (\d+), total: (\d+)\n"
TV = rb"FR=(\d+) SL=(\d+) CL=(-?\d+)\n"

X = (127,19,73,100,46)
Y = (73,72,73,71,72)
SCENES = tuple((f"third-x{x}", (127,19,x,100,46), Y, True) for x in (73,67,76,82,64))
EXTENDED = (
    ("right-m-left", (124,19,67,100,46), Y, True),
    ("left-m-right", (127,22,67,100,46), Y, True),
    ("sf-left", (127,19,67,100,43), Y, True),
    ("sm-left", (127,19,67,97,46), Y, True),
    ("sm-right", (127,19,76,103,46), Y, True),
    ("five-new-xs", (130,22,70,103,43), Y, True),
    ("band-up", (127,19,67,100,46), (69,68,69,67,68), True),
    ("band-down", (127,19,76,100,46), (78,77,78,76,77), True),
    ("vertical-spread", (127,19,67,100,46), (74,68,83,71,76), True),
)


def set_scene(session, xs, ys):
    addresses = range(0x81, 0x8b)
    values = list(xs)+list(ys)
    for address, value in zip(addresses,values):
        session.command(f"POKE 0x{address:04x} 0x{value:02x}")
    reply = session.command("PEEK "+" ".join(f"0x{a:04x}" for a in addresses))
    assert [int(v,16) for v in re.findall(rb" = 0x([0-9a-f]+)",reply)] == values


def replay(rom, out, group):
    if group == "legacy":
        from legacy_stimuli import soak, seeded
        scenes = [(n,x,y,True) for n,x,y,_ in [*soak(),*seeded()][:20]]
        block = 3
    elif group == "soak":
        scenes = [SCENES[0], SCENES[1], SCENES[2], EXTENDED[6], EXTENDED[7], SCENES[1]]
        block = 100
    elif group == "extended":
        scenes, block = EXTENDED, 4
    else:
        scenes, block = (*SCENES, SCENES[0], SCENES[2], SCENES[1]), 4
    out.mkdir(parents=True, exist_ok=False)
    with Session([str(BIN), "HEADLESS", str(rom.resolve())], "g5be3") as s:
        s.receive(time.monotonic()+15)
        expect(s, "VERSION REVISION", VERSION)
        expect(s, "CARTRIDGE MAPPER", rb"F6\n")
        # Gopher's automatic screenshot aperture needs a few boot frames to settle.
        for i in range(20):
            s.command("STEP FRAME")
            top,bottom,total = map(int,expect(s,"TV FRAME",FRAME).groups())
            record("warmup", i=i, top=top,bottom=bottom,scanlines=total)
        previous = None
        for mode, (label,x,y,_) in enumerate(scenes):
            set_scene(s,x,y)
            record("switch", mode=mode, label=label, x=x, y=y)
            for i in range(block):
                s.command("STEP FRAME")
                frame = int(expect(s, "TV", TV)[1])
                assert previous is None or frame == previous+1
                previous = frame
                top,bottom,total = map(int,expect(s,"TV FRAME",FRAME).groups())
                path = out/f"frame_{frame:04d}.png"
                expect(s,f"SCREENSHOT {path}",rb"saving screenshot\n")
                record("raster", mode=mode, label=label, x=x, y=y, admitted=True, dynamic=True,
                       transition=i==0, frame=frame, top=top,bottom=bottom,scanlines=total,path=path.name)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("rom",type=Path)
    p.add_argument("images",type=Path)
    p.add_argument("--group",choices=("third","extended","legacy","soak"),default="third")
    a = p.parse_args()
    replay(a.rom,a.images.resolve(),a.group)
