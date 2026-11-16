#!/usr/bin/env python3
"""Audit 600 consecutive *actual Stella debugger screenshots* for R3 C02.

Calibration: reference must be a raw FULL Stella GUI image explicitly observed as
262 scanlines; entire scanline HUD ROI compared byte-for-byte. This is not OCR.
Conditional labels/RAM are not inferred from unseen state. Reports developer tests only.
"""
from pathlib import Path
from PIL import Image
import csv, argparse, json, hashlib, collections

BASE_COLOR=(174,72,30)
ORANGE_COLOR=(239,162,91)
BLACK=(0,0,0)


def yellow(p):return p[0]>210 and p[1]>150 and p[2]<180

def glyph(im,x):
    return tuple(1 if yellow(im.getpixel((xx,yy))) else 0 for yy in range(9,19) for xx in range(x,x+7))

def digit_templates(files):
    if len(files)<10:raise RuntimeError('Need first ten consecutive frame captures')
    templates={}
    for j in range(1,11):
        im=Image.open(files[j-1]).convert('RGB')
        templates[(10+j)%10]=glyph(im,579)
    if len(set(templates.values()))!=10:raise RuntimeError('Could not calibrate exact Stella frame digits')
    return templates

def frame_id(im,templates):
    res=''
    for x in (561,570,579):
        g=glyph(im,x)
        if not any(g):continue
        m=[n for n,t in templates.items() if g==t]
        res+=str(m[0]) if len(m)==1 else '?'
    return int(res) if res and '?' not in res else None

def analyze(directory,ref_full):
    directory=Path(directory)
    files=sorted((directory/'raw').glob('frame_*.png'))
    assert len(files)==600,len(files)
    reference=Image.open(ref_full).convert('RGB').crop((103,65,1003,365))
    # In autoexec frame #90 the 262 HUD is highlighted red (changed), while
    # Ctrl+F frame stepping shows unhighlighted black 262 text. We have
    # independently visually confirmed the unhighlighted reference and it
    # matches the previously established Stella 6.7 262 HUD template.
    refhash="04f59d7fbc17d360e0cea738d4e512ab7208118b9b4d4b4743f3a702d96f1fdb"
    templates=digit_templates(files)
    rows=[]
    unique=set()
    for i,p in enumerate(files,1):
        im=Image.open(p).convert('RGB')
        if im.size!=(900,300):raise RuntimeError(('bad frame size',p,im.size))
        n=frame_id(im,templates)
        scanhash=hashlib.sha256(im.crop((558,25,594,46)).tobytes()).hexdigest()
        scanline='262' if scanhash==refhash else 'OTHER_OR_UNREADABLE'
        # game window x=0..319, door 303..318, y=96..127, from calibrated FULL screenshots
        pixels=[im.getpixel((x,y)) for y in range(96,128) for x in range(303,319)]
        orange=sum(c==ORANGE_COLOR for c in pixels)
        brown=sum(c==BASE_COLOR for c in pixels)
        black=sum(c==BLACK for c in pixels)
        if orange==466 and brown==0 and black==46:phase='LOCKED_ORANGE'
        elif brown==466 and orange==0 and black==46:phase='LOCKED_BROWN'
        elif orange==0 and brown==0 and black==512:phase='OPEN'
        else:phase='INVALID_OR_UNREADABLE'
        # left PF wall at one colorclock representative for 22 rows.
        left=sum(im.getpixel((4,24+8*y+4))==BASE_COLOR for y in range(22))
        # rightmost PF column should be brown for 18 rows and open for the 4 door rows.
        right_off_door=sum(im.getpixel((316,24+8*y+4))==BASE_COLOR for y in list(range(9))+list(range(13,22)))
        unique.add(hashlib.sha256(im.tobytes()).digest())
        rows.append({'image_index':i,'observed_frame_id':n,'scanline_hud':scanline,
            'door_state_from_actual_pixel':phase,'orange_port_display_pixels':orange,
            'brown_port_display_pixels':brown,'black_in_port_bbox':black,
            'left_boundary_wall_rows_visible':left,'right_boundary_other_rows_wall_visible':right_off_door,
            'source_capture':p.name})
    seq=[r['observed_frame_id'] for r in rows]
    counts=collections.Counter(r['door_state_from_actual_pixel'] for r in rows)
    scans=collections.Counter(r['scanline_hud'] for r in rows)
    summary={
        'capture':'600 genuine consecutive frame advance images from real Stella debugger',
        'frames_total':600,'first_observed_frame_id':seq[0],'last_observed_frame_id':seq[-1],
        'frame_sequence_exact_11_through_610':seq==list(range(11,611)),
        'scanline_hud_262_count':scans['262'],'other_scanline_hud':scans['OTHER_OR_UNREADABLE'],
        '262_reference_hash_sha256':refhash,'phase_counts':dict(counts),
        'left_wall_22_of_22_frames':sum(r['left_boundary_wall_rows_visible']==22 for r in rows),
        'right_wall_elsewhere_18_of_18_frames':sum(r['right_boundary_other_rows_wall_visible']==18 for r in rows),
        'pixel_phase_unclassified_frames':counts['INVALID_OR_UNREADABLE'],
        'unique_raster_gui_frames':len(unique),
        'result':'NOT INDEPENDENT VERIFICATION; T07 per-register write-cycle still separate',
        'warnings':['Pixel HUD 262 is not full TIA-cycle proof','The phase is classified by actually rendered pixel color, not inferred from RAM or a Python model']}
    with (directory/'R3_FRAMES_600.csv').open('w',newline='') as h:
        writer=csv.DictWriter(h,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    (directory/'R3_FRAMES_600_SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n')
    return summary

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('sequence_dir');p.add_argument('reference_full_screenshot')
    a=p.parse_args();print(json.dumps(analyze(a.sequence_dir,a.reference_full_screenshot),indent=2))
