#!/usr/bin/env python3
"""Fail-closed objective R1 phase1 microscope on *real* Stella X11 frame screenshots.
Each NPC must be exactly 9 rows of either canonical large-male or large-female
source bytes. Report both top-to-bottom and byte-reversed orientations distinctly.
No simulated rendering is accepted as raster evidence.
"""
from pathlib import Path
from PIL import Image
from collections import Counter
import json,hashlib,sys,csv
R=Path(__file__).resolve().parent
REPO=R.parents[3]
canon=json.loads((R/'canon_masks.json').read_text())['sprites']
files=sorted((R/'evidence/pilot/raw').glob('frame_*.png'))
assert len(files)==24,len(files)
# Native source array is top to bottom in JSON; prior R1af code selects Y 8 down to 0.
def make_points(rows):
    return {(2*bit+d,row) for row,b in enumerate(rows) for bit in range(8) for d in (0,1) if int(b,2) & (0x80>>bit)}
SPRITES={name:{'literal':make_points(canon[name]),'reverse':make_points(canon[name][::-1])} for name in ('large_male','large_female')}
player_rows=['00111100','01111110','00011000','01111110','00011110','00111100','00011000','00100100','01000010']
PLAYER={kind:make_points(rows) for kind,rows in [('literal',player_rows),('reverse',player_rows[::-1])]}
def brown(p):
    r,g,b=p[:3]
    return r>=65 and g>=22 and r>=g*1.25 and g>=b*1.15 and b<110 and not (r>185 and g>140)
def white(p):
    rgb=p[:3]
    return min(rgb)>180 and max(rgb)-min(rgb)<40
def yellow(p):
    r,g,b=p[:3]
    return r>120 and g>100 and b<100 and not brown(p)
def shift(s,x,y):return {(u+x,v+y) for u,v in s}
rows=[]
for index,p in enumerate(files,1):
    im=Image.open(p).convert('RGB')
    assert im.size==(900,300),im.size
    pix=im.load()
    whites={(x,y) for y in range(50,195) for x in range(336) if white(pix[x,y])}
    yellows={(x,y) for y in range(50,195) for x in range(336) if yellow(pix[x,y])}
    y0=min((y for x,y in whites),default=-1)
    matches=[]
    if y0>=0:
        for orient in ('literal','reverse'):
            m=SPRITES['large_male'][orient];f=SPRITES['large_female'][orient]
            mx=[x for x in range(0,320) if shift(m,x,y0).issubset(whites)]
            fx=[x for x in range(0,320) if shift(f,x,y0).issubset(whites)]
            matches.extend([(orient,xm,xf) for xm in mx for xf in fx
                            if shift(m,xm,y0)|shift(f,xf,y0)==whites and xm!=xf])
    # Yellow: 9-row original player plus one 2-pixel single-shot.
    yellow_matches=[]
    for orient,template in PLAYER.items():
        for x in range(0,320):
            glyph=shift(template,x,y0)
            if glyph.issubset(yellows):
                shot=yellows-glyph
                if len(shot)==2:
                    a,b=sorted(shot)
                    if a[1]==b[1] and b[0]==a[0]+1:
                        yellow_matches.append((orient,x,a[0],a[1]))
    hud=hashlib.sha256(im.crop((558,25,594,46)).tobytes()).hexdigest()
    sample={
      'image':p.name,'frame_from_script':index+10,'nine_line_y0':y0,
      'white_pixels':len(whites),'yellow_pixels':len(yellows),
      'exact_2_mask_combos':len(matches),
      'modes':'|'.join(a[0] for a in matches),
      'male_x':matches[0][1] if matches else '',
      'female_x':matches[0][2] if matches else '',
      'both_complete_original_masks':len(matches)>0,
      'yellow_full_p0_and_1_m0':len(yellow_matches)>0,
      'ntsc_hud_refhash':hud,
      'brown_left_9lines':all(sum(brown(pix[x,y]) for x in range(0,32))>=3 for y in range(y0,y0+9)) if y0>=0 else False,
      'brown_right_9lines':all(sum(brown(pix[x,y]) for x in range(300,336))>=3 for y in range(y0,y0+9)) if y0>=0 else False,
    }
    rows.append(sample)
    if index<=8:print('PILOT',index,[(a[0],a[1],a[2]) for a in matches],len(whites),len(yellows),len(yellow_matches))
with (R/'dist/pilot_results.csv').open('w') as fp:
    writer=csv.DictWriter(fp,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
X_pairs=sorted(set((r['male_x'],r['female_x']) for r in rows if r['both_complete_original_masks']))
summary={
 'real_Stella_GUI_frames':len(rows),
 'source_blob':'058800a4c1904d1ff289e7e61b3902aa111ba16d',
 'two_full_original_masks_frames':sum(r['both_complete_original_masks'] for r in rows),
 'two_exact_independently_set_X_combinations':X_pairs,
 'all_2_by_2_independent_factor_crossproduct':len({a for a,b in X_pairs})>=2 and len({b for a,b in X_pairs})>=2 and len(X_pairs)==len({a for a,b in X_pairs})*len({b for a,b in X_pairs}),
 'full_yellow_P0_M0_frames':sum(r['yellow_full_p0_and_1_m0'] for r in rows),
 'brown_left_rows_frames':sum(r['brown_left_9lines'] for r in rows),
 'brown_right_rows_frames':sum(r['brown_right_9lines'] for r in rows),
 'scanline_HUD_values_not_yet_interpreted':dict(Counter(r['ntsc_hud_refhash'] for r in rows)),
 'conclusion':'RUN_NOT_ACCEPTED_UNTIL_REAL_MASKS_AND_262_HUD_AND_TIA_TRAPS_AUDITED',
}
(R/'dist/pilot_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
if summary['two_full_original_masks_frames'] !=24:
    raise SystemExit('FAIL: not all 24 real Stella captures show two complete original 8x9 masks')
if summary['full_yellow_P0_M0_frames'] !=24:
    raise SystemExit('FAIL: intact P0+M0 not proven 24/24')
if not summary['all_2_by_2_independent_factor_crossproduct']:
    raise SystemExit('FAIL: two independently changing X positions not visible as full 2x2 cross-product')
if min(summary['brown_left_rows_frames'],summary['brown_right_rows_frames'])!=24:
    raise SystemExit('FAIL: two brown PF walls not preserved')
print('DEVELOPER_LOCAL_PILOT_PASS_AS_2X2_GRAPHICS_NOT_FULL_R1')
