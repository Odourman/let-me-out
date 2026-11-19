"""Generate second-slot candidates and retain exact ITER4 controls."""
import json
from pathlib import Path

from schedule_base import search

THIRD = (73,67,76,64,82)
BASE = [json.loads(row) for row in Path("iter4-solver.jsonl").read_text().splitlines()]
LEFT = ((46,100,127),(43,100,127),(49,100,127),(52,100,127))
UNIFIED = ((46,100,127),(43,97,127),(49,103,133),(52,100,136))


def trial(second,fourth,right,x):
    reference=next((row for row in BASE if (row["x"],row["fourth"],row["right"])==(x,fourth,right)),None)
    if second==46 and reference:
        return reference
    clocks=[22,(second+47)//3,(x+47)//3,(fourth+47)//3,(right+47)//3]
    r=search("all-p1-calibrated" if second==43 else "all-p1",clocks=clocks,fetch=3,limit=73)
    if r["status"]!="sat":
        r=search("all-p1-calibrated",clocks=clocks,fetch=3,limit=73)
    return r


if __name__=="__main__":
    for second,fourth,right in dict.fromkeys((*LEFT,*UNIFIED)):
        for x in THIRD:
            print(json.dumps(dict(trial(second,fourth,right,x),second=second,x=x,fourth=fourth,right=right)),flush=True)
