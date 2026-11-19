"""Generate first-slot RESP1 phase candidates, retaining the ITER5 control."""
import json
from pathlib import Path

from layouts import DIRECT,COMBINED,THIRD
from schedule_base import search

BASE = [json.loads(row) for row in Path("iter5-solver.jsonl").read_text().splitlines()]


def trial(first,second,fourth,right,x):
    ref=next((r for r in BASE if (r["second"],r["x"],r["fourth"],r["right"])==(second,x,fourth,right)),None)
    if first==19 and ref:
        return ref
    clocks=[(first+47)//3,(second+47)//3,(x+47)//3,(fourth+47)//3,(right+47)//3]
    result=search("all-p1-calibrated",clocks=clocks,fetch=3,limit=73)
    if result["status"]!="sat":
        result=search("all-p1",clocks=clocks,fetch=3,limit=73)
    return result


if __name__=="__main__":
    for first,second,fourth,right in dict.fromkeys((*DIRECT,*COMBINED)):
        for x in THIRD:
            record=trial(first,second,fourth,right,x)
            print(json.dumps(dict(record,first=first,second=second,right=right,fourth=fourth,x=x)),flush=True)
