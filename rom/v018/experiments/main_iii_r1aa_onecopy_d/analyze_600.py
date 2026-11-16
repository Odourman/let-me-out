#!/usr/bin/env python3
"""R1y: eight coarse-shifted M0 X positions passing second P1 right edge; strict Stella collision audit.

Fail-closed: four different original 8x9 masks and original yellow player every
frame, both early/late white fourth positions, fixed yellow/P1, exactly one M0,
no ghost pixels, 262 lines, and 16-frame phase alternation.

No claim of full 160CC free X or six NPC. Actual snapshots, not offline renders.
"""
from pathlib import Path
from PIL import Image
import hashlib,json,re,csv,sys
ROOT=Path(__file__).resolve().parent
HEIGHT=14
OUT=ROOT/"evidence_600"
RAW=OUT/"raw"
REF=json.loads((ROOT.parent/"main_ii_three_masks"/"REFERENCE_8x9_MASKS_FROM_MAIN.json").read_text())
SRC=(ROOT/"r1aa.asm").read_text()
Y=162-65
NPCS={
 "large_male":("MaleRows",166-103),
 "small_male":("SmallMaleRows",406-103)
}
FEMALE_XS=(248-103,280-103)  # measured raw Stella x248 (+2 TIA CC first-copy shift at 18CC double RESP1), x280; BOTH original 8x9 exact
FOURTH=("SmallFemaleRows",330-103,348-103,360-103,378-103)
PLAYERX=216-103
M0Y=167-65
M0_GUI_XS=(286,288,290,292,294,296,298,300)
M0_LOCAL_XS=tuple(x-103 for x in M0_GUI_XS)
def sourcebytes(label):
    m=re.search(rf"^{label}:\s*\n\s+BYTE (.+)$",SRC,re.M)
    if not m:raise ValueError("Missing source mask "+label)
    return [int(z.strip().replace("$","0x"),16) for z in m.group(1).split(",")][::-1]
MASKS={}
for name,(sym,x) in NPCS.items():
    original=[int(q,2) for q in REF["sprites"][name]]
    assert sourcebytes(sym)==original, f"Source changed ORIGINAL 8x9 mask {name}"
    value=[original[i*9//HEIGHT] for i in range(HEIGHT)]
    assert sourcebytes(sym+str(HEIGHT))==value,f"Derived mask error {name}"
    MASKS[name]=value
original_small=[int(q,2) for q in REF["sprites"]["small_female"]]
assert sourcebytes(FOURTH[0])==original_small
MASKS["small_female"]=[original_small[i*9//HEIGHT] for i in range(HEIGHT)]
assert sourcebytes("SmallFemaleRows"+str(HEIGHT))==MASKS["small_female"]
original_large=[int(q,2) for q in REF["sprites"]["large_female"]]
assert sourcebytes("FemaleRows")==original_large
MASKS["large_female"]=[original_large[i*9//HEIGHT] for i in range(HEIGHT)]
assert sourcebytes("FemaleRows"+str(HEIGHT))==MASKS["large_female"]
original_player=sourcebytes("PlayerRows")
assert len(original_player)==9
PLAYER=[original_player[i*9//HEIGHT] for i in range(HEIGHT)]
assert sourcebytes("PlayerRows"+str(HEIGHT))==PLAYER
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
def female_maskerror_with_real_missile_overlap(im,x,mask,shot_points):
    """Compare all visible NPC pixels; only genuine on-target M0 pixels may occlude white P1."""
    total=0
    occluded=0
    for i,byte in enumerate(mask):
        for bit in range(8):
            expected=bool(byte&(1<<(7-bit)))
            for dx in (0,1):
                p=(x+bit*2+dx,Y+i)
                pixel=im.getpixel(p)
                if expected and p in shot_points and yellow(pixel):
                    occluded+=1
                else:
                    total+=int(white(pixel)!=expected)
    return total,occluded
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

DOUBLE_FEMALE_POINTS=set()
for fx in FEMALE_XS: DOUBLE_FEMALE_POINTS|=bitpoints(fx,MASKS["large_female"])
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
    shape_errors={name:maskerror(img,x,MASKS["small_female"],white)
                  for name,x in zip(FOURTH_MODES,FOURTH[1:])}
    matches=[name for name,count in shape_errors.items() if count==0]
    mode=matches[0] if len(matches)==1 else "ambiguous"
    expected=EXPECTED_FIXED_WHITE|FOURTH_POINTS.get(mode,set())|DOUBLE_FEMALE_POINTS
    other={name:maskerror(img,x,MASKS[name],white) for name,(sym,x) in NPCS.items()}
    player_errors=maskerror(img,PLAYERX,PLAYER,yellow)
    # Count yellow projectile pixels OUTSIDE the complete original player.
    # Fail closed if a second missile copy, a third pixel, or a wrong X exists.
    raw_m0_xs=sorted(x for x in range(0,336)
                     if yellow(img.getpixel((x,M0Y))) and (x,M0Y) not in PLAYER_POINTS)
    shot_x=(raw_m0_xs[0] if len(raw_m0_xs)==2
            and raw_m0_xs[1]==raw_m0_xs[0]+1
            and raw_m0_xs[0] in M0_LOCAL_XS else None)
    shot_points=({(shot_x,M0Y),(shot_x+1,M0Y)} if shot_x is not None else set())
    female_checks=[female_maskerror_with_real_missile_overlap(
         img,x,MASKS["large_female"],shot_points) for x in FEMALE_XS]
    female_errs=[item[0] for item in female_checks]
    second_female_yellow_missile_overlay_pixels=female_checks[1][1]
    extra_white=0;extra_yellow=0
    for y in range(Y,Y+HEIGHT):
        for x in range(0,336):
            p=img.getpixel((x,y))
            extra_white+=int(white(p) and (x,y) not in expected)
            extra_yellow+=int(yellow(p) and (x,y) not in (PLAYER_POINTS|shot_points))
    shot=len(raw_m0_xs) if shot_x is not None else 0
    old_head_shot=sum(yellow(img.getpixel((x,160-65))) for x in range(0,336))
    ghost_x296=sum(white(img.getpixel((x,M0Y))) for x in (296-103,296-103+2))
    shot_row=sum(yellow(img.getpixel((x,M0Y))) for x in range(0,336))
    hud=hashlib.sha256(img.crop((558,25,594,46)).tobytes()).hexdigest()
    # Diagnostic color of bottom-only region written from real CXM0P bit7.
    # This is an actual hardware latch reading, NOT a software hitbox.
    collision_diag_rgb=img.getpixel((180-103,195-65))
    expected_m0_p1_contact=(shot_x is not None and
                            (shot_x+103)<296 and (shot_x+103+1)>=280)
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
      "fourth_gui_x":{"pre_mask":330,"post_mask":348,"post_lda":360,"post_color":378}.get(mode),
      "fourth_mask_error_pixels_per_mode":json.dumps(shape_errors),
      "large_male_errors":other["large_male"],
      "large_female_early_errors":female_errs[0],
      "large_female_late_errors":female_errs[1],
      "both_female_original_masks_exact_excluding_real_missile_overlay":female_errs==[0,0],
      "second_female_yellow_missile_overlay_pixels":second_female_yellow_missile_overlay_pixels,
      "small_male_errors":other["small_male"],
      "yellow_player_errors":player_errors,
      "ghost_white_gui_pixels":extra_white,
      "ghost_yellow_gui_pixels":extra_yellow,
      "M0_gui_pixels":shot,"M0_row_yellow_total":shot_row,
      "M0_gui_x":(shot_x+103 if shot_x is not None else None),
      "M0_gui_y":167,
      "raw_projectile_x_coords":json.dumps([x+103 for x in raw_m0_xs]),
      "old_head_line_M0_pixels":old_head_shot,"duplicated_m0_x296_white_pixels":ghost_x296,
      "stella_hud_hash":hud,
      "collision_background_rgb":json.dumps(collision_diag_rgb),
      "expected_M0_first_female_contact":expected_m0_p1_contact,
      "left_ball_exact_x0":left_exact,
      "right_door_mode":door_state,
      "right_door_32row_geometry_pass":gap_pass,
      "right_wall_outside_door_closed":right_outside,
      "right_missing_rows":json.dumps(gap)
    }
    result["local_pass"]=(result["stella_frame_id"]==result["expected_frame_id"] and
        result["ntsc_262"] and mode!="ambiguous" and
        all(v==0 for v in other.values()) and female_errs==[0,0] and player_errors==0 and
        extra_white==0 and extra_yellow==0 and shot==2 and shot_row==len({x for (x,y) in (PLAYER_POINTS|shot_points) if y==M0Y}) and old_head_shot==0 and ghost_x296==0 and
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
    phase_offsets=[offset for offset in range(128) if all(
        row["fourth_mode"]==FOURTH_MODES[((row["stella_frame_id"]+offset)&0x30)>>4]
        and row["right_door_mode"]==("open" if ((row["stella_frame_id"]+offset)&0x40) else "locked")
        and row["M0_gui_x"]==M0_GUI_XS[(row["stella_frame_id"]+offset)&0x07]
        for row in records if row["stella_frame_id"] is not None)]
    counts={name:sum(row["fourth_mode"]==name for row in records)
            for name in (*FOURTH_MODES,"ambiguous")}
    all_ok=sum(row["local_pass"] for row in records)==600
    all_modes_seen=all(counts[name]>0 for name in FOURTH_MODES)
    m0_counts={x:sum(row["M0_gui_x"]==x for row in records) for x in M0_GUI_XS}
    combo32={f"{mode}_x{mx}_{door}":sum(
        row["fourth_mode"]==mode and row["M0_gui_x"]==mx and row["right_door_mode"]==door
        for row in records)
        for mode in FOURTH_MODES for mx in M0_GUI_XS for door in ("locked","open")}
    door_counts={state:sum(r["right_door_mode"]==state for r in records)
                 for state in ("locked","open")}
    combination_counts={mode+"_"+state:sum(
        r["fourth_mode"]==mode and r["right_door_mode"]==state for r in records)
        for mode in FOURTH_MODES for state in ("locked","open")}
    overlap_rgb={r["collision_background_rgb"] for r in records
                 if r["expected_M0_first_female_contact"]}
    miss_rgb={r["collision_background_rgb"] for r in records
              if not r["expected_M0_first_female_contact"]}
    collision_diag_ok=(len(overlap_rgb)==1 and len(miss_rgb)==1 and
                       overlap_rgb.isdisjoint(miss_rgb))
    phase_ok=(bool(phase_offsets) and all_modes_seen and counts["ambiguous"]==0 and
              all(n>0 for n in door_counts.values()) and
              all(n>0 for n in combination_counts.values()) and
              all(n>0 for n in m0_counts.values()) and
              all(n>0 for n in combo32.values()) and collision_diag_ok)
    with (OUT/"frames_600.csv").open("w",newline="") as f:
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
      "eight_projectile_x_gui_counts":m0_counts,
      "all_64_fourth_x_by_m0_x_by_door_combinations":combo32,
      "collision_diag_contact_rgb":sorted(overlap_rgb),
      "collision_diag_noncontact_rgb":sorted(miss_rgb),
      "collision_diag_exact_match_pass":collision_diag_ok,
      "expected_m0_p1_contact_frames":sum(r["expected_M0_first_female_contact"] for r in records),
      "yellow_m0_pixels_visually_covering_second_female":sum(r["second_female_yellow_missile_overlay_pixels"] for r in records),
      "BALL_left_x0_exact_frames":sum(r["left_ball_exact_x0"] for r in records),
      "PF_only_right_32row_geometry_frames":sum(r["right_door_32row_geometry_pass"] for r in records),
      "genuine_24_cc_range_four_independent_X_positions":all_ok and phase_ok,
      "white_ghost_gui_pixels_total":sum(row["ghost_white_gui_pixels"] for row in records),
      "yellow_ghost_gui_pixels_total":sum(row["ghost_yellow_gui_pixels"] for row in records),
      "ROM_sha256":hashlib.sha256((ROOT/"r1aa_F6.bin").read_bytes()).hexdigest(),
      "fifth_large_female_original_mask_both_positions_exact_frames":sum(r["both_female_original_masks_exact_excluding_real_missile_overlay"] for r in records),
      "first_10_failed_frames":[r for r in records if not r["local_pass"]][:10],
      "limits":"Research-only R1y +9CC more RESM0 delay versus R1x, M0 x286..300 across second P1 exit; must test M0 color and absence of clones; not full-screen travel or gameplay hit logic."
    }
    summary["height_display_rows"]=HEIGHT
    summary["yellow_single_M0_y167_at_one_of_four_x_frames"]=sum(r["M0_gui_pixels"]==2 for r in records)
    summary["all_eight_m0_hmove_positions_seen"]=all(n>0 for n in m0_counts.values())
    summary["old_m0_head_line_absent_frames"]=sum(r["old_head_line_M0_pixels"]==0 for r in records)
    summary["no_NUSIZ0_duplicate_x296_frames"]=sum(r["duplicated_m0_x296_white_pixels"]==0 for r in records)
    summary["source_original_8x9_masks_preserved_byte_for_byte"]=True
    summary["status"]="LOCAL_PASS_R1AA_ONECOPY_D_600" if all_ok and phase_ok else "FAIL_OR_INCONCLUSIVE"
    (OUT/"summary.json").write_text(
        json.dumps(summary,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps(summary,ensure_ascii=False,indent=2))
    sys.exit(0 if summary["status"].startswith("LOCAL_PASS") else 1)
if __name__=="__main__":main()
