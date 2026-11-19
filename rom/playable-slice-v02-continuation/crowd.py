"""Freeze deliberate coordinates in the playable ROM to measure tight sprite bands."""
import argparse
from pathlib import Path
from time import monotonic
import re

from capture import BIN, Session, record
from pixels import PLAYER, YELLOW, colored, expected_mask, npc_pixels, picture
from replay import FRAME, peek

CASES = (
    ("small-overlap-player-below", (24,159), (90,30,60,50,81), (153,45,60,82,86), None),
    ("small-same-y-player-below", (24,159), (90,30,60,50,81), (153,45,60,86,86), None),
    ("small-same-y-player-above", (52,55), (90,30,60,50,81), (153,38,42,86,86), None),
    ("all-five-same-y", (24,159), (20,44,68,92,116), (86,86,86,86,86), None),
    ("player-shares-band", (34,83), (90,30,60,50,81), (153,45,60,82,86), None),
    ("projectile-in-opposite-band", (52,55), (90,30,60,50,81), (153,38,42,86,86), (120,91)),
)


def run(rom, output):
    output.mkdir(parents=True,exist_ok=False)
    for label,player,nx,ny,shot in CASES:
        with Session([str(BIN),"HEADLESS",str(rom.resolve())],label) as s:
            s.receive(monotonic()+30)
            for _ in range(24):
                s.command("STEP FRAME")
            positions={0x80:player[0],0x81:player[1],0xB3:1,0x84:int(shot is not None)}
            positions.update({0x91+i:x for i,x in enumerate(nx)})
            positions.update({0x96+i:y for i,y in enumerate(ny)})
            if shot:
                positions.update({0x85:shot[0],0x86:shot[1]})
            for address,value in positions.items():
                s.command(f"POKE 0x{address:04x} 0x{value:02x}")
            for _ in range(4):
                s.command("STEP FRAME")
            image=output/f"{label}.png"
            s.command(f"SCREENSHOT {image}")
            objects,extra=npc_pixels(image,nx,ny,[255]*5)
            yellow=colored(picture(image),YELLOW)
            expected=expected_mask(PLAYER,player[0],player[1]+15)
            if shot:
                expected.add((shot[0],shot[1]+15))
            total=int(re.search(FRAME,s.command("TV FRAME"))[3])
            rendered,assist=peek(s,[0xec,0xf5])
            record("crowd",case=label,player=player,objects=objects,white_extra=extra,
                   yellow_missing=len(expected-yellow),yellow_extra=len(yellow-expected),
                   scanlines=total,rendered=rendered,assist=assist)


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("rom",type=Path)
    parser.add_argument("output",type=Path)
    args=parser.parse_args()
    run(args.rom,args.output)
