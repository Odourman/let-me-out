#!/usr/bin/env python3
"""R1i-A: research-only 8-kernel probe, based on the proven R1h 600-frame ROM.
Move the existing second RESP1 into a 3-cycle BIT padding slot for each
fourth-NPC-X mode. No additions to any visible scanline's CPU cycle total.
Only a diagnostic standard 16KiB F6 ROM, not main or ROM DEVELOPMENT.
"""
from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
PARENT = ROOT.parent / "main_ii_r1h_integrated"
subprocess.run([sys.executable, str(PARENT / "build_integrated.py")], check=True)
original_rom = (PARENT / "r1h_F6.bin").read_bytes()
EXPECTED_R1H = "2a6fc522b139eaebbec6731df8cab1f1c9297f2266ed44a38a9cc2f29b453a39"
assert len(original_rom) == 16384
assert hashlib.sha256(original_rom).hexdigest() == EXPECTED_R1H, "R1h baseline drift"
base = (PARENT / "r1h_integrated.asm").read_text()
selector_anchor = (
    " LDY #8\n"
    " ; Select independent fourth-NPC X once per frame, OUTSIDE visible row loops.\n"
)
assert base.count(selector_anchor) == 1
head, rest = base.split(selector_anchor)
assert rest.count("R1gRowsA:\n") == 1
old_selector, rest = rest.split("R1gRowsA:\n", 1)
assert rest.count("R1gAfterRows:\n") == 1
row_section, tail = rest.split("R1gAfterRows:\n", 1)
row_section = "R1gRowsA:\n" + row_section
sections = {}
for i, suffix in enumerate("ABCD"):
    marker = f"R1gRows{suffix}:\n"
    next_marker = (
        f"R1gRows{'ABCD'[i+1]}:\n" if i < 3 else ""
    )
    assert row_section.count(marker) == 1
    part = row_section.split(marker, 1)[1]
    if next_marker:
        part = part.split(next_marker, 1)[0]
    assert part.count("\n BIT FRAMELO\n BIT FRAMELO\n") == 1
    assert part.count(f"\nR1cSecondDelay{suffix}:\nR1cSecondRESP1{suffix}:\n STA RESP1\n") == 1
    assert part.count(f"\n BPL R1gRows{suffix}\n") == 1
    sections[suffix] = marker + part

def copy_with_new_suffix(source, old, new):
    labels = set(re.findall(r"(?m)^([A-Za-z][A-Za-z0-9_]*):\s*$", source))
    assert any(x.endswith(old) for x in labels)
    result = source
    for label in sorted(labels, key=len, reverse=True):
        assert label.endswith(old), label
        result = re.sub(r"\b" + re.escape(label) + r"\b", label[:-1] + new, result)
    return result

early = {}
for old, new in zip("ABCD", "EFGH"):
    section = copy_with_new_suffix(sections[old], old, new)
    needle = (
        "\n BIT FRAMELO\n BIT FRAMELO\n"
        f"R1cSecondDelay{new}:\n"
        f"R1cSecondRESP1{new}:\n"
        " STA RESP1\n"
    )
    replacement = (
        f"\nR1cSecondRESP1{new}:\n"
        " STA RESP1\n"
        " BIT FRAMELO\n"
        " BIT FRAMELO\n"
        f"R1cSecondDelay{new}:\n"
    )
    assert section.count(needle) == 1
    section = section.replace(needle, replacement)
    assert section.count(" BIT FRAMELO\n") == 2
    assert section.count(" STA RESP1\n") == 3
    early[new] = section

selector = """ LDY #8
 ; R1i P1 female mode is independent FRAMELO bit7.
 ; Fourth small-female P0 mode remains bits4-5, door bit6.
 LDA FRAMELO
 BMI R1iEarlySelector
 LDA FRAMELO
 AND #$30
 BEQ R1iLateA
 CMP #$10
 BEQ R1iLateB
 CMP #$20
 BEQ R1iLateC
 JMP R1gRowsD
R1iLateA:
 JMP R1gRowsA
R1iLateB:
 JMP R1gRowsB
R1iLateC:
 JMP R1gRowsC
R1iEarlySelector:
 LDA FRAMELO
 AND #$30
 BEQ R1iEarlyE
 CMP #$10
 BEQ R1iEarlyF
 CMP #$20
 BEQ R1iEarlyG
 JMP R1gRowsH
R1iEarlyE:
 JMP R1gRowsE
R1iEarlyF:
 JMP R1gRowsF
R1iEarlyG:
 JMP R1gRowsG
"""
src = (
    head + selector
    + "".join(sections[k] for k in "ABCD")
    + "".join(early[k] for k in "EFGH")
    + "R1gAfterRows:\n" + tail
)
assert src.count("R1gAfterRows:\n") == 1
assert src.count(" ORG $F400") == 1, "Must not alter reference masks"
for suffix in "ABCDEFGH":
    assert src.count(f"R1gRows{suffix}:\n") == 1
    assert src.count(f"R1cSecondRESP1{suffix}:\n") == 1
    assert src.count(f"R1fYellowRESP0{suffix}:\n") == 1
    assert src.count(f"R1fWhiteRESP0{suffix}:\n") == 1
for label in ("MaleRows", "FemaleRows", "SmallMaleRows", "SmallFemaleRows", "PlayerRows"):
    oldmask = base.split(f"{label}:\n", 1)[1].split("\n", 1)[0]
    newmask = src.split(f"{label}:\n", 1)[1].split("\n", 1)[0]
    assert oldmask == newmask, f"Mask unexpectedly changed {label}"

(ROOT / "r1i.asm").write_text(src)
subprocess.run(
    ["dasm", "r1i.asm", "-f3", "-or1i_4k.bin", "-lr1i.lst", "-sr1i.sym"],
    cwd=ROOT, check=True
)
raw = (ROOT / "r1i_4k.bin").read_bytes()
assert len(raw) == 4096
rom = raw * 4
(ROOT / "r1i_F6.bin").write_bytes(rom)
sha = hashlib.sha256(rom).hexdigest()
(ROOT / "ROM_SHA256.txt").write_text(sha + "  r1i_F6.bin\n")
info = {
    "status": "BUILT_UNVERIFIED_R1I_A",
    "rom_bytes": len(rom),
    "mapper": "standard F6 (4 identical 4KiB code banks)",
    "r1h_base_rom_sha256": EXPECTED_R1H,
    "r1i_rom_sha256": sha,
    "late_second_resp1_end_cycle": 45,
    "early_second_resp1_end_cycle": 39,
    "fourth_small_female_modes": 4,
    "new_large_female_modes": 2,
    "door_modes": 2,
    "hypothesized_total_combinations": 16,
    "limits": "No additional NPC. No free 160CC X; actual Stella pixel evidence required."
}
(ROOT / "build_manifest.json").write_text(json.dumps(info, indent=2) + "\n")
print(json.dumps(info, indent=2))
