"""Compare the original physical P0, M0 and PF pixels, including RGB values."""
import argparse
import json
from pathlib import Path

from measure import measure, pixels

X = [127, 19, 73, 100, 46]
Y = [73, 72, 73, 71, 72]


def channels(path, height):
    raster = pixels(path, height)
    offset = measure(raster, X, Y, range(5))["y_base"]
    groups = {"p0": set(), "m0": set(), "pf": set()}
    for i, color in enumerate(raster):
        r, g, b = color
        x, y = i % 160, i // 160 - offset
        if r > 200 and g > 200 and b < 100:
            groups["p0" if 8 <= x < 18 else "m0"].add((x, y, color))
        if r > 100 and r > 1.3*g and g > 1.4*b:
            groups["pf"].add((x, y, color))
    return groups


def compare(root, height, reference, images):
    expected = channels(reference, height)
    for image in sorted(images):
        seen = channels(image, height)
        result = {
            key: dict(count=len(seen[key]), missing=sorted(expected[key]-seen[key]),
                      extra=sorted(seen[key]-expected[key]))
            for key in expected
        }
        print(json.dumps(dict(image=str(image.relative_to(root)), **result)))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    parser.add_argument("--stella", action="store_true")
    args = parser.parse_args()
    root = args.root
    if args.stella:
        for version in ("671", "70"):
            reference = min((root/f"stella-{version}-baseline-select/images").glob("*.png"))
            compare(root, 228, reference, root.glob(f"stella-{version}-*-select/images/*.png"))
    else:
        reference = min((root/"baseline-png").glob("*.png"))
        images = (p for name in ("baseline","latch4","sharep0","shareclean","sharefour","shareearly")
                  for p in (root/f"{name}-png").glob("*.png"))
        compare(root, 214, reference, images)
