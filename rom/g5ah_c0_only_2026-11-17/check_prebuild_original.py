#!/usr/bin/env python3
"""G5AH prebuild F9 source/list/sym/ROM validation. No assembly, no mutations."""
import hashlib,json,re,sys
from pathlib import Path

src=Path(sys.argv[1]); masks=json.loads(Path(sys.argv[2]).read_text())["sprites"]
out=Path(sys.argv[3])
base=src/"rom/v018/experiments/r1_free_xy"
stem="r1_f9_three_masks_three_binary_ram_x_ONE_ROM"
source=(base/(stem+".asm")).read_text()
lst=(base/"dist"/(stem+".lst")).read_text()
sym=(base/"dist"/(stem+".sym")).read_text()
rom=(base/"dist"/(stem+"_F6.bin")).read_bytes()
old=(base/"dist"/(stem+".4k.bin")).read_bytes()
expected="6c2585148eb082fb8bc794d664edc4869b18849fcfabb9cada23373d1dc1318b"
assert len(rom)==16384 and hashlib.sha256(rom).hexdigest()==expected
assert len(old)==4096
assert rom==old*4, "F9 image is not exact 4x repeated original F6 bank"
for address,bytes2,label in ((0xF1EE,b"\x85\x11","RESP1"),(0xF1F0,b"\x85\x1c","GRP1"),
                             (0xF1F6,b"\x85\x11","RESP1"),(0xF1F8,b"\x85\x1c","GRP1")):
    assert old[(address & 0xFFF):((address & 0xFFF)+2)]==bytes2,(hex(address),label)
    matches=[line for line in lst.splitlines() if re.search(r"\b"+f"{address:04x}"+r"\b",line)]
    assert any("STA" in line.upper() and label in line.upper() for line in matches), (hex(address),matches)
assert re.search(r"(?m)^X0_SELECT\s+00a0\b",sym)
assert re.search(r"(?m)^F9_000_Row00\s+f126\b",sym)
M=[int(x,2) for x in masks["large_male"]]
assert len(M)==9 and M==[60,60,24,255,24,36,36,66,66]
rows=[]
for y in range(9):
    label=f"F9_000_Row{y:02d}:"
    start=source.index(label)
    stop=source.find("\nF9_000_Row",start+len(label))
    if stop<0:stop=source.find("\nF9_001_Row",start+len(label))
    if stop<0:stop=source.find("\nF9AfterRows:",start+len(label))
    part=source[start:stop]
    vals=re.findall(r"\bLDA\s+#\$([0-9a-fA-F]{2})\b",part)
    assert len(vals)>=3,(label,vals)
    val=int(vals[2],16)
    assert val==M[y],(label,val,M[y])
    rows.append({"top_down_row":y,"original_m_mask_hex":f"{M[y]:02x}","source_label":label})
details={"original_frozen_rom_sha256":expected,"original_f9_bank_repetition":4,
         "source_mask_rows":rows,"source_SHA256":hashlib.sha256(source.encode()).hexdigest(),
         "lst_SHA256":hashlib.sha256(lst.encode()).hexdigest(),
         "sym_SHA256":hashlib.sha256(sym.encode()).hexdigest(),
         "actual_pre_STA_pc_hex":"f1ee","actual_pre_opcode_bytes":"85 11",
         "source_inferred_instruction_cycles":3}
(out/"F9_SOURCE_LIST_SYM_MASK_STATIC_CHECK.json").write_text(json.dumps(details,indent=2)+"\n")
print("G5AH_F9_PREBUILD_SOURCE_LIST_SYM_ROM_MASK_PASS",json.dumps(details))
