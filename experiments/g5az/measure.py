"""Pixel oracle on raw Gopher PNGs. Expected mask geometry comes from RAM values."""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path

from PIL import Image

TYPES = ("large_male","large_male","large_female","small_male","small_female")
MASKS = json.loads(Path("masks.json").read_text())["sprites"]
BITS = [{(x,y) for y,row in enumerate(MASKS[t]) for x,bit in enumerate(row) if bit=="1"} for t in TYPES]
PLAYER = {(x,y) for y,b in enumerate((0x3c,0x7e,0x18,0x7e,0x1e,0x3c,0x18,0x24,0x42))
          for x in range(8) if b & (0x80>>x)}


def measure(pixels, xs, ys, ids):
    white = {(i%160,i//160) for i,c in enumerate(pixels) if min(c)>180 and max(c)-min(c)<40}
    yellow = {(i%160,i//160) for i,(r,g,b) in enumerate(pixels) if r>200 and g>200 and b<100}
    # Identify the fixed player position using its complete mask, independently
    # of NPC positions and without allowing per-NPC registration.
    top = min(y for x,y in yellow if 8<=x<18)
    player_candidates = [{(x+left,y+top) for x,y in PLAYER} for left in range(8,11)]
    player = max(player_candidates,key=lambda p:len(p&yellow))
    y_base = top-72
    parts = [{(left+x, y_base+high+y) for x,y in shape}
             for left,high,shape in zip(xs,ys,BITS)]
    selected = [parts[i] for i in ids]
    union = set.union(*selected)
    unique = [parts[i] - set.union(*(parts[j] for j in range(5) if j!=i)) for i in range(5)]
    wall = sum(r>100 and r>1.3*g and g>1.4*b for r,g,b in pixels)
    return dict(y_base=y_base, missing=len(union-white),extra=len(white-union),
                union_pixels=len(union), missing_by_actor=[len(p-white) for p in parts],
                unique_total=[len(p) for p in unique],
                unique_seen=[len(p&white) for p in unique],
                extra_xy=sorted(white-union), p0=len(player&yellow), m0=len(yellow-player),
                pf=wall)


def pixels(path, height):
    with Image.open(path) as image:
        return list(image.convert("RGB").resize((160,height), Image.Resampling.NEAREST).get_flattened_data())


def analyze(mode, log, directory):
    cached, rows = {}, []
    for line in log.read_text().splitlines():
        event = json.loads(line)
        if event["event"]!="raster":
            continue
        ids = [0] if mode in ("one","single") else [(event["rotate_next"]-1)%5] if mode in ("rotate","rotatefine") else list(range(5))
        path = directory/event["path"]
        digest=hashlib.sha256(path.read_bytes()).hexdigest()
        key=(digest,tuple(event["x"]),tuple(event["y"]),tuple(ids))
        if key not in cached:
            cached[key]=measure(pixels(path,event["bottom"]-event["top"]+1),event["x"],event["y"],ids)
        rows.append({**event,**cached[key],"sha256":digest,"expected_ids":ids})
    return rows


def summary(rows):
    groups = defaultdict(list)
    for row in rows:
        groups[row["label"]].append(row)
    for label, group in groups.items():
        first=group[0]
        print(label,len(group),"exact",sum(not(r["missing"] or r["extra"]) for r in group),
              "scanlines",dict(Counter(r["scanlines"] for r in group)),
              "pixel_error_hist",dict(Counter((r["missing"],r["extra"]) for r in group)),
              "unique_missing_first",[t-s for t,s in zip(first["unique_total"],first["unique_seen"])],
              "misses_first",first.get("planner_misses_previous"),"p0/m0/pf_hist",
              dict(Counter((r["p0"],r["m0"],r["pf"]) for r in group)))
    for i in range(5):
        counts=Counter()
        consecutive=longest=0
        for r in rows:
            if r["unique_seen"][i]:
                counts["visible"]+=1
                consecutive=0
            elif not r["unique_total"][i]:
                counts["ambiguous"]+=1
                consecutive=0
            else:
                counts["absent"]+=1
                consecutive+=1
                longest=max(longest,consecutive)
        print(f"NPC{i} unique pixels",dict(counts),"longest wholly absent",longest)


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("mode")
    for key in ("log","images","output"):
        p.add_argument(key,type=Path)
    a=p.parse_args()
    rows=analyze(a.mode,a.log,a.images)
    a.output.write_text("".join(json.dumps(r)+"\n" for r in rows))
    summary(rows)
