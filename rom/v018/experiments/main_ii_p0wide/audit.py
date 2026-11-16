#!/usr/bin/env python3
"""Pixel-accurate Stella 6.7.1 proof of yellow P0 and independently colored wide copy.

No claim of a fourth distinct NPC: both P0 copies share the same 8x9 bitmap.
The M0-shot handling in the recolor variant is deliberately NOT integrated.
"""
import hashlib,json,re,sys
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parent
REF=json.loads((ROOT.parent/"main_ii_three_masks"/"REFERENCE_8x9_MASKS_FROM_MAIN.json").read_text())
Y0=162
def yellow(p):
    return p[0]>120 and p[1]>100 and p[2]<100
def white(p):
    return min(p)>180 and max(p)-min(p)<40
def sample(im,x0,mask,test):
    errors=0
    for i,bits in enumerate(mask):
        for bit in range(8):
            expected=bool(bits & (1<<(7-bit)))
            for dx in (0,1):
                actual=test(im.getpixel((x0+2*bit+dx,Y0+i)))
                errors+=int(actual!=expected)
    return errors
def find(im,mask,test,lo,hi):
    return sorted((sample(im,x,mask,test),x) for x in range(lo+(lo%2),hi,2))[:15]
def inspect(name):
    folder=ROOT/name
    text=(folder/"probe.asm").read_text()
    imfile=folder/"evidence"/"frame"/"stella_full.png"
    im=Image.open(imfile).convert("RGB")
    if im.size!=(1366,900):raise ValueError("Unknown debugger geometry")
    m=re.search(r"^PlayerRows:\s*\n\s+BYTE (.+)$",text,re.M)
    assert m, "Missing source P0 mask"
    player=[int(s.strip().replace("$","0x"),16) for s in m.group(1).split(",")][::-1]
    masks={n:[int(v,2) for v in REF["sprites"][n]]
           for n in ("large_male","large_female","small_male")}
    p1s={"large_male":166,"large_female":280,"small_male":394}
    p1errors={n:sample(im,x,masks[n],white) for n,x in p1s.items()}
    first_yellow=find(im,player,yellow,104,142)
    second_yellow=find(im,player,yellow,216,268)
    second_white=find(im,player,white,216,268)
    known_white=set()
    for n,x in p1s.items():
        for i,bits in enumerate(masks[n]):
            for bit in range(8):
                if bits & (1<<(7-bit)):
                    known_white.add((x+2*bit,Y0+i)); known_white.add((x+2*bit+1,Y0+i))
    # If a second P0 is white, include its exact pixel mask when counting ghosts.
    second_x=second_white[0][1] if second_white[0][0]==0 else None
    if second_x is not None:
        for i,bits in enumerate(player):
            for bit in range(8):
                if bits & (1<<(7-bit)):
                    known_white.update(((second_x+2*bit,Y0+i),
                                        (second_x+2*bit+1,Y0+i)))
    ghost=[(x,y) for y in range(Y0,Y0+9) for x in range(103,460)
           if white(im.getpixel((x,y))) and (x,y) not in known_white]
    hud=hashlib.sha256(im.crop((661,90,697,111)).tobytes()).hexdigest()
    scans=262 if hud in (
      "04f59d7fbc17d360e0cea738d4e512ab7208118b9b4d4b4743f3a702d96f1fdb",
      "a169787b7bdcf465b5a1b7505dca83c31f60fa2c16337d39fea3e957ea13ace2"
    ) else None
    shot_y=166 if name=="p0wide_control" else 160
    shot=sum(yellow(im.getpixel((x,shot_y))) for x in range(239,244))
    passes={
      "ntsc_262":scans==262,
      "three_original_white_masks":all(v==0 for v in p1errors.values()),
      "first_p0_player_yellow":first_yellow[0][0]==0,
      "second_p0_copy_yellow" :second_yellow[0][0]==0 if name=="p0wide_control" else None,
      "second_p0_copy_white" :second_white[0][0]==0 if name=="p0wide_recolor" else None,
      "no_unexpected_white_pixels":len(ghost)==0,
      "yellow_m0_test_pixel":shot>0
    }
    result={
      "variant":name,
      "source_p0_mask": [f"{n:02x}" for n in player],
      "p1_mask_biterrors":p1errors,
      "p0_first_yellow_top_candidates":first_yellow[:5],
      "p0_second_yellow_top_candidates":second_yellow[:5],
      "p0_second_white_top_candidates":second_white[:5],
      "ghost_white_pixel_count":len(ghost),
      "ghost_first_50":ghost[:50],
      "shot_expected_gui_y":shot_y,
      "shot_yellow_pixel_count":shot,
      "stella_scanlines":scans,
      "checks":passes,
      "status":"LOCAL_PASS_COPY_COLOR_ONLY" if all(v is None or v for v in passes.values()) else "FAIL_OR_INCONCLUSIVE",
      "limits":"P0 duplicates same original player mask. Recolor M0 shot is moved to preceding line. Not fourth unique original mask or full gameplay."
    }
    return result
def main():
    results={name:inspect(name) for name in ("p0wide_control","p0wide_recolor")}
    (ROOT/"audit.json").write_text(json.dumps(results,indent=2,ensure_ascii=False)+"\n")
    for name,r in results.items():
        print(name,r["status"],"P1 biterrors",r["p1_mask_biterrors"],
              "yellow first",r["p0_first_yellow_top_candidates"][0],
              "yellow copy",r["p0_second_yellow_top_candidates"][0],
              "white copy",r["p0_second_white_top_candidates"][0],
              "ghost",r["ghost_white_pixel_count"],
              "M0",r["shot_yellow_pixel_count"],"scan",r["stella_scanlines"])
    sys.exit(0 if all(r["status"]=="LOCAL_PASS_COPY_COLOR_ONLY" for r in results.values()) else 1)
if __name__=="__main__":main()
