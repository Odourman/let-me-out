#!/usr/bin/env python3
"""600 consecutive ACTUAL Stella X11 debugger frames, independent fourth NPC X.

Fail-closed: four different original 8x9 masks and original yellow player every
frame, both early/late white fourth positions, fixed yellow/P1, exactly one M0,
no ghost pixels, 262 lines, and 16-frame phase alternation.

No claim of full 160CC free X or six NPC. Actual snapshots, not offline renders.
"""
from pathlib import Path
from PIL import Image
import hashlib,json,re,csv,sys
ROOT=Path(__file__).resolve().parent
RAW=ROOT/"evidence_600"/"raw"
REF=json.loads((ROOT.parent/"main_ii_three_masks"/"REFERENCE_8x9_MASKS_FROM_MAIN.json").read_text())
SRC=(ROOT/"r1f_dynamic.asm").read_text()
Y=162-65
NPCS={
 "large_male":("MaleRows",166-103),
 "large_female":("FemaleRows",280-103),
 "small_male":("SmallMaleRows",406-103)
}
FOURTH=("SmallFemaleRows",330-103,348-103)
PLAYERX=216-103
M0Y=160-65
M0X=240-103
def sourcebytes(label):
    m=re.search(rf"^{label}:\s*\n\s+BYTE (.+)$",SRC,re.M)
    if not m:raise ValueError("Missing source mask "+label)
    return [int(z.strip().replace("$","0x"),16) for z in m.group(1).split(",")][::-1]
MASKS={}
for name,(sym,x) in NPCS.items():
    value=[int(q,2) for q in REF["sprites"][name]]
    assert sourcebytes(sym)==value, f"Source changed original mask {name}"
    MASKS[name]=value
MASKS["small_female"]=[int(q,2) for q in REF["sprites"]["small_female"]]
assert sourcebytes(FOURTH[0])==MASKS["small_female"]
PLAYER=sourcebytes("PlayerRows")
assert len(PLAYER)==9
def white(p):return min(p)>180 and max(p)-min(p)<40
def yellow(p):return p[0]>120 and p[1]>100 and p[2]<100
def maskerror(im,x,mask,color):
    total=0
    for i,byte in enumerate(mask):
        for bit in range(8):
            expected=bool(byte&(1<<(7-bit)))
            for dx in (0,1):
                total+=int(color(im.getpixel((x+bit*2+dx,Y+i)))!=expected)
    return total
def bitpoints(x,mask):
    out=set()
    for i,byte in enumerate(mask):
        for bit in range(8):
            if byte&(1<<(7-bit)):
                out.add((x+bit*2,Y+i))
                out.add((x+bit*2+1,Y+i))
    return out
EXPECTED_FIXED_WHITE=set()
for name,(sym,x) in NPCS.items():
    EXPECTED_FIXED_WHITE |= bitpoints(x,MASKS[name])
PLAYER_POINTS=bitpoints(PLAYERX,PLAYER)
FOURTH_POINTS={name:bitpoints(x,MASKS["small_female"]) for name,x in
               (("early",FOURTH[1]),("late",FOURTH[2]))}
def glyph(im,x):
    return tuple((lambda p:p[0]>210 and p[1]>150 and p[2]<180)(im.getpixel((a,b)))
                 for b in range(9,19) for a in range(x,x+7))
def digit_templates(files):
    known={}
    for i in range(10):
        with Image.open(files[i]) as f:
            known[(i+11)%10]=glyph(f.convert("RGB"),579)
    if len(set(known.values()))!=10:raise ValueError("Stella HUD digits not uniquely readable")
    return known
def frameid(im,lookup):
    digits=[]
    for x in (561,570,579):
        g=glyph(im,x)
        if not any(g):continue
        matched=[n for n,bits in lookup.items() if g==bits]
        if len(matched)!=1:return None
        digits.append(str(matched[0]))
    return int("".join(digits)) if digits else None
SCAN262={
 "04f59d7fbc17d360e0cea738d4e512ab7208118b9b4d4b4743f3a702d96f1fdb",
 "a169787b7bdcf465b5a1b7505dca83c31f60fa2c16337d39fea3e957ea13ace2"
}
def measure(img,idx,templates):
    if img.size!=(900,300):raise ValueError("Unknown Stella crop geometry")
    a=maskerror(img,FOURTH[1],MASKS["small_female"],white)
    b=maskerror(img,FOURTH[2],MASKS["small_female"],white)
    mode="early" if a==0 and b>0 else "late" if b==0 and a>0 else "ambiguous"
    expected=EXPECTED_FIXED_WHITE|FOURTH_POINTS.get(mode,set())
    other={name:maskerror(img,x,MASKS[name],white) for name,(sym,x) in NPCS.items()}
    player_errors=maskerror(img,PLAYERX,PLAYER,yellow)
    extra_white=0;extra_yellow=0
    for y in range(Y,Y+9):
        for x in range(0,336):
            p=img.getpixel((x,y))
            extra_white+=int(white(p) and (x,y) not in expected)
            extra_yellow+=int(yellow(p) and (x,y) not in PLAYER_POINTS)
    shot=sum(yellow(img.getpixel((x,M0Y))) for x in (M0X,M0X+1))
    shot_row=sum(yellow(img.getpixel((x,M0Y))) for x in range(0,336))
    hud=hashlib.sha256(img.crop((558,25,594,46)).tobytes()).hexdigest()
    fid=frameid(img,templates)
    result={
      "index":idx,"expected_frame_id":10+idx,"stella_frame_id":fid,
      "ntsc_262":hud in SCAN262,
      "fourth_mode":mode,
      "fourth_gui_x":330 if mode=="early" else 348 if mode=="late" else None,
      "early_shape_errors":a,"late_shape_errors":b,
      "large_male_errors":other["large_male"],
      "large_female_errors":other["large_female"],
      "small_male_errors":other["small_male"],
      "yellow_player_errors":player_errors,
      "ghost_white_gui_pixels":extra_white,
      "ghost_yellow_gui_pixels":extra_yellow,
      "M0_gui_pixels":shot,"M0_row_yellow_total":shot_row,
      "stella_hud_hash":hud
    }
    result["local_pass"]=(result["stella_frame_id"]==result["expected_frame_id"] and
        result["ntsc_262"] and mode!="ambiguous" and
        all(v==0 for v in other.values()) and player_errors==0 and
        extra_white==0 and extra_yellow==0 and shot==2 and shot_row==2)
    return result
def main():
    paths=sorted(RAW.glob("frame_*.png"))
    if len(paths)!=600:raise ValueError(f"Only {len(paths)} captured images instead of 600")
    lookup=digit_templates(paths)
    records=[]
    for i,path in enumerate(paths,1):
        with Image.open(path) as pic:
            records.append(measure(pic.convert("RGB"),i,lookup))
    # A single frame-counter phase offset may differ by 0/1 at debugger entry.
    phase_offsets=[offset for offset in range(32) if all(
        row["fourth_mode"]==("late" if ((row["stella_frame_id"]+offset)&16) else "early")
        for row in records if row["stella_frame_id"] is not None)]
    counts={name:sum(row["fourth_mode"]==name for row in records)
            for name in ("early","late","ambiguous")}
    all_ok=sum(row["local_pass"] for row in records)==600
    both_seen=counts["early"]>0 and counts["late"]>0
    phase_ok=bool(phase_offsets) and both_seen and counts["ambiguous"]==0
    with (ROOT/"evidence_600"/"frames_600.csv").open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(records[0]))
        w.writeheader()
        w.writerows(records)
    summary={
      "evidence":"600_CONSECUTIVE_AUTHENTIC_STELLA_6.7.1_DEBUGGER_SCREENSHOTS",
      "source_original_masks_unchanged":True,
      "captured_frames":len(records),
      "consecutive_stella_ids_pass":sum(
          row["stella_frame_id"]==row["expected_frame_id"] for row in records),
      "NTSC_262_scanlines_pass":sum(row["ntsc_262"] for row in records),
      "all_four_original_masks_player_single_M0_zero_ghost_pass":sum(
          row["local_pass"] for row in records),
      "early_fourth_x330_frames":counts["early"],
      "late_fourth_x348_frames":counts["late"],
      "ambiguous_fourth_frames":counts["ambiguous"],
      "phase_offsets_matching_alternating_16_frame_blocks":phase_offsets,
      "genuine_9_cc_independent_fourth_X_toggle":all_ok and phase_ok,
      "white_ghost_gui_pixels_total":sum(row["ghost_white_gui_pixels"] for row in records),
      "yellow_ghost_gui_pixels_total":sum(row["ghost_yellow_gui_pixels"] for row in records),
      "ROM_sha256":hashlib.sha256((ROOT/"r1f_F6.bin").read_bytes()).hexdigest(),
      "first_10_failed_frames":[r for r in records if not r["local_pass"]][:10],
      "limits":"Two discrete fourth X positions; yellow player static; three P1 NPC static; M0 on preceding scanline; no arbitrary full-screen X, PF walls, key, fifth/sixth NPC, PAL or independent VERIFICATION."
    }
    summary["status"]="LOCAL_PASS_R1F_INDEPENDENT_FOURTH_X_600" if all_ok and phase_ok else "FAIL_OR_INCONCLUSIVE"
    (ROOT/"evidence_600"/"summary.json").write_text(
        json.dumps(summary,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps(summary,ensure_ascii=False,indent=2))
    sys.exit(0 if summary["status"].startswith("LOCAL_PASS") else 1)
if __name__=="__main__":main()
