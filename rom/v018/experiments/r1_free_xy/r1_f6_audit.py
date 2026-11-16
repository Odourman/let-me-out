#!/usr/bin/env python3
"""F6 genuine-Stella-only two top-down original-mask pixel audit.
Two genuinely different matchers: XY set union + per-scanline bitfield.
No flipped canonical rows, no R1ba source/auditor, no synthetic positive.
"""
import argparse,json,hashlib
from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parent
ROOT=R.parents[3]
J=json.loads((R/"canon_masks.json").read_text())
M=J["sprites"]["large_male"];F=J["sprites"]["large_female"]
assert [int(b,2) for b in M]==[0x3c,0x3c,0x18,0xff,0x18,0x24,0x24,0x42,0x42]
assert [int(b,2) for b in F]==[0x3c,0x3c,0x18,0xff,0x3c,0x7e,0x7e,0x24,0x24]
P0=["00111100","01111110","00011000","01111110","00011110","00111100","00011000","00100100","01000010"]
WIDTH=336
HUD262={"04f59d7fbc17d360e0cea738d4e512ab7208118b9b4d4b4743f3a702d96f1fdb",
        "a169787b7bdcf465b5a1b7505dca83c31f60fa2c16337d39fea3e957ea13ace2"}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def white(p):return min(p[:3])>180 and max(p[:3])-min(p[:3])<40
def brown(p):
    r,g,b=p[:3]
    return r>=65 and g>=22 and r>=g*1.25 and g>=b*1.15 and b<110 and not (r>185 and g>140)
def yellow(p):
    r,g,b=p[:3]
    return r>120 and g>100 and b<100 and not brown(p)
def canonset(bits,x,y):
    return {(x+2*j+d,y+i) for i,row in enumerate(bits) for j,bit in enumerate(row) if bit=="1" for d in (0,1)}
def matcher_A(im):
    pix=im.load()
    whites={(x,y) for y in range(50,195) for x in range(WIDTH) if white(pix[x,y])}
    if not whites:return {"ok":False,"reason":"NO_WHITE_PIXELS","starts":None,"union_cost":999}
    y0=min(y for x,y in whites)
    # Source-only expectation y0=96 remains a separate strict guard.
    columns=sorted({x for x,y in whites})
    groups=[]
    for x in columns:
        if not groups or x-groups[-1][-1]>16:groups.append([])
        groups[-1].append(x)
    if len(groups)!=2:
        return {"ok":False,"reason":"EXPECTED_TWO_WHITE_GROUPS","group_count":len(groups),
                "y0":y0,"starts":None,"union_cost":999,"white_count":len(whites)}
    starts=[];costs=[];zero_candidates=[]
    for bits,g in zip((M,F),groups):
        actual={(x,y) for x,y in whites if g[0]<=x<=g[-1]}
        opts=[]
        for start in range(max(0,g[0]-16),g[0]+1):
            exp=canonset(bits,start,y0)
            opts.append((len(actual^exp),start,len(exp-actual),len(actual-exp)))
        opts.sort()
        costs.append(opts[0][0]);starts.append(opts[0][1])
        zero_candidates.append([x for cost,x,mis,extr in opts if cost==0])
    wanted=canonset(M,starts[0],y0)|canonset(F,starts[1],y0)
    union_cost=len(whites^wanted)
    return {"ok":(len(zero_candidates[0])==len(zero_candidates[1])==1 and
                 costs==[0,0] and union_cost==0 and y0==96),
         "reason":"EXACT" if costs==[0,0] and union_cost==0 else "PIXEL_OR_ORIENTATION_OR_GHOST",
         "group_count":len(groups),"starts":starts,"y0":y0,"white_count":len(whites),
         "individual_symmetric_differences":costs,"union_cost":union_cost,
         "unique_zero_cost_starts":zero_candidates}
def matcher_B(im):
    # Independent non-set approach: row03 each original mask has exactly
    # 0xFF -> 16 contiguous physical white pixels. Locate both runs directly;
    # use Python integer bitmasks to prove every other TOP-DOWN row.
    pix=im.load()
    rows=[]
    for y in range(50,195):
        v=0
        for x in range(WIDTH):
            if white(pix[x,y]):v|=1<<x
        rows.append(v)
    ys=[i+50 for i,v in enumerate(rows) if v]
    if not ys:return {"ok":False,"reason":"EMPTY_WHITE","starts":None}
    y0=min(ys)
    cols=[x for x in range(WIDTH) if white(pix[x,y0+3])]
    runs=[]
    for x in cols:
        if not runs or x!=runs[-1][-1]+1:runs.append([])
        runs[-1].append(x)
    if len(runs)!=2 or [len(r) for r in runs]!=[16,16]:
        return {"ok":False,"reason":"FULL_FF_ROW03_NOT_TWO_SEPARATE_RUNS",
                "starts":None,"run_lengths":[len(r) for r in runs],"y0":y0}
    starts=[run[0] for run in runs]
    def bm(bits,idx,x0):
        result=0
        for col,ch in enumerate(bits[idx]):
            if ch=="1": result|=(3<<(x0+2*col))
        return result
    costs=[]
    for idx in range(9):
        expected=bm(M,idx,starts[0])|bm(F,idx,starts[1])
        costs.append((rows[y0+idx-50]^expected).bit_count())
    outside=sum(r.bit_count() for i,r in enumerate(rows) if not(y0-50<=i<=y0+8-50))
    return {"ok":(all(c==0 for c in costs) and outside==0 and y0==96),
            "reason":"EXACT" if all(c==0 for c in costs) and outside==0 else "ROW_BITMAP_MISMATCH",
            "starts":starts,"y0":y0,"nine_row_XOR_popcount":costs,
            "outside_9_rows":outside}
def controls(im,y0):
    p=im.load()
    if y0 is None:return {"P0_yellow":False,"M0_active":False,"PF_brown_left":False,
                          "PF_brown_right":False,"NTSC_262":False}
    yellowpix={(x,y) for y in range(y0,y0+9) for x in range(WIDTH) if yellow(p[x,y])}
    player_pts={(2*j+d,i) for i,row in enumerate(P0) for j,ch in enumerate(row) if ch=="1" for d in (0,1)}
    player_ok=False;missile_ok=False;playerX=None;missile=None
    for x0 in range(320):
        expected={(x0+dx,y0+dy) for dx,dy in player_pts}
        if not expected.issubset(yellowpix):continue
        remaining=sorted(yellowpix-expected)
        if len(remaining)==2 and remaining[0][1]==remaining[1][1]==y0+4 and remaining[1][0]==remaining[0][0]+1:
            player_ok=True;missile_ok=True;playerX=x0;missile=remaining;break
    left=all(sum(brown(p[x,y]) for x in range(0,32))>=3 for y in range(y0,y0+9))
    right=all(sum(brown(p[x,y]) for x in range(300,WIDTH))>=3 for y in range(y0,y0+9))
    hud=hashlib.sha256(im.crop((558,25,594,46)).tobytes()).hexdigest()
    return {"P0_yellow":player_ok,"M0_active":missile_ok,"PF_brown_left":left,
            "PF_brown_right":right,"NTSC_262":hud in HUD262,"NTSC_HUD_sha256":hud,
            "observed_P0_x":playerX,"observed_M0_two_pixels":missile}
def inspect(im):
    im=im.convert("RGB")
    if im.size!=(900,300):
        return {"strict":False,"status":"NTSC_TIMING_FAIL_BAD_CROP_SIZE","size":im.size}
    A=matcher_A(im);B=matcher_B(im)
    C=controls(im,A.get("y0"))
    same=(A.get("starts") is not None and A.get("starts")==B.get("starts"))
    geom=bool(A.get("ok") and B.get("ok") and same)
    invariants=all(C.get(k) for k in ["P0_yellow","M0_active","PF_brown_left","PF_brown_right","NTSC_262"])
    if not C.get("NTSC_262"):category="NTSC_TIMING_FAIL"
    elif not geom:category="FIRST_MASK_LOST_OR_PIXEL_ORIENTATION_FAIL_OR_GHOST"
    elif not invariants:category="P0_M0_PF_FAIL"
    else:category="TWO_TOP_DOWN_ORIGINAL_MASKS_EXACT"
    return {"strict":bool(geom and invariants),
            "category":category,"rendered_x":A.get("starts"),
            "y0":A.get("y0"),"source_set_union":A,
            "independent_integer_bitmap":B,"P0_M0_PF_NTSC":C}
def negative_mutant(im,base,where):
    where.mkdir(parents=True,exist_ok=True)
    if not base["strict"]:return {"executed":False,"reason":"BASE_REAL_IMAGE_ALREADY_FAILED"}
    xy=sorted(canonset(M,base["rendered_x"][0],base["y0"]))[0]
    m=im.convert("RGB").copy()
    assert white(m.getpixel(xy))
    m.putpixel(xy,(30,30,30))
    f=where/"SYNTHETIC_ERASE_ONE_MALE_TOP_DOWN_PIXEL_NOT_STELLA.png";m.save(f)
    re=inspect(m)
    assert not re["strict"] and not re["source_set_union"]["ok"] and not re["independent_integer_bitmap"]["ok"]
    return {"executed":True,"synthetic_not_stella":True,"file":f.name,"sha256":sha(f),
            "set_oracle_rejected":True,"independent_bitmap_oracle_rejected":True}
def main():
    ar=argparse.ArgumentParser()
    ar.add_argument("--first",type=int,choices=[21,23],required=True)
    ar.add_argument("--raw",type=Path,required=True)
    ar.add_argument("--out",type=Path,required=True)
    ar.add_argument("--mutants",type=Path,required=True)
    args=ar.parse_args()
    paths=sorted(args.raw.glob("frame_*.png"))
    assert len(paths)==16,(len(paths),args.raw)
    result=[]
    for i,p in enumerate(paths,1):
        with Image.open(p) as im:r=inspect(im)
        r["genuine_unmodified_Stella_PNG"]=p.name
        r["png_SHA256"]=sha(p);r["expected_frame_if_ctrl_f_once"]=10+i
        result.append(r)
        print("F6_GENUINE_STELLA",args.first,i,"observed",r.get("rendered_x"),
              "TOP_DOWN_BOTH",r["strict"],"category",r.get("category"),flush=True)
    good=all(x["strict"] for x in result)
    positions={tuple(r["rendered_x"]) for r in result if r.get("rendered_x")}
    stable=len(positions)==1 and len(result)==16
    requested=[43,99] if args.first==21 else [45,99]
    mutant=negative_mutant(Image.open(paths[0]),result[0],args.mutants)
    category="TWO_MASK_BASELINE_VALID" if args.first==21 and good and stable else (
       "TWO_MASK_IMAGES_VALID" if good and stable else "MASK_PIXEL_COLOR_OR_SCANLINE_FAIL")
    out={"F6_first_RESP1_cycle_STATIC":args.first,"second_RESP1_cycle_STATIC":32,
         "preregistered_model_requested_cropX":requested,
         "observed_rendered_pairs":[list(x) for x in sorted(positions)],
         "all_16_masks_top_down_and_controls_exact":good,"stable_16_physical_X":stable,
         "classification":category,
         "baseline_safe_to_authorize_second_compiled_variant":bool(args.first==21 and good and stable),
         "mutant_negative":mutant,"source_canon_blob":"058800a4c1904d1ff289e7e61b3902aa111ba16d",
         "NO_R1_ACCEPTANCE":True,"real_Stella_frames":result}
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(out,indent=2)+"\n")
    print("F6_PIXEL_GATE",args.first,category,"stable",stable,"x",sorted(positions),"SECOND_COMPILE_ALLOWED",out["baseline_safe_to_authorize_second_compiled_variant"])
    # Pixel or source corruption is a HARD STOP, but JSON is always written first.
    if not good or not stable:raise SystemExit(3)
if __name__=="__main__":main()
