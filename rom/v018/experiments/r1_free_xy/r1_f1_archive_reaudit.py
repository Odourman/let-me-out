#!/usr/bin/env python3
"""Independent read-only R1-F1 pixel audit of frozen Google Drive evidence ZIP.
Usage: python3 r1_f1_archive_reaudit.py <R1_evidence.zip> [output.csv]
Requires Pillow. Never synthesizes emulator frames. Does not assert free X/Y.
"""
import sys,zipfile,json,io,hashlib,csv
from collections import Counter
from PIL import Image
with zipfile.ZipFile(sys.argv[1]) as z:
    assert z.testzip() is None
    sprites=json.loads(z.read('source/canon_masks.json'))['sprites']
    masks={k:{(2*j+d,i) for i,row in enumerate(rows) for j,ch in enumerate(row)
             for d in (0,1) if ch=='1'} for k,rows in sprites.items()}
    scenarios={
      'N5':('evidence/scaling_n3_n6/n5/raw',
            ['large_male','large_male','large_female','small_male','small_female']),
      '6B':('evidence/six_sweep_n6B_n6E/n6B/raw',
            ['large_male','large_male','large_female','large_female','small_male','small_female']),
      '6C':('evidence/six_sweep_n6B_n6E/n6C/raw',
            ['large_male','large_male','large_female','large_female','small_male','small_female'])}
    records=[]
    for v,(folder,required) in scenarios.items():
        paths=sorted(x for x in z.namelist() if x.startswith(folder+'/frame_') and x.endswith('.png'))
        assert len(paths)==16,(v,len(paths))
        for path in paths:
            raw=z.read(path); im=Image.open(io.BytesIO(raw)).convert('RGB')
            assert im.size==(900,300)
            px=im.load()
            white={(x,y) for y in range(50,195) for x in range(336)
                   if min(px[x,y])>180 and max(px[x,y])-min(px[x,y])<40}
            y0=min(y for x,y in white)
            groups=[]
            for x in sorted({x for x,y in white}):
                if not groups or x-groups[-1][-1]>16:groups.append([])
                groups[-1].append(x)
            matched=[]
            for g in groups:
                blob={(x,y) for x,y in white if g[0]<=x<=g[-1]}
                options=[]
                for typ,mask in masks.items():
                    for start in range(max(0,g[0]-16),g[0]+1):
                        expected={(x+start,y+y0) for x,y in mask}
                        options.append((len(expected^blob),typ,start))
                matched.append(min(options))
            # ORIGINAL BUG: len(groups)==v where v was a STRING like "6B".
            exact=(len(groups)==len(required) and
                   Counter(t for cost,t,x in matched if cost==0)==Counter(required) and
                   all(cost==0 for cost,t,x in matched))
            ghost=all(min(px[x,y0+6])>180 and max(px[x,y0+6])-min(px[x,y0+6])<40 for x in (1,2))
            yellow=all(px[x,y0+4][0]>200 and px[x,y0+4][1]>200 and
                       px[x,y0+4][2]<120 for x in (317,318))
            records.append(dict(variant=v,png=path,png_sha256=hashlib.sha256(raw).hexdigest(),
                stella_frame=int(path[-7:-4])+10,actual_groups=len(groups),
                matched_types=';'.join(t for cost,t,x in matched),
                mask_starts=';'.join(str(x) for cost,t,x in matched),
                pixel_costs=';'.join(str(cost) for cost,t,x in matched),
                corrected_pixel_exact=exact,left_ghost_y6_x1_x2=ghost,
                yellow_M0_y4_x317_x318=yellow))
    for v in scenarios:
        rr=[r for r in records if r['variant']==v]
        print(v,'exact',sum(x['corrected_pixel_exact'] for x in rr),'/',len(rr),
              'ghost',sum(x['left_ghost_y6_x1_x2'] for x in rr),'/',len(rr))
    if len(sys.argv)>2:
        with open(sys.argv[2],'w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=list(records[0]));w.writeheader();w.writerows(records)
