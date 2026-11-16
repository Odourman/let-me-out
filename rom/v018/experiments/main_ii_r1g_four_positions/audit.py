#!/usr/bin/env python3
"""Fail-closed real-Stella proof gate for R1f P0 independence.

Every white/colored original bitmap must be exact 8x9 in RAW debugger images,
with exactly one copy of each, 0 ghost white/yellow pixels, a single M0,
262 NTSC lines, and the yellow player position identical across two
variants while fourth small female position CHANGES independent of it.
"""
from pathlib import Path
from PIL import Image
import hashlib,json,re,sys
ROOT=Path(__file__).resolve().parent
REF=json.loads((ROOT.parent/"main_ii_three_masks"/"REFERENCE_8x9_MASKS_FROM_MAIN.json").read_text())
VARIANTS=("pre_mask","post_mask","post_lda","post_color")
NAMES=("large_male","large_female","small_male","small_female")
LABELS=("MaleRows","FemaleRows","SmallMaleRows","SmallFemaleRows")
Y0=162
def white(p): return min(p)>180 and max(p)-min(p)<40
def yellow(p):return p[0]>120 and p[1]>100 and p[2]<100
def source_data(src,label):
    m=re.search(rf"^{label}:\s*\n\s+BYTE (.+)$",src,re.M)
    if not m:raise ValueError("Missing source table "+label)
    return [int(x.strip().replace("$","0x"),16) for x in m.group(1).split(",")][::-1]
def score(im,x,rows,fn):
    errors=0
    for j,mask in enumerate(rows):
        for bit in range(8):
            wanted=bool(mask & (1<<(7-bit)))
            for sub in (0,1):
                got=fn(im.getpixel((x+bit*2+sub,Y0+j)))
                errors+=int(got!=wanted)
    return errors
def shape_points(x,rows):
    out=set()
    for j,mask in enumerate(rows):
        for bit in range(8):
            if mask&(1<<(7-bit)):
                out.add((x+bit*2,Y0+j))
                out.add((x+bit*2+1,Y0+j))
    return out
KNOWN262={
"04f59d7fbc17d360e0cea738d4e512ab7208118b9b4d4b4743f3a702d96f1fdb",
"a169787b7bdcf465b5a1b7505dca83c31f60fa2c16337d39fea3e957ea13ace2"
}
results={}
for variant in VARIANTS:
    folder=ROOT/variant
    src=(folder/"probe.asm").read_text()
    imfile=folder/"evidence"/"frame"/"stella_full.png"
    image=Image.open(imfile).convert("RGB")
    if image.size!=(1366,900):raise ValueError("Stella UI geometry changed")
    source_originals={}
    masks={}
    for name,label in zip(NAMES,LABELS):
        reference=[int(bits,2) for bits in REF["sprites"][name]]
        actual=source_data(src,label)
        source_originals[name]=actual==reference
        masks[name]=reference
    player=source_data(src,"PlayerRows")
    match={}
    for name in NAMES+("yellow_player",):
        rows=player if name=="yellow_player" else masks[name]
        fn=yellow if name=="yellow_player" else white
        # All potential positions, including negative results, checked at 2x GUI scale.
        top=sorted((score(image,x,rows,fn),x) for x in range(106,427,2))
        exact=[x for count,x in top if count==0]
        match[name]={
           "best_error_gui_pixels":top[0][0],
           "best_x_raw_gui":top[0][1],
           "exact_match_xs":exact,
           "unique_full_original_mask":len(exact)==1
        }
    knownwhite=set();knownyellow=set()
    for name in NAMES:
        if match[name]["unique_full_original_mask"]:
            knownwhite|=shape_points(match[name]["exact_match_xs"][0],masks[name])
    if match["yellow_player"]["unique_full_original_mask"]:
        knownyellow=shape_points(match["yellow_player"]["exact_match_xs"][0],player)
    extra_white=[(x,y) for y in range(Y0,Y0+9) for x in range(105,429)
                 if white(image.getpixel((x,y))) and (x,y) not in knownwhite]
    extra_yellow=[(x,y) for y in range(Y0,Y0+9) for x in range(105,429)
                  if yellow(image.getpixel((x,y))) and (x,y) not in knownyellow]
    shot=[x for x in range(105,429) if yellow(image.getpixel((x,160)))]
    hud=hashlib.sha256(image.crop((661,90,697,111)).tobytes()).hexdigest()
    phasepass=(
       all(source_originals.values()) and
       all(m["unique_full_original_mask"] for m in match.values()) and
       len(extra_white)==0 and len(extra_yellow)==0 and
       shot==[240,241] and hud in KNOWN262
    )
    results[variant]={
      "exact_approved_source_masks":source_originals,
      "screenshot_sha256":hashlib.sha256(imfile.read_bytes()).hexdigest(),
      "matched_shapes":match,
      "white_ghost_gui_pixels":len(extra_white),
      "yellow_ghost_gui_pixels":len(extra_yellow),
      "white_ghost_first_32":extra_white[:32],
      "yellow_ghost_first_32":extra_yellow[:32],
      "single_m0_gui_x":shot,
      "ntsc_262":hud in KNOWN262,
      "stella_hud_sha256":hud,
      "local_phase_pass":phasepass
    }
def unique_x(variant,name):
    obj=results[variant]["matched_shapes"][name]
    return obj["exact_match_xs"][0] if obj["unique_full_original_mask"] else None
p0_x=[unique_x(v,"yellow_player") for v in VARIANTS]
fourth_x=[unique_x(v,"small_female") for v in VARIANTS]
p1_fixed=all(unique_x(VARIANTS[0],name) is not None and
              all(unique_x(v,name)==unique_x(VARIANTS[0],name) for v in VARIANTS)
              for name in NAMES if name!="small_female")
p0_stays=p0_x[0] is not None and all(x==p0_x[0] for x in p0_x)
white_changes=all(x is not None for x in fourth_x) and len(set(fourth_x))>=3
allpass=all(results[v]["local_phase_pass"] for v in VARIANTS)
summary={
  "status":"LOCAL_PASS_FOURTH_X_INDEPENDENT_MULTIPLE_CLEAN_CONFIGS" if
      allpass and p0_stays and white_changes and p1_fixed else "FAIL_OR_INCONCLUSIVE",
  "real_stella_6_7_1_four_configs":True,
  "individual_variants_full_mask_clean":{v:results[v]["local_phase_pass"] for v in VARIANTS},
  "yellow_player_x_gui":p0_x,
  "fourth_white_small_female_x_gui":fourth_x,
  "player_x_unchanged":p0_stays,
  "white_fourth_x_changed_independent_of_player":white_changes,
  "first_three_p1_original_x_unchanged":p1_fixed,
  "fourth_white_independent_range_tia_cc":(max(fourth_x)-min(fourth_x))/2 if white_changes else None,
  "limits":"Four cycle-equal RESP0 variants, at least three independent fourth NPC positions; NOT arbitrary 160-CC X, close overlap, 600 continuous frame movement, full PF walls or six NPCs. M0 on preceding row, no independent Verification."
}
report={"summary":summary,"variants":results}
(ROOT/"audit.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n")
print(json.dumps(report,ensure_ascii=False,indent=2))
sys.exit(0 if summary["status"].startswith("LOCAL_PASS") else 1)
