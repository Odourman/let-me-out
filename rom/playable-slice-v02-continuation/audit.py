"""Summarize actual Gopher frames, scheduler eligibility and native PNG pixels."""
import argparse
from collections import Counter
import json
from pathlib import Path

from pixels import BROWN, ROOT, colored, expected_mask, picture

ORANGE = (255, 185, 86)
DARK = (6, 6, 6)
GOLD = (255, 255, 47)
KEY = (0, 0x70, 0x50, 0x7e, 0x24, 0x04, 0, 0, 0)


def events(path, event):
    return [row for line in path.open() if (row:=json.loads(line))["event"]==event]


def soak(folder):
    entries=events(folder/"soak.jsonl","soak")
    assert len(entries)==600 and [r["n"] for r in entries]==list(range(600))
    numbers=[int(row["tv"].split()[0].split("=")[1]) for row in entries]
    assert numbers==list(range(numbers[0],numbers[0]+600))
    report={}
    for i,name in enumerate(("M (0)","M (1)","F","SM","SF","key")):
        bit=1<<i
        eligible=queued=run=longest=0
        for row in entries:
            active=bool(row["eligible"]&bit)
            included=bool(row["rendered"]&bit)
            eligible+=active
            queued+=included
            run=run+1 if active and not included else 0
            longest=max(run,longest)
        report[name]={"eligible":eligible,"queued":queued,"omitted":eligible-queued,
                      "longest_omission_streak":longest}
    assert all(row["omitted"]==(row["eligible"]&~row["rendered"]).bit_count() for row in entries)
    return {"scanlines":dict(Counter(r["scanlines"] for r in entries)),
            "omissions":dict(Counter(r["omitted"] for r in entries)), "objects":report}


def visibility(folder):
    samples=events(folder/"soak.jsonl","soak_pixels")
    assert [sample["n"] for sample in samples]==list(range(600))
    actors={}
    for index,name in enumerate(("M (0)","M (1)","F","SM","SF")):
        counts=Counter()
        run=longest=0
        for frame in samples:
            obj=next((o for o in frame["objects"] if o["index"]==index),None)
            if obj is None:
                counts["inactive"]+=1
            elif obj["visible"]==0:
                counts["absent"]+=1
            elif obj["visible"]==obj["expected"]:
                counts["complete"]+=1
            else:
                counts["partial"]+=1
            run=run+1 if obj is not None and obj["visible"]==0 else 0
            longest=max(run,longest)
        actors[name]=dict(counts,longest_pixel_absence=longest)
    return {"frames":len(samples),"frames_with_extra_white":sum(r["unattributed_white"]>0 for r in samples),
            "actors":actors}


def key_lifetime(folder):
    floor=[r for r in events(folder/"unseeded.jsonl","key_lifetime") if r["state"]==1]
    return {"floor_frames":len(floor),"exact":sum(r["key_pixels"]==14 and r["extra"]==0 for r in floor),
            "no_pixels":sum(r["key_pixels"]==0 for r in floor)}


def graphics(folder):
    data=json.loads((ROOT/"design/OPEN_ROOMS_V019_40x22_CANDIDATES.json").read_text())
    grid=next(m["grid"] for m in data["maps"] if m["id"]=="A_OPEN_01")
    walls={(x,y+15) for y in range(176) for x in range(160) if grid[y//8][x//4]=="#"}
    images={
        "quiet":"calibration/P1-64.png",
        "closed":"door-locked/door-without-key.png",
        "open-before-passage":"door-held-open/open-before-passage.png",
        "open-during-exit":"unseeded/unseeded-exit.png",
        "controlled-key":"key-door/key-on-floor.png",
        "cold-key":"unseeded/unseeded-key-floor.png",
    }
    result={}
    for label,image in images.items():
        pixels=picture(folder/image)
        brown=colored(pixels,BROWN)
        right=[pixels[y*160+x] for y in range(87,119) for x in range(156,160)]
        left=[pixels[y*160+x] for y in range(87,119) for x in range(4)]
        result[label]={"wall_missing":len(walls-brown),"wall_extra":len(brown-walls),
                       "right_orange":right.count(ORANGE),"right_dark":right.count(DARK),
                       "left_brown":left.count(BROWN)}
        if label in {"controlled-key","cold-key"}:
            x,y=(79,60) if label=="controlled-key" else (85,153)
            oracle=expected_mask(KEY,x,y+15)
            gold=colored(pixels,GOLD)
            result[label].update(key_expected=len(oracle),key_correct=len(gold&oracle),
                                 key_missing=len(oracle-gold),key_extra=len(gold-oracle))
    return {"expected_brown_excluding_door":len(walls),"images":result}


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("folder",type=Path)
    args=parser.parse_args()
    print(json.dumps({"soak":soak(args.folder),"visibility":visibility(args.folder),
                      "key_lifetime":key_lifetime(args.folder),"graphics":graphics(args.folder)},indent=2))
