"""Geometry-specific audit. The frozen side-door oracle stays unchanged."""
import argparse
import json
from pathlib import Path

from audit import events, soak, visibility
from build import DOOR_ROWS
from door_trial import ORANGE, BROWN, BLACK
from pixels import ROOT, colored, picture


def report(folder,edge):
    maps=json.loads((ROOT/"design/OPEN_ROOMS_V019_40x22_CANDIDATES.json").read_text())["maps"]
    grid=next(m["grid"] for m in maps if m["id"]=="A_OPEN_01")
    rows=range(15,23) if edge=="top" else range(183,191)
    aperture={(x,y) for x in range(64,96) for y in rows}
    walls={(x,y+15) for y in range(176) for x in range(160)
           if grid[y//8][x//4]!="."}
    locked_brown={(x,y) for row,y in enumerate(rows) for x in range(64,96)
                 if DOOR_ROWS[row] & (1<<((min(x,159-x)-48)//4))}
    shapes={}
    for name,state in (("locked","locked"),("open","open"),
                       ("key-floor","cold")):
        src=folder/("cold" if state=="cold" else "door")/f"{name}.png"
        image=picture(src)
        brown=colored(image,BROWN)
        black=colored(image,BLACK)
        orange=colored(image,ORANGE)
        expected=walls-aperture
        if state!="open":
            expected|=locked_brown
        expected_border={p for p in expected if p[1] in rows}
        expected_black=aperture if state=="open" else aperture-locked_brown
        actual_border={p for p in brown if p[1] in rows}
        shapes[name]=dict(interior_wall_missing=len({p for p in walls if p[1] not in rows}-brown),
                          border_brown_missing=sorted(expected_border-brown),
                          border_brown_extra=sorted(actual_border-expected_border),
                          black_oracle_missing=sorted(expected_black-black),
                          black_oracle_extra=sorted((black&aperture)-expected_black),
                          orange_outside_band=len({p for p in orange if p[1] not in rows}),
                          orange_outside_aperture=len(orange-aperture),
                          orange_inside_aperture=len(orange&aperture),
                          black_in_aperture=len(black&aperture),
                          open_black_missing=sorted(aperture-black) if state=="open" else [])
    floor=[r for r in events(folder/"cold.jsonl","key_lifetime") if r["state"]==1]
    exact=sum(r["key_pixels"]==14 and not r["extra"] for r in floor)
    return dict(edge=edge,soak=soak(folder),visibility=visibility(folder),
                key_lifetime=dict(exact=exact,frames=len(floor)),geometry=shapes)


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("folder",type=Path)
    parser.add_argument("edge",choices=("top","bottom"))
    a=parser.parse_args()
    print(json.dumps(report(a.folder,a.edge),indent=2))
