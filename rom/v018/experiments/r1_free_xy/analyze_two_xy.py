#!/usr/bin/env python3
"""Strict fail-closed real Stella, source-exact upright two independent X/Y outcomes.
No software-rendered source picture is counted as hardware result."""
from pathlib import Path
from PIL import Image
from collections import Counter
import json,hashlib,csv
R=Path(__file__).resolve().parent
ref=json.loads((R/'canon_masks.json').read_text())['sprites']
def pattern(rows):
 return {(bit*2+d,y) for y,s in enumerate(rows) for bit,v in enumerate(s) if v=='1' for d in (0,1)}
M=pattern(ref['large_male']);F=pattern(ref['large_female'])
P=pattern(['00111100','01111110','00011000','01111110','00011110','00111100','00011000','00100100','01000010'])
scanhash='04f59d7fbc17d360e0cea738d4e512ab7208118b9b4d4b4743f3a702d96f1fdb'
def white(p):return min(p[:3])>180 and max(p[:3])-min(p[:3])<40
def brown(p):
 r,g,b=p[:3];return r>=65 and g>=22 and r>=g*1.25 and g>=b*1.15 and b<110 and not (r>185 and g>140)
def yellow(p):
 r,g,b=p[:3];return r>120 and g>100 and b<100 and not brown(p)
def shifted(s,x,y):return {(u+x,v+y) for u,v in s}
def matches(blob,template):
 if not blob:return []
 lowx=min(x for x,y in blob);lowy=min(y for x,y in blob)
 return [(x,y) for x in range(max(0,lowx-16),lowx+1) for y in range(lowy-1,lowy+1) if shifted(template,x,y)==blob]
records=[]
files=sorted((R/'evidence/two_xy/raw').glob('frame_*.png'))
assert len(files)==48,len(files)
for i,path in enumerate(files,1):
 im=Image.open(path).convert('RGB');assert im.size==(900,300)
 pix=im.load()
 whites={(x,y) for y in range(50,195) for x in range(336) if white(pix[x,y])}
 yellows={(x,y) for y in range(50,195) for x in range(336) if yellow(pix[x,y])}
 xs=sorted({x for x,y in whites});groups=[]
 for x in xs:
  if not groups or x-groups[-1][-1]>16:groups.append([])
  groups[-1].append(x)
 fitted=[]
 if len(groups)==2:
  for group,templ in zip(groups,[M,F]):
   blob={(x,y) for x,y in whites if group[0]<=x<=group[-1]}
   fitted.append(matches(blob,templ))
 exact=len(groups)==2 and all(len(z)==1 for z in fitted)
 # player's 9 source rows, independently centered in its own raster Y.
 yellow_exact=False
 if yellows:
  lowy=min(y for x,y in yellows)
  for x in range(0,320):
   p=shifted(P,x,lowy)
   if p.issubset(yellows):
    shot=yellows-p
    if len(shot)==2:
     a,b=sorted(shot)
     if a[1]==b[1] and b[0]==a[0]+1:yellow_exact=True;break
 hud=hashlib.sha256(im.crop((558,25,594,46)).tobytes()).hexdigest()
 left=all(sum(brown(pix[x,y]) for x in range(0,32))>=3 for y in range(125,135))
 right=all(sum(brown(pix[x,y]) for x in range(300,336))>=3 for y in range(125,135))
 r={'frame_i':i,'exact':exact,'male_x':fitted[0][0][0] if exact else '',
  'male_y':fitted[0][0][1] if exact else '', 'female_x':fitted[1][0][0] if exact else '',
  'female_y':fitted[1][0][1] if exact else '', 'yellow_p0_m0':yellow_exact,
  'left_brown_wall':left,'right_brown_wall':right,'ntsc_262':hud==scanhash,
  'white_clusters':len(groups),'raw_image':str(path)}
 records.append(r)
counts=Counter((r['male_x'],r['female_x'],r['male_y'],r['female_y']) for r in records if r['exact'])
X=sorted(set((r['male_x'],r['female_x']) for r in records if r['exact']))
Y=sorted(set((r['male_y'],r['female_y']) for r in records if r['exact']))
full_cart=sorted(set((a,b) for a,b in [(r['male_x'],r['female_x']) for r in records if r['exact']]))
summary={'real_stella_frames':len(records),'two_full_original_upright_masks':sum(r['exact'] for r in records),
 'yellow_p0_and_m0':sum(r['yellow_p0_m0'] for r in records),
 'ntsc262':sum(r['ntsc_262'] for r in records),'brown_left':sum(r['left_brown_wall'] for r in records),
 'brown_right':sum(r['right_brown_wall'] for r in records),
 'independent_X_pairs':X,'independent_Y_pairs':Y,
 'distinct_combined_XY_quads':len(counts),'each_combined_mode_counts':{'/'.join(map(str,k)):v for k,v in counts.items()},
 'strict_16_xy_factor_crossproduct':len(X)==4 and len(Y)==4 and len(counts)==16 and all((mx,fx,my,fy) in counts for mx,fx in X for my,fy in Y)}
# Wall area uses physical y <= ; inspect if fixed y 125-135 is correct for crop in field.
(R/'dist/two_xy_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
with (R/'dist/two_xy_results.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(records[0]));w.writeheader();w.writerows(records)
print(json.dumps(summary,indent=2))
assert summary['two_full_original_upright_masks']==48
assert summary['yellow_p0_and_m0']==48
assert summary['ntsc262']==48
assert summary['strict_16_xy_factor_crossproduct']
print('R1 TWO_INDEPENDENT_XY: LOCAL_PIXELS_PASS_48_ONLY_NOT_FULL_R1')
