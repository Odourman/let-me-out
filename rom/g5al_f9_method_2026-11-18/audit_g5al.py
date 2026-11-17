#!/usr/bin/env python3
"""G5AL LM-D25: independent fail-closed parser of NEW Stella 6.7.1 sessions.
A verdict is an emulator-method development self-check, NEVER Verification II.
"""
import csv, hashlib, json, re, sys
from pathlib import Path
from PIL import Image, ImageChops

EXPECTED="6c2585148eb082fb8bc794d664edc4869b18849fcfabb9cada23373d1dc1318b"
KEYS=("pc","_fCount","_scan","_sCycles","_bank")
def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else "MISSING"
def values(s,k):
    lines=s.splitlines()
    found=[]
    pattern=re.compile(r"(?i)\bprint\s+"+re.escape(k)+r"\s*$")
    for i,line in enumerate(lines):
        if not pattern.search(line.strip()): continue
        for next_line in lines[i+1:i+4]:
            val=next_line.strip()
            if re.search(r"(?i)\b(print|saveSes|saveSnap|tia|break|run|frame)\b",val): break
            matches=re.findall(r"#(\d+)\b",val)
            if matches:
                found.append(int(matches[-1])); break
            m=re.search(r"(?<![\w])(?:\$([0-9a-fA-F]+)|(\d+))(?![\w])",val)
            if m:
                found.append(int(m.group(1),16) if m.group(1) else int(m.group(2)));break
    return found
def parsed(p):
    s=p.read_text(errors="replace") if p.exists() else ""
    out={"file":p.name,"bytes":p.stat().st_size if p.exists() else 0,"sha256":sha(p),
         "stella_header":"Stella 6.7.1" in s,
         "tia": all(x in s for x in ("COLUxx:","P0:","P1:","M0:")),
         "trap_added": bool(re.search(r"\badded trap\s+\$?[0-9a-f]+\b",s,re.I)),
         "trap_removed": "removed trap" in s,
         "step_three": "executed 3 cycles" in s.lower()}
    for k in KEYS:out[k]=values(s,k)
    for n in range(4):
        out[f"break_set_{n}"]=bool(re.search(r"set breakpoint at \$f1ee \+ mirrors in bank #"+str(n)+r"\b",s,re.I))
    out["break_cleared"]=bool(re.search(r"cleared breakpoint",s,re.I))
    return out
def last(d,k):
    return d[k][-1] if d[k] else None
def gate(stage,d):
    if d["bytes"]<=150:return False
    if stage.endswith("HANDSHAKE"):
        return d["stella_header"] and bool(d["pc"]) and bool(d["_bank"]) and 0<=last(d,"_bank")<=3
    if stage in ("A_FRAME","B_FRAME"):
        return last(d,"_fCount")==136 and bool(d["pc"]) and 0<=last(d,"_bank")<=3
    if stage=="A_TRAP_ACK":
        return d["trap_added"] and not d["trap_removed"]
    if stage=="A_TRAP":
        return (d["tia"] and d["pc"][-2:]==[0xF1F0,0xF1F0] and last(d,"_fCount")==136
                and d["_scan"][-2:]==[123,123] and last(d,"_sCycles")==21
                and last(d,"_bank") in (0,1,2,3))
    if stage.startswith("B_SET_"):
        n=int(stage.rsplit("_",1)[-1])
        return d[f"break_set_{n}"] and not d["break_cleared"]
    if stage=="B_PRE":
        return (d["tia"] and d["pc"][-2:]==[0xF1EE,0xF1EE] and last(d,"_fCount")==136
                and last(d,"_scan")==123 and last(d,"_bank") in (0,1,2,3))
    if stage=="C_POST":
        return (d["tia"] and d["step_three"] and d["pc"][-2:]==[0xF1F0,0xF1F0]
                and last(d,"_fCount")==136 and last(d,"_scan")==123
                and last(d,"_bank") in (0,1,2,3))
    return False
def native(p):
    r={"sha256":sha(p),"ok":False}
    if not p.exists():return r
    try:
        with Image.open(p) as im:
            r["size"]=[im.width,im.height];r["mode"]=im.mode
            r["ok"]=im.size==(320,228) and im.mode=="RGB"
    except Exception as e:r["error"]=str(e)
    return r
def compare_png(a,b):
    r={"g5al_sha256":sha(a),"g5af_sha256":sha(b),"pixel_equal":False}
    if not a.exists() or not b.exists():return r
    with Image.open(a) as ia, Image.open(b) as ib:
        r["g5al_size"]=list(ia.size);r["g5af_size"]=list(ib.size)
        if ia.size!=ib.size or ia.mode!=ib.mode:return r
        delta=ImageChops.difference(ia,ib)
        r["diff_bbox"]=delta.getbbox()
        r["pixel_equal"]=delta.getbbox() is None
        r["different_pixels"]=sum(1 for px in delta.getdata() if px!=(0,0,0))
    return r

if len(sys.argv)>=4 and sys.argv[1]=="--gate":
    stage,p=sys.argv[2],Path(sys.argv[3])
    observed=parsed(p);ok=gate(stage,observed)
    print("G5AL_SESSION_GATE",json.dumps({"stage":stage,"pass":ok,"observed":observed},sort_keys=True),flush=True)
    sys.exit(0 if ok else 7)

root=Path(sys.argv[1]).resolve()
names=("A_HANDSHAKE","A_FRAME","A_TRAP_ACK","A_TRAP","B_HANDSHAKE","B_FRAME",
       "B_SET_0","B_SET_1","B_SET_2","B_SET_3","B_PRE","C_POST")
stages={}
for n in names:
    parent=root/("A_TRAP" if n.startswith("A_") else "B_BREAK_STEP")
    p=parent/(n+"_session.txt")
    d=parsed(p)
    stages[n]={"observed":d,"session_gate":gate(n,d),"path":str(p.relative_to(root))}
imgs={}
for n in ("A_TRAP","B_PRE","C_POST"):
    parent=root/("A_TRAP" if n.startswith("A_") else "B_BREAK_STEP")
    imgs[n]=native(parent/(n+"_native_TIA.png"))
ref=root.parent.parent.parent/"ref_g5af"/"F9_000_M_RESP1"/"native_TIA_original.png"
cmp=compare_png(root/"A_TRAP"/"A_TRAP_native_TIA.png",ref)
(root/"G5AL_G5AF_NATIVE_COMPARISON.json").write_text(json.dumps(cmp,indent=2)+"\n")
A=bool((root/"A_TRAP"/"STAGE_A_PASS.txt").exists() and
       all(stages[n]["session_gate"] for n in ("A_HANDSHAKE","A_FRAME","A_TRAP_ACK","A_TRAP")) and
       imgs["A_TRAP"]["ok"] and cmp["pixel_equal"])
B=bool(A and (root/"B_BREAK_STEP"/"STAGE_B_PASS.txt").exists() and
       all(stages[n]["session_gate"] for n in
           ("B_HANDSHAKE","B_FRAME","B_SET_0","B_SET_1","B_SET_2","B_SET_3","B_PRE"))
       and imgs["B_PRE"]["ok"])
pre=stages["B_PRE"]["observed"];post=stages["C_POST"]["observed"]
C=bool(B and (root/"B_BREAK_STEP"/"STAGE_C_PASS.txt").exists() and
       stages["C_POST"]["session_gate"] and imgs["C_POST"]["ok"] and
       last(post,"_sCycles")-last(pre,"_sCycles")==3 and
       all(last(post,k)==last(pre,k) for k in ("_fCount","_scan","_bank")))
pre_sha=(root/"F9_ROM_SHA_PRE.txt").read_text(errors="replace") if (root/"F9_ROM_SHA_PRE.txt").exists() else ""
post_sha=(root/"F9_ROM_SHA_POST.txt").read_text(errors="replace") if (root/"F9_ROM_SHA_POST.txt").exists() else ""
ROM=("OK" in pre_sha and "OK" in post_sha)
code=(root/"script_exit_code.txt").read_text().strip() if (root/"script_exit_code.txt").exists() else "MISSING"
complete=A and B and C and ROM and code=="0"
status=("G5AL_F9_METHOD_READY_BOUNDED_PENDING_ARCHIVE_READBACK" if complete else
        "G5AL_F9_METHOD_PARTIAL_NOT_DETERMINABLE" if A else "G5AL_F9_TRAP_CONTROL_FAIL")
rows=[]
for n in names:
    d=stages[n]["observed"]
    executed=d["bytes"]>0
    rows.append({
        "case":n,"status":"STELLA_OBSERVED" if stages[n]["session_gate"] else
                             "NOT_DETERMINABLE" if executed else "NOT_RUN",
        "gate_pass":str(stages[n]["session_gate"]),"pc_dec":last(d,"pc"),
        "frame_dec":last(d,"_fCount"),"scan_dec":last(d,"_scan"),
        "sCycles_dec":last(d,"_sCycles"),"bank_dec":last(d,"_bank"),
        "session_bytes":d["bytes"],"session_SHA256":d["sha256"],
        "native_SHA256":imgs[n]["sha256"] if n in imgs else "NOT_APPLICABLE",
        "source_inferred_STA_BUS_PHASE":"SOURCE_INFERRED_NOT_MEASURED",
        "C0_X40_X104":"NOT_RUN_NO_ROM",
        "F9_ROM_SHA256":EXPECTED})
with (root/"G5AL_EVIDENCE.csv").open("w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
summary={"A_pass":A,"B_pass":B,"C_pass":C,"D_archive_readback":"PENDING_SEPARATE_JOB",
         "pre_archive_verdict":status,"ROM_source_sha_pass":ROM,"script_exit_code":code,
         "sessions":stages,"native":imgs,"g5af_image_comparison":cmp,
         "registered_four_bank_break_strategy":"break $f1ee #0 #1 #2 #3 each once",
         "historical_G5AJ":"TRAP_CONTROL_FAIL_UNCHANGED",
         "physical_TIA_BUS_CLOCK":"SOURCE_INFERRED_NOT_OBSERVED"}
(root/"G5AL_AUDIT.json").write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n")
(root/"G5AL_PRE_ARCHIVE_VERDICT.txt").write_text(status+"\n")
print("G5AL_AUDIT",json.dumps({k:summary[k] for k in
    ("A_pass","B_pass","C_pass","pre_archive_verdict","ROM_source_sha_pass")}),flush=True)
sys.exit(0 if complete else 8)
