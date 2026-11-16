#!/usr/bin/env python3
"""Asymmetric right-only PF0 door: real Stella pixel audit for two frame modes.

The PF0 bit D4 must remain at x=0 on every one of 48 rows, including when
right door x=39 is OPEN. Door opens only for 32 middle rows. Locked state
keeps right wall all 48; same 262 NTSC. This is isolated R3-style PF, NOT
the 4-NPC R1f simultaneous kernel, nor a full colored-keyhole design pass.
"""
from pathlib import Path
from PIL import Image
import hashlib,json,sys
ROOT=Path(__file__).resolve().parent
KNOWN262={
 "04f59d7fbc17d360e0cea738d4e512ab7208118b9b4d4b4743f3a702d96f1fdb",
 "a169787b7bdcf465b5a1b7505dca83c31f60fa2c16337d39fea3e957ea13ace2"
}
def nonblack(p):
    return max(p)>35 and max(p)-min(p)<135 # brown PF, not UI text
imgs={}
results={}
for name in ("locked","open"):
    path=ROOT/"evidence"/name/"stella_full.png"
    im=Image.open(path).convert("RGB")
    assert im.size==(1366,900), f"Stella GUI geometry changed {im.size}"
    imgs[name]=im
    colored_rows={}
    for y in range(80,285):
        xs=[x for x in range(103,423) if nonblack(im.getpixel((x,y)))]
        if xs:colored_rows[y]=xs
    left_rows=[y for y,xs in colored_rows.items() if any(x<120 for x in xs)]
    right_rows=[y for y,xs in colored_rows.items() if any(x>=408 for x in xs)]
    center_pixels=sum(sum(120<=x<408 for x in xs) for xs in colored_rows.values())
    hud=hashlib.sha256(im.crop((661,90,697,111)).tobytes()).hexdigest()
    results[name]={
      "seen_nonblack_rows":sorted(colored_rows),
      "left_wall_rows":left_rows,
      "right_wall_rows":right_rows,
      "left_wall_row_count":len(left_rows),
      "right_wall_row_count":len(right_rows),
      "unwanted_midfield_brown_pixels":center_pixels,
      "left_wall_x_middle":sorted(x for x in colored_rows.get(left_rows[len(left_rows)//2],[]) if x<120) if left_rows else [],
      "right_wall_x_middle":sorted(x for x in colored_rows.get(left_rows[len(left_rows)//2],[]) if x>=408) if left_rows else [],
      "ntsc_262":hud in KNOWN262,
      "hud_hash":hud,
      "screenshot_sha256":hashlib.sha256(path.read_bytes()).hexdigest()
    }
a=results["locked"];b=results["open"]
left_equal=a["left_wall_rows"]==b["left_wall_rows"]
left_contiguous=(
    len(a["left_wall_rows"])==48 and
    a["left_wall_rows"]==list(range(a["left_wall_rows"][0],a["left_wall_rows"][0]+48)))
locked_right=a["right_wall_rows"]==a["left_wall_rows"]
open_right=(
   b["right_wall_rows"]==
   b["left_wall_rows"][:8]+b["left_wall_rows"][-8:] if left_contiguous else False)
all_ok=(left_equal and left_contiguous and locked_right and open_right and
        a["ntsc_262"] and b["ntsc_262"] and
        a["unwanted_midfield_brown_pixels"]==0 and b["unwanted_midfield_brown_pixels"]==0)
summary={
 "status":"LOCAL_PASS_ASYMMETRIC_PF_LEFT_CLOSED_RIGHT_OPENS" if all_ok else "FAIL_OR_INCONCLUSIVE",
 "left_wall_identical_locked_open":left_equal,
 "left_wall_48_contiguous_rows":left_contiguous,
 "locked_right_wall_48_rows":locked_right,
 "open_right_32_central_rows_only":open_right,
 "NTSC_262_both":a["ntsc_262"] and b["ntsc_262"],
 "limitations":"Brown PF0 left/right R3 geometry primitive; NOT the full map, no orange port or black keyhole, no same-line four NPC or independent Verification."
}
(ROOT/"audit.json").write_text(json.dumps({"summary":summary,"samples":results},ensure_ascii=False,indent=2)+"\n")
print(json.dumps({"summary":summary,
 "counts":{n:{k:v for k,v in row.items() if k in ("left_wall_row_count","right_wall_row_count","unwanted_midfield_brown_pixels","ntsc_262","left_wall_x_middle","right_wall_x_middle")} for n,row in results.items()}},
 indent=2,ensure_ascii=False))
sys.exit(0 if all_ok else 1)
