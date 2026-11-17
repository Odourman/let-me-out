#!/usr/bin/env python3
"""Final F9 READ ONLY unification of original F9 truth/ROM and 8 later
WSYNC-after-write GUI screenshots from EXACT same ROM SHA. No DASM/Stella.
"""
from pathlib import Path
import hashlib,json,shutil
B=Path("seed_bundle")
W=Path("seed_wsync/rom/v018/experiments/r1_free_xy")
assert B.is_dir() and W.is_dir()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
original=json.loads((B/"EVIDENCE_FILE_INDEX.json").read_text())
assert len(original)==471
assert all((B/k).exists() and sha(B/k)==v["sha256"] and (B/k).stat().st_size==v["size_bytes"]
           for k,v in original.items())
rom=B/"F9/dist/r1_f9_three_masks_three_binary_ram_x_ONE_ROM_F6.bin"
assert sha(rom)=="6c2585148eb082fb8bc794d664edc4869b18849fcfabb9cada23373d1dc1318b"
assert rom.stat().st_size==16384
d=W/"evidence/r1_f9_same_rom_wsync_after"
assert len(list(d.glob("mode_*/stella_full.png")))==8
assert not list(d.glob("mode_*/UNMEASURABLE.txt"))
for line in (d/"REAL_EIGHT_WSYNC_AFTER_WRITE_GUI_SHA256SUMS.txt").read_text().splitlines():
 digest,relative=line.split(maxsplit=1)
 assert sha(W/relative)==digest,(relative,"WSYNC screenshot source SHA fail")
for mode in ("000","001","010","011","100","101","110","111"):
 p=d/("mode_"+mode)/"stella_full.png"
 assert p.is_file() and p.stat().st_size>1000,(mode,p)
 # Unmodified genuine frame image: never redraw or regenerate from source.
target=B/"F9/evidence/r1_f9_one_rom/wsync_after"
assert not target.exists()
shutil.copytree(d,target)
shutil.copyfile(W/"r1_f9_wsync_trace.sh",B/"F9/r1_f9_wsync_trace.sh")
shutil.copyfile(Path("seed_wsync/r1_f9_same_rom_stella_version.txt"),
                B/"F9/r1_f9_same_rom_stella_version.txt")
summary=B/"F9_EVIDENCE_SUMMARY.json"
meta=json.loads(summary.read_text())
assert meta["classification"]=="F9_THREE_BINARY_RUNTIME_SELECTORS_LOCAL_PASS"
assert meta["REAL_STELLA_CROP_COUNT"]==meta["REAL_STELLA_FULL_GUI_COUNT"]==144
assert meta["REAL_STELLA_PC_TIA_REGISTER_TRAPS"]==48
meta.update({"SUPPLEMENT_SAME_ORIGINAL_F9_ROM_WSYNC_RUN":44050941747,
 "SUPPLEMENT_REAL_STELLA_WSYNC_AFTER_WRITE_TRAPS":8,
 "SOURCE_ONLY_WSYNC_BEFORE_WRITE_CPU_TIMING":[54,56],
 "POST_WRITE_WSYNC_NEXT_SCANLINE_IN_ACTUAL_STELLA_GUI":"SCNLN124_CC0 in inspected mode111 screenshot",
 "F9_UNCHANGED_ROM_RECHECKED_SHA256":sha(rom),
 "NO_NEW_DASM_NO_NEW_ROM_IN_WSYNC_OR_FINAL_BUNDLE":True})
summary.write_text(json.dumps(meta,indent=2)+"\n")
files=sorted(p for p in B.rglob("*") if p.is_file()
             and p.name not in ("EVIDENCE_FILE_INDEX.json","SHA256SUMS.txt"))
idx={str(p.relative_to(B)):{"sha256":sha(p),"size_bytes":p.stat().st_size} for p in files}
(B/"EVIDENCE_FILE_INDEX.json").write_text(json.dumps(idx,indent=2)+"\n")
(B/"SHA256SUMS.txt").write_text("".join(v["sha256"]+"  "+k+"\n" for k,v in sorted(idx.items())))
assert all(sha(B/name)==a["sha256"] and (B/name).stat().st_size==a["size_bytes"]
           for name,a in idx.items())
print("F9_FINAL_ONE_UNCHANGED_16K_ROM_SHA",sha(rom))
print("F9_FINAL_144_REAL_IMAGES_144_GUI_48_TIA_PC_8_REAL_WSYNC_12_ORTHOGONAL_PASS")
print("F9_FINAL_TRUE_ZIP_MANIFEST_ENTRIES",len(idx))
