"""Compare each physical row of untouched Gopher PNGs with original 8x9 bits."""
import argparse
import json
from pathlib import Path

from measure import BITS, pixels

def mask_byte(positions, origin):
    return f"{sum(0x80 >> (x-origin) for x in positions if origin <= x < origin+8):02x}"

def main():
    p = argparse.ArgumentParser()
    p.add_argument("metrics", type=Path)
    p.add_argument("images", type=Path)
    args = p.parse_args()
    for line in args.metrics.read_text().splitlines():
        row = json.loads(line)
        if row["label"] != "historic-reorder":
            continue
        image = pixels(args.images/row["path"], row["bottom"]-row["top"]+1)
        white = {(i%160,i//160-row["y_base"]) for i,c in enumerate(image)
                 if min(c)>180 and max(c)-min(c)<40}
        for y in range(min(row["y"]),max(row["y"])+9):
            actual = {x for x,r in white if r==y}
            parts = [{start+dx for dx,dy in shape if start_y+dy==y}
                     for shape,start,start_y in zip(BITS,row["x"],row["y"])]
            expected = set.union(*parts)
            print(json.dumps(dict(frame=row["frame"], y=y,
                                  expected_bytes=[mask_byte(part,x) for part,x in zip(parts,row["x"])],
                                  seen_bytes=[mask_byte(actual,x) for x in row["x"]],
                                  missing_x=sorted(expected-actual),
                                  extra_x=sorted(actual-expected))))

if __name__ == "__main__":
    main()
