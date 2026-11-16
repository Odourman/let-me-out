#!/usr/bin/env python3
"""Developer-only pixel audit of authentic Stella 6.7.1 R3/C02 GUI screenshots.

All coordinates are calibrated to full 1366x900 X11 image of Stella Debugger.
This is not independent verification and is not per-TIA CPU cycle tracing.
"""
from pathlib import Path
import argparse, json, re, hashlib
from PIL import Image

BROWN=(174,72,30)
ORANGE=(239,162,91)
BLACK=(0,0,0)
BASE_X=103
BASE_Y=89

def analyze(folder):
    folder=Path(folder)
    grid=json.loads((folder/'dist/source_geometry.json').read_text())['grid_exact']
    shots={n:Image.open(folder/'evidence'/n/'stella_full.png').convert('RGB') for n in ('new_brown','new_orange','new_open')}
    actual=shots['new_open']
    scored=0
    mismatches=[]
    for y in range(176):
        for x in range(40):
            rgb=actual.getpixel((BASE_X+8*x+4,BASE_Y+y))
            observed=rgb==BROWN
            expected=(grid[y//8][x]=='#')
            scored+=observed==expected
            if observed!=expected:mismatches.append({'x':x,'line':y,'rgb':rgb,'expected':expected})
    assert scored==176*40,(scored,mismatches[:10])
    assert all(row[0]=='#' for row in grid)
    assert [y for y,row in enumerate(grid) if row[39]=='D']==[9,10,11,12]
    # Derive expected door mask from the actual generated .inc used by DASM.
    text=(folder/'dist/r3_tables.inc').read_text()
    s=text.split('DOORROWS:\n',1)[1]
    ints=[int(v,16) for v in re.findall(r'\$([0-9A-F]{2})',s)]
    assert len(ints)==176,len(ints)
    mask=ints[9*8:13*8]
    assert len(mask)==32 and sum(int.bit_count(v) for v in mask)==233
    orange_pixels=[(x,y) for y in range(BASE_Y,BASE_Y+176) for x in range(BASE_X,BASE_X+320)
                   if shots['new_orange'].getpixel((x,y))==ORANGE]
    assert orange_pixels
    x0=min(x for x,y in orange_pixels)
    y0=min(y for x,y in orange_pixels)
    assert (x0,y0)==(406,161),(x0,y0)
    fidelity=0
    for j in range(32):
        for i in range(8):
            expect=bool(mask[j]&(1<<(7-i)))
            pix=shots['new_orange'].getpixel((x0+i*2+1,y0+j))
            if (pix==ORANGE)==expect:fidelity+=1
    assert fidelity==256,fidelity
    # Exact difference between ROM phases: only P1 door graphics may change.
    diff={}
    for a,b in (('new_brown','new_orange'),('new_orange','new_open')):
        changes=[(x,y) for y in range(BASE_Y,BASE_Y+176) for x in range(BASE_X,BASE_X+320)
                 if shots[a].getpixel((x,y))!=shots[b].getpixel((x,y))]
        diff[a+'_vs_'+b]={'changed_display_pixels':len(changes),'bounding_box':[
            min(x for x,y in changes),min(y for x,y in changes),max(x for x,y in changes),max(y for x,y in changes)],
            'outside_expected_gate_pixels':sum(not (x0<=x<x0+16 and y0<=y<y0+32) for x,y in changes)}
        assert len(changes)==466 and diff[a+'_vs_'+b]['outside_expected_gate_pixels']==0
    out={
      'test':'R3 C02 original-map-and-separate-keyhole Stella screenshot pixel audit',
      'status':'DEVELOPER_LOCAL_PASS limited visual requirements; not full R3/independent verification',
      'map_176_scanlines_40_cells_samples_matched':scored,'map_samples_total':176*40,
      'left_wall_columns_22_of_22':'CLOSED','right_door_only_rows':[9,10,11,12],
      'R3_keyhole_source_mask_pixels_matching_real_stella':fidelity,'mask_pixels_total':256,
      'orange_P1_on_pixels_in_8x32':233,'black_transparent_keyhole_pixels_in_8x32':23,
      'actual_port_bounds_GUI':[x0,y0,x0+15,y0+31],
      'locked_brown_rgb':BROWN,'locked_orange_rgb':ORANGE,
      'phase_diff':diff,'raw_evidence':{k:hashlib.sha256((folder/'evidence'/k/'stella_full.png').read_bytes()).hexdigest() for k in shots},
      'limitations':['Pixel grid and door masks checked in Stella Debugger GUI, not standalone CRT output',
        'Full 600 frames must be assessed separately','Full TIA write-cycle trace must be assessed separately',
        'Recognition of keyhole shape is visual/human and cannot be established by mask exactness alone']}
    return out

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('artifact_dir');p.add_argument('--out')
    args=p.parse_args();result=analyze(args.artifact_dir)
    print(json.dumps(result,indent=2))
    if args.out:Path(args.out).write_text(json.dumps(result,indent=2)+'\n')
