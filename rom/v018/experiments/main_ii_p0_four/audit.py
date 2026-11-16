#!/usr/bin/env python3
"""Fail-closed actual Stella 6.7.1 audit of four DIFFERENT 8x9 original NPCs.

P1: original large male / large female / small male.
P0: original yellow 8x9 player and white wide-copy original small female.
M0: single-shot test on the preceding raster row. This is NOT full R1.
"""
from PIL import Image
from pathlib import Path
import json,hashlib,re,sys
ROOT=Path(__file__).resolve().parent
REF=json.loads((ROOT.parent/"main_ii_three_masks"/"REFERENCE_8x9_MASKS_FROM_MAIN.json").read_text())
TEXT=(ROOT/"r1e_four_originals.asm").read_text()
IMPATH=ROOT/"evidence"/"frame"/"stella_full.png"
IM=Image.open(IMPATH).convert("RGB")
assert IM.size==(1366,900), f"Unexpected raw Stella X11 geometry {IM.size}"
Y0=162
def white(p):return min(p)>180 and max(p)-min(p)<40
def yellow(p):return p[0]>120 and p[1]>100 and p[2]<100
def getbits(label):
    m=re.search(rf"^{label}:\s*\n\s+BYTE (.+)$",TEXT,re.M)
    if not m:raise ValueError(f"Missing assembler symbol data {label}")
    return [int(x.strip().replace("$","0x"),16) for x in m.group(1).split(",")][::-1]
DATA=[
 ("large_male","MaleRows",white,142,191),
 ("large_female","FemaleRows",white,247,311),
 ("small_female","SmallFemaleRows",white,308,378),
 ("small_male","SmallMaleRows",white,382,428),
 ("yellow_player","PlayerRows",yellow,180,230)
]
def score(mask,x,fn):
    errors=0
    for i,bits in enumerate(mask):
        for b in range(8):
            wanted=bool(bits&(1<<(7-b)))
            for dx in (0,1):
                seen=fn(IM.getpixel((x+2*b+dx,Y0+i)))
                errors+=int(wanted!=seen)
    return errors
results={}
for name,label,fn,lo,hi in DATA:
    mask=getbits(label)
    if name!="yellow_player":
        expected=[int(s,2) for s in REF["sprites"][name]]
        if mask!=expected:raise ValueError(f"ASM source mask differs from approved original {name}")
    options=sorted((score(mask,x,fn),x) for x in range(lo+(lo%2),hi,2))
    exact=[x for e,x in options if e==0]
    results[name]={"x_best":options[0][1], "pixel_errors_best":options[0][0],
                   "unique_full_match":len(exact)==1, "exact_xs":exact,
                   "top_candidates":options[:5]}
white_masks={"large_male","large_female","small_female","small_male"}
known_white=set();known_yellow=set()
for name,label,fn,lo,hi in DATA:
    if not results[name]["unique_full_match"]:continue
    x0=results[name]["exact_xs"][0]
    target=known_white if name in white_masks else known_yellow
    for i,bits in enumerate(getbits(label)):
        for b in range(8):
            if bits&(1<<(7-b)):
                target.add((x0+2*b,Y0+i))
                target.add((x0+2*b+1,Y0+i))
wghost=[(x,y) for y in range(Y0,Y0+9) for x in range(104,435)
        if white(IM.getpixel((x,y))) and (x,y) not in known_white]
yghost=[(x,y) for y in range(Y0,Y0+9) for x in range(104,435)
        if yellow(IM.getpixel((x,y))) and (x,y) not in known_yellow]
# Snapshot crop uses Stella 1366x900, screen scan counter at fixed HUD box.
hud=hashlib.sha256(IM.crop((661,90,697,111)).tobytes()).hexdigest()
known262={
"04f59d7fbc17d360e0cea738d4e512ab7208118b9b4d4b4743f3a702d96f1fdb",
"a169787b7bdcf465b5a1b7505dca83c31f60fa2c16337d39fea3e957ea13ace2"
}
shot_yellow=[x for x in range(235,252) if yellow(IM.getpixel((x,160)))]
shot_duplicate_yellow=[x for x in range(363,380) if yellow(IM.getpixel((x,160)))]
checks={
 "all_4_original_white_masks_exact":all(results[n]["unique_full_match"] for n in white_masks),
 "yellow_player_original_mask_exact":results["yellow_player"]["unique_full_match"],
 "no_extra_white_pixels":len(wghost)==0,
 "no_extra_yellow_pixels_in_NPC_band":len(yghost)==0,
 "262_scanlines":hud in known262,
 "single_M0_shot_visible":len(shot_yellow)>0 and len(shot_duplicate_yellow)==0
}
result={
 "status":"LOCAL_PASS_STATIC_FOUR_DISTINCT_ORIGINALS" if all(checks.values()) else "FAIL_OR_INCONCLUSIVE",
 "references":{"approved_original_masks":"main/design/NPC_REFERENCE_8x9_masks.json",
               "architecture":"P1 three close retriggers plus P0 NUSIZ0=$04 wide copy"},
 "exact_pixel_matches":results,"checks":checks,
 "white_ghost_pixel_count":len(wghost),"white_ghost_examples":wghost[:50],
 "yellow_ghost_pixel_count":len(yghost),"yellow_ghost_examples":yghost[:50],
 "M0_test_yellow_pixel_count":len(shot_yellow),
 "M0_wide_duplicate_yellow_pixel_count":len(shot_duplicate_yellow),
 "262_hud_hash":hud,
 "ROM_sha256":hashlib.sha256((ROOT/"r1e_F6.bin").read_bytes()).hexdigest(),
 "limitations":"Single static frame. M0 moved to preceding raster and needs real gameplay integration. No independent free X, six NPC or PF wall/double-door integration, no 600-frame stability, no independent Verification."
}
(ROOT/"evidence"/"audit.json").write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n")
print(json.dumps(result,indent=2,ensure_ascii=False))
sys.exit(0 if result["status"].startswith("LOCAL_PASS") else 1)
