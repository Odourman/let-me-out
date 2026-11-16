#!/usr/bin/env python3
"""R1ba strict diagnostic: classify every white sprite cluster against full
four canonical 8x9 original source masks. Never assume fifth/sixth exists.
The only source change is NUSIZ1; report missing or extra white pixels.
"""
from PIL import Image
from pathlib import Path
from collections import Counter,defaultdict
import re,json,hashlib,csv,sys
R=Path(__file__).resolve().parent
O=R/"evidence_600"
SRC=(R/"r1ba.asm").read_text()
META=json.loads((R/"manifest.json").read_text())
HUD_SCAN262={
 "04f59d7fbc17d360e0cea738d4e512ab7208118b9b4d4b4743f3a702d96f1fdb",
 "a169787b7bdcf465b5a1b7505dca83c31f60fa2c16337d39fea3e957ea13ace2"}
def mask(name):
 m=re.search(r"^"+name+r":\s*\n\s+BYTE ([^\n]+)",SRC,re.M)
 if not m:raise ValueError(name)
 return [int(i.strip().removeprefix("$"),16) for i in m.group(1).split(",")][::-1]
def pts(arr):
 return {(bit*2+dx,y) for y,byte in enumerate(arr)
         for bit in range(8) if byte&(0x80>>bit) for dx in (0,1)}
MS={
 "M":pts(mask("MaleRows")),
 "F":pts(mask("FemaleRows")),
 "SM":pts(mask("SmallMaleRows")),
 "SF":pts(mask("SmallFemaleRows"))
}
PLAYER=pts(mask("PlayerRows"))
assert mask("MaleRows")==[0x42,0x42,0x24,0x24,0x18,0xff,0x18,0x3c,0x3c]
assert mask("FemaleRows")==[0x24,0x24,0x7e,0x7e,0x3c,0xff,0x18,0x3c,0x3c]
assert mask("SmallMaleRows")==[0,0,0x3c,0x3c,0x18,0x7e,0x18,0x24,0]
assert mask("SmallFemaleRows")==[0,0,0x3c,0x3c,0x18,0x7e,0x3c,0x24,0]
assert mask("PlayerRows")==[0x42,0x24,0x18,0x3c,0x1e,0x7e,0x18,0x7e,0x3c]
def glyph(im,x):
 return tuple((lambda c:c[0]>210 and c[1]>150 and c[2]<180)
  (im.getpixel((a,b))) for b in range(9,19) for a in range(x,x+7))
def hud_id(im,lookup):
 vals=[]
 for x in (561,570,579):
  g=glyph(im,x)
  if not any(g):continue
  hits=[k for k,v in lookup.items() if v==g]
  if len(hits)!=1:return None
  vals.append(str(hits[0]))
 return int("".join(vals)) if vals else None
def shifted(s,x,y):
 return {(a+x,b+y) for a,b in s}
def classify(whites,top_y,sm_dy,sf_dy):
 if not whites:return [],len(whites),0
 xs=sorted({x for x,y in whites})
 groups=[[xs[0]]]
 for x in xs[1:]:
  if x-groups[-1][-1]>16:groups.append([])
  groups[-1].append(x)
 detected=[]
 unexplained=set()
 for group in groups:
  left=min(group);right=max(group)
  blob={(x,y) for x,y in whites if left<=x<=right}
  candidates=[]
  for name,pattern in MS.items():
   for x in range(max(0,left-16),left+1):
    dy=(sm_dy if name=="SM" else sf_dy if name=="SF" else 0)
    expect=shifted(pattern,x,top_y+dy)
    missing=len(expect-blob);extra=len(blob-expect)
    candidates.append((missing+extra,missing,extra,name,x))
  candidates.sort()
  best=candidates[0]
  detected.append({"type":best[3],"x":best[4],
      "missing":best[1],"extra":best[2],"cost":best[0],
      "cluster_min_x":left,"cluster_max_x":right})
  if best[0]:unexplained|=blob
 return detected,sum(x["missing"] for x in detected),sum(x["extra"] for x in detected)
def yellow_check(actual,top_y):
 if not actual:return 0,None,999,0
 low=max(0,min(x for x,y in actual)-16)
 high=min(320,max(x for x,y in actual)+1)
 opts=[]
 for x in range(low,high+1):
  p=shifted(PLAYER,x,top_y)
  miss=len(p-actual);extra=actual-p
  shot=sorted(extra,key=lambda z:(z[1],z[0]))
  shot_ok=(len(shot)==2 and shot[0][1]==shot[1][1]==top_y+4
    and shot[1][0]==shot[0][0]+1)
  opts.append((miss+(0 if shot_ok else len(extra)+10),x,miss,shot_ok))
 opts.sort()
 best=opts[0]
 return int(best[2]==0 and best[3]),best[1],best[2],int(best[3])
def is_brown(p):
 r,g,b=p[:3]
 # Atari NTSC COLUPF $26 is a dark orange/brown hue. Exclude white
 # silhouettes and yellow P0/M0 explicitly by color ratios.
 return r>=65 and g>=22 and r>=g*1.25 and g>=b*1.15 and b<110 and not (r>185 and g>140)
def wall_rows(im,ys):
 p=im.load()
 out=[]
 for y in ys:
  left=sum(is_brown(p[x,y]) for x in range(0,72))
  right=sum(is_brown(p[x,y]) for x in range(270,336))
  middle=sum(is_brown(p[x,y]) for x in range(100,235))
  out.append((left,right,middle))
 return out

def audit(im,i,lookup):
 if im.size!=(900,300):raise ValueError((im.size,i))
 p=im.load()
 whites={(x,y) for y in range(50,195) for x in range(336)
  if min(p[x,y])>180 and max(p[x,y])-min(p[x,y])<40}
 yellows={(x,y) for y in range(50,195) for x in range(336)
  if p[x,y][0]>120 and p[x,y][1]>100 and p[x,y][2]<100 and not is_brown(p[x,y])}
 base=min((y for x,y in whites),default=None)
 profile_idx=None
 if base is not None:
  tests=[]
  for idx,(sm_dy,sf_dy) in enumerate(META["y_profiles"]):
   detected,miss,extr=classify(whites,base,sm_dy,sf_dy)
   tests.append((miss+extr,idx,detected,miss,extr))
  tests.sort(key=lambda a:(a[0],a[1]))
  _,profile_idx,groups,missing,extra=tests[0]
 else:
  groups,missing,extra=[],999,999
 yellow_ok,p0_x,p0_missing,shot_ok=yellow_check(yellows,base) if base is not None else (0,None,999,0)
 ys=sorted({y for x,y in whites}) if whites else []
 wall_measurements=wall_rows(im,ys)
 left_rows=sum(l>=6 for l,r,m in wall_measurements)
 right_rows=sum(r>=6 for l,r,m in wall_measurements)
 center_rows=sum(m>0 for l,r,m in wall_measurements)
 walls_ok=(len(ys)==9 and left_rows==9 and right_rows==9 and center_rows==0)
 fid=hud_id(im,lookup)
 scan=hashlib.sha256(im.crop((558,25,594,46)).tobytes()).hexdigest() in HUD_SCAN262
 counts=Counter(g["type"] for g in groups if g["cost"]==0)
 exact_all=all(g["cost"]==0 for g in groups) and bool(groups)
 retained=all(counts[k]>=1 for k in ("M","F","SM","SF"))
 six=(counts==Counter({"M":2,"F":2,"SM":1,"SF":1}))
 strict_common=(fid==i+10 and scan and yellow_ok==1
  and len(yellows)>0 and base is not None
  and sorted({y for x,y in whites})==list(range(base,base+9)))
 return {
 "frame":i,"stella_frame_id":fid,"ntsc_262":scan,
 "left_brown_wall_rows":left_rows,"right_brown_wall_rows":right_rows,
 "center_brown_rows":center_rows,"mirrored_brown_walls_exact":walls_ok,
 "selected_Y_profile":profile_idx,
 "yellow_player_and_one_shot_exact":bool(yellow_ok),
 "player_x_gui":p0_x,
 "white_group_count":len(groups),
 "full_mask_count":sum(g["cost"]==0 for g in groups),
 "white_missing_pixels":missing,"white_extra_pixels":extra,
 "mask_types":";".join(g["type"] for g in groups),
 "mask_x_gui":";".join(str(g["x"]) for g in groups),
 "mask_costs":";".join(str(g["cost"]) for g in groups),
 "original_four_types_all_present":retained,
 "strict_four_or_more":bool(strict_common and exact_all and retained),
 "strict_exact_six_2M2F1SM1SF":bool(strict_common and exact_all and six),
 "original_mask_integrity":bool(exact_all),
 "yellow_player_missing":p0_missing,
 "shot_ok":bool(shot_ok),
 }
def main():
 photos=sorted((O/"raw").glob("frame_*.png"))
 assert len(photos)==600,len(photos)
 lookup={}
 for i in range(10):
  with Image.open(photos[i]) as f:
   lookup[(i+11)%10]=glyph(f.convert("RGB"),579)
 assert len(set(lookup.values()))==10
 records=[]
 for i,path in enumerate(photos,1):
  with Image.open(path) as f:records.append(audit(f.convert("RGB"),i,lookup))
  if i%100==0:print(f"PIXEL_AUDIT {i}/600",flush=True)
 hashes=defaultdict(int)
 for r in records:
  hashes[(r["white_group_count"],r["mask_types"],r["mask_costs"])]+=1
 strict4=sum(r["strict_four_or_more"] for r in records)
 strict6=sum(r["strict_exact_six_2M2F1SM1SF"] for r in records)
 summary={
  "evidence":"600_CONSECUTIVE_AUTHENTIC_STELLA_6_7_1_DEBUGGER_IMAGES",
  "batch_NUSIZ1":META["NUSIZ1_value"],
  "ROM_SHA256":META["ROM_SHA256"],
  "frames":len(records),
  "correct_frame_id":sum(r["stella_frame_id"]==r["frame"]+10 for r in records),
  "correct_ntsc_262":sum(r["ntsc_262"] for r in records),
  "one_full_yellow_P0_and_one_yellow_M0":sum(r["yellow_player_and_one_shot_exact"] for r in records),
  "strict_all_four_original_types_preserved":strict4,
  "strict_exact_six_2M_2F_1SM_1SF":strict6,
  "both_brown_side_wall_frames":sum(r["mirrored_brown_walls_exact"] for r in records),
  "total_missing_white_pixels":sum(r["white_missing_pixels"] for r in records),
  "total_extra_white_pixels":sum(r["white_extra_pixels"] for r in records),
  "distributions":[{"groups":g[0],"types":g[1],"costs":g[2],"frames":v} for g,v in sorted(hashes.items(),key=lambda kv:-kv[1])],
  "first_failed_four":[r for r in records if not r["strict_four_or_more"]][:5],
  "first_failed_six":[r for r in records if not r["strict_exact_six_2M2F1SM1SF"]][:5],
  "limits":"Research only. Six if strict is just static constrained X, NOT full 6 independently movable NPC."
 }
 positions={}
 for record in records:
  if record["strict_exact_six_2M2F1SM1SF"]:
   k=record["mask_x_gui"]
   positions[k]=positions.get(k,0)+1
 summary["runtime_six_mask_position_signatures"]=positions
 summary["one_or_more_strict_six_layouts"]=(len(positions)>=1)
 summary["exactly_three_runtime_X_layouts_observed"]=(len(positions)==3 and all(v>=100 for v in positions.values()))
 profile_counts={str(idx):sum(r["selected_Y_profile"]==idx and r["strict_exact_six_2M2F1SM1SF"] for r in records) for idx in range(3)}
 summary["runtime_Y_profile_frame_counts"]=profile_counts
 summary["exactly_three_Y_profiles_observed"]=(len(profile_counts)==3 and all(v>=100 for v in profile_counts.values()))
 summary["status"]=(
  "LOCAL_RESEARCH_R1BA_X_Y_PF_SIX_EXACT_ORIGINAL_MASKS_600_PASS" if strict6==600 and summary["exactly_three_runtime_X_layouts_observed"] and summary["exactly_three_Y_profiles_observed"] and summary["both_brown_side_wall_frames"]==600 else
  "LOCAL_RESEARCH_FOUR_OR_MORE_PRESERVED_600" if strict4==600 else
  "FAIL_FOUR_ORIGINALS_OR_TIMING_OR_SHOT")
 O.mkdir(exist_ok=True)
 (O/"summary.json").write_text(json.dumps(summary,indent=2,ensure_ascii=False)+"\n")
 with (O/"frames_600.csv").open("w",newline="") as f:
  writer=csv.DictWriter(f,fieldnames=list(records[0]))
  writer.writeheader();writer.writerows(records)
 print(json.dumps(summary,indent=2,ensure_ascii=False))
 # The CI is specifically a six-NPC feasibility proof; fail closed on
 # any mode not actually producing exactly six source-perfect instances.
 sys.exit(0 if strict6==600 and summary["exactly_three_runtime_X_layouts_observed"] and summary["exactly_three_Y_profiles_observed"] and summary["both_brown_side_wall_frames"]==600 else 1)
if __name__=="__main__":main()
