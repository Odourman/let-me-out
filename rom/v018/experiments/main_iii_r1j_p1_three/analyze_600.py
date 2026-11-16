#!/usr/bin/env python3
"""R1j-A: 600 actual Stella frames, third middle P1 X plus four fourth P0 X modes.

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
SRC=(ROOT/"r1j.asm").read_text()
Y=162-65
NPCS={
 "large_male":("MaleRows",166-103),
 "small_male":("SmallMaleRows",406-103)
}
FEMALE_MODES=("early","middle","late")
# Predicted from unchanged R1h TIA phase: moving second RESP1 c45->c39 = -18CC = -36 GUI pixels.
FEMALE_GUI_X={"early":244,"middle":262,"late":280}
FOURTH=("SmallFemaleRows",330-103,348-103,360-103,378-103)
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
MASKS["large_female"]=[int(q,2) for q in REF["sprites"]["large_female"]]
assert sourcebytes("FemaleRows")==MASKS["large_female"]
PLAYER=sourcebytes("PlayerRows")
assert len(PLAYER)==9
def white(p):return min(p)>180 and max(p)-min(p)<40
def yellow(p):return p[0]>120 and p[1]>100 and p[2]<100
def brown(p):return p[0]>145 and 60<p[1]<p[0] and p[2]<p[1] and p[2]<100
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
FEMALE_POINTS={name:bitpoints(gui_x-103,MASKS["large_female"]) for name,gui_x in FEMALE_GUI_X.items()}
FOURTH_MODES=("pre_mask","post_mask","post_lda","post_color")
FOURTH_POINTS={name:bitpoints(x,MASKS["small_female"]) for name,x in
               zip(FOURTH_MODES,FOURTH[1:])}
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
    female_shape_errors={name:maskerror(img,gui_x-103,MASKS["large_female"],white) for name,gui_x in FEMALE_GUI_X.items()}
    female_matches=[name for name,error in female_shape_errors.items() if error==0]
    female_mode=female_matches[0] if len(female_matches)==1 else "ambiguous"
    shape_errors={name:maskerror(img,x,MASKS["small_female"],white)
                  for name,x in zip(FOURTH_MODES,FOURTH[1:])}
    matches=[name for name,count in shape_errors.items() if count==0]
    mode=matches[0] if len(matches)==1 else "ambiguous"
    expected=EXPECTED_FIXED_WHITE|FOURTH_POINTS.get(mode,set())|FEMALE_POINTS.get(female_mode,set())
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
    # Source GUI image is cropped +103,+65, right PF extreme x423 = local320.
    # At raw GUI y155 door center is inside opening; y185 outside 32-row band.
    door_state="locked" if brown(img.getpixel((320,155-65))) else "open"
    right_outside=brown(img.getpixel((320,185-65)))
    left_155=[x for x in range(104-103,130-103)
              if brown(img.getpixel((x,155-65)))]
    left_185=[x for x in range(104-103,130-103)
              if brown(img.getpixel((x,185-65)))]
    right_rows=[y for y in range(115,220)
                if brown(img.getpixel((423-103,y-65)))]
    gap=sorted(set(range(115,220))-set(right_rows))
    gap_pass=(not gap if door_state=="locked" else
              len(gap)==32 and gap==list(range(gap[0],gap[0]+32)) and
              gap[0]==149 and gap[-1]==180)
    left_exact=left_155==list(range(104-103,112-103)) and left_185==list(range(104-103,112-103))
    fid=frameid(img,templates)
    result={
      "index":idx,"expected_frame_id":10+idx,"stella_frame_id":fid,
      "ntsc_262":hud in SCAN262,
      "fourth_mode":mode,
      "female_mode":female_mode,
      "female_gui_x":FEMALE_GUI_X.get(female_mode),
      "female_errors_by_mode":json.dumps(female_shape_errors),
      "fourth_gui_x":{"pre_mask":330,"post_mask":348,"post_lda":360,"post_color":378}.get(mode),
      "fourth_mask_error_pixels_per_mode":json.dumps(shape_errors),
      "large_male_errors":other["large_male"],
      "large_female_errors":female_shape_errors.get(female_mode,1000),
      "small_male_errors":other["small_male"],
      "yellow_player_errors":player_errors,
      "ghost_white_gui_pixels":extra_white,
      "ghost_yellow_gui_pixels":extra_yellow,
      "M0_gui_pixels":shot,"M0_row_yellow_total":shot_row,
      "stella_hud_hash":hud,
      "left_ball_exact_x0":left_exact,
      "right_door_mode":door_state,
      "right_door_32row_geometry_pass":gap_pass,
      "right_wall_outside_door_closed":right_outside,
      "right_missing_rows":json.dumps(gap)
    }
    result["local_pass"]=(result["stella_frame_id"]==result["expected_frame_id"] and
        result["ntsc_262"] and mode!="ambiguous" and female_mode!="ambiguous" and
        all(v==0 for v in other.values()) and player_errors==0 and
        extra_white==0 and extra_yellow==0 and shot==2 and shot_row==2 and
        left_exact and right_outside and gap_pass)
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
    phase_offsets=[offset for offset in range(256) if all(
        row["fourth_mode"]==FOURTH_MODES[((row["stella_frame_id"]+offset)&0x30)>>4]
        and row["female_mode"]==("early" if ((row["stella_frame_id"]+offset)&0x0C)==0 else ("middle" if ((row["stella_frame_id"]+offset)&0x0C)==4 else "late"))
        and row["right_door_mode"]==("open" if ((row["stella_frame_id"]+offset)&0x40) else "locked")
        for row in records if row["stella_frame_id"] is not None)]
    counts={name:sum(row["fourth_mode"]==name for row in records)
            for name in (*FOURTH_MODES,"ambiguous")}
    female_counts={name:sum(row["female_mode"]==name for row in records) for name in ("early","middle","late","ambiguous")}
    all_ok=sum(row["local_pass"] for row in records)==600
    all_modes_seen=all(counts[name]>0 for name in FOURTH_MODES)
    door_counts={state:sum(r["right_door_mode"]==state for r in records)
                 for state in ("locked","open")}
    combination_counts={mode+"_"+state:sum(
        r["fourth_mode"]==mode and r["right_door_mode"]==state for r in records)
        for mode in FOURTH_MODES for state in ("locked","open")}
    all_24_combinations={female+"_"+fourth+"_"+door:sum(
        r["female_mode"]==female and r["fourth_mode"]==fourth and r["right_door_mode"]==door
        for r in records) for female in FEMALE_MODES for fourth in FOURTH_MODES
        for door in ("locked","open")}
    phase_ok=(bool(phase_offsets) and all_modes_seen and counts["ambiguous"]==0 and
              female_counts["early"]>0 and female_counts["middle"]>0 and female_counts["late"]>0 and female_counts["ambiguous"]==0 and
              all(v>0 for v in all_24_combinations.values()) and
              all(n>0 for n in door_counts.values()) and
              all(n>0 for n in combination_counts.values()))
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
      "fourth_x330_frames":counts["pre_mask"],
      "fourth_x348_frames":counts["post_mask"],
      "fourth_x360_frames":counts["post_lda"],
      "fourth_x378_frames":counts["post_color"],
      "ambiguous_fourth_frames":counts["ambiguous"],
      "phase_offsets_matching_four_X_and_64_frame_right_door":phase_offsets,
      "door_state_frames":door_counts,
      "all_eight_X_door_combinations":combination_counts,
      "female_P1_mode_frames":female_counts,
      "all_twentyfour_P1_P0_door_combinations":all_24_combinations,
      "observed_two_independent_X_axes":all_ok and phase_ok,
      "BALL_left_x0_exact_frames":sum(r["left_ball_exact_x0"] for r in records),
      "PF_only_right_32row_geometry_frames":sum(r["right_door_32row_geometry_pass"] for r in records),
      "genuine_24_cc_range_four_independent_X_positions":all_ok and phase_ok,
      "white_ghost_gui_pixels_total":sum(row["ghost_white_gui_pixels"] for row in records),
      "yellow_ghost_gui_pixels_total":sum(row["ghost_yellow_gui_pixels"] for row in records),
      "ROM_sha256":hashlib.sha256((ROOT/"r1j_F6.bin").read_bytes()).hexdigest(),
      "first_10_failed_frames":[r for r in records if not r["local_pass"]][:10],
      "limits":"Four discrete fourth P0-X slots + three discrete second-P1-X slots, 32-row right-only BROWN door, BL left wall, M0 preceding NPC band; four NPC only, not free 160CC X, no independent verification."
    }
    summary["status"]="LOCAL_PASS_R1J_P1_THREE_X_P0_FOUR_X_600" if all_ok and phase_ok else "FAIL_OR_INCONCLUSIVE"
    (ROOT/"evidence_600"/"summary.json").write_text(
        json.dumps(summary,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps(summary,ensure_ascii=False,indent=2))
    sys.exit(0 if summary["status"].startswith("LOCAL_PASS") else 1)
if __name__=="__main__":main()
