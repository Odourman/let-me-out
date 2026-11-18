"""Measure native Stella snapshots from boot and Select fixtures."""
import argparse
import hashlib
import json
from pathlib import Path

from measure import measure, pixels
from stimuli import BASE_X, BASE_Y

FIXTURES = {
    ("pair", "positive"): ([19, 52, 151, 73, 75], [3, 4]),
    ("pair", "negative"): ([19, 52, 151, 73, 81], [3, 4]),
    ("rowprobe", "positive"): ([19, 52, 151, 73, 75], [3, 4]),
    ("rowprobe", "negative"): ([19, 52, 151, 73, 81], [3, 4]),
    ("hybrid", "positive"): (BASE_X, list(range(5))),
    ("hybrid", "negative"): ([73, 74, 75, 76, 77], list(range(5))),
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    args = parser.parse_args()
    for (mode, state), (xs, actors) in FIXTURES.items():
        images = sorted((args.root / f"stella-{mode}-{state}" / "images").glob("*.png"))
        if len(images) != 12:
            raise ValueError(f"expected 12 images for {mode} {state}, got {len(images)}")
        for image in images:
            result = measure(pixels(image, 228), xs, BASE_Y, actors)
            print(json.dumps(dict(mode=mode, state=state, file=image.name,
                                  sha256=hashlib.sha256(image.read_bytes()).hexdigest(),
                                  **result)))
