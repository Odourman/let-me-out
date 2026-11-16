#!/usr/bin/env python3
"""Independent 2x-pixel Stella screenshot analysis: NUSIZ=$03 four-mask probe.

This audit deliberately never upgrades a duplicate to a fourth distinct NPC.
Returns nonzero if the fourth-mask probe fails. Every unexpected pixel is kept.
"""
from pathlib import Path
from PIL import Image
import json,re,hashlib,sys
ROOT=Path(__file__).resolve().parent
REF=json.loads((ROOT.parent/"main_ii_three_masks"/"REFERENCE_8x9_MASKS_FROM_MAIN.json").read_text())
NAMES=("large_male","large_female","small_male","small_female")
LABELS=("MaleRows","FemaleRows","SmallMaleRows","SmallFemaleRows")
MASKS={name:[int(bits,2) for bits in REF["sprites"][name]] for name in NAMES}
Y0=162
def white(px):
    return min(px)>180 and max(px)-min(px)<40
def yellow(px):
    return px[0]>120 and px[1]>100 and px[2]<100
def source_mask_ok(text,label,name):
    match=re.search(rf"^{label}:\s*\n\s+BYTE (.+)$",text,re.M)
    if not match:return False
    vals=[int(x.strip().replace("$","0x"),16) for x in match.group(1).split(",")]
    return vals[::-1]==MASKS[name]
def matches_mask(im,x,name):
    mismatches=0
    expected=MASKS[name]
    for row,byte in enumerate(expected):
        for bit in range(8):
            on=bool(byte & (1<<(7-bit)))
            for dx in (0,1):
                mismatches+=int(white(im.getpixel((x+bit*2+dx,Y0+row)))!=on)
    return mismatches
def check(name):
    folder=ROOT/name
    text=(folder/"probe.asm").read_text()
    imfile=folder/"evidence"/"frame"/"stella_full.png"
    im=Image.open(imfile).convert("RGB")
    if im.size!=(1366,900):raise ValueError("Unknown debugger screenshot format")
    types=NAMES[:3] if name=="nusiz3_only" else NAMES
    results={}
    for t in types:
        scores=[(matches_mask(im,x,t),x) for x in range(104,439,2)]
        scores.sort()
        exact=[x for e,x in scores if e==0]
        results[t]={"best_errors":scores[0][0], "best_x":scores[0][1],
                    "exact_match_xs":exact, "unique_exact":len(exact)==1,
                    "assembler_mask_matches_reference":source_mask_ok(text,LABELS[NAMES.index(t)],t)}
    anchored=[(t,results[t]["exact_match_xs"][0]) for t in types if results[t]["unique_exact"]]
    whites=[(x,y) for y in range(Y0,Y0+9) for x in range(102,470)
            if white(im.getpixel((x,y)))]
    unexplained=[]
    for x,y in whites:
        recognized=False
        for t,x0 in anchored:
            dx=x-x0
            if 0<=dx<16 and MASKS[t][y-Y0]&(1<<(7-dx//2)):
                recognized=True;break
        if not recognized:unexplained.append((x,y))
    # P0 can move in the four-mask variant. M0 may be on prior scanline.
    ypc=sum(yellow(im.getpixel((x,y))) for y in range(160,171) for x in range(102,157))
    ym0=sum(yellow(im.getpixel((x,y))) for y in range(146,173) for x in range(225,260))
    sha=hashlib.sha256(im.crop((661,90,697,111)).tobytes()).hexdigest()
    scans=262 if sha in (
        "04f59d7fbc17d360e0cea738d4e512ab7208118b9b4d4b4743f3a702d96f1fdb",
        "a169787b7bdcf465b5a1b7505dca83c31f60fa2c16337d39fea3e957ea13ace2"
    ) else None
    valid=len(anchored)==len(types) and len(unexplained)==0 and scans==262 and ypc>0 and ym0>0
    return {
      "variant":name,"required_types":list(types),
      "all_source_masks_match_ref":all(results[t]["assembler_mask_matches_reference"] for t in types),
      "masks":results,"white_gui_pixel_count":len(whites),
      "unexplained_white_pixel_count":len(unexplained),
      "unexplained_white_first":unexplained[:80],
      "yellow_player_pixel_count":ypc,"yellow_missile_pixel_count":ym0,
      "ntsc_262":scans==262,"hud_sha256":sha,
      "raster_test":"STATIC one frame only; not a 600-frame proof",
      "four_distinct_exact_status":"LOCAL_PASS_STATIC_4_ORIGINAL_MASKS" if valid and name=="four_mask_probe" else "FAIL_OR_INCONCLUSIVE"
    }
def main():
    result={name:check(name) for name in ("nusiz3_only","four_mask_probe")}
    (ROOT/"evidence_audit.json").write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n")
    for name,v in result.items():
        print(name,"4_MASK_RESULT",v["four_distinct_exact_status"],
             "ghost_pixels",v["unexplained_white_pixel_count"],
             "raster_262",v["ntsc_262"],
             "p0",v["yellow_player_pixel_count"],
             "m0",v["yellow_missile_pixel_count"])
        for t,d in v["masks"].items():
            print(" ",t,"errors",d["best_errors"],"x",d["best_x"],
                  "number_of_exact_matches",len(d["exact_match_xs"]))
    print("Detailed report: evidence_audit.json")
    sys.exit(0 if result["four_mask_probe"]["four_distinct_exact_status"]=="LOCAL_PASS_STATIC_4_ORIGINAL_MASKS" else 1)
if __name__=="__main__":main()
