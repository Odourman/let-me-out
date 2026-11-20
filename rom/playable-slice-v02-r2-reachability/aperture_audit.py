"""Score native screenshots in beam coordinates using the logged TV aperture."""
import argparse
import json
from pathlib import Path
import re

from PIL import Image

from audit import KEY, GOLD
from pixels import WHITE, YELLOW, PLAYER, colored, expected_mask, masks_for_project

TV = re.compile(r"top: (\d+), bottom: (\d+), total: (\d+)\n")
ORIGIN = 29
HEIGHT = 214
BLACK = (6,6,6)


def native_picture(path, bounds):
    """Anchor output coordinates to physical line 29, rather than stretch Y."""
    top, bottom = bounds
    with Image.open(path) as image:
        pixels = list(image.convert("RGB").resize(
            (160, bottom-top+1), Image.Resampling.NEAREST).get_flattened_data())
    out = [BLACK]*(160*HEIGHT)
    start, end = max(top, ORIGIN), min(bottom+1, ORIGIN+HEIGHT)
    out[(start-ORIGIN)*160:(end-ORIGIN)*160] = pixels[(start-top)*160:(end-top)*160]
    return out


def rescore(log, images, mode):
    masks = masks_for_project()
    aperture = None
    apertures = {}
    next_path = ""
    key_x, key_y = 85, 153
    summary = []
    for line in log.open():
        row = json.loads(line)
        event = row["event"]
        if event=="tx":
            command = bytes.fromhex(row["hex"]).decode("ascii").rstrip("\x04")
            if command.startswith("SCREENSHOT "):
                next_path = Path(command.removeprefix("SCREENSHOT ")).name
        elif event=="ack":
            answer = row["answer"]
            if match:=TV.fullmatch(answer):
                aperture = (int(match[1]),int(match[2]))
            if answer=="saving screenshot\n" and aperture is not None:
                apertures[next_path] = aperture
        elif event=="check" and row["label"]=="key-floor":
            key_x,key_y = row["key_position"]
        elif event in ("blink","cold_blink","soak_pixels"):
            name= row.get("png") or f"frame-{row['n']+1:03}.png"
            bounds=apertures[name]
            row.update(aperture=list(bounds))
            if bounds == (ORIGIN,ORIGIN+HEIGHT-1):
                summary.append(row)
                continue
            rgb=native_picture(images/name,bounds)
            if "objects" in row:
                white=colored(rgb,WHITE)
                all_masks=set()
                for obj in row["objects"]:
                    mask=expected_mask(masks[obj["index"]],obj["x"],obj["y"]+15)
                    obj["visible"]=len(mask&white)
                    all_masks.update(mask)
                row["white_extra" if event=="blink" else "unattributed_white"]=len(white-all_masks)
            if event=="blink":
                color=colored(rgb,YELLOW if mode else GOLD)
                yellow=colored(rgb,YELLOW)
                key=expected_mask(KEY,85,168)
                player=expected_mask(PLAYER,row["px"],row["py"]+15)
                shot={(120,175)} if row["shot"] else set()
                box={xy for xy in color if 85<=xy[0]<93 and 168<=xy[1]<177}
                row.update(key=len(box&key),key_extra=len(box-key),player_missing=len(player-yellow),
                           yellow_extra=len(yellow-player-shot-(key if mode else set())),
                           shot_pixels=len(shot&yellow))
            if event=="cold_blink":
                yellow=colored(rgb,YELLOW)
                key=expected_mask(KEY,key_x,key_y+15)
                row["key"]=len(key&yellow)
            summary.append(row)
        elif event not in ("ack","tx","rx"):
            summary.append(row)
    return summary,apertures


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("log",type=Path)
    p.add_argument("images",type=Path)
    p.add_argument("mode",type=int)
    p.add_argument("--apertures",type=Path)
    a=p.parse_args()
    rows,bounds=rescore(a.log,a.images,a.mode)
    for row in rows:
        print(json.dumps(row))
    if a.apertures:
        a.apertures.write_text(json.dumps(bounds,sort_keys=True)+"\n")
