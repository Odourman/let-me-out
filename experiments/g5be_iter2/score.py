"""Compare native captures to exact mask geometry and frozen per-emulator RGB."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

from measure import BITS, measure, pixels
from replay import SCENES

WINDOWS = ((76, 77), (74, 78), (71, 81))


def profile(path, height, xs, ys):
    data = pixels(path, height)
    base = measure(data, xs, ys, range(5))["y_base"]
    layers = {key: {} for key in ("npc", "player", "shot", "wall")}
    for i, rgb in enumerate(data):
        x, y = i % 160, i // 160 - base
        r, g, b = rgb
        if min(rgb) > 180 and max(rgb) - min(rgb) < 40:
            key = "npc"
        elif r > 200 and g > 200 and b < 100:
            key = "player" if 8 <= x < 18 else "shot"
        elif r > 100 and r > 1.3 * g and g > 1.4 * b:
            key = "wall"
        else:
            continue
        layers[key][x, y] = rgb
    return layers


def compare(path, height, xs, ys, reference, bounds, admitted):
    layers = profile(path, height, xs, ys)
    parts = [{(left+x, top+y) for x,y in shape}
             for left, top, shape in zip(xs, ys, BITS)]
    full = set.union(*parts)
    target = {(x,y) for x,y in full if bounds[0] <= y <= bounds[1]} if admitted else set()
    seen = set(layers["npc"])
    other = {}
    for layer in ("player", "shot", "wall"):
        actual, expected = layers[layer], reference[layer]
        other[layer] = dict(expected=len(expected), seen=len(actual), mismatch=len(actual.items() ^ expected.items()))
    white_rgb = set(reference["npc"].values())
    wrong_rgb = sum(rgb not in white_rgb for rgb in layers["npc"].values())
    row_diff = []
    for y in range(71, 82):
        row_diff.append(dict(y=y, missing_x=sorted(x for x,ry in target-seen if y == ry),
                             extra_x=sorted(x for x,ry in seen-target if y == ry),
                             expected=sum(ry == y for x,ry in target),
                             seen=sum(ry == y for x,ry in seen)))
    geometry = dict(missing=len(target-seen), extra=len(seen-target),
                    full_missing=len(full-seen), full_extra=len(seen-full),
                    full_missing_by_actor=[len(part-seen) for part in parts],
                    full_seen_by_actor=[len(part&seen) for part in parts])
    return dict(**geometry, peripheral=other, wrong_npc_rgb=wrong_rgb,
                rgb={name: sorted(set(values.values())) for name, values in layers.items()},
                status="PASS" if admitted and not (target^seen or wrong_rgb or any(
                    value["mismatch"] for value in other.values())) else "FAIL", rows=row_diff)


def score_run(log, images, ref, ref_height):
    reference = profile(ref, ref_height, SCENES[0][1], SCENES[0][2])
    cache = {}
    for line in log.read_text().splitlines():
        evt = json.loads(line)
        if evt["event"] != "raster":
            continue
        path = images / evt["path"]
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        bounds = WINDOWS[2 if evt["dynamic"] else evt["mode"]]
        height = evt["bottom"]-evt["top"]+1
        key = (digest, height, tuple(evt["x"]), tuple(evt["y"]), bounds, evt["admitted"])
        if key not in cache:
            cache[key] = compare(path, height, evt["x"], evt["y"], reference, bounds, evt["admitted"])
        print(json.dumps({**evt, **cache[key], "sha256": digest,
                          "timing": "PASS" if evt["scanlines"] == 262 else "FAIL"},
                         separators=(",", ":")))


def score_stella(images, ref):
    _, xs, ys, _ = SCENES[0]
    reference = profile(ref, 228, xs, ys)
    for path in sorted(images.glob("*.png")):
        result = compare(path, 228, xs, ys, reference, WINDOWS[2], True)
        print(json.dumps(dict(path=path.name, sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                              **result), separators=(",", ":")))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("images", type=Path)
    parser.add_argument("ref", type=Path)
    parser.add_argument("--log", type=Path)
    parser.add_argument("--ref-height", type=int, default=192)
    args = parser.parse_args()
    if args.log:
        score_run(args.log, args.images, args.ref, args.ref_height)
    else:
        score_stella(args.images, args.ref)
