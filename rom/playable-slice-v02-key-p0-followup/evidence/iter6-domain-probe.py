"""Probe the historical ITER6 combined ROM without changing its code."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path.cwd()))
import replay

replay.UNIFIED = (("iter6-positive", (133,22,76,103,49), (74,68,83,71,76), True),)
replay.NEGATIVE = (
    ("v02-hard", (20,44,68,92,116), (86,)*5, True),
    ("v02-reordered", (116,20,92,44,68), (86,)*5, True),
    ("v02-close", (50,56,62,68,74), (86,)*5, True),
)
replay.replay(Path("roms/combined.bin"), Path(sys.argv[1]).resolve(), "unified")
