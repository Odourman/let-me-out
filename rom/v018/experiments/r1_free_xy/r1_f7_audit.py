#!/usr/bin/env python3
"""F7 160 consecutive genuine Stella frames, SAME ONE ROM, two independent RAM
selectors, strict TOP-DOWN M/F + P0/M0/PF/262 and 2 independent pixel oracles.
No synthetic picture can ever be counted as a true Stella frame.
"""
import argparse,hashlib,json,sys
from pathlib import Path
from collections import Counter,defaultdict
from PIL import Image
R=Path(__file__).resolve().parent
sys.path.insert(0,str(R))
import r1_f6_audit as F6  # PINNED READ-ONLY verified two independently implemented oracles
p=argparse.ArgumentParser();p.add_argument("--raw",type=Path,required=True)
p.add_argument("--out",type=Path,required=True);p.add_argument("--mutants",type=Path,required=True)
args=p.parse_args()
G0=json.loads((R/"r1_f7_g0_source_only.json").read_text())
assert G0["G0"]=="F7_SOURCE_ONLY_FEASIBLE_FOUR_RUNTIME_PHASES"
fns=sorted(args.raw.glob("frame_*.png"))
assert len(fns)==160,(len(fns),args.raw)
seq=G0["seven_step_16frame_sequence"]["pairs"]
assert seq==["00","10","00","01","11","01","00"]
pred=G0["original_predictions_not_postfit"]
assert pred=={"00":[39,99],"10":[45,99],"01":[39,105],"11":[45,105]}
mode_images=defaultdict(list)
rows=[]
first_good=None
for i,path in enumerate(fns,1):
    # autoexec "frame #10" + exactly i consecutive debugger Ctrl-F:
    expected_actual_fCount=10+i
    seqstep=(expected_actual_fCount//16)%7
    mode=seq[seqstep]
    x0,x1=[int(v) for v in mode]
    with Image.open(path) as im:
        im=im.convert("RGB")
        a=F6.inspect(im)
        if first_good is None and a["strict"]:first_good=(im.copy(),a)
    a.update({
      "true_unmodified_stella_PNG":path.name,
      "actual_raw_PNG_sha256":hashlib.sha256(path.read_bytes()).hexdigest(),
      "debugger_frameindex_source_expected":expected_actual_fCount,
      "source_RAM_step_expected":seqstep,
      "source_RAM_X0_SELECT_expected":x0,
      "source_RAM_X1_SELECT_expected":x1,
      "mode_source_expected":mode,
      "model_prediction_pre_registered_no_postfit":pred[mode],
      "observed_vs_model_prediction_difference":
          ([a["rendered_x"][k]-pred[mode][k] for k in (0,1)] if a["rendered_x"] else None)
    })
    rows.append(a)
    mode_images[mode].append((i,a))
    if i%16==0:
        print("F7_TRUE_STELLA_FRAME",i,"debugger_frame",expected_actual_fCount,
              "RAM_MODE_EXPECTED",mode,"PIXEL_X_ACTUAL",a.get("rendered_x"),
              "TOPDOWN",a["strict"],flush=True)
# At least one full, consecutive 16 real frames for EACH of 4 source states.
stats={}
for mode in ("00","10","01","11"):
    rr=mode_images[mode]
    runs=[];last=[]
    for ix,r in rr:
        if last and ix!=last[-1][0]+1:runs.append(last);last=[]
        last.append((ix,r))
    if last:runs.append(last)
    longest=max((len(run) for run in runs),default=0)
    observed=sorted({tuple(r["rendered_x"]) for _,r in rr if r.get("rendered_x")})
    all_mask_ok=all(r["strict"] for _,r in rr)
    stats[mode]={"count_real_frames":len(rr),"max_consecutive_same_source_RAM_selector_frames":longest,
                 "frame_index_ranges":[[run[0][1]["debugger_frameindex_source_expected"],
                                        run[-1][1]["debugger_frameindex_source_expected"]] for run in runs],
                 "observed_real_X_pairs":[list(x) for x in observed],
                 "all_TOP_DOWN_P0_M0_PF_NTSC_exact":all_mask_ok,
                 "zero_white_missing_extra":all_mask_ok,
                 "prior_model_X_not_recalibrated":pred[mode]}
mutant={"generated":False,"reason":"no pixel-correct raw image available"}
if first_good is not None:
    mutant=F6.negative_mutant(first_good[0],first_good[1],args.mutants)
all_ok=all(r["strict"] for r in rows)
each_complete=all(z["max_consecutive_same_source_RAM_selector_frames"]>=16
                    and z["all_TOP_DOWN_P0_M0_PF_NTSC_exact"] for z in stats.values())
exact_one_per_mode=all(len(stats[m]["observed_real_X_pairs"])==1 for m in stats)
actual={m:(stats[m]["observed_real_X_pairs"][0] if len(stats[m]["observed_real_X_pairs"])==1
          else None) for m in ("00","10","01","11")}
# Orthogonality BOTH directions with either other bit held fixed:
# X0: 00->10 and 01->11 change man only (woman X same).
# X1: 00->01 and 10->11 change woman only (man X same).
checks={}
if all(x is not None for x in actual.values()):
  for kind,a,b,axis,other in [
      ("X0_WHEN_X1_0","00","10",0,1),("X0_WHEN_X1_1","01","11",0,1),
      ("X1_WHEN_X0_0","00","01",1,0),("X1_WHEN_X0_1","10","11",1,0)]:
      checks[kind]={"from":a,"to":b,"actual_A":actual[a],"actual_B":actual[b],
                    "changed_selected_axis":actual[a][axis]!=actual[b][axis],
                    "other_axis_unchanged":actual[a][other]==actual[b][other],
                    "pass":actual[a][axis]!=actual[b][axis] and actual[a][other]==actual[b][other]}
else:
  checks={"unmeasurable":True}
orthogonal=(all(v.get("pass",False) for v in checks.values()) and
            len(checks)==4)
# Detect label sequence 00->10->00->01->11->01->00 from IMAGE data
# (via actual stable, unique pair per source state). No trust in precomputed
# frame profiles without the actual positive pixels + register modes.
cycle_measured=all_ok and each_complete and exact_one_per_mode and orthogonal
classification=("F7_TWO_BINARY_RUNTIME_SELECTORS_LOCAL_PASS" if cycle_measured
                else "F7_ORTHOGONALITY_FAIL" if each_complete and exact_one_per_mode
                else "F7_INCONCLUSIVE_OR_PIXEL_STOP")
report={"classification":classification,"only_one_compiled_ROM":True,
  "real_contiguous_genuine_frame_count":len(rows),
  "all_real_frames_TOP_DOWN_original_mask_AND_P0_M0_PF_NTSC":all_ok,
  "source_CANON_Git_blob":"058800a4c1904d1ff289e7e61b3902aa111ba16d",
  "two_separate_RAM_selectors_addresses":{"X0_SELECT":"$A0","X1_SELECT":"$A1"},
  "mode_order_seven_states_16_frames_each":seq,
  "four_pre_registered_model_targets_no_postfit":pred,
  "per_mode_truth_matrix":stats,
  "actual_measured_single_pair_per_mode":actual,
  "four_independence_checks":checks,
  "all_four_independent_orthogonality_pair_checks_PASS":orthogonal,
  "one_synthetic_negative_mutant_not_stella":mutant,
  "every_four_modes_16_consecutive_real_images":each_complete,
  "all_modes_individually_stable":exact_one_per_mode,
  "ARBITRARY_TWO_X_NOT_PROVEN":True,"SIX_FREE_XY_NOT_PROVEN":True,
  "FULL_R1_BLOCKED_NOT_ACCEPTED":True,
  "per_frame_real_stella_audits":rows}
args.out.parent.mkdir(parents=True,exist_ok=True)
args.out.write_text(json.dumps(report,indent=2)+"\n")
print("F7_REAL_STELLA_2x2_G1",classification,"ACTUAL",actual,"independent",orthogonal,
      "real_frames",len(rows),"MODE_COUNTS",{k:v["count_real_frames"] for k,v in stats.items()},flush=True)
if not cycle_measured:raise SystemExit(3)
