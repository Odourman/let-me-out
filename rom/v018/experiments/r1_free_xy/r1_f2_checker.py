#!/usr/bin/env python3
"""R1-F2 read-only exact 8x9 per-index Stella crop audit, with mutant negative controls.
Use only genuine raw 900x300 PNG from Stella as positive evidence.
Mutations remain isolated diagnostic copies, NEVER labelled genuine frames.
"""
import argparse,csv,hashlib,json
from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parent
J=json.loads((R/'canon_masks.json').read_text())
assert J['width']==8 and J['height']==9
TYPES=['large_male','large_male','large_female','large_female','small_male','small_female']
MASKS={t:{(2*j+d,y) for y,row in enumerate(bits) for j,ch in enumerate(row) if ch=='1' for d in (0,1)} for t,bits in J['sprites'].items()}
PLAYER=['00111100','01111110','00011000','01111110','00011110','00111100','00011000','00100100','01000010']
P0={(2*j+d,y) for y,row in enumerate(PLAYER) for j,ch in enumerate(row) if ch=='1' for d in (0,1)}
BASE=[43,75,129,183,243,303]
EXPECTED={'M2':[43,75,117,183,243,303],'P1':[43,75,135,183,243,303],
          'BASE':BASE}
def white(p):
    return min(p)>180 and max(p)-min(p)<40
def yellow(p):
    r,g,b=p
    return r>120 and g>100 and b<100 and not (r>=65 and g>=22 and r>=g*1.25 and g>=b*1.15 and b<110 and r<=185)
def brown(p):
    r,g,b=p
    return r>=65 and g>=22 and r>=g*1.25 and g>=b*1.15 and b<110 and not (r>185 and g>140)
def audit_image(im,requested):
    im=im.convert('RGB')
    assert im.size==(900,300),(im.size,'bad crop')
    pix=im.load()
    whitepix={(x,y) for y in range(50,195) for x in range(336) if white(pix[x,y])}
    if not whitepix:
        return dict(exact=False,reason='NO_WHITE_MASK',rendered=[],costs=[],y0=None)
    y0=min(y for x,y in whitepix)
    groups=[]
    for x in sorted({x for x,y in whitepix}):
        if not groups or x-groups[-1][-1]>16: groups.append([])
        groups[-1].append(x)
    rendered=[];costs=[]; row_costs=[]
    for i,g in enumerate(groups):
        if i>=len(TYPES): break
        typ=TYPES[i];found={(x,y) for x,y in whitepix if g[0]<=x<=g[-1]}
        opts=[]
        for start in range(max(0,g[0]-16),g[0]+1):
            expected={(x+start,y+y0) for x,y in MASKS[typ]}
            diff=expected^found
            opts.append((len(diff),abs(start-requested[i]),start,
                         [len({(x,y) for x,y in diff if y==y0+row}) for row in range(9)]))
        cost,_,start,perrow=min(opts)
        rendered.append(start);costs.append(cost);row_costs.append(perrow)
    ys={(x,y) for y in range(y0,y0+9) for x in range(336) if yellow(pix[x,y])}
    p0_ok=False;m0_ok=False;p0_x=None;missile=None
    for px in range(320):
        player={(x+px,y+y0) for x,y in P0}
        if player.issubset(ys):
            remain=ys-player
            if len(remain)==2:
                p,q=sorted(remain)
                if p[1]==q[1] and q[0]==p[0]+1:
                    p0_ok=True;m0_ok=True;p0_x=px;missile=p;break
    wall_left=all(sum(brown(pix[x,y]) for x in range(0,32))>=3 for y in range(y0,y0+9))
    wall_right=all(sum(brown(pix[x,y]) for x in range(300,336))>=3 for y in range(y0,y0+9))
    hud_hash=hashlib.sha256(im.crop((558,25,594,46)).tobytes()).hexdigest()
    ntsc262=(hud_hash=='04f59d7fbc17d360e0cea738d4e512ab7208118b9b4d4b4743f3a702d96f1fdb')
    all_mask_exact=len(groups)==6 and len(rendered)==6 and all(k==0 for k in costs)
    static_ok=len(rendered)==6 and all(rendered[j]==BASE[j] for j in range(6) if j!=2)
    requested_ok=rendered==requested
    exact=all((all_mask_exact,static_ok,requested_ok,p0_ok,m0_ok,wall_left,wall_right,ntsc262))
    return dict(exact=exact,group_count=len(groups),y0=y0,rendered=rendered,
                requested=requested,types=TYPES,mask_costs=costs,mask_row_costs=row_costs,
                static_five_exact=static_ok,requested_pixel_x_exact=requested_ok,
                P0_yellow=p0_ok,M0_active=m0_ok,P0_x=p0_x,M0_pixel=missile,
                PF_brown_left=wall_left,PF_brown_right=wall_right,
                ntsc262=ntsc262,hud_sha256=hud_hash)
def run(mode,raw,output,mutants):
    req=EXPECTED.get(mode,BASE)
    paths=sorted(raw.glob('frame_*.png'))
    expected_count=32 if mode=='RUNTIME' else 16
    assert len(paths)==expected_count,(mode,'frame_count',len(paths),expected_count)
    rows=[];all_ok=True
    for i,path in enumerate(paths,1):
        requested=req if mode!='RUNTIME' else EXPECTED['P1'] if ((10+i)&4) else BASE
        info=audit_image(Image.open(path),requested)
        record=dict(frame_id=10+i,mode=mode,raw_png=str(path),
            png_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),**info)
        rows.append(record)
        print('F2_REAL_STELLA',mode,10+i,info.get('exact'),info.get('rendered'),info.get('mask_costs'),
              'P0_M0_PF_262=',[info.get(x) for x in ('P0_yellow','M0_active','PF_brown_left','PF_brown_right','ntsc262')])
        all_ok&=bool(info['exact'])
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(rows,indent=2)+'\n')
    if mutants:
        mutants.mkdir(parents=True,exist_ok=True)
        source=Image.open(paths[0]).convert('RGB')
        good=audit_image(source, rows[0]['requested'])
        assert good['exact'],('cannot test mutant detector on FAILED real screenshot')
        pix=source.load()
        y0=good['y0'];start=good['rendered'][2]
        # Mutant A: erase one actual white P1 pixel from third original mask.
        mask=MASKS[TYPES[2]]
        xx,yy=next((x+start,y+y0) for x,y in sorted(mask) if white(pix[x+start,y+y0]))
        ma=source.copy();ma.putpixel((xx,yy),(40,40,40))
        ma.save(mutants/'MUTANT_ERASE_ONE_REAL_WHITE_PIXEL_NOT_STELLA.png')
        ra=audit_image(ma,rows[0]['requested'])
        # Mutant B: create a fake unconnected white x0 ghost like original 6C.
        mb=source.copy();mb.putpixel((1,y0+6),(255,255,255));mb.putpixel((2,y0+6),(255,255,255))
        mb.save(mutants/'MUTANT_ADD_LEFT_GHOST_NOT_STELLA.png')
        rb=audit_image(mb,rows[0]['requested'])
        assert not ra['exact'] and not rb['exact'],(ra,rb)
        (mutants/'MUTANT_EXPECTED_FAILURES.json').write_text(json.dumps({
            'MUTANT_ERASE_ONE_REAL_WHITE_PIXEL':{'detected':not ra['exact'],'mask_costs':ra.get('mask_costs'),'png_sha256':hashlib.sha256((mutants/'MUTANT_ERASE_ONE_REAL_WHITE_PIXEL_NOT_STELLA.png').read_bytes()).hexdigest()},
            'MUTANT_ADD_LEFT_GHOST':{'detected':not rb['exact'],'group_count':rb.get('group_count'),'png_sha256':hashlib.sha256((mutants/'MUTANT_ADD_LEFT_GHOST_NOT_STELLA.png').read_bytes()).hexdigest()},
        },indent=2)+'\n')
        print('F2_MUTANT_NEGATIVE_TESTS',not ra['exact'],not rb['exact'])
    print('F2_REPRODUCIBLE_AUDIT',mode,'frames',len(rows),'strict_pass',all_ok)
    if not all_ok: raise SystemExit(2)
if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--mode',choices=['BASE','M2','P1','RUNTIME'],required=True)
    ap.add_argument('--raw',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--mutants',type=Path)
    a=ap.parse_args()
    run(a.mode,a.raw,a.output,a.mutants)
