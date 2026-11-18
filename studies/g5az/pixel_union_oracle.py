#!/usr/bin/env python3
"""G5AZ independent SOURCE-ONLY pixel-union oracle, NOT a ROM/TIA PASS.

Run from project root:
  python3 studies/g5az/pixel_union_oracle.py

Reads exact approved design/NPC_REFERENCE_8x9_masks.json TOP-DOWN masks.
Computes least number of <=8-column bitmap groups per raster row *provided
every active NPC row stays wholly in one group*. Pixel groups have no
hardware deadlines, so values do NOT prove P1 retrigger or overlap timing.
"""
import json
from pathlib import Path

MASKS = json.loads(Path("design/NPC_REFERENCE_8x9_masks.json").read_text())
assert (MASKS["width"], MASKS["height"]) == (8, 9)
TYPES = ("large_male", "large_male", "large_female", "small_male", "small_female")
SCENES = {
    "separated": ((19,46,73,100,127), (72,72,72,72,72)),
    "reorder": ((130,19,73,103,46), (73,72,73,71,72)),
    "staggered": ((46,127,19,100,73), (70,71,72,73,74)),
    "same_x_two": ((73,73,19,100,46), (75,74,73,72,71)),
    "close3": ((73,76,79,82,85), (72,72,72,72,72)),
    "close1": ((73,74,75,76,77), (72,72,72,72,72)),
    "exact_same_x_five": ((73,73,73,73,73), (72,72,72,72,72)),
}

def row_bits(x, y, scan, kind):
    r = scan - y
    if r < 0 or r >= 9:
        return set()
    mask = MASKS["sprites"][kind][r]
    assert len(mask) == 8 and set(mask) <= {"0", "1"}
    return {x + bit for bit, pixel in enumerate(mask) if pixel == "1"}

def partition(bits):
    """Exact minimum 8-column groups, WITHOUT splitting a source NPC row.

    Position and bitmap per group are witnesses in abstract pixel space.
    Does not model TIA START, sprite copies, cycle deadlines, or ghosts.
    """
    active = [i for i, item in enumerate(bits) if item]
    if not active:
        return []
    whole = (1 << len(active)) - 1
    valid = {}
    for mask in range(1, whole + 1):
        union = set().union(*(bits[active[j]] for j in range(len(active)) if mask & (1 << j)))
        valid[mask] = max(union) - min(union) < 8
    dp = {0: []}
    for mask in range(1, whole + 1):
        first = mask & -mask
        choices = []
        sub = mask
        while sub:
            if sub & first and valid[sub]:
                ids = [active[j] for j in range(len(active)) if sub & (1 << j)]
                pix = set().union(*(bits[i] for i in ids))
                left = min(pix)
                word = sum(128 >> (p - left) for p in pix)
                assert pix == {left + j for j in range(8) if word & (128 >> j)}
                choices.append(dp[mask ^ sub] + [{"ids": ids, "left": left, "byte": f"{word:02X}"}])
            sub = (sub - 1) & mask
        dp[mask] = min(choices, key=len)
    groups = dp[whole]
    decoded = set()
    for g in groups:
        decoded |= {g["left"] + j for j in range(8) if int(g["byte"], 16) & (128 >> j)}
    assert decoded == set().union(*bits)
    return groups

def scene_report(name, xs, ys):
    out = []
    for scan in range(min(ys), max(ys) + 9):
        bits = [row_bits(xs[i], ys[i], scan, TYPES[i]) for i in range(5)]
        grp = partition(bits)
        out.append({"scan": scan, "active": sum(bool(x) for x in bits),
                    "patterns": len(grp), "groups": grp})
    return {"name": name, "actor_rows": sum(x["active"] for x in out),
            "patterns": sum(x["patterns"] for x in out),
            "peak": max(x["patterns"] for x in out), "rows": out}

def same_x_regression():
    missing = []
    for scan in range(75, 83):
        old = row_bits(73, 75, scan, "large_male")
        second = row_bits(73, 74, scan, "large_male")
        union = old | second
        byte = sum(128 >> (p - 73) for p in union)
        missing.append((scan, f"{byte:02X}", len(union - old)))
    assert sum(count for _, _, count in missing) == 10
    return missing

def main():
    result = {"classification": "SOURCE_ONLY_NOT_TIA_VERIFIED",
              "overlap_rows": same_x_regression(),
              "scenes": [scene_report(name, *args) for name,args in SCENES.items()]}
    print("G5AZ source-only pixel-union oracle (NOT a ROM/TIA PASS)")
    for s in result["scenes"]:
        print(f'{s["name"]:20} {s["actor_rows"]:2} NPC rows => '
              f'{s["patterns"]:2} ideal 8-bit groups; peak {s["peak"]} per scanline')
    print("same-X OR unique pixels recoverable:", sum(r[2] for r in result["overlap_rows"]))
    print("G5AY extra 2 pixels: NOT TESTED")
    print("Future TIA/6507 scheduling, collision readability and real ROM: NOT TESTED")

if __name__ == "__main__":
    main()
