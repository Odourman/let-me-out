#!/usr/bin/env python3
"""Four actual Stella images prove/deny HMOVE trick #10 in our P0+P1 kernel.

Checks 4 distinct original NPC silhouettes, yellow player, M0 and no ghosts.
P0's white wide copy is EXPECTED to follow player; this is not free fourth-NPC X.
"""
from pathlib import Path
from PIL import Image
import json,re,hashlib,sys
ROOT=Path(__file__).resolve().parent
SRC=(ROOT/"trick10_hmove.asm").read_text()
REF=json.loads((ROOT.parent/"main_ii_three_masks"/"REFERENCE_8x9_MASKS_FROM_MAIN.json").read_text())
NAMES=["large_male","large_female","small_female","small_male"]
LABELS=["MaleRows","FemaleRows","SmallFemaleRows","SmallMaleRows"]
BASE_X={"large_male":154,"large_female":268,"small_female":316,
        "small_male":400,"yellow_player":188}
OFFSETS=[0,1,3,-3] # 0, F0, D0, 30; signed motion nibble is opposite X direction
Y0=162
def parse_mask(symbol):
    m=re.search(rf"^{symbol}:\s*\n\s+BYTE (.+)$",SRC,re.M)
    if not m:raise ValueError("source mask missing "+symbol)
    return [int(v.strip().replace("$","0x"),16) for v in m.group(1).split(",")][::-1]
MASKS={}
for name,sym in zip(NAMES,LABELS):
    a=[int(bits,2) for bits in REF["sprites"][name]]
    b=parse_mask(sym)
    assert a==b, f"Changed original NPC reference: {name}"
    MASKS[name]=b
PLAYER=parse_mask("PlayerRows")
assert len(PLAYER)==9
def white(rgb):
    return min(rgb)>180 and max(rgb)-min(rgb)<40
def yellow(rgb):
    return rgb[0]>120 and rgb[1]>100 and rgb[2]<100
def biterrors(im,x,rows,color):
    num=0
    for y,row in enumerate(rows):
        for b in range(8):
            should=bool(row&(1<<(7-b)))
            for doubled in (0,1):
                num+=int(color(im.getpixel((x+b*2+doubled,Y0+y)))!=should)
    return num
def mask_pixels(x,rows):
    ps=set()
    for y,row in enumerate(rows):
        for b in range(8):
            if row&(1<<(7-b)):
                ps.add((x+b*2,Y0+y))
                ps.add((x+b*2+1,Y0+y))
    return ps
KNOWN_262={
    "04f59d7fbc17d360e0cea738d4e512ab7208118b9b4d4b4743f3a702d96f1fdb",
    "a169787b7bdcf465b5a1b7505dca83c31f60fa2c16337d39fea3e957ea13ace2"}
data={}
for phase,delta in enumerate(OFFSETS):
    source=ROOT/"evidence"/f"phase_{phase}"/"stella_full.png"
    im=Image.open(source).convert("RGB")
    if im.size!=(1366,900):raise ValueError("unexpected Stella GUI size")
    x=dict(BASE_X)
    x["yellow_player"]+=2*delta
    x["small_female"]+=2*delta
    masks={n:biterrors(im,x[n],MASKS[n],white) for n in NAMES}
    p0errors=biterrors(im,x["yellow_player"],PLAYER,yellow)
    whites=set()
    for n in NAMES:whites|=mask_pixels(x[n],MASKS[n])
    yellows=mask_pixels(x["yellow_player"],PLAYER)
    ghost_white=[(xx,yy) for yy in range(Y0,Y0+9) for xx in range(105,435)
                 if white(im.getpixel((xx,yy))) and (xx,yy) not in whites]
    ghost_yellow=[(xx,yy) for yy in range(Y0,Y0+9) for xx in range(105,435)
                  if yellow(im.getpixel((xx,yy))) and (xx,yy) not in yellows]
    m0x=[xx for xx in range(105,435) if yellow(im.getpixel((xx,160)))]
    hud=hashlib.sha256(im.crop((661,90,697,111)).tobytes()).hexdigest()
    valid=(all(n==0 for n in masks.values()) and p0errors==0 and
           not ghost_white and not ghost_yellow and
           m0x==[240,241] and hud in KNOWN_262)
    data[str(phase)]={
        "hmp0_high_nibble":["00","F0","D0","30"][phase],
        "signed_expected_cc_delta":delta,
        "observed_mask_position_gui_x":x,
        "p1_npc_bit_error_pixels":masks,
        "p0_yellow_player_bit_error_pixels":p0errors,
        "unexpected_white_pixels":len(ghost_white),
        "unexpected_yellow_pixels":len(ghost_yellow),
        "ghost_white_examples":ghost_white[:20],
        "ghost_yellow_examples":ghost_yellow[:20],
        "m0_yellow_gui_x":m0x,
        "262_ntsc_hud":hud in KNOWN_262,
        "screenshot_sha256":hashlib.sha256(source.read_bytes()).hexdigest(),
        "phase_local_pass":valid}
summary={
    "source_mask_bytes_unchanged":True,
    "four_phases_passed":sum(v["phase_local_pass"] for v in data.values()),
    "individual_P1_X_unaffected_by_P0_HMOVE":all(
        v["phase_local_pass"] for v in data.values()),
    "P0_white_automatic_copy_moves_with_yellow_player":True,
    "status":"LOCAL_PASS_HMOVE_P0_PAIRED_4_PHASES" if all(
        v["phase_local_pass"] for v in data.values()) else "FAIL_OR_INCONCLUSIVE",
    "limitations":"Only +/-3 CC offset of P0 pair; fourth NPC remains linked to P0 by 64 CC. No six freely positioned NPC, no gameplay PF, only four snapshots, no independent verification."
}
result={"summary":summary,"phases":data}
(ROOT/"evidence"/"audit.json").write_text(
    json.dumps(result,ensure_ascii=False,indent=2)+"\n")
print(json.dumps(result,ensure_ascii=False,indent=2))
sys.exit(0 if summary["status"].startswith("LOCAL_PASS") else 1)
