"""Summarize pixel evidence with separate key and player oracles."""
import argparse
from collections import Counter
import json
from itertools import groupby
from pathlib import Path

from audit import events
from aperture_audit import native_picture
from build import DOOR_ROWS
from pixels import ROOT, BROWN, colored, picture
from door_trial import BLACK

p=argparse.ArgumentParser()
p.add_argument("runs", type=Path)
a=p.parse_args()
grid=next(room["grid"] for room in json.loads(
    (ROOT/"design/OPEN_ROOMS_V019_40x22_CANDIDATES.json").read_text())["maps"]
          if room["id"]=="A_OPEN_01")
for mode in (0,8,6):
    root=a.runs/str(mode)
    for edge in ("top","bottom"):
        prefix=root/edge
        rows=events(prefix.with_name(edge+"-blink.jsonl"),"blink")
        assert len(rows)==104
        cases=[]
        streaks=[]
        for px,py,shot in ((24,151,False),(60,151,False),(60,159,False),(60,159,True)):
            subset=[r for r in rows if (r["px"],r["py"],r["shot"])==(px,py,shot) and r["n"]<=24]
            assert len(subset)==24 and {r["scanlines"] for r in subset}=={262}
            if mode:
                assert Counter(r["phase"] for r in subset)==dict.fromkeys(range(12),2)
                assert all(y["phase"]==(x["phase"]+1)%12 for x,y in zip(subset,subset[1:]))
            actors=[]
            for index in range(5):
                counts=[(r["objects"][index]["visible"],r["objects"][index]["expected"])
                        for r in subset]
                absent=[v==0 for v,_ in counts]
                partial=[v!=expected for v,expected in counts]
                actors.append(dict(index=index,visible=sum(not q for q in absent),
                    longest_absent=max((sum(1 for _ in group) for flag,group in groupby(absent) if flag),default=0),
                    longest_incomplete=max((sum(1 for _ in group) for flag,group in groupby(partial) if flag),default=0)))
            streaks.append(dict(px=px,py=py,shot=shot,actors=actors))
            for on in (True,False):
                group=[r for r in subset if r["wanted"]==on]
                if group:
                    cases.append(dict(px=px,py=py,shot=shot,on=on,total=len(group),
                        exact=sum(r["key"]==(14 if on else 0) and r["key_extra"]==0 for r in group),
                        keys=sorted({r["key"] for r in group}),sm=sorted({r["objects"][3]["visible"] for r in group}),
                        player_missing=sorted({r["player_missing"] for r in group}),
                        shots=sorted({r["shot_pixels"] for r in group}),
                        white_extra=sorted({r["white_extra"] for r in group}),
                        queued=sum(r["queued"] for r in group)))
        door=root/f"{edge}-door"
        route="route" if mode else "cold"
        cold=root/f"{edge}-{route}-on"
        rim=range(15,23) if edge=="top" else range(183,191)
        walls={(x,y+15) for y in range(176) if y+15 not in rim
               for x in range(160) if grid[y//8][x//4]=="#"}
        aperture={(x,y) for x in range(64,96) for y in rim}
        predicted={(x,y) for row,y in enumerate(rim) for x in range(64,96)
                   if DOOR_ROWS[row] & (1<<((min(x,159-x)-48)//4))}
        def read(path):
            bounds=path.parent.with_suffix(".apertures.json")
            return native_picture(path,json.loads(bounds.read_text())[path.name]) if bounds.exists() else picture(path)
        locked=read(door/"locked.png")
        opened=read(door/"open.png")
        key_floor=read(cold/"key-floor.png")
        metrics=dict(mode=mode,edge=edge,cases=cases,npc_streaks=streaks,
            internal_pf=[len(walls-colored(img,BROWN)) for img in (locked,opened,key_floor)],
            locked_exact=(colored(locked,BROWN)&aperture)==predicted
                and (colored(locked,BLACK)&aperture)==(aperture-predicted),
            open_black=len(colored(opened,BLACK)&aperture))
        for policy in ("on","off") if mode else ("on",):
            log=root/f"{edge}-{route}-{policy}.jsonl"
            done=events(log,"result")
            assert done and done[-1]["status"]=="PASS"
            if mode:
                stream=events(log,"cold_blink")
                floor=[r for r in stream if r["state"]==1]
                for wanted in (True,False):
                    batch=[r for r in floor if r["wanted"]==wanted]
                    metrics[f"cold_{policy}_{'on' if wanted else 'off'}"]=[
                        sum(r["key"]==(14 if wanted else 0) for r in batch),len(batch)]
                pickup=next(r for r in stream if r["state"]==2)
                metrics[f"pickup_{policy}"]=pickup["phase"]
            else:
                floor=[r for r in events(log,"key_lifetime") if r["state"]==1]
                metrics["cold_control"]=[sum(r["key_pixels"]==14 and not r["extra"] for r in floor),len(floor)]
        print(json.dumps(metrics))
