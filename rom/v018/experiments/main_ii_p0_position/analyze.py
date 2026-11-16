#!/usr/bin/env python3
"""Stella 6.7.1 P0Delay calibration; report measured X, not guesses."""
from pathlib import Path
from PIL import Image
import json,hashlib
ROOT=Path(__file__).resolve().parent
PLAYER=[0x3c,0x7e,0x18,0x7e,0x1e,0x3c,0x18,0x24,0x42]
def yellow(p):return p[0]>120 and p[1]>100 and p[2]<100
def score(im,x):
    errors=0
    for row,byte in enumerate(PLAYER):
        for b in range(8):
            want=bool(byte & (1<<(7-b)))
            for dx in (0,1):
                seen=yellow(im.getpixel((x+2*b+dx,162+row)))
                errors+=int(want!=seen)
    return errors
result={}
for v in [4,6,8,10,12,13,14,15]:
    f=ROOT/("delay_%02d"%v)/"evidence"/"stella_full.png"
    im=Image.open(f).convert("RGB")
    if im.size!=(1366,900):raise ValueError("unexpected Stella screen")
    candidates=sorted((score(im,x),x) for x in range(104,420,2))
    exact=[x for err,x in candidates if err==0]
    hud=hashlib.sha256(im.crop((661,90,697,111)).tobytes()).hexdigest()
    scan262=hud in {
     "04f59d7fbc17d360e0cea738d4e512ab7208118b9b4d4b4743f3a702d96f1fdb",
     "a169787b7bdcf465b5a1b7505dca83c31f60fa2c16337d39fea3e957ea13ace2"
    }
    result[str(v)]={
        "p0_delay_loop":v, "best_mask_error":candidates[0][0],
        "best_gui_x":candidates[0][1], "exact_full_8x9_gui_x":exact,
        "ntsc_262":scan262, "top_6_candidates":candidates[:6],
        "screenshot_sha256":hashlib.sha256(f.read_bytes()).hexdigest()
    }
(ROOT/"calibration.json").write_text(json.dumps(result,indent=2)+"\n")
for k,v in result.items():
    print("P0Delay",k,"GUI X",v["best_gui_x"],"mask errors",v["best_mask_error"],
          "exact x",v["exact_full_8x9_gui_x"],"NTSC262",v["ntsc_262"])
