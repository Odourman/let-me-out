#!/usr/bin/env python3
"""Fail-closed one frozen F9 preflight, no C0 ROM unless this PASS."""
import hashlib,json,re,sys
from pathlib import Path
from PIL import Image
p=Path(sys.argv[1]).resolve()
def sha(q):return hashlib.sha256(q.read_bytes()).hexdigest() if q.is_file() else "MISSING"
def parse(q):
    s=q.read_text(errors="replace") if q.exists() else ""
    def values(k):
        z=[]
        for m in re.finditer(r"(?m)^>\s+print\s+"+re.escape(k)+r"\s*$",s):
            future=s[m.end():]
            m2=re.search(r"(?m)^\s*([^\n]+)\s*$",future)
            if m2:
                d=re.findall(r"#(\d+)\b",m2.group(1))
                if d:z.append(int(d[-1]))
        return z
    return {"length":len(s.encode()),"pc":values("pc"),"frame":values("_fCount"),
            "scan":values("_scan"),"cpu_cycles":values("_sCycles"),
            "bank":values("_bank"),"RAM_X0_SELECT":values("X0_SELECT"),
            "has_tia_registers":"COLUxx:" in s and "P0:" in s and "P1:" in s,
            "disasm_RESP1":"RESP1" in s and "disAsm" in s,
            "has_sym_missing":"symbol file" in s and "not found" in s,
            "has_lst_missing":"list file" in s and "not found" in s,
            "step_3cycles":"executed 3 cycles" in s,
            "sha256":sha(q)}
a=parse(p/"pre_step_debugger_session.txt")
b=parse(p/"post_step_debugger_session.txt")
png={}
for k in ("pre_step","post_step"):
    q=p/(k+"_native_TIA.png")
    z={"sha256":sha(q),"path":q.name}
    if q.exists():
        try:
            with Image.open(q) as im:
                rgb=im.convert("RGB")
                z["size"]=[im.width,im.height]
                z["source_2x_image"]=(im.width==320 and im.height==228)
                diffs=[(x,y) for y in range(rgb.height) for x in range(160)
                       if rgb.getpixel((2*x,y))!=rgb.getpixel((2*x+1,y))]
                # Stella source draws a 3x3 beam marker over 2x pixels.
                z["pixel_pair_inequality_count"]=len(diffs)
                z["overlay_bounding_box"]=[min(x for x,y in diffs),min(y for x,y in diffs),
                                         max(x for x,y in diffs),max(y for x,y in diffs)] if diffs else []
                z["pair_transform_valid_except_cursor"]=(len(diffs)<=9 and (
                    not diffs or (max(x for x,y in diffs)-min(x for x,y in diffs)<=2 and
                                  max(y for x,y in diffs)-min(y for x,y in diffs)<=2)))
        except Exception as e:z["error"]=str(e)
    png[k]=z
stable = (
 a["pc"] == [0xF1EE] and b["pc"] and b["pc"][-1]==0xF1F0
 and a["frame"]==[136] and b["frame"] and b["frame"][-1]==136
 and a["scan"]==[123] and b["scan"] and b["scan"][-1]==123
 and a["cpu_cycles"] and b["cpu_cycles"] and b["cpu_cycles"][-1]-a["cpu_cycles"][0]==3
 and a["bank"]==[0] and b["bank"] and b["bank"][-1]==0
 and a["RAM_X0_SELECT"]==[0] and b["RAM_X0_SELECT"] and b["RAM_X0_SELECT"][-1]==0
 and a["has_tia_registers"] and b["has_tia_registers"]
 and b["step_3cycles"] and a["disasm_RESP1"]
 and not a["has_sym_missing"] and not a["has_lst_missing"]
 and a["length"]>300 and b["length"]>400
 and all(z.get("pair_transform_valid_except_cursor") for z in png.values())
)
data={"pass":bool(stable),"pre":a,"post":b,"native_PNG":png,
      "source_mapping":"TiaOutputWidget draws each of 160 raw indexed TIA pixels twice, then 3x3 electron-beam overlay. native PNG cannot be read as 320 independent colorclocks",
      "STA_write_clock_status":"SOURCE_INFERRED_ONLY (CPU 3-cycle STA instruction, not raw bus event)",
      "C0_ROM_BUILT":False,"C0_RAM_X40_X104_VERIFIED":False,
      "phase_a_verdict":"PASS_CAPABILITY_ONLY" if stable else "FAIL_HARD_NO_BUILD"}
(p/"PHASE_A_ACTUAL_AUDIT.json").write_text(json.dumps(data,indent=2)+"\n")
(p/"PHASE_A_VERDICT.txt").write_text(data["phase_a_verdict"]+"\n")
with (p/"SHA256SUMS.txt").open("w") as f:
 for q in sorted(x for x in p.iterdir() if x.is_file() and x.name!="SHA256SUMS.txt"):
  f.write(f"{sha(q)}  {q.name}\n")
print("G5AH_PHASE_A_AUDIT",json.dumps(data,ensure_ascii=True),flush=True)
if not stable:
 print("G5AH_C0_NO_BUILD_INSTRUMENTATION_BLOCKER",flush=True)
sys.exit(0 if stable else 8)
