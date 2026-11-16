#!/usr/bin/env python3
"""Assess actual Stella two-line rendering, without hiding source-mask fidelity.

An experimental result is valid when control is pixel-exact and both real ROM
screenshots are present. A negative two-line design outcome is a VALID finding.
"""
from pathlib import Path
from PIL import Image
import json,re,hashlib,sys
ROOT=Path(__file__).resolve().parent
REF=json.loads((ROOT.parent/"main_ii_three_masks"/"REFERENCE_8x9_MASKS_FROM_MAIN.json").read_text())
SRC=(ROOT/"two_line_naive"/"probe.asm").read_text()
NPCS=[("large_male","MaleRows",154),("large_female","FemaleRows",268),
      ("small_female","SmallFemaleRows",316),("small_male","SmallMaleRows",400)]
Y0=162
def mask(sym):
    q=re.search(rf"^{sym}:\s*\n\s+BYTE (.+)$",SRC,re.M)
    assert q
    return [int(x.strip().replace("$","0x"),16) for x in q.group(1).split(",")][::-1]
MASKS={}
for name,sym,x in NPCS:
    exp=[int(s,2) for s in REF["sprites"][name]]
    got=mask(sym)
    assert exp==got, f"source was modified {name}"
    MASKS[name]=got
PLAYER=mask("PlayerRows")
def white(p):return min(p)>180 and max(p)-min(p)<40
def yellow(p):return p[0]>120 and p[1]>100 and p[2]<100
def err(im,x,rows,c,ystart,ystep):
    errors=0
    for row,data in enumerate(rows):
        for b in range(8):
            exp=bool(data & (1<<(7-b)))
            for dbl in (0,1):
                seen=c(im.getpixel((x+2*b+dbl,ystart+ystep*row)))
                errors+=int(seen!=exp)
    return errors
KNOWN262={
 "04f59d7fbc17d360e0cea738d4e512ab7208118b9b4d4b4743f3a702d96f1fdb",
 "a169787b7bdcf465b5a1b7505dca83c31f60fa2c16337d39fea3e957ea13ace2"}
results={}
for variant in ("control_one_line","two_line_naive"):
    path=ROOT/variant/"evidence"/"stella_full.png"
    img=Image.open(path).convert("RGB")
    assert img.size==(1366,900)
    h=hashlib.sha256(img.crop((661,90,697,111)).tobytes()).hexdigest()
    nc={name:err(img,x,MASKS[name],white,Y0,1) for name,sym,x in NPCS}
    ec={name:err(img,x,MASKS[name],white,Y0,2) for name,sym,x in NPCS}
    p0=err(img,188,PLAYER,yellow,Y0,1)
    results[variant]={
      "original_source_masks_unchanged":True,
      "raw_screenshot_sha256":hashlib.sha256(path.read_bytes()).hexdigest(),
      "ntsc_262":h in KNOWN262,
      "ntsc_hud_sha256":h,
      "nine_original_rows_at_original_y_error_pixels":nc,
      "nine_original_rows_every_second_line_error_pixels":ec,
      "p0_yellow_original_9row_errors":p0,
      "distinct_white_pixels_in_original_9row_band":sum(white(img.getpixel((xx,yy))) for yy in range(Y0,Y0+9) for xx in range(150,430))
    }
control=results["control_one_line"]
two=results["two_line_naive"]
control_pass=(control["ntsc_262"] and
    all(v==0 for v in control["nine_original_rows_at_original_y_error_pixels"].values())
    and control["p0_yellow_original_9row_errors"]==0)
two_pass=(two["ntsc_262"] and
    all(v==0 for v in two["nine_original_rows_at_original_y_error_pixels"].values())
    and two["p0_yellow_original_9row_errors"]==0)
summary={
    "control_valid_4_original_masks":control_pass,
    "two_line_variant_original_9x9_fidelity":two_pass,
    "two_line_test_outcome":"LOCAL_PASS_9ROW" if two_pass else "NEGATIVE_VARIANT_DOES_NOT_PRESERVE_9ROW",
    "experiment_valid":control_pass,
    "limitations":"This is one naive double-scanline kernel, not all two-line/VDEL architectures; no 600 frames, no independent verification."
}
result={"summary":summary,"variants":results}
(ROOT/"audit.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
print(json.dumps(result,ensure_ascii=False,indent=2))
sys.exit(0 if control_pass else 1)
if __name__=="__main__":main()
