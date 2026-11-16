#!/usr/bin/env python3
"""Read exact BALL 4CC colors and 262 NTSC from actual Stella X11 frames."""
from pathlib import Path
from PIL import Image
import hashlib,json,sys
ROOT=Path(__file__).resolve().parent
KNOWN262={
 "04f59d7fbc17d360e0cea738d4e512ab7208118b9b4d4b4743f3a702d96f1fdb",
 "a169787b7bdcf465b5a1b7505dca83c31f60fa2c16337d39fea3e957ea13ace2"}
def brown(p):return p[0]>145 and 60<p[1]<p[0] and p[2]<p[1] and p[2]<100
results={}
for delay in range(8):
    path=ROOT/f"delay_{delay}"/"evidence"/"open"/"stella_full.png"
    img=Image.open(path).convert("RGB")
    assert img.size==(1366,900)
    # Pick a row below sprite band; ball and PF walls persist every scanline.
    y=180
    xs=[x for x in range(104,424) if brown(img.getpixel((x,y)))]
    left=[x for x in xs if x<200]
    right=[x for x in xs if x>=400]
    scanhash=hashlib.sha256(img.crop((661,90,697,111)).tobytes()).hexdigest()
    results[str(delay)]={
      "brown_ball_left_gui_x":left,
      "brown_rightedge_x":right,
      "left_4cc_ball_8raw_gui_pixels":len(left)==8 and left==list(range(left[0],left[0]+8)),
      "NTSC_262":scanhash in KNOWN262,
      "screenshot_sha256":hashlib.sha256(path.read_bytes()).hexdigest()
    }
winners=[int(k) for k,v in results.items()
  if v["brown_ball_left_gui_x"]==list(range(104,112))
  and v["brown_rightedge_x"]==[] and v["NTSC_262"]]
summary={
 "status":"CALIBRATED_BALL_X0_WITH_R1G_KERNEL" if winners else "NEGATIVE_OR_NEEDS_NEW_RESBL_DELAY",
 "exact_left_edge_NOP_counts":winners,
 "expected_left_wall_gui_x":list(range(104,112)),
 "tested_real_stella_images":len(results),
 "each_262NTSC":all(v["NTSC_262"] for v in results.values()),
 "open_frame_has_no_right_wall":all(v["brown_rightedge_x"]==[] for v in results.values()),
 "limits":"Calibration only; four 8x9 NPC mask regression and locked right door still require integrated 600-frame run."
}
(ROOT/"calibration.json").write_text(json.dumps({"summary":summary,"variants":results},indent=2)+"\n")
print(json.dumps({"summary":summary,"positions":{k:(v["brown_ball_left_gui_x"],v["brown_rightedge_x"]) for k,v in results.items()}},indent=2))
sys.exit(0 if winners else 1)
