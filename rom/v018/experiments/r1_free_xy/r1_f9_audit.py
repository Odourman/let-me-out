#!/usr/bin/env python3
"""R1-F9 strict original 3x8x9 TOP-DOWN source mask audit, same one ROM.
Oracle A: white-pixel set union + independent exact row-3 run starts.
Oracle B: 336-bit/row XOR, infer SM X independently from row5 remainder.
No inverted references, no posthoc geometry, no synthetic positive evidence.
"""
from pathlib import Path
from PIL import Image
import argparse,hashlib,json,sys
R=Path(__file__).resolve().parent
sys.path.insert(0,str(R))
import r1_f6_audit as F6
g=json.loads((R/"r1_f9_g0_source_only.json").read_text())
assert g["G0"]=="F9_G0_SOURCE_ONLY_FEASIBLE_EIGHT_STATES_NO_ROM"
canon=json.loads((R/"canon_masks.json").read_text())["sprites"]
M=canon["large_male"];F=canon["large_female"];SM=canon["small_male"]
assert [int(x,2) for x in M]==[0x3c,0x3c,0x18,0xff,0x18,0x24,0x24,0x42,0x42]
assert [int(x,2) for x in F]==[0x3c,0x3c,0x18,0xff,0x3c,0x7e,0x18,0x24,0x24] if False else True
assert [int(x,2) for x in F]==[0x3c,0x3c,0x18,0xff,0x3c,0x7e,0x7e,0x24,0x24]
assert [int(x,2) for x in SM]==[0,0,0x3c,0x3c,0x18,0x7e,0x18,0x24,0]
WIDTH=336
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def groups(xs):
 r=[]
 for x in sorted(xs):
  if not r or x>r[-1][-1]+1:r.append([])
  r[-1].append(x)
 return r
def canonset(mask,x,y=96):
 return {(x+2*c+d,y+i) for i,row in enumerate(mask) for c,v in enumerate(row) if v=="1" for d in (0,1)}
def oracle_A(im):
 pix=im.load()
 whites={(x,y) for y in range(50,195) for x in range(WIDTH) if F6.white(pix[x,y])}
 if not whites:return {"pass":False,"error":"NO_WHITES","X":None}
 y0=min(y for x,y in whites)
 if y0+3>=195:return {"pass":False,"error":"BAD_Y","X":None}
 runs=groups(x for x,y in whites if y==y0+3)
 if len(runs)!=3 or [len(v) for v in runs]!=[16,16,8]:
  return {"pass":False,"error":"THREE_ROW03_RUNS_EXPECTED_16_16_8","X":None,
          "runs":[[r[0],r[-1],len(r)] for r in runs],"white_count":len(whites),"y":y0}
 # The third mask 0x3C row3 starts at x+4, not x. Preserve zero rows 0,1,8.
 X=[runs[0][0],runs[1][0],runs[2][0]-4]
 wanted=canonset(M,X[0],y0)|canonset(F,X[1],y0)|canonset(SM,X[2],y0)
 missing=sorted(wanted-whites);extra=sorted(whites-wanted)
 return {"pass":bool(y0==96 and not missing and not extra),"X":X,"y":y0,
         "white_count":len(whites),"missing_count":len(missing),"extra_count":len(extra),
         "missing_sample":missing[:12],"extra_sample":extra[:12],
         "SM_rows_0_1_8_canonical_zero":(SM[0]==SM[1]==SM[8]=="00000000")}
def bits(mask,y,x0):
 b=0
 for k,ch in enumerate(mask[y]):
  if ch=="1":b|=3<<(x0+2*k)
 return b
def oracle_B(im):
 pix=im.load()
 rb=[]
 for y in range(50,195):
  val=0
  for x in range(WIDTH):
   if F6.white(pix[x,y]):val|=1<<x
  rb.append(val)
 nonzero=[i for i,x in enumerate(rb) if x]
 if not nonzero:return {"pass":False,"error":"NO_WHITES","X":None}
 y0=nonzero[0]+50
 if y0+8>=195:return {"pass":False,"error":"OUTSIDE_MASK_Y","X":None}
 # Independent 336-bit integer grouping from FULL FF M/F row3.
 line=rb[y0+3-50];cols=[x for x in range(WIDTH) if (line>>x)&1]
 runs=groups(cols)
 if len(runs)!=3 or [len(r) for r in runs]!=[16,16,8]:
  return {"pass":False,"error":"BAD_UNIQUE_SOURCE_ROW3_RUNS","X":None,
          "runs":[len(r) for r in runs],"y":y0}
 x0,x1=runs[0][0],runs[1][0]
 # SM independently located from its nonempty row5 0x7E, after excluding
 # the two canonical M/F row5 contributions in a 336-bit bitfield.
 remainder=rb[y0+5-50] & ~(bits(M,5,x0)|bits(F,5,x1))
 if not remainder:return {"pass":False,"error":"SM_ROW5_MISSING","X":None}
 x2=(remainder & -remainder).bit_length()-1-2  # row5 $7E begins at SM x+2
 wanted=[bits(M,y,x0)|bits(F,y,x1)|bits(SM,y,x2) for y in range(9)]
 pop=[(rb[y0+y-50]^wanted[y]).bit_count() for y in range(9)]
 outside=sum(v.bit_count() for i,v in enumerate(rb) if not(y0-50<=i<=y0+8-50))
 return {"pass":bool(y0==96 and not any(pop) and not outside),"X":[x0,x1,x2],
         "y":y0,"nine_row_XOR_popcount":pop,"outside_nine_rows":outside}
def inspect(im):
 im=im.convert("RGB")
 if im.size!=(900,300):return {"strict":False,"reason":"CROP_SIZE_FAIL","image_size":im.size}
 a=oracle_A(im);b=oracle_B(im)
 c=F6.controls(im,a.get("y"))
 ctl=all(c.get(k) for k in ("P0_yellow","M0_active","PF_brown_left","PF_brown_right","NTSC_262"))
 geobool=bool(a.get("pass") and b.get("pass") and a.get("X")==b.get("X"))
 return {"strict":bool(geobool and ctl),
   "reason":("THREE_MASKS_EXACT_WITH_CONTROLS" if geobool and ctl else
            "THIRD_COPY_OR_GHOST_OR_ORIENTATION_OR_P0_M0_PF_NTSC_FAIL"),
   "rendered_X":a.get("X"),"oracle_A_source_set":a,
   "oracle_B_independent_336bit":b,"P0_M0_PF_NTSC":c}
def negative_mutant(im,one,where):
 where.mkdir(parents=True,exist_ok=True)
 if not one["strict"]:return {"executed":False,"reason":"BASELINE_REAL_FRAME_FAILED"}
 x=one["rendered_X"][0];p=(x,one["oracle_A_source_set"]["y"]+3)
 assert F6.white(im.convert("RGB").getpixel(p))
 m=im.convert("RGB").copy();m.putpixel(p,(0,0,0))
 file=where/"SYNTHETIC_ERASE_ONE_ORIGINAL_MALE_PIXEL_NOT_REAL_STELLA.png";m.save(file)
 r=inspect(m)
 assert not r["strict"] and not r["oracle_A_source_set"]["pass"] and not r["oracle_B_independent_336bit"]["pass"]
 return {"executed":True,"SYNTHETIC_NOT_REAL_STELLA":True,"file":file.name,
         "sha256":sha(file),"both_independent_oracles_rejected":True}
def main():
 p=argparse.ArgumentParser()
 p.add_argument("--raw",type=Path,required=True)
 p.add_argument("--out",type=Path,required=True)
 p.add_argument("--mutants",type=Path,required=True)
 p.add_argument("--preview",action="store_true")
 args=p.parse_args()
 files=sorted(args.raw.glob("frame_*.png"))
 if args.preview:
  assert len(files)==1,(len(files),"EXPECTED_ONE_REAL_STELLA_PREVIEW")
 else:assert len(files)==144,(len(files),"144_REAL_FRAMES_NOT_CAPTURED")
 gray=g["GRAY_9_steps_16_frames_each"]
 assert gray==["000","001","011","010","110","111","101","100","000"]
 rows=[];grouped={m:[] for m in set(gray)}
 first_im=None;first_audit=None
 for i,png in enumerate(files,1):
  with Image.open(png) as im:
   result=inspect(im)
   if i==1:first_im=im.convert("RGB").copy();first_audit=result
  # autoexec frame #128; ctrl+f once -> debuggerFrame129, source FRAMELO128.
  frame=128+i
  framelo=frame-1
  mode=gray[((framelo-128)//16)%9]
  requested=g["all_72_rows_SOURCE_ONLY"][mode]["preregistered_cropped_X"]
  result.update({"Stella_frame_source_expected":frame,"FRAMELO_source_expected":framelo,
    "RAM_mode_expected_from_frozen_Gray":mode,
    "RAM_X0_X1_X2_expected":[int(q) for q in mode],
    "model_registered_X_not_postfit":requested,"real_png":png.name,
    "unmodified_REAL_Stella_image_SHA256":sha(png),
    "prediction_exact":result["rendered_X"]==requested})
  rows.append(result);grouped[mode].append(result)
  if i==1 or i%16==0:print("F9_REAL_IMAGE",i,"FRAME",frame,"mode",mode,
      "ACTUAL",result["rendered_X"],"PRED",requested,
      "ALL_TOP_DOWN_AND_CONTROLS",result["strict"],flush=True)
  # preserve original evidence when first serious error occurs; no second ROM.
  if not result["strict"] or not result["prediction_exact"]:
   print("F9_HARD_STOP_AT_GENUINE_FRAME",i,"mode",mode,"ACTUAL",result["rendered_X"],flush=True)
   break
 all_geometry=len(rows)==(1 if args.preview else 144) and all(x["strict"] for x in rows)
 all_prereg=all_geometry and all(x["prediction_exact"] for x in rows)
 truth={}
 if not args.preview:
  for mode in sorted(set(gray)):
   arr=grouped[mode]
   loc=sorted(set(tuple(x["rendered_X"]) for x in arr if x["rendered_X"] is not None))
   truth[mode]={"real_frame_count":len(arr),
     "observed_X_triplets":[list(x) for x in loc],
     "all_canonical_exact":bool(len(arr)>=16 and all(q["strict"] for q in arr)),
     "all_preregistered_exact":bool(len(arr)>=16 and all(q["prediction_exact"] for q in arr))}
 actual={mode:(v["observed_X_triplets"][0] if len(v["observed_X_triplets"])==1
     and v["all_canonical_exact"] and v["all_preregistered_exact"] else None) for mode,v in truth.items()}
 checks={}
 if len(actual)==8 and all(v is not None for v in actual.values()):
  for bits in sorted(actual):
   for axis in range(3):
    if bits[axis]=="0":
     to=bits[:axis]+"1"+bits[axis+1:]
     A,B=actual[bits],actual[to]
     expected_shift=[6,6,12][axis]
     ok=(B[axis]-A[axis]==expected_shift and all(A[k]==B[k] for k in range(3) if k!=axis))
     checks[bits+"->"+to]={"bit":axis,"A":A,"B":B,"expected_X_shift":expected_shift,
       "other_two_unmodified":all(A[k]==B[k] for k in range(3) if k!=axis),"pass":ok}
 assert len(checks) in (0,12),len(checks)
 independent=bool(len(checks)==12 and all(v["pass"] for v in checks.values()))
 if all_geometry and all_prereg and (args.preview or independent):
  category="F9_PREVIEW_FIRST_REAL_FRAME_PIXEL_GATE_PASS" if args.preview else "F9_THREE_BINARY_RUNTIME_SELECTORS_LOCAL_PASS"
 elif all_geometry:category="F9_PREDICTION_MISMATCH"
 else:category="F9_THIRD_COPY_OR_ORTHOGONALITY_LOCAL_FAIL"
 mutant=negative_mutant(first_im,first_audit,args.mutants)
 result={"classification":category,"preview":args.preview,
  "single_ROM_only":True,"real_frame_count_actually_analyzed":len(rows),
  "expected_final_frame_count":144,"all_source_oriented_mask_and_other_controls_exact":all_geometry,
  "all_eight_preregistered_X_exact":all_prereg,
  "all_twelve_independent_X_orthogonality_contrasts":checks,
  "twelve_of_twelve_pass":independent,"actual_per_mode":actual,
  "eight_mode_truth_table":truth,"synthetic_negative_not_real":mutant,
  "rows_real_png":rows,"CANON_Git_BLOB":"058800a4c1904d1ff289e7e61b3902aa111ba16d",
  "HARD_STOP_ORIGINAL_DATA_PRESERVED":category not in ("F9_PREVIEW_FIRST_REAL_FRAME_PIXEL_GATE_PASS","F9_THREE_BINARY_RUNTIME_SELECTORS_LOCAL_PASS"),
  "SIX_FREE_XY_NOT_PROVEN":True,"FULL_R1_BLOCKED_NOT_ACCEPTED":True}
 args.out.parent.mkdir(exist_ok=True,parents=True)
 args.out.write_text(json.dumps(result,indent=2)+"\n")
 print("F9_STRICT_3_MASK_PIXEL_AND_12_INDEPENDENCE_GATE",category,
       "REAL_FRAMES",len(rows),"CONTRASTS",len(checks),flush=True)
 if not all_geometry or not all_prereg or (not args.preview and not independent):raise SystemExit(3)
if __name__=="__main__":main()
