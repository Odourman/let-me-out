"""Exact raster-row oracle for the isolated proof ROMs."""
import argparse
import json
from pathlib import Path
from pixels import expected_mask

p=argparse.ArgumentParser()
p.add_argument("log",type=Path)
p.add_argument("player",type=int)
p.add_argument("sm",type=int)
p.add_argument("shot",type=int)
a=p.parse_args()
row=next(r for line in a.log.open() if (r:=json.loads(line))["event"]=="raster")
player=expected_mask((0x7e,0x1e,0x3c,0x18,0x24),a.player,40)
key=expected_mask((0x70,0x50,0x7e,0x24,0x04),85,40)
sm=expected_mask((0x7e,0x18,0x24,0,0),a.sm,40)
shot={(a.shot,42)}
walls={(x,y) for x in (*range(4),*range(156,160)) for y in range(40,45)}
yellow=set(map(tuple,row["yellow"]))
white=set(map(tuple,row["white"]))
brown=set(map(tuple,row["brown_band"]))
print(json.dumps(dict(key=len(key&yellow),player=len(player&yellow),
    shot=len(shot&yellow),sm=len(sm&white),brown=len(walls&brown),
    extra_yellow=sorted(yellow-player-key-shot),extra_white=sorted(white-sm),
    extra_brown=sorted(brown-walls),scanlines=row["lines"],mapper=row["mapper"])))
assert yellow==player|key|shot and white==sm and brown==walls and row["lines"]==262 and row["mapper"]=="F6"
