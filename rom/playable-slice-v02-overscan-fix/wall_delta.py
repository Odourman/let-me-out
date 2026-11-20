"""Compare matching native screenshots against the frozen ROM and room map."""
import argparse
import json
from pathlib import Path

from pixels import BROWN, ROOT, WHITE, YELLOW, colored, picture


def comparison(before, after, edge):
    maps = json.loads((ROOT / "design/OPEN_ROOMS_V019_40x22_CANDIDATES.json").read_text())["maps"]
    grid = next(room["grid"] for room in maps if room["id"] == "A_OPEN_01")
    border = range(15, 23) if edge == "top" else range(183, 191)
    walls = {(x, y + 15) for y in range(176) if y + 15 not in border
             for x in range(160) if grid[y // 8][x // 4] == "#"}
    for old_file in sorted(before.glob("*.png")):
        new_file = after / old_file.name
        old, new = map(picture, (old_file, new_file))
        old_brown, new_brown = (colored(image, BROWN) for image in (old, new))
        yield {"fixture": old_file.stem,
               "missing_before": len(walls - old_brown),
               "missing_after": len(walls - new_brown),
               "brown_added": sorted(new_brown - old_brown),
               "brown_lost": sorted(old_brown - new_brown),
               "white_changed": len(colored(old, WHITE) ^ colored(new, WHITE)),
               "yellow_changed": len(colored(old, YELLOW) ^ colored(new, YELLOW))}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("before", type=Path)
    parser.add_argument("after", type=Path)
    parser.add_argument("edge", choices=("top", "bottom"))
    args = parser.parse_args()
    for item in comparison(args.before, args.after, args.edge):
        print(json.dumps(item))
