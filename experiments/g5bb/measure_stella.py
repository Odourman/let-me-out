"""Measure stock Stella snapshots against the same mask observation as Gopher."""
import hashlib
import json
from pathlib import Path
import sys
from measure import measure, pixels

for argument in sys.argv[1:]:
    folder = Path(argument)
    selection = folder.name.endswith("-select")
    xs, ys = (
        ([127, 19, 73, 100, 46], [73, 72, 73, 71, 72])
        if selection else ([19, 46, 73, 100, 127], [72] * 5)
    )
    images = sorted((folder / "images").glob("*.png"))
    if len(images) != 12:
        raise ValueError(f"{folder.name}: expected 12 images, got {len(images)}")
    for image in images:
        result = measure(pixels(image, 228), xs, ys, range(5))
        print(json.dumps(dict(series=folder.name, image=image.name,
                              sha256=hashlib.sha256(image.read_bytes()).hexdigest(),
                              **result)))
