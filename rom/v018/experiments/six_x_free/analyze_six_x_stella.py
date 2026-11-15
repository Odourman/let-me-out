#!/usr/bin/env python3
"""Pixel-only analysis of unmodified Stella 6.7.1 debugger X11 frame captures.
No synthetic visibility claims: a sprite must actually appear in the image.
Requires Pillow. A match to a verified 262-HUD pixel template is the only
accepted scanline result; other strings remain UNREADABLE rather than guessed.
"""
from __future__ import annotations
import argparse, csv, hashlib, json, re, statistics
from collections import Counter
from pathlib import Path
from PIL import Image

LINE_262_HASH = "04f59d7fbc17d360e0cea738d4e512ab7208118b9b4d4b4743f3a702d96f1fdb"
MASKS = {
 'large_male':["00111100","00111100","00011000","11111111","00011000","00100100","00100100","01000010","01000010"],
 'large_female':["00111100","00111100","00011000","11111111","00111100","01111110","01111110","00100100","00100100"],
 'small_male':["00000000","00000000","00111100","00111100","00011000","01111110","00011000","00100100","00000000"],
 'small_female':["00000000","00000000","00111100","00111100","00011000","01111110","00111100","00100100","00000000"],
}
TYPES=['large_male','large_male','large_female','large_female','small_male','small_female']


def paths_from_asm(p:Path):
 s=p.read_text();paths=[]
 for i in range(6):
  m=re.search(rf'^Path{i}:\s*\n BYTE ([^\n]+)\n BYTE ([^\n]+)',s,re.M)
  if not m:raise ValueError(f'Missing Path{i}')
  vals=[int(x.strip().replace('$','0x'),16) for text in m.groups() for x in text.split(',')]
  assert len(vals)==32,(i,vals)
  paths.append(vals)
 return paths

def yellow(p):return p[0]>210 and p[1]>150 and p[2]<180

def white(p):return min(p)>215 and max(p)-min(p)<9

def glyph(im,x):
 return tuple(1 if yellow(im.getpixel((xx,yy))) else 0 for yy in range(9,19) for xx in range(x,x+7))

def build_digit_patterns(files):
 if len(files)<10: raise RuntimeError('Need 10 first sequential screenshots to calibrate 0-9')
 templates={}
 for j in range(1,11):
  im=Image.open(files[j-1]).convert('RGB');templates[(10+j)%10]=glyph(im,579)
 assert len(set(templates.values()))==10
 return templates

def frame_number(im,templates):
 s=''
 for x in (561,570,579):
  g=glyph(im,x)
  if not any(g):continue
  matches=[d for d,t in templates.items() if g==t]
  s+=str(matches[0]) if len(matches)==1 else '?'
 return int(s) if s and '?' not in s else None

def x_components(im):
 # Atari visible image is x=0..319, y=96..104 in these X11 debugger captures.
 xs=set()
 for y in range(96,105):
  for x in range(0,320):
   if white(im.getpixel((x,y))):xs.add(x)
 out=[]
 for x in sorted(xs):
  if not out or x>out[-1][-1]+1:out.append([x])
  else:out[-1].append(x)
 return [(a[0],a[-1]) for a in out]

def bitmap_score(im,mask,x0,y0=96):
 points=0
 if x0<0 or x0+16>=320:return 0
 for y in range(9):
  for x in range(8):
   obs=white(im.getpixel((x0+x*2+1,y0+y)))
   exp=mask[y][x]=='1'
   points+=obs==exp
 return points

def individual_visibility(im,req,scene):
 # Hardware-actual pixel evidence: search each requested X around its
 # own approx screen offset; do not use code intention as visibility.
 components=x_components(im)
 # Join pieces separated by small bitmap holes. One horizontal NPC body
 # has an unbroken head/torso or full-width arm row across its rasterband.
 merged=[]
 for a,b in components:
  if not merged or a>merged[-1][1]+2:merged.append([a,b])
  else:merged[-1][1]=b
 components=[tuple(v) for v in merged]
 available=components.copy()
 actual=[None]*6;fidelity=[None]*6;visible=[0]*6
 for i in range(6):
  # A rendered sprite can be ~0..6 color clocks to right of a requested
  # TIA coordinate. PF quantizes to 4 clocks; allow <=9-clock deviation.
  matches=[(abs((lo/2)-req[i]),j,lo,hi) for j,(lo,hi) in enumerate(available) if abs((lo/2)-req[i])<=9]
  if not matches:continue
  d,j,lo,hi=min(matches)
  visible[i]=1;actual[i]=round(lo/2,1)
  # Find best horizontal alignment for this exact approved 8x9 mask.
  mask=MASKS[TYPES[i]]
  fidelity[i]=max(bitmap_score(im,mask,x0) for x0 in range(max(0,lo-8),min(319,lo+5),2))
  available.pop(j)
 return visible,actual,fidelity,components

def max_invisible(seq):
 now=longest=0
 for item in seq:
  if not item:now+=1;longest=max(longest,now)
  else:now=0
 return longest

def analyze(rawdir,asm,outdir,variant,expected_count=600):
 rawdir=Path(rawdir);outdir=Path(outdir);outdir.mkdir(parents=True,exist_ok=True)
 files=sorted(rawdir.glob('frame_*.png'))
 if len(files)!=expected_count:raise ValueError(f'Expected {expected_count} raw frames, found {len(files)}')
 patterns=build_digit_patterns(files);paths=paths_from_asm(Path(asm))
 results=[];all_seen=[[] for _ in range(6)];scores=[[] for _ in range(6)]
 scan_counts=Counter();frame_sequence_errors=[]
 for index,p in enumerate(files,1):
  im=Image.open(p).convert('RGB')
  if im.size!=(900,300):raise ValueError(f'Capture size {im.size} is not 900x300')
  frame=frame_number(im,patterns)
  if frame!=10+index:frame_sequence_errors.append({'image_index':index,'observed_frame':frame,'expected_frame':10+index})
  scanhash=hashlib.sha256(im.crop((558,25,594,46)).tobytes()).hexdigest()
  scan='262' if scanhash==LINE_262_HASH else 'OTHER_OR_UNREADABLE'
  scan_counts[scan]+=1
  # FrameLO follows Stella counter - 1 in this diagnostic (readback at F22).
  requested=[paths[i][((frame if frame is not None else 10+index)-1)%32] for i in range(6)]
  seen,actual,fidelity,groups=individual_visibility(im,requested,variant)
  yellowpos=[(x,y) for y in range(96,105) for x in range(220,320) if yellow(im.getpixel((x,y)))]
  player=any(240<=x<=290 for x,y in yellowpos)
  shot=any(x>=305 for x,y in yellowpos)
  for i in range(6):
   all_seen[i].append(seen[i])
   if fidelity[i] is not None:scores[i].append(fidelity[i])
  results.append({'image_index':index,'observed_frame':frame,'scene_id':f'SEX_X_FREE_{variant.upper()}',
    'scanlines_stella_HUD':scan,'npc_x0':requested[0],'npc_x1':requested[1],'npc_x2':requested[2],
    'npc_x3':requested[3],'npc_x4':requested[4],'npc_x5':requested[5],
    'actual_x0':actual[0],'actual_x1':actual[1],'actual_x2':actual[2],'actual_x3':actual[3],
    'actual_x4':actual[4],'actual_x5':actual[5],
    'visible_mask_6bit':''.join(str(x) for x in seen[::-1]),
    'mask_match0_of72':fidelity[0],'mask_match1_of72':fidelity[1],
    'mask_match2_of72':fidelity[2],'mask_match3_of72':fidelity[3],
    'mask_match4_of72':fidelity[4],'mask_match5_of72':fidelity[5],
    'observed_white_components':len(groups),'player_yellow_observed':int(player),
    'shot_yellow_observed':int(shot),'source_capture':p.name})
 with (outdir/f'frames_600_{variant}.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(results[0]));w.writeheader();w.writerows(results)
 summary={
  'variant':variant,'total_captured_frames':len(files),'observed_frame_ids_sequential':len(frame_sequence_errors)==0,
  'frame_id_errors':frame_sequence_errors[:20],
  'scanline_hud_262_count':scan_counts['262'],'scanline_hud_other_count':scan_counts['OTHER_OR_UNREADABLE'],
  'observed_yellow_player_frames':sum(x['player_yellow_observed'] for x in results),
  'observed_yellow_shot_frames':sum(x['shot_yellow_observed'] for x in results),
  'npc_visibility_stats':[{'npc':i,'type':TYPES[i],'visible_frames':sum(all_seen[i]),
    'visible_fraction':round(sum(all_seen[i])/len(files),5),
    'longest_consecutive_invisible_frames':max_invisible(all_seen[i]),
    'max_mask_match_bits_of_72':max(scores[i]) if scores[i] else None,
    'mean_mask_match_bits_of_72':round(statistics.mean(scores[i]),2) if scores[i] else None}
    for i in range(6)],
  'acceptance_status':'NOT_APPROVED',
  'scanline_method':'Pixel-exact HUD comparison to Stella 6.7.1 262-reference screenshot (hash), not CPU-model output.',
  'visibility_method':'Per-frame P1/PF white pixel groups in actual Stella debugger image. A priori planned X is separate from pixels.',
  'warning':'Mask fidelity and color comparators are automated development diagnostics; separate Verification and human readability review remain required.'
 }
 (outdir/f'summary_{variant}.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False)+'\n')
 return summary

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--raw',required=True);p.add_argument('--asm',required=True);p.add_argument('--out',required=True);p.add_argument('--variant',choices=['a','b'],required=True);p.add_argument('--count',type=int,default=600)
 args=p.parse_args();print(json.dumps(analyze(args.raw,args.asm,args.out,args.variant,args.count),indent=2,ensure_ascii=False))
