#!/usr/bin/env python3
"""Read-only cycle audit of R1h DASM listing; no ROM build or modification.
Usage: python main_iii_r1h_cycle_audit.py r1h.lst r1h.sym
Artifact source: GitHub Actions #43821560463 / artifact #14204881614.
"""
import json
import re
import sys
from pathlib import Path

if len(sys.argv) != 3:
    raise SystemExit("Usage: python main_iii_r1h_cycle_audit.py r1h.lst r1h.sym")
listing = Path(sys.argv[1]).read_text()
symbols = Path(sys.argv[2]).read_text()
syms = {m.group(1): int(m.group(2), 16) for line in symbols.splitlines()
        if (m := re.match(r"^(\\w+)\\s+([0-9a-f]{4})\\s+", line, re.I))}
names = [f"R1gRows{c}" for c in "ABCD"] + ["R1gAfterRows"]
if any(name not in syms for name in names):
    raise RuntimeError("Missing labels; refuse to infer timing")
inst = []
for line in listing.splitlines():
    m = re.match(r"^\\s*\\d+\\s+([0-9a-f]{4})\\s+((?:[0-9a-f]{2}\\s+){1,3})(\\w+)\\s*(.*)$", line, re.I)
    if m:
        inst.append((int(m.group(1), 16), bytes.fromhex(m.group(2)),
                     m.group(3).upper(), m.group(4).split(";", 1)[0].strip()))

audit = {}
for ch in "ABCD":
    start = syms[f"R1gRows{ch}"]
    end = syms["R1gAfterRows"] if ch == "D" else syms[f"R1gRows{chr(ord(ch)+1)}"]
    rows = [x for x in inst if start <= x[0] < end]
    if not rows or rows[0][2:] != ("STA", "WSYNC"):
        raise RuntimeError(f"{ch} does not start with WSYNC")
    elapsed = 0
    events = []
    for pc, opcode, mnemonic, operand in rows[1:]:
        if mnemonic == "JMP":
            break
        crossing = False
        if mnemonic == "STA" and operand == "WSYNC":
            cycles = 3
        elif mnemonic in ("STA", "STX", "BIT") and len(opcode) == 2:
            cycles = 3
        elif mnemonic in ("LDA", "LDX") and len(opcode) == 3 and operand.endswith(",Y"):
            base = int.from_bytes(opcode[1:], "little")
            if any((base+y)>>8 != base>>8 for y in range(9)):
                raise RuntimeError(f"Indexed page crossing in {ch}")
            cycles = 4
        elif mnemonic == "LDA" and len(opcode) == 2 and operand.startswith("#"):
            cycles = 2
        elif mnemonic == "DEY":
            cycles = 2
        elif mnemonic == "BPL":
            signed = opcode[1] if opcode[1] < 128 else opcode[1]-256
            dest = (pc + 2 + signed) & 65535
            if dest != start:
                raise RuntimeError("Unexpected branch destination")
            crossing = (dest >> 8) != ((pc+2) >> 8)
            cycles = 3 + int(crossing)  # taken BPL, first eight rows
        else:
            raise RuntimeError(f"Unexpected instruction {mnemonic} {operand}")
        elapsed += cycles
        events.append({"pc":f"${pc:04X}", "op":mnemonic, "operand":operand,
                       "end_cycle":elapsed, "branch_page_crossing":crossing})
        if mnemonic == "STA" and operand == "WSYNC":
            break
    if events[-1]["operand"] != "WSYNC":
        raise RuntimeError("Missing terminating WSYNC")
    audit[ch] = {"cycles_including_next_WSYNC":elapsed, "spare":76-elapsed,
                 "taken_BPL_crosses_page":any(e["branch_page_crossing"] for e in events),
                 "events":events}
if [audit[c]["cycles_including_next_WSYNC"] for c in "ABCD"] != [75,74,74,74]:
    raise RuntimeError("Source differs from recorded R1h, cannot inherit results")
for ch in "ABCD":
    e = audit[ch]["events"]
    if [v["end_cycle"] for v in e if v["op"] == "STA" and v["operand"] == "RESP1"] != [26,45,66]:
        raise RuntimeError("Unexpected P1 schedule")
    if [v["end_cycle"] for v in e if v["op"] == "BIT" and v["operand"] == "FRAMELO"] != [39,42]:
        raise RuntimeError("Unexpected 3-cycle padding slots")
print(json.dumps({"status":"STATIC_CPU_ANALYSIS_ONLY; no TIA/ROM evidence for R1i",
                  "original_R1h_run":"https://github.com/Odourman/let-me-out/actions/runs/43821560463",
                  "candidate_P1_second_strobe_slots":[39,42,45],
                  "candidate_additional_P1_strobe":39,
                  "audit":audit},indent=2))
