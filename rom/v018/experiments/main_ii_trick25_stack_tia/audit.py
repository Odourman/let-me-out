#!/usr/bin/env python3
"""Actual Stella #25 stack PHA mirror pixel-equivalence check.

Both PF wall/door states must EXACTLY match STA COLUPF baseline at each
screen pixel, with brown PF retained and 262 NTSC scanlines.
A stack color write in Reset can prove TIA mirror, not a cycle saving in R1.
"""
from pathlib import Path
from PIL import Image
import hashlib,json,sys
ROOT=Path(__file__).resolve().parent
SRC=(ROOT/"stack_pha"/"probe.asm").read_text()
assert " LDX #$08\n TXS\nR25PhaColor:\n PHA\n LDX #$FF\n TXS" in SRC
KNOWN262={
 "04f59d7fbc17d360e0cea738d4e512ab7208118b9b4d4b4743f3a702d96f1fdb",
 "a169787b7bdcf465b5a1b7505dca83c31f60fa2c16337d39fea3e957ea13ace2"
}
def brown(p):return p[0]>145 and 60<p[1]<p[0] and p[2]<p[1] and p[2]<100
results={}
for state in ("locked","open"):
  paths={name:ROOT/name/"evidence"/state/"stella_full.png"
         for name in ("control_sta","stack_pha")}
  images={}
  for name,p in paths.items():
    im=Image.open(p).convert("RGB")
    if im.size!=(1366,900):raise ValueError("wrong Stella GUI")
    images[name]=im
  control=images["control_sta"];stack=images["stack_pha"]
  # The Stella debugger HUD contains bank/memory artifacts; only compare TIA output ROI.
  difference=0
  for y in range(82,287):
    for x in range(104,424):
      difference+=int(control.getpixel((x,y))!=stack.getpixel((x,y)))
  brown_rows={name:{
    "left": [y for y in range(82,287) if
              any(brown(im.getpixel((x,y))) for x in range(104,112))],
    "right": [y for y in range(82,287) if
               any(brown(im.getpixel((x,y))) for x in range(416,424))]
  } for name,im in images.items()}
  hashp={name:hashlib.sha256(im.crop((661,90,697,111)).tobytes()).hexdigest()
         for name,im in images.items()}
  scans={name:hashp[name] in KNOWN262 for name in images}
  expected_right=48 if state=="locked" else 16
  passed=(difference==0 and all(scans.values()) and
          all(len(rows["left"])==48 and len(rows["right"])==expected_right
          for rows in brown_rows.values()))
  results[state]={
     "pixel_differences_in_real_TIA_viewport":difference,
     "left_wall_brown_rows":{n:len(r["left"]) for n,r in brown_rows.items()},
     "right_wall_brown_rows":{n:len(r["right"]) for n,r in brown_rows.items()},
     "both_ROMs_262_NTSC":all(scans.values()),
     "same_TIA_raster_pixels":difference==0,
     "local_state_pass":passed,
     "screenshot_sha256":{n:hashlib.sha256(p.read_bytes()).hexdigest() for n,p in paths.items()}
  }
summary={
  "status":"LOCAL_PASS_PHA_WRITES_MIRRORED_TIA_COLUPF" if
     all(x["local_state_pass"] for x in results.values()) else "FAIL_OR_INCONCLUSIVE",
  "both_states_exact_TIA_image_match":all(x["same_TIA_raster_pixels"] for x in results.values()),
  "stack_pointer_restored_in_source":True,
  "R1_CPU_cycle_saving_demonstrated":False,
  "limitations":"PHA from stack pointer $08 writes $0108 mirrored TIA COLUPF only during Reset; no per-row timing benefit, no verified hardware console, no independent Verification."
}
(ROOT/"audit.json").write_text(json.dumps({"summary":summary,"states":results},ensure_ascii=False,indent=2)+"\n")
print(json.dumps({"summary":summary,"states":results},ensure_ascii=False,indent=2))
sys.exit(0 if summary["status"].startswith("LOCAL_PASS") else 1)
