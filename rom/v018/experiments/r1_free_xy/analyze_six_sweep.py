#!/usr/bin/env python3
"""Strict all-white-pixel original 8x9 source mask matcher for R1 N=3..6.
This reads only raw Stella screenshots; 6502 code is not treated as raster truth.
"""
from pathlib import Path
from PIL import Image
from collections import Counter
import json,csv,hashlib
R=Path(__file__).resolve().parent
canon=json.loads((R/'canon_masks.json').read_text())['sprites']
assert len(canon)==4
required=['large_male','large_male','large_female','large_female','small_male','small_female']
scenarios={k:required for k in ('6B','6C','6D','6E')}

def pattern(rows):
  return {(j*2+d,i) for i,s in enumerate(rows) for j in range(8) if s[j]=='1' for d in (0,1)}
M={k:pattern(rows) for k,rows in canon.items()}
player=['00111100','01111110','00011000','01111110','00011110','00111100','00011000','00100100','01000010']
P=pattern(player)
def brown(p):
 r,g,b=p[:3];return r>=65 and g>=22 and r>=g*1.25 and g>=b*1.15 and b<110 and not (r>185 and g>140)
def white(p):
 rgb=p[:3];return min(rgb)>180 and max(rgb)-min(rgb)<40
def yellow(p):
 r,g,b=p[:3];return r>120 and g>100 and b<100 and not brown(p)
def shifted(template,x,y):return {(a+x,b+y) for a,b in template}
scanhash='04f59d7fbc17d360e0cea738d4e512ab7208118b9b4d4b4743f3a702d96f1fdb'
records=[];summary={}
for n,required in scenarios.items():
  files=sorted((R/f'evidence/six_sweep/n{n}/raw').glob('frame_*.png'))
  assert len(files)==16,(n,len(files))
  scores=Counter();unique_x=Counter()
  for i,path in enumerate(files,1):
    im=Image.open(path).convert('RGB');assert im.size==(900,300)
    pix=im.load()
    whites={(x,y) for y in range(50,195) for x in range(336) if white(pix[x,y])}
    yellows={(x,y) for y in range(50,195) for x in range(336) if yellow(pix[x,y])}
    y0=min((b for a,b in whites),default=-1)
    xs=sorted({x for x,y in whites})
    groups=[]
    for x in xs:
      if not groups or x-groups[-1][-1]>16:groups.append([])
      groups[-1].append(x)
    matched=[]
    for group in groups:
      blob={(x,y) for x,y in whites if group[0]<=x<=group[-1]}
      candidates=[]
      for typ,template in M.items():
        for start in range(max(0,group[0]-16),group[0]+1):
          expect=shifted(template,start,y0)
          cost=len(expect^blob)
          candidates.append((cost,typ,start))
      matched.append(min(candidates) if candidates else (999,'UNKNOWN',-1))
    exact=bool(whites) and len(groups)==n and Counter(tp for c,tp,x in matched if c==0)==Counter(required) and all(c==0 for c,t,x in matched)
    pyellow=False
    for x in range(320):
      obj=shifted(P,x,y0)
      if obj.issubset(yellows):
        rem=yellows-obj
        if len(rem)==2:
          a,b=sorted(rem)
          if a[1]==b[1] and b[0]==a[0]+1:pyellow=True;break
    wall_left=(y0>=0 and all(sum(brown(pix[x,y]) for x in range(0,32))>=3 for y in range(y0,y0+9)))
    wall_right=(y0>=0 and all(sum(brown(pix[x,y]) for x in range(300,336))>=3 for y in range(y0,y0+9)))
    hud=hashlib.sha256(im.crop((558,25,594,46)).tobytes()).hexdigest()
    r={'N':n,'frame':i+10,'groups':len(groups),'expected':';'.join(required),'actual':';'.join(tp for c,tp,x in matched),
       'X_positions':';'.join(str(x) for c,tp,x in matched),'mask_costs':';'.join(str(c) for c,tp,x in matched),
       'exact_masks':exact,'p0_plus_m0':pyellow,'brown_left':wall_left,'brown_right':wall_right,'ntsc_262':hud==scanhash,'raw_image':str(path)}
    records.append(r)
    scores.update({'exact':int(exact),'p0m0':int(pyellow),'left':int(wall_left),'right':int(wall_right),'ntsc':int(hud==scanhash)})
    unique_x[r['X_positions']]+=1
  summary[n]={'sampled_actual_Stella_frames':16,**scores,'unique_x_groups':dict(unique_x),
      'strict_16of16':all(scores[k]==16 for k in ('exact','p0m0','left','right','ntsc'))}
with (R/'dist/six_sweep_pixel_audit.csv').open('w') as f:
 wr=csv.DictWriter(f,fieldnames=list(records[0]));wr.writeheader();wr.writerows(records)
(R/'dist/six_sweep_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
print('R1 scaling reality: '+', '.join('N%d=%s'%(k,'LOCAL_PASS_16' if v['strict_16of16'] else 'FAIL') for k,v in summary.items()))
