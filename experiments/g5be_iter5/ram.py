"""Account for live RIOT allocations and validate the emulator's stack readback."""
import argparse
import json
from pathlib import Path
import re


def measure(family, log):
    path = Path(f"roms/{family}-bank0.sym")
    symbols = {p[0]: int(p[1],16) for l in path.read_text().splitlines()
               if len(p:=l.split())>=2 and re.fullmatch("[0-9a-f]{4}",p[1])}
    stack = next(json.loads(line)["readout"] for line in log.read_text().splitlines()
                 if json.loads(line)["event"] == "stack")
    sp = int(re.search(r"SP=([0-9a-f]+)",stack)[1],16)
    assert sp==(0xff if family=="segmented" else 0xfd), stack
    allotments = {
        "FRAME":1,"XP":5,"YP":5,"ORDER":5,"PTR":10,
        "VALID":1,"STENCIL":1,"TMP":1,"LIMIT_Y":1,"BANKSEL":1,
        "MODE":1,"START":1,"POINTER":2,"CACHE":(92 if family=="segmented" else 85 if family=="unified" else 55),
    }
    if family=="segmented":
        del allotments["MODE"]
    used=set()
    ranges=[]
    for key,length in allotments.items():
        addr=symbols[key]
        claimed=set(range(addr,addr+length))
        assert not used&claimed and claimed <= set(range(0x80,0xfe))
        ranges.append([key,f"{addr:02x}",f"{addr+length-1:02x}"])
        used |= claimed
    return dict(rom=family, ranges=ranges, stack=stack.strip(), stack_bytes=0xff-sp,
                bytes_with_stack=len(used)+0xff-sp)


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("family",choices=("left","unified","segmented"))
    p.add_argument("log",type=Path)
    a=p.parse_args()
    print(json.dumps(measure(a.family,a.log)))
