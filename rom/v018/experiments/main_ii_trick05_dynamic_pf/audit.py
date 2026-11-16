#!/usr/bin/env python3
"""Fail-closed Stella 6.7.1 comparison of trick #05 PF1 raster sprite.

Four 16KB standard-F6 ROMs contain identical source NPCs and player. The extra
PF1 pattern moves four color clocks per PF bit, and automatically repeats in
the playfield's other half. No claim of independent same-Y humanoid sprites.
"""
from pathlib import Path
from PIL import Image
import hashlib,json,re,sys
ROOT=Path(__file__).resolve().parent
MANIFEST=json.loads((ROOT/"manifest.json").read_text())
REF=json.loads((ROOT.parent/"main_ii_three_masks"/"REFERENCE_8x9_MASKS_FROM_MAIN.json").read_text())
NAMES={"large_male":("MaleRows",154),"large_female":("FemaleRows",268),
       "small_female":("SmallFemaleRows",316),"small_male":("SmallMaleRows",400)}
BASE_COL=None
Y=162
def white(p):return min(p)>180 and max(p)-min(p)<40
def yellow(p):return p[0]>120 and p[1]>100 and p[2]<100
def extract(src,label):
    m=re.search(rf"^{label}:\s*\n\s+BYTE (.+)$",src,re.M)
    if not m:raise ValueError("No bitmap "+label)
    return [int(b.strip().replace("$","0x"),16) for b in m.group(1).split(",")][::-1]
def maskerrors(im,x,rows,test):
    err=0
    for y,row in enumerate(rows):
        for b in range(8):
            expected=bool(row & (1<<(7-b)))
            for dbl in (0,1):
                err+=int(test(im.getpixel((x+b*2+dbl,Y+y)))!=expected)
    return err
KNOWN_262={
 "04f59d7fbc17d360e0cea738d4e512ab7208118b9b4d4b4743f3a702d96f1fdb",
 "a169787b7bdcf465b5a1b7505dca83c31f60fa2c16337d39fea3e957ea13ace2"}
results={}
PF_SETS={}
for name in ("left2","left1","right1","right2"):
    dir=ROOT/name
    src=(dir/"probe.asm").read_text()
    imgpath=dir/"evidence"/"stella_full.png"
    img=Image.open(imgpath).convert("RGB")
    assert img.size==(1366,900)
    assert [f"{v:02X}" for v in extract(src,"PFRow")]==MANIFEST[name]["top_down_pf_rows_hex"]
    npc_errors={}
    for npc,(label,x) in NAMES.items():
        original=[int(b,2) for b in REF["sprites"][npc]]
        assert extract(src,label)==original
        npc_errors[npc]=maskerrors(img,x,original,white)
    player_error=maskerrors(img,188,extract(src,"PlayerRows"),yellow)
    missile_pixels=[x for x in range(104,423) if yellow(img.getpixel((x,160)))]
    hud=hashlib.sha256(img.crop((661,90,697,111)).tobytes()).hexdigest()
    pfcolor=img.getpixel((168,156)) if name=="left2" else img.getpixel((160,156)) if name=="left1" else img.getpixel((144,156)) if name=="right1" else img.getpixel((136,156))
    if BASE_COL is None:BASE_COL=pfcolor
    actual={(x,y) for y in range(152,161) for x in range(103,423)
             if img.getpixel((x,y))==BASE_COL}
    PF_SETS[name]=actual
    ghost_white=0;ghost_yellow=0
    expected_white=set()
    for npc,(label,x0) in NAMES.items():
        rows=extract(src,label)
        for iy,pattern in enumerate(rows):
            for bit in range(8):
                if pattern & (1<<(7-bit)):
                    expected_white.add((x0+2*bit,Y+iy))
                    expected_white.add((x0+2*bit+1,Y+iy))
    expected_yellow=set()
    for iy,pattern in enumerate(extract(src,"PlayerRows")):
        for bit in range(8):
            if pattern & (1<<(7-bit)):
                expected_yellow.add((188+2*bit,Y+iy))
                expected_yellow.add((188+2*bit+1,Y+iy))
    for y in range(Y,Y+9):
        for x in range(105,423):
            p=img.getpixel((x,y))
            ghost_white+=int(white(p) and (x,y) not in expected_white)
            ghost_yellow+=int(yellow(p) and (x,y) not in expected_yellow)
    results[name]={
      "pf_shift_register_bits":MANIFEST[name]["shift_pf_bits"],
      "pf_color_rgb":list(BASE_COL),
      "pf_colored_gui_pixels":len(actual),
      "pf_row156_colored_x":sorted(x for x,y in actual if y==156),
      "all_four_source_mask_pixel_errors":npc_errors,
      "yellow_P0_mask_errors":player_error,
      "M0_yellow_x_on_160":missile_pixels,
      "unexpected_NPC_band_white_pixels":ghost_white,
      "unexpected_NPC_band_yellow_pixels":ghost_yellow,
      "ntsc_262":hud in KNOWN_262,
      "screen_sha256":hashlib.sha256(imgpath.read_bytes()).hexdigest()}
base=PF_SETS["left2"]
dx={"left2":0,"left1":-8,"right1":-24,"right2":-32}
for name in results:
    expected={(x+dx[name],y) for x,y in base}
    results[name]["pf_entire_sprite_exact_translation"]=(PF_SETS[name]==expected)
    row=sorted(x for x,y in PF_SETS[name] if y==156)
    runs=[]
    for xx in row:
        if not runs or xx>runs[-1][-1]+1:runs.append([xx])
        else:runs[-1].append(xx)
    results[name]["middle_row_pf_runs"]=[[r[0],r[-1],len(r)] for r in runs]
    results[name]["playfield_duplicated_half_80cc"]=(
        len(runs)==2 and runs[1][0]-runs[0][0]==160)
    r=results[name]
    r["local_test_pass"]=(r["ntsc_262"] and
        all(v==0 for v in r["all_four_source_mask_pixel_errors"].values()) and
        r["yellow_P0_mask_errors"]==0 and r["M0_yellow_x_on_160"]==[240,241] and
        r["unexpected_NPC_band_white_pixels"]==0 and
        r["unexpected_NPC_band_yellow_pixels"]==0 and
        r["pf_colored_gui_pixels"]==len(base)==320 and
        r["pf_entire_sprite_exact_translation"] and
        r["playfield_duplicated_half_80cc"])
summary={
 "status":"LOCAL_PASS_PF1_COARSE_SPRITE_SEPARATE_BAND" if
  all(r["local_test_pass"] for r in results.values()) else "FAIL_OR_INCONCLUSIVE",
 "variants_passed":sum(r["local_test_pass"] for r in results.values()),
 "pf_width_tia_cc_per_bit":4,
 "pf_two_copies_gui_separation_px":160,
 "four_original_npc_masks_preserved":all(
   all(v==0 for v in r["all_four_source_mask_pixel_errors"].values())
   for r in results.values()),
 "limitations":"PF figure occupies distinct band above 4 NPCs; cannot substitute an exact 8-bit 8x9 humanoid or freely positioned same-Y NPC; no walls, door, 600 frames or independent verification."}
out={"summary":summary,"variants":results}
(ROOT/"audit.json").write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n")
print(json.dumps({"summary":summary,"variants":{
 name:{k:v for k,v in r.items() if k not in ("pf_row156_colored_x",)} for name,r in results.items()
}},indent=2,ensure_ascii=False))
sys.exit(0 if summary["status"].startswith("LOCAL_PASS") else 1)
