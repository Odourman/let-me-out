"""Count native standard-profile RGB differences without the new borders."""
from collections import Counter
import json
from pathlib import Path
import sys

from pixels import BROWN, WHITE, YELLOW, picture

base,trial=map(Path,sys.argv[1:])
counts=Counter()
for n in range(1,601):
    name=f"frame-{n:03}.png"
    paths=[folder/"soak"/name for folder in (base,trial)]
    if paths[0].read_bytes()==paths[1].read_bytes():
        continue
    old,new=map(picture,paths)
    start,end=23*160,183*160
    for label,color in (("white",WHITE),("yellow",YELLOW),("brown",BROWN)):
        # Omit the previous door's rightmost four columns from the brown oracle.
        indices=(i for i in range(start,end) if label!="brown" or i%160<156)
        removed=added=0
        for i in indices:
            if old[i]==new[i]:
                continue
            removed+=old[i]==color
            added+=new[i]==color
        if removed or added:
            counts[label+"_frames"]+=1
            counts[label+"_lost"]+=removed
            counts[label+"_gained"]+=added
print(json.dumps(counts,indent=2))
