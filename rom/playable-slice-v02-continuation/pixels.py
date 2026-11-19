"""Measure the project masks and wall geometry in unmodified Gopher screenshots."""
from pathlib import Path
import argparse
import json

from PIL import Image

ROOT=Path(__file__).resolve().parents[2]
PLAYER=(0x3c,0x7e,0x18,0x7e,0x1e,0x3c,0x18,0x24,0x42)
YELLOW=(255,255,41)
WHITE=(255,255,254)
BROWN=(199,107,33)


def picture(path,height=214):
    with Image.open(path) as image:
        return list(image.convert("RGB").resize((160,height),Image.Resampling.NEAREST).get_flattened_data())


def colored(data,rgb):
    return {(i%160,i//160) for i,p in enumerate(data) if p==rgb}


def expected_mask(rows,left,top):
    return {(left+x,top+y) for y,bits in enumerate(rows)
            for x in range(8) if bits & (128>>x)}


def masks_for_project():
    sprites=json.loads((ROOT/"design/NPC_REFERENCE_8x9_masks.json").read_text())["sprites"]
    return tuple(tuple(int(row,2) for row in sprites[name]) for name in (
        "large_male","large_male","large_female","small_male","small_female"))


def npc_pixels(path,npc_x,npc_y,life):
    white=colored(picture(path),WHITE)
    objects=[]
    all_expected=set()
    for index,(mask,x,y,status) in enumerate(zip(masks_for_project(),npc_x,npc_y,life)):
        if status!=255:
            continue
        expected=expected_mask(mask,x,y+15)
        all_expected.update(expected)
        objects.append({"index":index,"x":x,"y":y,"expected":len(expected),
                        "visible":len(white&expected)})
    return objects,len(white-all_expected)


def score(checks,directory):
    mapdata=json.loads((ROOT/"design/OPEN_ROOMS_V019_40x22_CANDIDATES.json").read_text())
    cells=next(m["grid"] for m in mapdata["maps"] if m["id"]=="A_OPEN_01")
    masks=masks_for_project()
    ideal_wall={(x,y+15) for y in range(176) for x in range(160) if cells[y//8][x//4]=="#"}
    for line in checks.read_text().splitlines():
        if not line.startswith("{"):
            continue
        row=json.loads(line)
        if row.get("event")!="check":
            continue
        data=picture(directory/f'{row["label"]}.png')
        white,yellow,brown=(colored(data,c) for c in (WHITE,YELLOW,BROWN))
        x,y,*_=row["state"]
        px=expected_mask(PLAYER,x,y+15)
        if row["state"][4]:
            px.add((row["state"][5],row["state"][6]+15))
        expected=set.union(set(),*(expected_mask(mask,x,y+15)
                    for mask,x,y,life in zip(masks,row["npc_x"],row["npc_y"],row["life"]) if life==255))
        # Room coordinates are anchored by the captured Gopher aperture and the
        # measured Room start SL44, not aligned independently for each actor.
        print(json.dumps(dict(label=row["label"],npc_expected=len(expected),npc_observed=len(white),
                              npc_missing=len(expected-white),npc_extra=len(white-expected),
                              player_and_shot_diff=len(px^yellow),wall_diff=len(ideal_wall^brown),
                              omitted=row["omitted"])))


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("log",type=Path)
    p.add_argument("images",type=Path)
    a=p.parse_args()
    score(a.log,a.images)
