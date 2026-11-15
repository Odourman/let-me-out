#!/usr/bin/env python3
"""Pixel-accurate auditing of raw Stella 6.7.1 debugger PNGs.

The 8x9 masks are byte-exact to main/design/NPC_REFERENCE_8x9_masks.json.
This script recognizes actual GUI pixels, not ROM mask bytes. The screenshot
ROI is fixed to the 1366x900 Stella debugger format from the CI runner.
"""
import json
import sys
from pathlib import Path
from PIL import Image

MALE = [0x3C,0x3C,0x18,0xFF,0x18,0x24,0x24,0x42,0x42]
FEMALE = [0x3C,0x3C,0x18,0xFF,0x3C,0x7E,0x7E,0x24,0x24]
BASE = Path(__file__).resolve().parent

def analyze(path):
    im = Image.open(path).convert("RGB")
    if im.size != (1366,900):
        return {"error":"unsupported_debugger_geometry","size":im.size}
    def white(x,y):
        rgb=im.getpixel((x,y))
        return min(rgb)>180 and max(rgb)-min(rgb)<40
    pixels=[(x,y) for y in range(150,190) for x in range(160,420) if white(x,y)]
    xs=sorted({x for x,y in pixels})
    if not xs:
        return {"error":"no_white_pixels","path":str(path)}
    runs=[]
    start=last=xs[0]
    for x in xs[1:]:
        if x != last+1:
            runs.append((start,last))
            start=x
        last=x
    runs.append((start,last))
    masks=[]
    for x0,x1 in runs:
        ys=[y for x,y in pixels if x0<=x<=x1]
        y0,y1=min(ys),max(ys)
        if x1-x0<7 or y1-y0<6:
            continue
        bits=[]
        for y in range(y0,y0+9):
            row=0
            for b in range(8):
                row=(row<<1)|int(white(x0+2*b,y))
            bits.append(row)
        masks.append({
            "gui_x":x0,
            "atari_x_approx":(x0-103)/2,
            "gui_y":y0,
            "rows_hex":[f"{r:02x}" for r in bits],
            "male_mask_exact":bits==MALE,
            "female_mask_exact":bits==FEMALE,
            "male_bit_errors":sum((a^b).bit_count() for a,b in zip(bits,MALE)),
            "female_bit_errors":sum((a^b).bit_count() for a,b in zip(bits,FEMALE)),
        })
    masks.sort(key=lambda x:x["gui_x"])
    # Any white pixel NOT explained by the two exact 8x9 sprites is a ghost.
    # The M0 missile is yellow and is therefore excluded from this test.
    unexplained=[(x,y) for (x,y) in pixels if 162<=y<=170
        and not any(m["gui_x"]<=x<=m["gui_x"]+15
                    and m["gui_y"]<=y<=m["gui_y"]+8 for m in masks)]
    player=sum(1 for y in range(162,171) for x in range(105,133)
        if (lambda rgb: rgb[0]>120 and rgb[1]>100 and rgb[2]<100)(im.getpixel((x,y))))
    missile=sum(1 for x in range(230,251) if (lambda rgb: rgb[0]>120 and rgb[1]>100 and rgb[2]<100)(im.getpixel((x,166))))
    return {
        "mask_count":len(masks),
        "unexplained_white_pixel_count":len(unexplained),
        "unexplained_white_pixels":unexplained[:40],
        "masks":masks,
        "p0_yellow_pixel_count":player,
        "m0_yellow_pixel_count":missile,
        "pass_pair":len(masks)==2 and
            masks[0]["male_mask_exact"] and masks[1]["female_mask_exact"] and
            masks[0]["gui_y"]==masks[1]["gui_y"] and len(unexplained)==0 and player>0 and missile>0,
    }

def main():
    results={}
    for phase in range(4):
        image=BASE/"evidence"/f"phase_{phase}"/"stella_full.png"
        results[str(phase)]=analyze(image)
    if all(results[str(i)].get("pass_pair") for i in range(4)):
        m=lambda i: results[str(i)]["masks"][0]["gui_x"]
        f=lambda i: results[str(i)]["masks"][1]["gui_x"]
        first_free=(f(1)==f(2) and m(1)!=m(2))
        second_free=(m(1)==m(3) and f(1)!=f(3))
        results["independent_coarse_placement"]={
            "first_can_move_with_second_fixed":first_free,
            "second_can_move_with_first_fixed":second_free,
            "passed":first_free and second_free
        }
        passed=first_free and second_free
    else:
        passed=False
    results["audit_status"]="LOCAL_PASS_4_CONFIGS" if passed else "FAIL_OR_INCONCLUSIVE"
    (BASE/"evidence"/"pixel_audit.json").write_text(
        json.dumps(results,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(results,indent=2,ensure_ascii=False))
    sys.exit(0 if passed else 1)
if __name__=="__main__":
    main()
