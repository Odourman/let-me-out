#!/usr/bin/env python3
"""Audit 600 real consecutive Stella X11 frames for THREE different original NPC masks.

Checks main-sourced 8x9 masks (including transparent rows), both 2x display
pixels per color-clock, extra/ghost white pixels, P0, M0, actual frame IDs
and Stella 262/270 HUD. Static positions only; never claim free X.
"""
from pathlib import Path
from PIL import Image
import csv,hashlib,json,re,sys
ROOT=Path(__file__).resolve().parent
RAW=ROOT/"evidence_600"/"raw"
REF=json.loads((ROOT/"REFERENCE_8x9_MASKS_FROM_MAIN.json").read_text())
ASM=(ROOT/"r1c_three_retriggers.asm").read_text()
TYPES=["large_male","large_female","small_male"]
SYMS=["MaleRows","FemaleRows","SmallMaleRows"]
POS={"large_male":166-103,"large_female":280-103,"small_male":394-103}
Y=162-65
assert REF["width"]==8 and REF["height"]==9
MASKS={}
for name,symbol in zip(TYPES,SYMS):
    expected=[int(s,2) for s in REF["sprites"][name]]
    m=re.search(rf'^{symbol}:\s*\n\s+BYTE (.+)$',ASM,re.M)
    if not m: raise ValueError("Missing source bitmap: "+symbol)
    source=[int(x.strip().replace("$","0x"),16) for x in m.group(1).split(",")]
    assert source[::-1]==expected, f"Unexpected change to original {name}"
    MASKS[name]=expected

HUD_HASHES_262={
"04f59d7fbc17d360e0cea738d4e512ab7208118b9b4d4b4743f3a702d96f1fdb",
"a169787b7bdcf465b5a1b7505dca83c31f60fa2c16337d39fea3e957ea13ace2"
}
HUD_HASHES_270={
"fc2474f98591f368a880e257df39fadf893dd673512a37535f8df9c41789f142",
"15dc4da891cb0c3aa06529efafc56ebae4c165928b72ab9d4e0a36f9bc83528c"
}
def white(p):
    return min(p)>180 and max(p)-min(p)<40
def game_yellow(p):
    return p[0]>120 and p[1]>100 and p[2]<100
def hud_digit_glyph(im,x):
    return tuple((lambda p:p[0]>210 and p[1]>150 and p[2]<180)(im.getpixel((xx,yy)))
                 for yy in range(9,19) for xx in range(x,x+7))
def calibrate_digit_templates(files):
    result={}
    for j in range(1,11):
        with Image.open(files[j-1]) as src:
            result[(10+j)%10]=hud_digit_glyph(src.convert("RGB"),579)
    if len(set(result.values()))!=10:
        raise ValueError("Actual 10 frame digits not distinguishable")
    return result
def frame_id(im,templates):
    digits=[]
    for x in (561,570,579):
        glyph=hud_digit_glyph(im,x)
        if not any(glyph):continue
        matches=[num for num,expected in templates.items() if glyph==expected]
        if len(matches)!=1:return None
        digits.append(str(matches[0]))
    return int("".join(digits)) if digits else None
def analyze_one(im,expected_idx,templates):
    if im.size!=(900,300):raise ValueError("Wrong Stella crop geometry")
    f=frame_id(im,templates)
    hud=hashlib.sha256(im.crop((558,25,594,46)).tobytes()).hexdigest()
    scan=262 if hud in HUD_HASHES_262 else (270 if hud in HUD_HASHES_270 else None)
    mismatches={}
    for name in TYPES:
        x=POS[name];mask=MASKS[name]
        errors=0
        for y,byte in enumerate(mask):
            for bit in range(8):
                expected=bool(byte&(1<<(7-bit)))
                for scale in (0,1):
                    actual=white(im.getpixel((x+2*bit+scale,Y+y)))
                    errors+=int(actual!=expected)
        mismatches[name]=errors
    ghosts=0
    for y in range(Y,Y+9):
        for x in range(55,347):
            if not white(im.getpixel((x,y))):continue
            explained=False
            for name in TYPES:
                dx=x-POS[name]
                if 0<=dx<16 and MASKS[name][y-Y]&(1<<(7-dx//2)):
                    explained=True
                    break
            ghosts+=int(not explained)
    p0=sum(game_yellow(im.getpixel((x,y))) for y in range(Y,Y+9) for x in range(2,33))
    m0=sum(game_yellow(im.getpixel((x,Y+4))) for x in range(127,148))
    return {"frame_index":expected_idx,"expected_frame_id":10+expected_idx,"stella_frame_id":f,
        "scanlines":scan,"large_male_errors":mismatches["large_male"],
        "large_female_errors":mismatches["large_female"],
        "small_male_errors":mismatches["small_male"],
        "extra_white_pixels":ghosts,"p0_yellow_pixels":p0,"m0_yellow_pixels":m0,
        "stella_hud_sha256":hud}
def main():
    files=sorted(RAW.glob("frame_*.png"))
    if len(files)!=600:raise ValueError(f"Exactly 600 captured raw frames required, found {len(files)}")
    templates=calibrate_digit_templates(files)
    rows=[]
    for i,p in enumerate(files,1):
        with Image.open(p) as src:
            rows.append(analyze_one(src.convert("RGB"),i,templates))
    with (ROOT/"evidence_600"/"frames_600.csv").open("w",newline="") as out:
        writer=csv.DictWriter(out,fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    summary={
      "source_original_masks_match_main":True,
      "captured_frames":len(rows),
      "frame_ids_consecutive_11_610":sum(r["stella_frame_id"]==r["expected_frame_id"] for r in rows),
      "ntsc_262_frame_count":sum(r["scanlines"]==262 for r in rows),
      "male_8x9_exact_frames":sum(r["large_male_errors"]==0 for r in rows),
      "female_8x9_exact_frames":sum(r["large_female_errors"]==0 for r in rows),
      "small_male_8x9_exact_frames":sum(r["small_male_errors"]==0 for r in rows),
      "p0_present_frames":sum(r["p0_yellow_pixels"]>0 for r in rows),
      "m0_present_frames":sum(r["m0_yellow_pixels"]>0 for r in rows),
      "extra_white_pixels_total":sum(r["extra_white_pixels"] for r in rows),
      "failed_frames_first_10":[r for r in rows if
        r["stella_frame_id"]!=r["expected_frame_id"] or r["scanlines"]!=262
        or r["large_male_errors"] or r["large_female_errors"] or r["small_male_errors"]
        or r["extra_white_pixels"] or not r["p0_yellow_pixels"] or not r["m0_yellow_pixels"]][:10],
      "limitations":"STATIC fixed three NPC positions; independent freely moving X, 4-6 NPC, PF, R2, hardware test, independent Verification not proven"
    }
    summary["status"]="LOCAL_PASS_STATIC_3_MASKS_600" if (
        summary["frame_ids_consecutive_11_610"]==600 and
        summary["ntsc_262_frame_count"]==600 and
        summary["male_8x9_exact_frames"]==600 and
        summary["female_8x9_exact_frames"]==600 and
        summary["small_male_8x9_exact_frames"]==600 and
        summary["p0_present_frames"]==600 and
        summary["m0_present_frames"]==600 and
        summary["extra_white_pixels_total"]==0) else "FAIL_OR_INCONCLUSIVE"
    (ROOT/"evidence_600"/"summary.json").write_text(json.dumps(summary,indent=2,ensure_ascii=False)+"\n")
    print(json.dumps(summary,indent=2,ensure_ascii=False))
    sys.exit(0 if summary["status"].startswith("LOCAL_PASS") else 1)
if __name__=="__main__":main()
