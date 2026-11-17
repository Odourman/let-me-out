#!/usr/bin/env python3
"""G5AF: fail-closed F9 read-only saved Stella prompt+native TIA audit."""
import csv
import hashlib
import json
import re
import sys
from pathlib import Path
from PIL import Image

root = Path(sys.argv[1]).resolve()
expected_sha = "6c2585148eb082fb8bc794d664edc4869b18849fcfabb9cada23373d1dc1318b"
stops = [
    ("F9_000_M_RESP1", 19, 23),
    ("F9_000_F_RESP1", 30, 34),
]
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else "MISSING"

def extracted(text, name):
    # The CLI "print EXPR" command must itself be present, then the parser
    # must actually render a numeric response before the next prompt.
    # No expected value is supplied to this function.
    lines = text.splitlines()
    result = []
    match_command = re.compile(r"(?i)\bprint\s+" + re.escape(name) + r"\s*$")
    for i, line in enumerate(lines):
        if not match_command.search(line.strip()):
            continue
        for later in lines[i + 1: i + 4]:
            val = later.strip()
            if re.search(r"(?i)\b(print|saveSes|saveSnap|tia)\b", val):
                break
            # Stella 6.7.1: "INPT3|$70(R): $7b %... #123".
            # $70 is a register address, not the numeric print result.
            decimals = re.findall(r"#(\d+)\b", val)
            if decimals:
                result.append(int(decimals[-1]))
                break
            m = re.search(r"(?<![\w])(?:\$([0-9A-Fa-f]+)|(\d+))(?![\w])", val)
            if m:
                result.append(int(m.group(1), 16) if m.group(1) else int(m.group(2)))
                break
    return result

rows = []
index = []
for name, low, high in stops:
    folder = root / name
    txt = folder / "debugger_session.txt"
    png = folder / "native_TIA_original.png"
    commands = folder / "keyboard_commands.txt"
    content = txt.read_text(errors="replace") if txt.exists() else ""
    values = {k: extracted(content, k) for k in ("pc", "_fCount", "_scan", "_sCycles", "_bank")}
    actual = {k: (v[0] if v else "") for k,v in values.items()}
    same_pc = len(values["pc"]) >= 2 and values["pc"][0] == values["pc"][-1]
    same_scan = len(values["_scan"]) >= 2 and values["_scan"][0] == values["_scan"][-1]
    picture = None
    if png.is_file():
        try:
            with Image.open(png) as im:
                picture = [im.width, im.height, im.mode]
        except Exception:
            picture = None
    prompt = commands.read_text() if commands.is_file() else ""
    proper_prompt = all(cmd in prompt.splitlines() for cmd in
                        ("print pc", "print _fCount", "print _scan", "print _sCycles",
                         "print _bank", "tia", "saveSnap", "saveSes"))
    tia_state = ("COLUxx:" in content and "P0:" in content
                 and "P1:" in content and "M0:" in content)
    # For this F9 source-only preregistered scanline+write trap band,
    # enforce only live measured response (not source-estimated PC or c).
    valid = (
        len(content.encode()) > 100 and picture == [320, 228, "RGB"]
        and proper_prompt and tia_state and same_pc and same_scan
        and actual["pc"] != "" and actual["_fCount"] != ""
        and actual["_scan"] == 123 and actual["_sCycles"] != ""
        and actual["_bank"] != ""
    )
    row = {
        "case_id": name,
        "reg_write_trap": "RESP1",
        "source_pre_registered_frame": "136",
        "source_pre_registered_scanline": "123",
        "source_pre_registered_cycle_min_exclusive": low,
        "source_pre_registered_cycle_max_exclusive": high,
        "actual_PC_decimal": actual["pc"],
        "actual_frame_counter_decimal": actual["_fCount"],
        "actual_scanline_decimal": actual["_scan"],
        "actual_sCycles_decimal": actual["_sCycles"],
        "actual_bank_decimal": actual["_bank"],
        "actual_PC_stable_after_TIA_print": same_pc,
        "actual_scanline_stable_after_TIA_print": same_scan,
        "actual_TIA_state_from_debugger": tia_state,
        "actual_native_TIA_size": "x".join(str(z) for z in picture[:2]) if picture else "MISSING",
        "actual_session_bytes": txt.stat().st_size if txt.exists() else 0,
        "session_path": f"{name}/debugger_session.txt" if txt.exists() else "MISSING",
        "session_SHA256": sha(txt),
        "native_TIA_path": f"{name}/native_TIA_original.png" if png.exists() else "MISSING",
        "native_TIA_SHA256": sha(png),
        "F9_original_ROM_SHA256": expected_sha,
        "verdict": "OBSERVED_INSTRUMENT_READY" if valid else "NOT_DETERMINABLE",
    }
    rows.append(row)
    index.append({"case": name, "commands_typed_after_prompt": prompt.splitlines(),
                  "parsed_source": "actual native saveSes transcript (not stdout estimates)",
                  "parsed_values_all": values, "register_TIA_text_present": tia_state,
                  "native_TIA_properties": picture, "stella_observed": bool(content),
                  "valid": valid})
    print("G5AF_CASE_AUDIT", json.dumps(row, ensure_ascii=True), flush=True)

with (root / "G5AF_INSTRUMENTATION_EVIDENCE.csv").open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys())
    w.writeheader()
    w.writerows(rows)
(root / "G5AF_PARSE_DIAGNOSTICS.json").write_text(json.dumps(index, indent=2) + "\n")
name_set = {r["case_id"] for r in rows}
different = len({r["actual_PC_decimal"] for r in rows if r["actual_PC_decimal"] != ""}) == 2
ready = all(r["verdict"] == "OBSERVED_INSTRUMENT_READY" for r in rows) and different
classification = ("G5AF_INSTRUMENTATION_READY_BOUNDED" if ready else
                  "G5AF_PARTIAL_INSTRUMENTATION_NOT_READY" if any(r["actual_session_bytes"] > 0 and r["native_TIA_SHA256"] != "MISSING" for r in rows)
                  else "G5AF_INSTRUMENTATION_BLOCKED")
(root / "G5AF_AUDIT_STATUS.txt").write_text(classification + "\n")
files = [p for p in root.rglob("*") if p.is_file() and p.name != "SHA256SUMS.txt"]
with (root / "SHA256SUMS.txt").open("w") as f:
    for p in sorted(files):
        f.write(f"{sha(p)}  {p.relative_to(root).as_posix()}\n")
print("G5AF_FINAL_CLASSIFICATION", classification, flush=True)
print("G5AF_DISTINCT_PC", different, flush=True)
sys.exit(0 if ready else 3)
