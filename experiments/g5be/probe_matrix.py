"""Score a physical packet line separately from full-frame regression."""
import argparse
import json
from pathlib import Path

from measure import BITS, measure, pixels

HIST_X = [127,19,73,100,46]
HIST_Y = [73,72,73,71,72]


def score(path,height,xs,ys,target):
    data = pixels(path,height)
    offset=measure(data,xs,ys,range(5))["y_base"]
    actual={i%160 for i,c in enumerate(data) if i//160==target+offset
            and min(c)>180 and max(c)-min(c)<40}
    npc=[{left+x for x,y in shape if y+top==target}
         for left,top,shape in zip(xs,ys,BITS)]
    expected=set.union(*npc)
    return dict(row=target, expected=[len(a) for a in npc],
                seen=[len(a&actual) for a in npc], missing_x=sorted(expected-actual),
                extra_x=sorted(actual-expected))


def run(root):
    for target in range(74,79):
        for p in sorted((root/f"y{target}-png").glob("*.png")):
            print(json.dumps(dict(source="Gopher",image=str(p.relative_to(root)),
                **score(p,214,HIST_X,HIST_Y,target))))
    for p in sorted((root/"packet-packet-permuted-png").glob("*.png")):
        print(json.dumps(dict(source="Gopher-permuted",image=str(p.relative_to(root)),
            **score(p,214,[19,127,73,46,97],[72,74,73,70,71],76))))
    for p in sorted((root/"packet-latesm-png").glob("*.png")):
        print(json.dumps(dict(source="Gopher-late-copy",image=str(p.relative_to(root)),
            **score(p,214,[19,127,73,46,103],[72,74,73,70,71],76))))
    for version in ("671","70"):
        for p in sorted((root/f"stella-{version}-packet-select/images").glob("*.png")):
            print(json.dumps(dict(source=f"Stella-{version}",image=str(p.relative_to(root)),
                **score(p,228,HIST_X,HIST_Y,76))))


if __name__=="__main__":
    arg=argparse.ArgumentParser()
    arg.add_argument("root",type=Path)
    run(arg.parse_args().root)
