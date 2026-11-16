#!/usr/bin/env python3
"""Independent pixel audit (not organizational VERIFICATION):
600 authentic real Stella 6.7.1 screenshot frames, full original 9-row
male/female P1 masks at same Y, single full yellow P0 and one M0 symbol;
4 nominal independently shifted P1 close-X pairs. Fail closed, report
per-frame mistakes and real bitmap position, never infer success from source.
"""
from pathlib import Path
from PIL import Image
import re,sys,csv,json,hashlib,collections
ROOT=Path(__file__).resolve().parent
OUT=ROOT/"evidence_600"
SRC=(ROOT/"r1ag.asm").read_text()
FRAME_RANGE=range(50,195)
X_RANGE=range(0,336)
HUD_SCAN262={
 "04f59d7fbc17d360e0cea738d4e512ab7208118b9b4d4b4743f3a702d96f1fdb",
 "a169787b7bdcf465b5a1b7505dca83c31f60fa2c16337d39fea3e957ea13ace2"
}
def mask(name):
 m=re.search(rf"^{name}:\s*\n\s+BYTE ([^\n]+)",SRC,re.M)
 if not m:raise ValueError(f"No {name}")
 return [int(v.strip().removeprefix("$"),16) for v in m.group(1).split(",")][::-1]
MALE=mask("MaleRows")
FEMALE=mask("FemaleRows")
PLAYER=mask("PlayerRows")
assert MALE==[0x42,0x42,0x24,0x24,0x18,0xff,0x18,0x3c,0x3c]
assert FEMALE==[0x24,0x24,0x7e,0x7e,0x3c,0xff,0x18,0x3c,0x3c]
assert PLAYER==[0x42,0x24,0x18,0x3c,0x1e,0x7e,0x18,0x7e,0x3c]
def pts(mask):
 return {(bit*2+dx,y) for y,byte in enumerate(mask)
         for bit in range(8) if byte & (0x80 >> bit) for dx in (0,1)}
M=pts(MALE);F=pts(FEMALE);P=pts(PLAYER)
ORDER=json.loads((ROOT/'manifest.json').read_text())['mask_order']
FIRST,SECOND=(F,M) if ORDER=='F->M' else (M,F)
def white(c):return min(c)>180 and max(c)-min(c)<40
def yellow(c):return c[0]>120 and c[1]>100 and c[2]<100
def glyph(im,x):
 return tuple((lambda c:c[0]>210 and c[1]>150 and c[2]<180)
       (im.getpixel((a,b))) for b in range(9,19) for a in range(x,x+7))
def hud_id(im,lookup):
 values=[]
 for x in (561,570,579):
  g=glyph(im,x)
  if not any(g):continue
  matched=[n for n,pat in lookup.items() if pat==g]
  if len(matched)!=1:return None
  values.append(str(matched[0]))
 return int("".join(values)) if values else None
def shifted(delta,x,y):
 return {(px+x,py+y) for (px,py) in delta}
def best_mask_pairs(actual,basey):
 """Find actual pair by FULL 9-row pattern correlation without assumed X."""
 if not actual:return (None,None,10000,10000,10000)
 xs=[p[0] for p in actual]
 lo=max(0,min(xs)-16);hi=min(320,max(xs)+1)
 # Candidate cost charges both missing and unexpected same-box pixels.
 # It is evaluated for ALL nine rows; ghosts outside the two boxes remain
 # in global delta and are never silently discounted.
 candidates=[]
 for delta in (FIRST,SECOND):
  rank=[]
  for x in range(lo,hi+1):
   expected=shifted(delta,x,basey)
   intersection=len(expected & actual)
   unexpected=sum(1 for wx,wy in actual if x<=wx<x+16)
   score=2*(len(expected)-intersection)+unexpected-intersection
   rank.append((score,x))
  rank.sort()
  candidates.append(rank[:10])
 best=None
 for _,a in candidates[0]:
  for _,b in candidates[1]:
   if b<a+16:continue
   first=shifted(FIRST,a,basey);second=shifted(SECOND,b,basey)
   exp=first|second
   missing=len(exp-actual)
   extra=len(actual-exp)
   score=missing+extra
   candidate=(a,b,missing,extra,score)
   if best is None or score<best[-1]:best=candidate
 return best if best is not None else (None,None,999,999,999)
def best_yellow(actual,basey):
 if not actual:return (None,999,999,999,0)
 xs=[p[0] for p in actual]
 low=max(0,min(xs)-16);high=min(320,max(xs)+1)
 rank=[]
 for x in range(low,high+1):
  player=shifted(P,x,basey)
  miss=len(player-actual)
  extras=actual-player
  # Test-shot is exactly two horizontal adjacent yellow pixels on one
  # other-than-player position, in this same nine-row band.
  shot=sorted(extras,key=lambda z:(z[1],z[0]))
  shot_pass=(len(shot)==2 and shot[0][1]==shot[1][1] and
             shot[1][0]==shot[0][0]+1 and shot[0][1]==basey+4)
  cost=miss+(0 if shot_pass else len(extras)+10)
  rank.append((cost,x,miss,len(extras),int(shot_pass)))
 rank.sort()
 return (rank[0][1],rank[0][2],rank[0][3],rank[0][0],rank[0][4])
def measure(im,i,templates):
 if im.size!=(900,300):raise ValueError(("wrong screenshot geometry",im.size))
 rgb=im.load()
 whites={(x,y) for y in FRAME_RANGE for x in X_RANGE if white(rgb[x,y])}
 yellows={(x,y) for y in FRAME_RANGE for x in X_RANGE if yellow(rgb[x,y])}
 all_ys=sorted({y for x,y in whites})
 basey=all_ys[0] if all_ys else None
 if basey is not None:
  # Include every white pixel anywhere in the playing region,
  # NOT just the 9-band. All would be a ghost outside expected mask.
  a,b,missing,extra,delta=best_mask_pairs(whites,basey)
  player_x,player_missing,player_extras,player_score,shot_ok=best_yellow(yellows,basey)
 else:
  a=b=player_x=None
  missing=extra=delta=999
  player_missing=player_extras=player_score=999
  shot_ok=0
 fid=hud_id(im,templates)
 hud_hash=hashlib.sha256(im.crop((558,25,594,46)).tobytes()).hexdigest()
 r={
   "image_index":i,"stella_frame_id":fid,"expected_stella_frame_id":10+i,
   "ntsc_262":hud_hash in HUD_SCAN262,
   "first_mask_P1_x_gui_crop":a,
   "second_mask_P1_x_gui_crop":b,
   "nine_row_top_y_gui_crop":basey,
   "P1_9x2mask_missing_white_pixels":missing,
   "P1_9x2mask_extra_white_pixels":extra,
   "P1_9x2mask_total_error_pixels":delta,
   "original_player_x_gui_crop":player_x,
   "original_player_missing_yellow_pixels":player_missing,
   "other_yellow_pixels":player_extras,
   "one_two_pixel_M0_at_middle_row":bool(shot_ok),
   "display_scan_9_rows":(all_ys==list(range(basey,basey+9)) if basey is not None else False)
 }
 r["strict_mask_and_shot_pass"]=(r["stella_frame_id"]==r["expected_stella_frame_id"] and
     r["ntsc_262"] and missing==0 and extra==0 and
     player_missing==0 and shot_ok and r["display_scan_9_rows"])
 return r
def main():
 photos=sorted((OUT/"raw").glob("frame_*.png"))
 if len(photos)!=600:raise ValueError(f"Must have 600 raw Stella PNGs, got {len(photos)}")
 lookup={}
 for i in range(10):
  with Image.open(photos[i]) as f:
   lookup[(i+11)%10]=glyph(f.convert("RGB"),579)
 if len(set(lookup.values()))!=10:
  raise ValueError("Cannot unambiguously decode true Stella debugger frame IDs")
 records=[]
 for i,p in enumerate(photos,1):
  with Image.open(p) as f:records.append(measure(f.convert("RGB"),i,lookup))
  if i%100==0:print(f"PIXEL_AUDIT {i}/600",flush=True)
 # Four externally visible independent X modes; cannot claim free-X
 # until all 4 distinct paired positions and C-D/C-E deltas are proved.
 modes={}
 for offset in range(4):
  per={key:set() for key in ("C","D","E","F")}
  for r in records:
   if r["stella_frame_id"] is None:continue
   mode=("C","D","E","F")[(r["stella_frame_id"]+offset)&3]
   per[mode].add((r["first_mask_P1_x_gui_crop"],r["second_mask_P1_x_gui_crop"]))
  modes[offset]={k:sorted(v,key=str) for k,v in per.items()}
 correct_phase=[]
 for offset,points in modes.items():
  if any(len(points[k])!=1 for k in points):continue
  (c1,c2)=points["C"][0];(d1,d2)=points["D"][0]
  (e1,e2)=points["E"][0];(f1,f2)=points["F"][0]
  if None in (c1,c2,d1,d2,e1,e2,f1,f2):continue
  independent=(4<=d1-c1<=16 and abs(d2-c2)<=2 and abs(e1-c1)<=2 and
       4<=e2-c2<=16 and abs(f1-d1)<=2 and abs(f2-e2)<=2)
  if independent:correct_phase.append(offset)
 hits=sum(bool(r["strict_mask_and_shot_pass"]) for r in records)
 summary={
  "evidence":"600_CONSECUTIVE_AUTHENTIC_STELLA_6_7_1_DEBUGGER_IMAGES",
  "mask_order":ORDER,
  "total_images":len(records),
  "correct_hud_stella_frame_id":sum(r["stella_frame_id"]==r["expected_stella_frame_id"] for r in records),
  "correct_ntsc_262":sum(r["ntsc_262"] for r in records),
  "all_original_9row_male_female_P1_mask_pixel_exact_and_yellow_P0_M0":hits,
  "white_original_mask_missing_pixels":sum(r["P1_9x2mask_missing_white_pixels"] for r in records),
  "white_ghost_pixels":sum(r["P1_9x2mask_extra_white_pixels"] for r in records),
  "yellow_original_player_missing_pixels":sum(r["original_player_missing_yellow_pixels"] for r in records),
  "one_yellow_M0_midrow_frames":sum(r["one_two_pixel_M0_at_middle_row"] for r in records),
  "model_modes_gui_crop_X":modes,
  "phase_offsets_proving_separate_two_X_changes":correct_phase,
  "source_approved_original_masks_unchanged":True,
  "format":"16 KiB standard F6 NTSC",
  "actual_ROM_SHA256":hashlib.sha256((ROOT/"r1ag_F6.bin").read_bytes()).hexdigest(),
  "first_ten_failed_frames":[r for r in records if not r["strict_mask_and_shot_pass"]][:10],
  "limits":"Isolated 2 P1 original mask research, not six NPC. Independent VERIFICATION not performed."
 }
 summary["status"]="LOCAL_PASS_R1AG_DUAL_ORIGINAL_9ROW_MASKS_TWO_X_ZERO_GHOST_600" if hits==600 and correct_phase else "FAIL_OR_INCONCLUSIVE"
 OUT.mkdir(exist_ok=True)
 (OUT/"summary.json").write_text(json.dumps(summary,indent=2,ensure_ascii=False)+"\n")
 with (OUT/"frames_600.csv").open("w",newline="") as f:
  w=csv.DictWriter(f,fieldnames=list(records[0]))
  w.writeheader();w.writerows(records)
 print(json.dumps(summary,indent=2,ensure_ascii=False))
 sys.exit(0 if summary["status"].startswith("LOCAL_PASS") else 1)
if __name__=="__main__":main()
