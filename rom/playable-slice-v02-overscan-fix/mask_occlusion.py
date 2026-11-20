"""Report the actual RGB color at each missing white M(1) pixel."""
import argparse
import json
from pathlib import Path

from audit import events
from pixels import WHITE, YELLOW, colored, expected_mask, masks_for_project, picture

parser = argparse.ArgumentParser()
parser.add_argument("capture", type=Path)
args = parser.parse_args()
for sample in events(args.capture / "soak.jsonl", "soak_pixels"):
    mask = next((obj for obj in sample["objects"] if obj["index"] == 1), None)
    if mask is None or mask["visible"] == mask["expected"]:
        continue
    frame = sample["n"] + 1
    image = picture(args.capture / "soak" / f"frame-{frame:03}.png")
    missing = expected_mask(masks_for_project()[1], mask["x"], mask["y"] + 15) - colored(image, WHITE)
    print(json.dumps({"frame": frame, "npc": mask,
                      "missing": [{"x": x, "y": y, "rgb": image[y*160+x],
                                   "yellow": image[y*160+x] == YELLOW}
                                  for x, y in sorted(missing)]}))
