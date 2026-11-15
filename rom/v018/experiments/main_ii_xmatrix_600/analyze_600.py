#!/usr/bin/env python3
"""Audit actual 600 cropped Stella 6.7.1 debugger captures.
Fail closed: unknown frame IDs or HUD scanline text are NOT 262 evidence.
All masks are original (main/design/NPC_REFERENCE_8x9_masks.json).
"""
from pathlib import Path
from collections import Counter
from PIL import Image
import csv,hashlib,json,sys

ROOT=Path(__file__).resolve().parent
RAWDIR=ROOT/"evidence_600"/"raw"
MALE=[0x3c,0x3c,0x18,0xff,0x18,0x24,0x24,0x42,0x42]
FEMALE=[0x3c,0x3c,0x18,0xff,0x3c,0x7e,0x7e,0x24,0x24]
A=[1,2,3,1,2,3,1,2]
B=[1,1,1,2,2,2,3,3]
SCAN_262="a169787b7bdcf465b5a1b7505dca83c31f60fa2c16337d39fea3e957ea13ace2"

def white(p):
    return min(p)>180 and max(p)-min(p)<40
def yellow(p):
    return p[0]>120 and p[1]>100 and p[2]<100
def glyph(im,x):
    return tuple(yellow(im.getpixel((xx,yy))) for yy in range(9,19) for xx in range(x,x+7))
def digit_templates(files):
    out={}
    for j in range(1,11):
        im=Image.open(files[j-1]).convert("RGB")
        out[(10+j)%10]=glyph(im,579)
    if len(set(out.values()))!=10:
        raise ValueError("Cannot calibrate 10 distinct Stella frame digit glyphs")
    return out
def frame_id(im,patterns):
    digits=[]
    for x in (561,570,579):
        g=glyph(im,x)
        if not any(g):continue
        matches=[digit for digit,pattern in patterns.items() if g==pattern]
        if len(matches)!=1:return None
        digits.append(str(matches[0]))
    return int("".join(digits)) if digits else None

def analyze(im,frame,patterns):
    if im.size!=(900,300):
        return {"error":"bad_resolution","size":im.size}
    n=frame_id(im,patterns)
    white_pixels=[(x,y) for y in range(97,106) for x in range(55,450) if white(im.getpixel((x,y)))]
    xs=sorted(set(x for x,y in white_pixels))
    ranges=[]
    if xs:
        left=prev=xs[0]
        for x in xs[1:]:
            if x>prev+1:
                ranges.append((left,prev))
                left=x
            prev=x
        ranges.append((left,prev))
    masks=[]
    for x0,x1 in ranges:
        if x1-x0<14:continue
        rows=[]
        for y in range(97,106):
            b=0
            for k in range(8):
                b=(b<<1)|int(white(im.getpixel((x0+2*k,y))))
            rows.append(b)
        masks.append({"x_gui":x0+103,"x_cropped":x0,
            "male_bit_errors":sum((a^b).bit_count() for a,b in zip(rows,MALE)),
            "female_bit_errors":sum((a^b).bit_count() for a,b in zip(rows,FEMALE))})
    unexplained=[(x,y) for x,y in white_pixels if not any(m["x_cropped"]<=x<m["x_cropped"]+16 for m in masks)]
    yellow_player=sum(yellow(im.getpixel((x,y))) for y in range(97,106) for x in range(1,40))
    yellow_missile=sum(yellow(im.getpixel((x,101))) for x in range(120,150))
    if n is None:
        phase=None
    else:
        phase=(n//16)%8
    expected=None
    if phase is not None:
        expected=[196+30*(A[phase]-1),334+30*(A[phase]+B[phase]-2)]
    x_pair=[m["x_gui"] for m in masks]
    exact_masks=(len(masks)==2 and masks[0]["male_bit_errors"]==0 and masks[1]["female_bit_errors"]==0)
    expected_positions=(x_pair==expected)
    scanhash=hashlib.sha256(im.crop((558,25,594,46)).tobytes()).hexdigest()
    return {
        "expected_image_index":frame,
        "expected_frame_id":10+frame,
        "observed_frame_id":n,
        "phase":phase,
        "a_delay":A[phase] if phase is not None else None,
        "b_delay":B[phase] if phase is not None else None,
        "male_x_gui":x_pair[0] if len(masks)>0 else None,
        "female_x_gui":x_pair[1] if len(masks)>1 else None,
        "expected_male_x_gui":expected[0] if expected else None,
        "expected_female_x_gui":expected[1] if expected else None,
        "masks_exact":exact_masks,
        "positions_exact":expected_positions,
        "extra_white_pixel_count":len(unexplained),
        "yellow_player_pixel_count":yellow_player,
        "yellow_missile_pixel_count":yellow_missile,
        "scan_262_exact_hud":scanhash==SCAN_262,
        "scan_hud_sha256":scanhash
    }

def main():
    files=sorted(RAWDIR.glob("frame_*.png"))
    if len(files)!=600: raise ValueError(f"Expected exactly 600 captured frames: {len(files)}")
    patterns=digit_templates(files)
    result=[]
    for j,p in enumerate(files,1):
        with Image.open(p) as src:
            result.append(analyze(src.convert("RGB"),j,patterns))
    fields=list(result[0])
    with (ROOT/"evidence_600"/"frames_600.csv").open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(result)
    frame_sequential=all(r["observed_frame_id"]==r["expected_frame_id"] for r in result)
    histogram=Counter(r["phase"] for r in result)
    scans=sum(r["scan_262_exact_hud"] for r in result)
    masks=sum(r["masks_exact"] for r in result)
    positions=sum(r["positions_exact"] for r in result)
    ghost=sum(r["extra_white_pixel_count"] for r in result)
    p0=sum(r["yellow_player_pixel_count"]>0 for r in result)
    m0=sum(r["yellow_missile_pixel_count"]>0 for r in result)
    summary={
        "evidence_class":"REAL_STELLA_6_7_1_600_SEQUENTIAL_X11_DEBUGGER_CROPS",
        "frame_count":len(result),
        "frame_ids_consecutive_11_to_610":frame_sequential,
        "stella_hud_262_frames":scans,
        "both_original_masks_bit_exact_frames":masks,
        "both_expected_x_positions_frames":positions,
        "frames_with_p0_yellow":p0,
        "frames_with_m0_yellow":m0,
        "extra_white_pixels_total":ghost,
        "phase_frame_counts":dict(sorted(histogram.items(),key=lambda z:str(z[0]))),
        "frame_errors":[r for r in result if
          r["observed_frame_id"]!=r["expected_frame_id"] or
          not r["scan_262_exact_hud"] or not r["masks_exact"] or
          not r["positions_exact"] or r["extra_white_pixel_count"]!=0 or
          r["yellow_player_pixel_count"]==0 or r["yellow_missile_pixel_count"]==0][:20],
        "status":"LOCAL_PASS_600" if
           frame_sequential and scans==600 and masks==600 and
           positions==600 and ghost==0 and p0==600 and m0==600 and
           len(histogram)==8 else "FAIL_OR_INCONCLUSIVE",
        "limitations":"Only eight coarse A/B timings, no overlap/near-X, no full six NPC, no PF walls, no independent VERIFICATION."
    }
    (ROOT/"evidence_600"/"summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps({k:v for k,v in summary.items() if k!="frame_errors"},indent=2,ensure_ascii=False))
    if summary["frame_errors"]:print("ERROR SAMPLES",json.dumps(summary["frame_errors"][:4],indent=2,ensure_ascii=False))
    sys.exit(0 if summary["status"]=="LOCAL_PASS_600" else 1)
if __name__=="__main__": main()
