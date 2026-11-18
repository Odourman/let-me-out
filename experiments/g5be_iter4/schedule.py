"""Pack P1 write deadlines for independently selected third and fifth X."""
import json
from pathlib import Path

from schedule_base import search

THIRD = (73, 67, 76, 82, 64)
RIGHT = (127, 130, 133, 136)
MIXED = ((127,100),(127,97),(127,103),(133,103))
REFERENCE = [json.loads(line) for line in Path("frozen-solver.jsonl").read_text().splitlines()]


def original(x):
    family = "all-p1-calibrated" if x in (76,82) else "all-p1"
    return next(r for r in REFERENCE if r["family"] == family and r["x"] == x and r["fetch"] == 3)


if __name__ == "__main__":
    for right in RIGHT:
        for x in THIRD:
            reference = original(x)
            clocks = [22,31,(x+47)//3,49,(right+47)//3]
            if right == 127:
                result = reference
            else:
                result = search("all-p1", clocks=clocks,fetch=3,limit=73,anchored=reference)
                if result["status"] != "sat":
                    result = search("all-p1-calibrated", clocks=clocks,fetch=3,limit=73)
            print(json.dumps(dict(result, x=x, right=right, fourth=100)),flush=True)
    for right,fourth in MIXED[1:]:
        for x in THIRD:
            reference = original(x)
            clocks = [22,31,(x+47)//3,(fourth+47)//3,(right+47)//3]
            result = search("all-p1", clocks=clocks,fetch=3,limit=73,anchored=reference,preserve_until=44)
            if result["status"] != "sat":
                result = search("all-p1-calibrated", clocks=clocks,fetch=3,limit=73)
            print(json.dumps(dict(result, x=x, right=right, fourth=fourth)),flush=True)
