#!/usr/bin/env python3
"""Fail-closed 2 REAL Stella snapshots: four distinct original NPC 8x9 masks,
one player+M0, BALL left outer wall x0, PF0 right-only 32-raster-line doorway.

This is a local RESEARCH proof, NOT full R1/R3, no orange/keyhole/physical Atari.
"""
from pathlib import Path
from PIL import Image
import hashlib,json,re,sys
ROOT=Path(__file__).resolve().parent
REF=json.loads((ROOT.parent/"main_ii_three_masks"/"REFERENCE_8x9_MASKS_FROM_MAIN.json").read_text())
SRC=(ROOT/"r1h_integrated.asm").read_text()
NPCS={"large_male":("MaleRows",166),"large_female":("FemaleRows",280),
      "small_male":("SmallMaleRows",406)}
FOURTH_X=(330,348,360,378)
KNOWN262={
 "04f59d7fbc17d360e0cea738d4e512ab7208118b9b4d4b4743f3a702d96f1fdb",
 "a169787b7bdcf465b5a1b7505dca83c31f60fa2c16337d39fea3e957ea13ace2"
}
def brown(p):return p[0]>145 and 60<p[1]<p[0] and p[2]<p[1] and p[2]<100
def white(p):return min(p)>180 and max(p)-min(p)<40
def yellow(p):return p[0]>120 and p[1]>100 and p[2]<100
def bytes_for(label):
    m=re.search(rf"^{label}:\s*\n\s+BYTE (.+)$",SRC,re.M)
    assert m,f"no source bytes {label}"
    return [int(q.strip().replace("$","0x"),16) for q in m.group(1).split(",")][::-1]
ORIGINAL={}
for name,(label,x) in NPCS.items():
    original=[int(q,2) for q in REF["sprites"][name]]
    assert bytes_for(label)==original
    ORIGINAL[name]=original
FOURTH=[int(q,2) for q in REF["sprites"]["small_female"]]
assert bytes_for("SmallFemaleRows")==FOURTH
PLAYER=bytes_for("PlayerRows")
def errors(im,x,mask,fn):
    count=0
    for y,byte in enumerate(mask):
        for bit in range(8):
            expected=bool(byte&(1<<(7-bit)))
            for d in (0,1):
                count+=int(fn(im.getpixel((x+bit*2+d,162+y)))!=expected)
    return count
def points(x,mask):
    return {(x+bit*2+d,162+y)
            for y,row in enumerate(mask) for bit in range(8) for d in (0,1)
            if row&(1<<(7-bit))}
known_white=set().union(*(points(x,ORIGINAL[name]) for name,(label,x) in NPCS.items()))
known_yellow=points(216,PLAYER)
results={}
imgs={}
for name in ("locked","open"):
    p=ROOT/"evidence"/name/"stella_full.png"
    img=Image.open(p).convert("RGB")
    assert img.size==(1366,900)
    imgs[name]=img
    fourth_errors={str(x):errors(img,x,FOURTH,white) for x in FOURTH_X}
    exact_fourth=[int(x) for x,n in fourth_errors.items() if n==0]
    fourth=exact_fourth[0] if len(exact_fourth)==1 else None
    expected_white=known_white|(points(fourth,FOURTH) if fourth is not None else set())
    npc_errors={name:errors(img,x,ORIGINAL[name],white) for name,(label,x) in NPCS.items()}
    player_errors=errors(img,216,PLAYER,yellow)
    extra_white=sum(white(img.getpixel((x,y))) and (x,y) not in expected_white
                    for y in range(162,171) for x in range(104,424))
    extra_yellow=sum(yellow(img.getpixel((x,y))) and (x,y) not in known_yellow
                    for y in range(162,171) for x in range(104,424))
    left_180=[x for x in range(104,130) if brown(img.getpixel((x,180)))]
    left_155=[x for x in range(104,130) if brown(img.getpixel((x,155)))]
    right_rows=[y for y in range(115,220) if brown(img.getpixel((423,y)))]
    shot=[x for x in range(104,424) if yellow(img.getpixel((x,160)))]
    hashud=hashlib.sha256(img.crop((661,90,697,111)).tobytes()).hexdigest()
    results[name]={
      "fourth_exact_positions":exact_fourth,
      "fourth_position_gui_x":fourth,
      "three_P1_original_mask_errors":npc_errors,
      "yellow_P0_original_mask_errors":player_errors,
      "white_ghost_pixels":extra_white,
      "yellow_ghost_pixels":extra_yellow,
      "left_ball_gui_x_155":left_155,
      "left_ball_gui_x_180":left_180,
      "right_PF0_visible_rows_at_x423":right_rows,
      "M0_yellow_gui_x":shot,
      "ntsc_262":hashud in KNOWN262,
      "screenshot_sha256":hashlib.sha256(p.read_bytes()).hexdigest()
    }
locked=results["locked"];opened=results["open"]
locked_rows=set(locked["right_PF0_visible_rows_at_x423"])
open_rows=set(opened["right_PF0_visible_rows_at_x423"])
gap=sorted(locked_rows-open_rows)
gap_contiguous=len(gap)==32 and gap==list(range(gap[0],gap[0]+32))
left_expected=list(range(104,112))
def basepass(r):
    return (r["fourth_position_gui_x"] is not None and
      all(n==0 for n in r["three_P1_original_mask_errors"].values()) and
      r["yellow_P0_original_mask_errors"]==0 and
      r["white_ghost_pixels"]==0 and r["yellow_ghost_pixels"]==0 and
      r["left_ball_gui_x_155"]==left_expected and
      r["left_ball_gui_x_180"]==left_expected and
      r["M0_yellow_gui_x"]==[240,241] and r["ntsc_262"])
complete=(basepass(locked) and basepass(opened) and
  gap_contiguous and all(y in gap for y in range(162,171)) and
  not(open_rows-locked_rows) and len(locked_rows)==105 and len(open_rows)==73)
summary={
 "status":"LOCAL_PASS_R1H_FOUR_NPCS_BALL_LEFT_PF_RIGHT_32ROW_DOOR" if complete else "FAIL_OR_INCONCLUSIVE",
 "two_real_Stella_frames":True,
 "original_four_8x9_NPC_masks_unchanged":True,
 "left_ball_x0_exact_both_states":all(r["left_ball_gui_x_180"]==left_expected for r in results.values()),
 "left_wall_same_during_opening":locked["left_ball_gui_x_180"]==opened["left_ball_gui_x_180"],
 "right_door_gap_contiguous_32_scanlines":gap_contiguous,
 "right_door_gap_first_last_y":[gap[0],gap[-1]] if gap else None,
 "gap_includes_all_nine_NPC_rows":all(y in gap for y in range(162,171)),
 "NTSC_262_both":locked["ntsc_262"] and opened["ntsc_262"],
 "ROM_sha256":hashlib.sha256((ROOT/"r1h_F6.bin").read_bytes()).hexdigest(),
 "limitations":"Only two still frames of one ROM; phase-correlated X+door selection; BALL permanently consumed; no orange keyhole, no full 40x22 map or independent Verification."
}
(ROOT/"evidence"/"audit_two.json").write_text(
 json.dumps({"summary":summary,"samples":results},indent=2,ensure_ascii=False)+"\n")
print(json.dumps({"summary":summary,"state_counts":{
 n:{k:v for k,v in result.items() if k in (
 "fourth_position_gui_x","three_P1_original_mask_errors","yellow_P0_original_mask_errors",
 "white_ghost_pixels","yellow_ghost_pixels","left_ball_gui_x_180","M0_yellow_gui_x","ntsc_262")} for n,result in results.items()}},indent=2))
sys.exit(0 if complete else 1)
