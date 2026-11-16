#!/usr/bin/env python3
"""Fail-closed actual Stella 6.7.1 image audit: THREE different original 8x9 masks.

All three masks are taken directly from the frozen copy of main/design/
NPC_REFERENCE_8x9_masks.json, including blank rows of small_male.
Do not mistake a near-copy of another bitmap for a distinct android.
"""
import json,re,hashlib,sys
from pathlib import Path
from PIL import Image

ROOT=Path(__file__).resolve().parent
reference=json.loads((ROOT/"REFERENCE_8x9_MASKS_FROM_MAIN.json").read_text())
asm=(ROOT/"r1c_three_retriggers.asm").read_text()
assert reference["width"]==8 and reference["height"]==9
types=["large_male","large_female","small_male"]
symbols=["MaleRows","FemaleRows","SmallMaleRows"]
masks={}
for name,symbol in zip(types,symbols):
    expected=[int(bits,2) for bits in reference["sprites"][name]]
    line=re.search(rf'^{symbol}:\s*\n\s+BYTE (.+)$',asm,re.M)
    if not line:raise ValueError(f"Missing source label {symbol}")
    source=[int(byte.strip().replace("$","0x"),16) for byte in line.group(1).split(",")]
    assert source[::-1]==expected, f"ASM mask for {name} differs from MAIN visual reference"
    masks[name]=expected

im=Image.open(ROOT/"evidence"/"frame"/"stella_full.png").convert("RGB")
assert im.size==(1366,900), f"Unrecognized Stella debugger geometry {im.size}"
def white(x,y):
    p=im.getpixel((x,y))
    return min(p)>180 and max(p)-min(p)<40
def yellow(x,y):
    p=im.getpixel((x,y))
    return p[0]>120 and p[1]>100 and p[2]<100
Y=162
# Candidate windows are intentionally distinct: this proof tests fixed 3-way raster.
windows={"large_male":(145,245),"large_female":(250,345),"small_male":(345,435)}
results={}
for name in types:
    expected=masks[name]
    lo,hi=windows[name]
    scored=[]
    for x0 in range(lo,hi):
        errors=sum(white(x0+2*b,Y+i)!=bool((v>>(7-b))&1)
                   for i,v in enumerate(expected) for b in range(8))
        if errors<=24:scored.append((errors,x0))
    scored.sort()
    results[name]={"best_candidates":scored[:10],"exact_x":[x for n,x in scored if n==0]}
    if len(results[name]["exact_x"])!=1:
        results[name]["status"]="FAIL_OR_INCONCLUSIVE"
        continue
    results[name]["status"]="EXACT_72_OF_72"
positions=[results[t]["exact_x"][0] for t in types if len(results[t]["exact_x"])==1]
extra=[]
if len(positions)==3:
    for y in range(Y,Y+9):
        for x in range(150,450):
            if not white(x,y):continue
            accounted=any(
                x0<=x<x0+16 and 
                ((masks[t][y-Y]>>(7-(x-x0)//2))&1)
                for x0,t in zip(positions,types))
            if not accounted:extra.append((x,y))
hud=hashlib.sha256(im.crop((661,90,697,111)).tobytes()).hexdigest()
scan262=hud in (
    "04f59d7fbc17d360e0cea738d4e512ab7208118b9b4d4b4743f3a702d96f1fdb",
    "a169787b7bdcf465b5a1b7505dca83c31f60fa2c16337d39fea3e957ea13ace2")
p0=sum(yellow(x,y) for y in range(Y,Y+9) for x in range(105,135))
m0=sum(yellow(x,166) for x in range(230,251))
clean= len(positions)==3 and len(extra)==0
status="LOCAL_PASS_STATIC_THREE_DISTINCT_MASKS" if clean and scan262 and p0>0 and m0>0 else "FAIL_OR_INCONCLUSIVE"
result={
    "reference_file":"design/NPC_REFERENCE_8x9_masks.json at main, blob 058800a4c1904d1ff289e7e61b3902aa111ba16d",
    "source_masks_match_reference":True,
    "actual_stella_png_sha256":hashlib.sha256((ROOT/"evidence"/"frame"/"stella_full.png").read_bytes()).hexdigest(),
    "mask_findings":results,
    "three_exact_positions":positions,
    "extra_white_pixels_total":len(extra),
    "extra_white_pixels_first":extra[:40],
    "p0_yellow_pixels":p0,
    "m0_yellow_pixels":m0,
    "scan_262_hud":scan262,
    "scan_hud_sha256":hud,
    "status":status,
    "limitations":"Single static raster image, zero independently moving NPC, no six-NPC or verification approval."
}
(ROOT/"evidence"/"audit.json").write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n")
print(json.dumps(result,indent=2,ensure_ascii=False))
sys.exit(0 if status.startswith("LOCAL_PASS") else 1)
