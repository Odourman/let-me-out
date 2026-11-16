#!/usr/bin/env python3
"""R1-F4 actual Stella pixel audit: two independent 8x9 union implementations.
Geometry uses observed physical X for shape, but a SEPARATELY PREREGISTERED
time-based requested_X from source-only preflight, never screenshot-derived.
NO sprite movement is FAIL/NO_RESPONSE, not successful geometry.
"""
from pathlib import Path
from PIL import Image
import argparse,hashlib,json
import r1_f2_checker as f2
TYPES=['large_male','large_male','large_female','large_female','small_male','small_female']
STATIC=[75,129,183,243,303]
BASE=[43]+STATIC
WIDTH=336
def h(path):return hashlib.sha256(path.read_bytes()).hexdigest()
# Independent matcher A: all actual image-white coordinates as XY set,
# exact union against all six original masks. No automatic "six groups" assumption.
def set_union(im):
    im=im.convert('RGB')
    pix=im.load()
    white={(x,y) for y in range(50,195) for x in range(WIDTH)
           if min(pix[x,y])>180 and max(pix[x,y])-min(pix[x,y])<40}
    if not white:return {'best_x':None,'cost':None,'exact_candidates':[],
                         'failure':'no white sprite source pixels'}
    y0=min(y for x,y in white)
    fixed=set()
    for typ,x0 in zip(TYPES[1:],STATIC):
        fixed|={(x0+dx,y0+dy) for dx,dy in f2.MASKS[typ]}
    tries=[]
    for x0 in range(0,80):
        wanted=fixed|{(x0+dx,y0+dy) for dx,dy in f2.MASKS[TYPES[0]]}
        cost=len(white^wanted)
        tries.append((cost,x0,len(white-wanted),len(wanted-white)))
    tries.sort()
    return {'y0':y0,'best_x':tries[0][1],'cost':tries[0][0],
            'extra':tries[0][2],'missing':tries[0][3],
            'exact_candidates':[x for n,x,ex,miss in tries if n==0],
            'white_count':len(white),'closest_three':tries[:3]}
# Independent matcher B: per-scanline 336-bit integer occupancy and XOR popcount;
# no group finder and no XY-set operations or arbitrary one-sprite edit.
def bitrow_union(im):
    pix=im.convert('RGB').load()
    rows=[]
    for y in range(50,195):
        bits=0
        for x in range(WIDTH):
            r,g,b=pix[x,y]
            if min(r,g,b)>180 and max(r,g,b)-min(r,g,b)<40:
                bits|=1<<x
        rows.append(bits)
    nonempty=[i for i,b in enumerate(rows) if b]
    if not nonempty:return {'best_x':None,'cost':None,'exact_candidates':[]}
    y0=50+nonempty[0]
    actual=rows[nonempty[0]:nonempty[0]+9]
    # Extra rows outside the original nine are cost, not silently ignored.
    outside=sum(b.bit_count() for i,b in enumerate(rows) if i<nonempty[0] or i>=nonempty[0]+9)
    def mask_row(typ,row,x0):
        bits=f2.J['sprites'][typ][row]
        res=0
        for j,ch in enumerate(bits):
            if ch=='1':res|=(3<<(x0+2*j))
        return res
    fixed=[0]*9
    for typ,x0 in zip(TYPES[1:],STATIC):
        for row in range(9):fixed[row]|=mask_row(typ,row,x0)
    tries=[]
    for x0 in range(0,80):
        wanted=[fixed[row]|mask_row(TYPES[0],row,x0) for row in range(9)]
        costs=[(actual[row]^wanted[row]).bit_count() for row in range(9)]
        tries.append((sum(costs)+outside,x0,costs))
    tries.sort()
    return {'y0':y0,'best_x':tries[0][1],'cost':tries[0][0],
            'row_costs':tries[0][2],'outside_cost':outside,
            'exact_candidates':[x for n,x,cs in tries if n==0],
            'closest_three':tries[:3]}
def inspect(im,phase,expected):
    a=set_union(im);b=bitrow_union(im)
    # P0/M0/PF/262 color and HUD tests from frozen F2 checker, no use of
    # F2's x-group segmentation for exact 8x9 mask or observed geometry.
    controls=f2.audit_image(im,expected)
    same=(a.get('exact_candidates')==b.get('exact_candidates') and
          a.get('y0')==b.get('y0'))
    unique=(len(a.get('exact_candidates',[]))==1 and len(b.get('exact_candidates',[]))==1)
    x=a.get('exact_candidates',[None])[0] if unique else a.get('best_x')
    colors=all(controls.get(k) for k in ('P0_yellow','M0_active','PF_brown_left','PF_brown_right','ntsc262'))
    exactly=bool(unique and same and a['cost']==0 and b['cost']==0 and a['y0']==96 and colors)
    return {'first_path_set':a,'second_path_row_bits':b,'rendered_x':[x]+STATIC if x is not None else None,
            'requested_linear_model_X':expected,'expected_shift_is_only_hypothesis':True,
            'linear_model_matches':([x]+STATIC==expected) if x is not None else False,
            'controls_P0_M0_PF_NTSC':{k:controls.get(k) for k in ('P0_yellow','M0_active','PF_brown_left','PF_brown_right','ntsc262')},
            'both_independent_masks_exact':exactly,
            'verified_all_nine_original_rows':exactly,
            'FIRST_X_ACTUALLY_MOVED':exactly and x!=43}
def mutant(src,phase,expected,result,out):
    if not result['both_independent_masks_exact']:return {'executed':False,'reason':'baseline real frame not source exact'}
    out.mkdir(parents=True,exist_ok=True)
    im=src.convert('RGB')
    y0=result['first_path_set']['y0'];x=result['rendered_x'][0]
    original=sorted(f2.MASKS[TYPES[0]])
    xy=next((x+dx,y0+dy) for dx,dy in original if f2.white(im.getpixel((x+dx,y0+dy))))
    modified=im.copy();modified.putpixel(xy,(25,25,25))
    bad=out/'MUTANT_ERASE_REAL_MASK_PIXEL_SYNTHETIC_NOT_STELLA.png'
    modified.save(bad)
    test=inspect(modified,phase,expected)
    assert not test['both_independent_masks_exact'],('mutant escaped checker',test)
    return {'executed':True,'label':'SYNTHETIC_MUTANT_NOT_REAL_STELLA',
            'filename':bad.name,'sha256':h(bad),
            'detected_set_matcher':test['first_path_set']['cost']>0,
            'detected_bitrow_matcher':test['second_path_row_bits']['cost']>0}
def main():
    p=argparse.ArgumentParser()
    p.add_argument('--phase',type=int,choices=[18,21],required=True)
    p.add_argument('--raw',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True)
    p.add_argument('--mutants',type=Path,required=True)
    a=p.parse_args()
    phase=a.phase
    meta_file=Path(__file__).resolve().parent/'dist'/f'r1_f4_6B_I0_C{phase:02d}_I2_FIXED_meta.json'
    meta=json.loads(meta_file.read_text())
    pre=json.loads((Path(__file__).resolve().parent/'r1_f4_source_preflight.json').read_text())
    requested=pre['linear_requested_crop_X_prior_to_stella'][f'c{phase}']
    assert requested==meta['linear_requested_crop_X_before_real_Stella']
    # Prior X independent from rendered images and immutable before Stella is run.
    assert requested==[37 if phase==18 else 55,75,129,183,243,303]
    paths=sorted(a.raw.glob('frame_*.png'))
    assert len(paths)==16,(len(paths),a.raw,'must have 16 sequential Stella images')
    raw=[]
    for i,path in enumerate(paths,1):
        im=Image.open(path)
        assert im.size==(900,300),(im.size,path)
        v=inspect(im,phase,requested)
        v['file']=path.name;v['raw_png_sha256']=h(path);v['real_stella_debugger_frame_label']=10+i
        raw.append(v)
        print('F4_GENUINE_STELLA',phase,10+i,
              'OBS_X',v['rendered_x'],'LINEAR_REQUESTED',requested,
              'PIXEL_EXACT',v['both_independent_masks_exact'],'ACTUAL_MOVE',v['FIRST_X_ACTUALLY_MOVED'],
              'SET_DIFFERENCE',v['first_path_set']['cost'],'BITROW_DIFFERENCE',v['second_path_row_bits']['cost'])
    allshape=all(v['both_independent_masks_exact'] for v in raw)
    allshift=all(v['FIRST_X_ACTUALLY_MOVED'] for v in raw)
    positions={v['rendered_x'][0] for v in raw if v['rendered_x']}
    if not allshape:status='DESTRUCTIVE_FAIL_OR_IMAGE_INCONCLUSIVE'
    elif allshift and len(positions)==1:status='F4_INDEX0_PHASE_GEOMETRY_LOCAL_PASS'
    elif allshape and positions=={43}:status='F4_NO_SECOND_X_PHASE_RESPONSE'
    else:status='INCONCLUSIVE_UNSTABLE_FIRST_X'
    mutant_res=mutant(Image.open(paths[0]),phase,requested,raw[0],a.mutants)
    output={'F4_phase':phase,'G0_source_only_status':pre['F4_G0'],
        'classification':status,'actual_position_set':sorted(positions),
        'all_16_source_union_exact':allshape,'all_16_moved':allshift,
        'requested_timing_pre_registered':{'first_resp_c':phase,'first_grp_c':meta['first_GRP1_CPU_cycle_SOURCE_ONLY'],
        'linear_crop_requested_X_hypothesis':requested,'baseline_crop_X':[43,75,129,183,243,303]},
        'real_stella_frames':raw,'mutant_negative':mutant_res,
        'no_synthetic_images_used_as_positive_evidence':True}
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(output,indent=2)+'\n')
    print('F4_PROBE_FINAL_CLASSIFICATION',phase,status,'positions',sorted(positions))
    if status in ('DESTRUCTIVE_FAIL_OR_IMAGE_INCONCLUSIVE','INCONCLUSIVE_UNSTABLE_FIRST_X'):
        raise SystemExit(3)
if __name__=='__main__':main()
