"""Compare unmodified emulator screenshots to the approved masks at scheduled coordinates."""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import re

from PIL import Image

TYPES = ("large_male", "large_male", "large_female", "small_male", "small_female")
MASKS = json.loads(Path("masks.json").read_text())["sprites"]
BITS = [set((x,y) for y,row in enumerate(MASKS[key]) for x,bit in enumerate(row) if bit=="1")
        for key in TYPES]
RECORD = re.compile(r"top: (\d+), bottom: (\d+), total: (\d+)")


def white(color):
    return min(color) > 180 and max(color)-min(color) < 40


def yellow(color):
    r, g, b = color
    return r > 200 and g > 200 and b < 100


def raw_grid(path, height):
    with Image.open(path) as image:
        scaled = image.convert("RGB").resize((160, height),Image.Resampling.NEAREST)
        return list(scaled.get_flattened_data())


def positions(scene, y_base):
    return [{(3*cycle-47+x,y_base+start+y) for x,y in mask}
            for cycle,start,mask in zip(scene["x_cycles"], scene["y"], BITS)]


def measure(path, height, scene):
    pixels = raw_grid(path,height)
    observed = {(i%160,i//160) for i,color in enumerate(pixels) if white(color)}
    yolk = {(i%160,i//160) for i,color in enumerate(pixels) if yellow(color)}
    # Packed P0 is left of x=24, with M0 far to the right. Its first visible
    # mask row is row 72 of the declared kernel. This anchors display cropping
    # independently of the NPC pixels and works for both emulator formats.
    player = {(x,y) for x,y in yolk if x<24}
    shot = {(x,y) for x,y in yolk if x>130}
    if not player:
        raise ValueError("P0 raster landmark missing")
    y_base = min(y for x,y in player)-72
    masks = positions(scene,y_base)
    union = set.union(*masks)
    misses = [len(mask-observed) for mask in masks]
    unique_hits, unique_total = [], []
    for i, mask in enumerate(masks):
        unique = mask-set.union(*(masks[j] for j in range(5) if j!=i))
        unique_hits.append(len(unique&observed))
        unique_total.append(len(unique))
    walls = sum(r>100 and r>1.3*g and g>1.4*b for r,g,b in pixels)
    return {
        "y_base":y_base,"white_pixels":len(observed),"union_missing":len(union-observed),
        "union_extra":len(observed-union),"extra_coordinates":sorted(observed-union),
        "mask_missing":misses,"unique_hits":unique_hits,"unique_total":unique_total,
        "player_pixels":len(player),"shot_pixels":len(shot),"wall_pixels":walls,
    }


def analyze(log, images, schedule, contrasts):
    events = [json.loads(row) for row in log.read_text().splitlines()]
    cache, result = {}, []
    for event in events:
        if event["event"] != "image":
            continue
        top,bottom,total = map(int,RECORD.fullmatch(event["timing"]).groups())
        f = event["frame"]
        index = ((f-2)//(4 if contrasts else 16)) % len(schedule)
        scene = schedule[index]["scene"]
        path = images/event["file"]
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        key = digest,index
        if key not in cache:
            cache[key] = measure(path,bottom-top+1,scene)
        result.append({"frame":f,"scanlines":total,"scene":scene["name"],"sha256":digest,**cache[key]})
    return result


def summarize(records):
    grouped = defaultdict(list)
    for row in records:
        grouped[row["scene"]].append(row)
    for scene, group in grouped.items():
        first = group[0]
        print(scene, len(group), "scanline_hist",dict(Counter(r["scanlines"] for r in group)),
              "exact_frames",sum(not(r["union_missing"] or r["union_extra"]) for r in group),
              "first_frame",first["frame"],"missing",first["union_missing"],"extra",first["union_extra"],
              "mask_missing",first["mask_missing"],"unique_hits",first["unique_hits"],
              "unique_total",first["unique_total"],"extra_at",first["extra_coordinates"],
              "P0/M0/PF",first["player_pixels"],first["shot_pixels"],first["wall_pixels"])
    for i in range(5):
        counts = Counter()
        streak = max_streak = 0
        for row in records:
            if not row["unique_total"][i]:
                streak=0
                counts["ambiguous"]+=1
            elif row["unique_hits"][i]:
                streak=0
                counts["visible_unique"]+=1
            else:
                streak+=1
                max_streak=max(streak,max_streak)
                counts["absent_unique"]+=1
            if not row["mask_missing"][i]:
                counts["all_expected_bits_present"]+=1
        print("NPC", i, dict(counts), "max_consecutive_no_unique",max_streak)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("log",type=Path)
    p.add_argument("images",type=Path)
    p.add_argument("schedule",type=Path)
    p.add_argument("output",type=Path)
    p.add_argument("--contrasts",action="store_true")
    args=p.parse_args()
    rows=analyze(args.log,args.images,json.loads(args.schedule.read_text()),args.contrasts)
    args.output.write_text("".join(json.dumps(row)+"\n" for row in rows))
    summarize(rows)
