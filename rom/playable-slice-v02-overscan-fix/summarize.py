"""Rescore the cold, door, shot, and paired standard runs for the timer repair."""
from argparse import ArgumentParser
import json
from pathlib import Path

from aperture_audit import native_picture, rescore
from audit import events
from build import DOOR_ROWS
from door_trial import BLACK
from pixels import BROWN, ROOT, colored, picture

parser = ArgumentParser()
parser.add_argument("runs", type=Path)
args = parser.parse_args()
grid = next(room["grid"] for room in json.loads(
    (ROOT / "design/OPEN_ROOMS_V019_40x22_CANDIDATES.json").read_text())["maps"]
    if room["id"] == "A_OPEN_01")

for blink in (0, 8, 6):
    root = args.runs / str(blink)
    for edge in ("top", "bottom"):
        def log(label):
            return root / f"{edge}-{label}.jsonl"

        def run(label):
            folder = root / f"{edge}-{label}"
            return rescore(log(label), folder, blink)

        def read(label, name, aperture):
            path = root / f"{edge}-{label}" / name
            return native_picture(path, aperture[name]) if name in aperture else picture(path)

        cold, cold_aperture = run("cold")
        _, door_aperture = run("door")
        rim = range(15, 23) if edge == "top" else range(183, 191)
        walls = {(x, y+15) for y in range(176) if y+15 not in rim
                 for x in range(160) if grid[y//8][x//4] == "#"}
        opening = {(x, y) for x in range(64, 96) for y in rim}
        closed_pf = {(x, y) for row, y in enumerate(rim) for x in range(64, 96)
                     if DOOR_ROWS[row] & (1 << ((min(x, 159-x)-48)//4))}
        locked = read("door", "locked.png", door_aperture)
        opened = read("door", "open.png", door_aperture)
        floor_image = read("cold", "key-floor.png", cold_aperture)
        standard = events(log("standard"), "paired")
        shot_log = log("shot-normalized") if log("shot-normalized").exists() else log("shot")
        shots = events(shot_log, "missile")
        done = [r for r in cold if r["event"] == "result"]
        metrics = dict(blink=blink, edge=edge, standard=[
            sum(r["rgb_equal"] and r["scanlines"] == 262 for r in standard), len(standard)],
            shots=[sum(r["correct"] for r in shots), len(shots)],
            locked_exact=(colored(locked, BROWN) & opening) == closed_pf
              and (colored(locked, BLACK) & opening) == (opening - closed_pf),
            open_black=len(colored(opened, BLACK) & opening),
            internal_pf=[len(walls - colored(img, BROWN)) for img in (locked, opened, floor_image)],
            result=done[-1]["status"])
        if blink:
            floor = [r for r in cold if r["event"] == "cold_blink" and r["state"] == 1]
            for on in (True, False):
                phase = [r for r in floor if r["wanted"] == on]
                metrics["key_on" if on else "key_off"] = [
                    sum(r["key"] == (14 if on else 0) and r["lines"] == 262 for r in phase),
                    len(phase)]
            pickup = next(r for r in cold if r["event"] == "cold_blink" and r["state"] == 2)
            metrics["pickup_phase"] = pickup["phase"]
        else:
            floor = [r for r in cold if r["event"] == "key_lifetime" and r["state"] == 1]
            metrics["key_on"] = [sum(r["key_pixels"] == 14 and not r["extra"] for r in floor), len(floor)]
        print(json.dumps(metrics))
