"""Offline comparison of unmodified Stella and Gopher snapshots."""
from collections import Counter
import json
from pathlib import Path
import sys
from PIL import Image

from pixels import BITS, measure, raw_grid, white, yellow


def stella(directory):
    plans = json.loads(Path("clean1/schedule.json").read_text())
    for path in sorted(directory.glob("*.png")):
        matches = sorted(
            (m["union_missing"]+m["union_extra"], p["scene"]["name"], m)
            for p in plans if (m := measure(path,228,p["scene"]))
        )
        _, name, data = matches[0]
        print(path.name,name,data["union_missing"],data["union_extra"],
              data["mask_missing"],"P0/M0/PF",data["player_pixels"],data["shot_pixels"],data["wall_pixels"])


def r2(mode, directory):
    plan = json.loads(Path(mode,"schedule.json").read_text())[0]["scene"]
    gold = (0x38,0x44,0x44,0x38,0x10,0x1c,0x10,0x18,0)
    key_bits = {(x,y) for y,byte in enumerate(gold) for x in range(8) if byte & (0x80>>x)}
    all_results = Counter()
    for path in sorted(directory.glob("*.png")):
        with Image.open(path) as image:
            height = image.height if image.width == 320 else 214
        grid = raw_grid(path,height)
        white_pixels={(i%160,i//160) for i,v in enumerate(grid) if white(v)}
        yellow_pixels={(i%160,i//160) for i,v in enumerate(grid) if yellow(v)}
        first=min(y for x,y in yellow_pixels if x<20)
        p0 = {(x,y) for x,y in yellow_pixels if x<20}
        m0 = {(x,y) for x,y in yellow_pixels if 20<=x<24}
        four=set.union(*[{(3*c-47+x,first+y) for x,y in BITS[i]}
                        for i,c in enumerate(plan["x_cycles"][:4])])
        key = {(145+x,first+y) for x,y in key_bits}
        gold_color = grid[next(y*160+x for x,y in sorted(key))]
        observed_gold = {(i%160,i//160) for i,v in enumerate(grid) if v==gold_color}
        door_outer=[grid[(first+y)*160+159] for y in range(9)]
        door_inner=[grid[(first+y)*160+152] for y in range(9)]
        colors=Counter(grid)
        result=(len(four-white_pixels),len(white_pixels-four),len(key-observed_gold),
                len(observed_gold-key),gold_color,len(p0),len(m0),
                tuple(door_outer),tuple(door_inner))
        all_results[result]+=1
        print(path.name,"NPC miss/extra",result[:2],"key miss/extra/RGB",result[2:5],
              "P0/M0",result[5:7],"door columns",result[7:],"palette",colors.most_common(7))
    print("unique measured summaries",len(all_results),"frame count",sum(all_results.values()))


if __name__=="__main__":
    if sys.argv[1]=="stella":
        stella(Path(sys.argv[2]))
    else:
        r2(sys.argv[1],Path(sys.argv[2]))
