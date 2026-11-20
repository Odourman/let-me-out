"""Compare the five illuminated rows against the actual ROM map and masks."""
import argparse
import json
from pathlib import Path
from pixels import expected_mask

p=argparse.ArgumentParser()
p.add_argument("directory",type=Path)
a=p.parse_args()
plan=json.loads((a.directory/"plan.json").read_text())
o=plan["options"]
row=next(r for line in (a.directory/"raw.jsonl").open() if (r:=json.loads(line))["event"]=="raster")
player=expected_mask(plan["player"],o["player"],40)
sm=expected_mask(plan["sm"],o["sm_x"],40)
key=expected_mask(plan["key"],o["key_x"],40)
shot={(o["shot_x"],42)} if o["shot"] else set()
walls=set()
for i,(p0,p1,p2) in enumerate(plan["pf"][:5]):
    bits=[bool(value&(1<<b)) for value,order in ((p0,range(4,8)),(p1,range(7,-1,-1)),(p2,range(8))) for b in order]
    walls.update((x,40+i) for x in range(160) if bits[min(x,159-x)//4])
yellow=set(map(tuple,row["yellow"]))
white=set(map(tuple,row["white"]))
brown=set(map(tuple,row["brown_band"]))
result=dict(key=[len(key&yellow),len(key)],player=[len(player&yellow),len(player)],
            sm=[len(sm&white),len(sm)],shot=[len(shot&yellow),len(shot)],
            pf=[len(walls&brown),len(walls)],extra_yellow=len(yellow-player-key-shot),
            extra_white=len(white-sm),extra_brown=len(brown-walls),lines=row["lines"])
print(json.dumps(result))
