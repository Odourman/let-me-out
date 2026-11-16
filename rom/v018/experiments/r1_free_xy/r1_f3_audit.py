#!/usr/bin/env python3
"""R1-F3 strict independent two-path audit of UNMODIFIED authentic Stella PNGs.

Input is only raw 900x300 crops from a single DASM ROM, not synthetic evidence.
Two checks: F2 per-group 8x9-index/row matcher, and independent white-pixel union.
Expected modes are derived solely from F3 ROM logic FRAMELO -> two RIOT-RAM
bytes, with F2-validated debugger completed-frame phase (frame label - 2).
Artificial mutation images are generated ONLY as explicitly labelled NEGATIVES.
"""
from pathlib import Path
from collections import Counter
from PIL import Image
import argparse,hashlib,json,csv
import r1_f2_checker as legacy
BASE=[43,75,129,183,243,303]
TYPES=['large_male','large_male','large_female','large_female','small_male','small_female']
assert TYPES==legacy.TYPES
def expected_for(mode,debugger_frame):
    source_framelo=(debugger_frame-2)&255
    if mode=='G0':
        return [49,75,129,183,243,303],0,0,source_framelo
    # THE TWO SEPARATE WRITABLE RIOT-RAM BYTES $83 and $84 are set from
    # distinct source bits 3 and 2 BEFORE the nine-row visible kernel.
    m0=source_framelo&8;m2=source_framelo&4
    return [43+(6 if m0 else 0),75,129+(6 if m2 else 0),183,243,303],m0,m2,source_framelo

def independent_white_union(im,req):
    rgb=im.convert('RGB');p=rgb.load()
    ys={(x,y) for y in range(50,195) for x in range(336)
        if min(p[x,y])>180 and max(p[x,y])-min(p[x,y])<40}
    if not ys:
        return {'exact':False,'failure':'NO_ORIGINAL_WHITE_PIXEL'}
    y0=min(y for x,y in ys)
    want=set()
    per_sprite=[]
    for i,(t,x0) in enumerate(zip(TYPES,req)):
        pixelset={(x0+dx,y0+dy) for dx,dy in legacy.MASKS[t]}
        if any(x>=336 or x<0 for x,y in pixelset):
            return {'exact':False,'failure':'MASK_WOULD_CROSS_PLAYFIELD'}
        want.update(pixelset)
        per_sprite.append([len({(x,y) for x,y in pixelset if y==y0+r} - ys) for r in range(9)])
    surplus=ys-want;lost=want-ys
    return {'exact':not lost and not surplus,
            'missing':len(lost),'ghost':len(surplus),
            'row_missing_per_sprite':per_sprite,
            'white_count':len(ys),'source_white_count':len(want),
            'example_missing':sorted(lost)[:5],'example_ghost':sorted(surplus)[:5]}

def check(im,expected):
    # F2 matching independently detects/labels individual source masks and
    # verifies P0/M0/PF and 262 NTSC. Dynamic source index0 is authorized.
    legacy.BASE[0]=expected[0]
    first=legacy.audit_image(im,expected)
    second=independent_white_union(im,expected)
    ok=bool(first.get('exact') and second['exact'])
    return first,second,ok

def mutants(src,req,directory):
    directory.mkdir(parents=True,exist_ok=True)
    im=src.convert('RGB')
    fst,snd,ok=check(im,req)
    assert ok,('cannot calibrate mutants against failed genuine source frame',fst,snd)
    y0=fst['y0']
    tests={}
    def test(name,clone,request):
        path=directory/(name+'_SYNTHETIC_TESTDATA_NOT_STELLA.png')
        clone.save(path)
        a,b,passed=check(clone,request)
        assert not passed,('mutant escaped',name,a,b)
        tests[name]={'detected':True,'legacy_exact':a.get('exact'),
                     'union_exact':b.get('exact'),
                     'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
    # 1. Erase original white mask pixel for selected index0.
    px,py=next((req[0]+dx,y0+dy) for dx,dy in sorted(legacy.MASKS[TYPES[0]])
               if legacy.white(im.getpixel((req[0]+dx,y0+dy))))
    altered=im.copy();altered.putpixel((px,py),(0,0,0))
    test('MUTANT_ERASE_ONE_MASK_PIXEL',altered,req)
    # 2. Additional white ghost x1-x2.
    altered=im.copy();altered.putpixel((1,y0+6),(255,255,255))
    altered.putpixel((2,y0+6),(255,255,255))
    test('MUTANT_GHOST_LEFT_EDGE',altered,req)
    # 3. Move a supposedly static source index1, preserving mask shape.
    altered=im.copy()
    staticmask={(req[1]+dx,y0+dy) for dx,dy in legacy.MASKS[TYPES[1]]}
    for xy in staticmask: altered.putpixel(xy,(0,0,0))
    for x,y in staticmask:altered.putpixel((x+6,y),(255,255,255))
    test('MUTANT_STATIC_INDEX1_MOVED_6_PIXELS',altered,req)
    # 4. Invert expected source RAM phase even though real pixels are unchanged.
    # This is a test of expected X oracle, not a simulator screenshot.
    altered=im.copy();wrong=req.copy()
    wrong[0]=49 if req[0]==43 else 43
    test('MUTANT_WRONG_SOURCE_RAM_FRAME_PHASE',altered,wrong)
    (directory/'MUTANT_NEGATIVES_RESULTS.json').write_text(json.dumps(tests,indent=2)+'\n')
    return tests

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--mode',choices=['G0','G1'],required=True)
    ap.add_argument('--raw',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--mutants',type=Path,required=True)
    a=ap.parse_args()
    paths=sorted(a.raw.glob('frame_*.png'))
    n=16 if a.mode=='G0' else 64
    assert len(paths)==n,('wrong frame count',len(paths),n)
    rows=[];modes=[];all_pass=True
    for k,p in enumerate(paths,1):
        frame=10+k
        req,m0,m2,frame_lo=expected_for(a.mode,frame)
        im=Image.open(p)
        fst,snd,ok=check(im,req)
        row=dict(debugger_frame_label=frame,source_rendered_FRAMELO=frame_lo,
            riotr_ram_83_x0=m0,riot_ram_84_x2=m2,mode_pair=f'{1 if m0 else 0}{1 if m2 else 0}',
            source_mask_types=TYPES,requested_X=req,rendered_X=fst.get('rendered'),
            original_9_row_pixel_costs=fst.get('mask_row_costs'),
            static_four_unchanged=all(fst.get('rendered',[])[j]==BASE[j] for j in [1,3,4,5]) if len(fst.get('rendered',[]))==6 else False,
            P0_yellow=fst.get('P0_yellow'),M0_active=fst.get('M0_active'),
            PF_brown_left=fst.get('PF_brown_left'),PF_brown_right=fst.get('PF_brown_right'),
            NTSC_262=fst.get('ntsc262'),source_exact_legacy=fst.get('exact'),
            source_exact_union=snd.get('exact'),white_missing=snd.get('missing'),
            white_ghost=snd.get('ghost'),PASS=ok,raw_image=p.name,
            original_raw_sha256=hashlib.sha256(p.read_bytes()).hexdigest())
        rows.append(row);modes.append(row['mode_pair']);all_pass &= bool(ok)
        print('F3_REAL_STELLA',a.mode,frame,row['mode_pair'],req,fst.get('rendered'),ok,'maskcosts',fst.get('mask_costs'))
    negative=mutants(Image.open(paths[0]),rows[0]['requested_X'],a.mutants)
    if a.mode=='G1':
        counts=Counter(modes)
        assert counts=={'00':16,'01':16,'11':16,'10':16},counts
        order=['00','01','11','10']
        transitions=[]
        for k in range(1,n):
            if modes[k]!=modes[k-1]:
                a0,a2=map(int,modes[k-1]);b0,b2=map(int,modes[k])
                assert (a0^b0)+(a2^b2)==1,('non-independent transition',k,modes[k-1],modes[k])
                transitions.append((10+k,modes[k-1],modes[k]))
        assert len(transitions)>=12,(len(transitions),'insufficient independent transitions')
        print('F3_TRUE_GRAY_MODE_TRANSITIONS',len(transitions),transitions)
    a.out.parent.mkdir(exist_ok=True,parents=True)
    a.out.write_text(json.dumps({'mode':a.mode,'frame_count':n,'all_exact':all_pass,
       'negative_mutants':negative,'source_of_requested_X':'ROM FRAMELO bit3/bit2 to two independently writable RIOT RAM $83/$84; completed Stella frame = debugger frame label -2',
       'no_synthetic_emulator_evidence':True,'per_frame':rows},indent=2)+'\n')
    print('F3_STRICT_AUDIT',a.mode,'exact',sum(r['PASS'] for r in rows),'/',n)
    if not all_pass:raise SystemExit(2)
if __name__=='__main__':main()
