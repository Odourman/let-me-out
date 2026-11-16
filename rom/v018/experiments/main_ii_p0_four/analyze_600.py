#!/usr/bin/env python3
"""Fail-closed 600-frame exact-pixel audit: FOUR DIFFERENT original NPCs, P0, M0.

Proof is actual Stella 6.7.1 X11 captures, consecutive frame HUD 11..610.
Uses unmodified source masks in main/design/NPC_REFERENCE_8x9_masks.json.
The shot M0 is on preceding scanline; no full six-NPC R1 claim.
"""
from pathlib import Path
from PIL import Image
import hashlib,json,re,csv,sys
ROOT=Path(__file__).resolve().parent
RAW=ROOT/"evidence_600"/"raw"
REF=json.loads((ROOT.parent/"main_ii_three_masks"/"REFERENCE_8x9_MASKS_FROM_MAIN.json").read_text())
SRC=(ROOT/"r1e_four_originals.asm").read_text()
NPCS=[
("large_male","MaleRows",154-103),
("large_female","FemaleRows",268-103),
("small_female","SmallFemaleRows",316-103),
("small_male","SmallMaleRows",400-103)
]
Y=162-65
def source_bytes(label):
    m=re.search(rf"^{label}:\s*\n\s+BYTE (.+)$",SRC,re.M)
    if not m:raise ValueError("Missing source mask "+label)
    return [int(z.strip().replace("$","0x"),16) for z in m.group(1).split(",")][::-1]
MASKS={}
for name,sym,x in NPCS:
    mask=[int(q,2) for q in REF["sprites"][name]]
    assert source_bytes(sym)==mask, f"Original mask {name} changed!"
    MASKS[name]=mask
PLAYER=source_bytes("PlayerRows")
assert len(PLAYER)==9
P0X=188-103
M0X=240-103
M0Y=160-65
def iswhite(p):return min(p)>180 and max(p)-min(p)<40
def isyellow(p):return p[0]>120 and p[1]>100 and p[2]<100
def hudglyph(im,x):
    return tuple((lambda p:p[0]>210 and p[1]>150 and p[2]<180)(im.getpixel((a,b)))
                 for b in range(9,19) for a in range(x,x+7))
def templates(files):
    out={}
    for j in range(1,11):
        with Image.open(files[j-1]) as im:
            out[(10+j)%10]=hudglyph(im.convert("RGB"),579)
    if len(set(out.values()))!=10:raise ValueError("10 real Stella HUD digit glyphs not unique")
    return out
def frame_number(im,lookup):
    digits=[]
    for x in (561,570,579):
        value=hudglyph(im,x)
        if not any(value):continue
        matches=[num for num,expected in lookup.items() if value==expected]
        if len(matches)!=1:return None
        digits.append(str(matches[0]))
    return int("".join(digits)) if digits else None
SCAN262={
 "04f59d7fbc17d360e0cea738d4e512ab7208118b9b4d4b4743f3a702d96f1fdb",
 "a169787b7bdcf465b5a1b7505dca83c31f60fa2c16337d39fea3e957ea13ace2"
}
SCAN270={
 "fc2474f98591f368a880e257df39fadf893dd673512a37535f8df9c41789f142",
 "15dc4da891cb0c3aa06529efafc56ebae4c165928b72ab9d4e0a36f9bc83528c"
}
def errors(im,x,mask,fn):
    errors=0
    for i,pattern in enumerate(mask):
        for b in range(8):
            desired=bool(pattern & (1<<(7-b)))
            for dx in (0,1):
                errors+=int(fn(im.getpixel((x+2*b+dx,Y+i)))!=desired)
    return errors
EXPECTED_WHITE=set();EXPECTED_YELLOW=set()
for name,sym,x in NPCS:
    for i,pattern in enumerate(MASKS[name]):
        for bit in range(8):
            if pattern & (1<<(7-bit)):
                EXPECTED_WHITE.add((x+2*bit,Y+i))
                EXPECTED_WHITE.add((x+2*bit+1,Y+i))
for i,pattern in enumerate(PLAYER):
    for bit in range(8):
        if pattern & (1<<(7-bit)):
            EXPECTED_YELLOW.add((P0X+2*bit,Y+i))
            EXPECTED_YELLOW.add((P0X+2*bit+1,Y+i))
def measure(im,idx,lookup):
    if im.size!=(900,300):raise ValueError("Unexpected Stella debugger crop size")
    observed=frame_number(im,lookup)
    scanhash=hashlib.sha256(im.crop((558,25,594,46)).tobytes()).hexdigest()
    scan=262 if scanhash in SCAN262 else 270 if scanhash in SCAN270 else None
    merrors={name:errors(im,x,MASKS[name],iswhite) for name,sym,x in NPCS}
    p0error=errors(im,P0X,PLAYER,isyellow)
    whiteghost=0;yellowghost=0
    for y in range(Y,Y+9):
        for x in range(0,340):
            p=im.getpixel((x,y))
            whiteghost+=int(iswhite(p) and (x,y) not in EXPECTED_WHITE)
            yellowghost+=int(isyellow(p) and (x,y) not in EXPECTED_YELLOW)
    shot=sum(isyellow(im.getpixel((x,M0Y))) for x in (M0X,M0X+1))
    duplicate=sum(isyellow(im.getpixel((x,M0Y))) for x in (M0X+128,M0X+129))
    shot_row_total=sum(isyellow(im.getpixel((x,M0Y))) for x in range(0,340))
    return {"image_number":idx,"expected_frame_id":10+idx,"stella_frame_id":observed,
       "scanlines":scan,"male_errors":merrors["large_male"],
       "female_errors":merrors["large_female"],
       "small_female_errors":merrors["small_female"],
       "small_male_errors":merrors["small_male"],
       "yellow_player_errors":p0error,
       "extra_white_pixels":whiteghost,"extra_yellow_pixels":yellowghost,
       "m0_yellow_pixels":shot,"m0_wide_duplicated_pixels":duplicate,
       "m0_row_yellow_total":shot_row_total,
       "hud_scanline_hash":scanhash}
def main():
    files=sorted(RAW.glob("frame_*.png"))
    if len(files)!=600:raise ValueError(f"Expected 600 consecutive captured PNGs, got {len(files)}")
    lookup=templates(files)
    rows=[]
    for i,f in enumerate(files,1):
        with Image.open(f) as source:
            rows.append(measure(source.convert("RGB"),i,lookup))
    with (ROOT/"evidence_600"/"frames_600.csv").open("w",newline="") as out:
        writer=csv.DictWriter(out,fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    rowpass=lambda r:(r["stella_frame_id"]==r["expected_frame_id"] and
      r["scanlines"]==262 and
      all(r[k]==0 for k in (
        "male_errors","female_errors","small_female_errors","small_male_errors",
        "yellow_player_errors","extra_white_pixels","extra_yellow_pixels",
        "m0_wide_duplicated_pixels")) and
      r["m0_yellow_pixels"]==2 and r["m0_row_yellow_total"]==2)
    fail=[r for r in rows if not rowpass(r)]
    summary={
      "evidence":"REAL_STELLA_6.7.1_600_CONSECUTIVE_X11_FRAMES",
      "source_masks_identical_to_original_main":True,
      "frames_captured":len(rows),
      "consecutive_frame_ids_11_to_610":sum(r["stella_frame_id"]==r["expected_frame_id"] for r in rows),
      "262_ntsc_scanlines_frames":sum(r["scanlines"]==262 for r in rows),
      "all_four_original_npc_masks_exact_frames":sum(all(r[k]==0 for k in
         ("male_errors","female_errors","small_female_errors","small_male_errors")) for r in rows),
      "yellow_player_mask_exact_frames":sum(r["yellow_player_errors"]==0 for r in rows),
      "single_yellow_M0_shot_frames":sum(
         r["m0_yellow_pixels"]==2 and r["m0_wide_duplicated_pixels"]==0 and
         r["m0_row_yellow_total"]==2 for r in rows),
      "extra_white_gui_pixels_total":sum(r["extra_white_pixels"] for r in rows),
      "extra_yellow_gui_pixels_total":sum(r["extra_yellow_pixels"] for r in rows),
      "completely_valid_frames":len(rows)-len(fail),
      "failed_frames_first_10":fail[:10],
      "ROM_sha256":hashlib.sha256((ROOT/"r1e_F6.bin").read_bytes()).hexdigest(),
      "limitations":"STATIC four NPC X; M0 on preceding scanline; no free independent X, PF walls, 5-6 NPC, independent Verification, or full-game R1."
    }
    summary["status"]="LOCAL_PASS_STATIC_FOUR_ORIGINALS_600" if not fail else "FAIL_OR_INCONCLUSIVE"
    (ROOT/"evidence_600"/"summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps(summary,ensure_ascii=False,indent=2))
    sys.exit(0 if not fail else 1)
if __name__=="__main__":main()
