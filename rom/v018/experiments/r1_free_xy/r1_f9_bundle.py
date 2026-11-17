#!/usr/bin/env python3
"""F9 READ ONLY archive of original ONE ROM and its already captured Stella.
No assembler, emulator, ROM rewriting, or synthetic positive PNG generation.
"""
from pathlib import Path
import hashlib,json,shutil
B=Path("bundle");B.mkdir(exist_ok=True)
A=Path("seed_g1/rom/v018/experiments/r1_free_xy")
F7=Path("seed_f7")
assert A.is_dir() and F7.is_dir(),"original prior artifacts must already exist"
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
stem="r1_f9_three_masks_three_binary_ram_x_ONE_ROM"
rom=A/"dist"/(stem+"_F6.bin")
data=rom.read_bytes()
assert len(data)==16384 and all(data[i*4096:(i+1)*4096]==data[:4096] for i in range(4))
meta=json.loads((A/"dist"/(stem+".json")).read_text())
assert meta["ROM_SHA256"]==sha(rom) and meta["ROM_bytes"]==16384
single=sorted((A/"dist").glob("r1_f9_*_F6.bin"))
assert len(single)==1 and single[0]==rom,("MORE_THAN_ONE_F9_ROM",single)
g=json.loads((A/"r1_f9_g0_source_only.json").read_text())
assert g["G0"]=="F9_G0_SOURCE_ONLY_FEASIBLE_EIGHT_STATES_NO_ROM"
assert g["F9_eight_nine_row_kernel_source_bytes"]==2670
assert len(g["all_72_rows_SOURCE_ONLY"])==8 and all(len(v["rows"])==9 for v in g["all_72_rows_SOURCE_ONLY"].values())
ev=A/"evidence/r1_f9_one_rom"
raw=list((ev/"raw").glob("frame_*.png"))
full=list((ev/"raw_full").glob("frame_*.png"))
traps=list((ev/"traps").glob("mode_*/*/stella_full.png"))
assert len(raw)==144 and len(full)==144 and len(traps)==48,(len(raw),len(full),len(traps))
assert not list((ev/"traps").glob("mode_*/*/UNMEASURABLE.txt"))
audit=json.loads((ev/"TRUE_144_ALL_THREE_MASK_8_STATE_12_CONTRAST_AUDIT.json").read_text())
assert audit["classification"]=="F9_THREE_BINARY_RUNTIME_SELECTORS_LOCAL_PASS"
assert audit["real_frame_count_actually_analyzed"]==144
assert audit["all_source_oriented_mask_and_other_controls_exact"]
assert audit["all_eight_preregistered_X_exact"] and audit["twelve_of_twelve_pass"]
assert len(audit["all_twelve_independent_X_orthogonality_contrasts"])==12
assert all(x["pass"] for x in audit["all_twelve_independent_X_orthogonality_contrasts"].values())
assert audit["synthetic_negative_not_real"]["both_independent_oracles_rejected"]
assert len(audit["rows_real_png"])==144
for row in audit["rows_real_png"]:
 p=ev/"raw"/row["real_png"]
 assert p.is_file() and sha(p)==row["unmodified_REAL_Stella_image_SHA256"]
 assert row["strict"] and row["prediction_exact"]
for mode in ("000","001","010","011","100","101","110","111"):
 assert len(list((ev/"traps"/("mode_"+mode)).glob("*/stella_full.png")))==6
for name in ("TRUE_144_CROP_SHA256SUMS.txt","TRUE_144_FULL_SHA256SUMS.txt"):
 for line in (ev/name).read_text().splitlines():
  digest,relative=line.split(maxsplit=1)
  p=A/relative
  assert p.is_file() and sha(p)==digest,(name,relative)
# Copy exactly the historical genuine ROM and original evidence, no transformations.
shutil.copytree(A,B/"F9",dirs_exist_ok=True)
for name in ("r1_f7_2x2_independent_RAM_X_ONE_ROM.asm",
  "dist/r1_f7_2x2_independent_RAM_X_ONE_ROM.lst",
  "dist/r1_f7_2x2_independent_RAM_X_ONE_ROM.sym"):
 src=F7/name
 d=B/"F7_PARENT_FROZEN"/name;d.parent.mkdir(parents=True,exist_ok=True)
 shutil.copyfile(src,d)
pins={"r1_f7_2x2_independent_RAM_X_ONE_ROM.asm":"2ea6ccbc765bb0472c662bc562c864299e8988dc433c945cf35dae999c79983c",
 "dist/r1_f7_2x2_independent_RAM_X_ONE_ROM.lst":"5b18b0f5a808b1c38e9b587542dae1b25132a0e92d4f1cd7273156b1b40bf481",
 "dist/r1_f7_2x2_independent_RAM_X_ONE_ROM.sym":"158e8b7a69a15b2ddf4b60c727d4c8c6d41f51ce8103303cfe6ef71c3c383b83"}
for name,digest in pins.items():assert sha(B/"F7_PARENT_FROZEN"/name)==digest
metadata={"classification":"F9_THREE_BINARY_RUNTIME_SELECTORS_LOCAL_PASS",
 "SCOPE":"DEVELOPER_LOCAL_DIAGNOSTIC_ONLY_NOT_FULL_R1",
 "F9_ONE_NEW_EXECUTABLE_ROM_SHA256":sha(rom),"F9_ROM_BYTES":len(data),
 "F9_F6_BROKEN_INTO_FOUR_IDENTICAL_4096_BYTE_BANKS":True,
 "G0_RUN_44049671587_SOURCE_ONLY_GREEN":True,
 "G1_RUN_44050126727_ONE_ACTUAL_DASM_ROM_AND_STELLA":True,
 "F7_OLD_VERIFIED_ARCHIVE_RUN":43968481385,
 "REAL_STELLA_CROP_COUNT":144,"REAL_STELLA_FULL_GUI_COUNT":144,
 "REAL_STELLA_PC_TIA_REGISTER_TRAPS":48,"synthetic_negative_not_real":True,
 "ALL_8_RAM_STATES":["000","001","011","010","110","111","101","100"],
 "TWELVE_ORTHOGONALITY_CONTRASTS_PASS":12,
 "preregistered_X_model_NOT_POSTFIT":{m:v["preregistered_cropped_X"] for m,v in g["all_72_rows_SOURCE_ONLY"].items()},
 "actual_measured_X":audit["actual_per_mode"],
 "old_F7_original_primary_files_SHA256":pins,
 "NO_NEW_ROM_OR_STELLA_IN_THIS_READ_ONLY_BUNDLE":True,
 "ARBITRARY_THREE_X_NOT_PROVEN":True,"SIX_FREE_XY_NOT_PROVEN":True,
 "FULL_R1_BLOCKED_NOT_ACCEPTED":True}
(B/"F9_EVIDENCE_SUMMARY.json").write_text(json.dumps(metadata,indent=2)+"\n")
files=sorted(p for p in B.rglob("*") if p.is_file() and p.name not in ("EVIDENCE_FILE_INDEX.json","SHA256SUMS.txt"))
index={str(p.relative_to(B)):{"sha256":sha(p),"size_bytes":p.stat().st_size} for p in files}
(B/"EVIDENCE_FILE_INDEX.json").write_text(json.dumps(index,indent=2)+"\n")
(B/"SHA256SUMS.txt").write_text("".join(v["sha256"]+"  "+n+"\n" for n,v in sorted(index.items())))
assert all(sha(B/name)==v["sha256"] and (B/name).stat().st_size==v["size_bytes"] for name,v in index.items())
print("F9_READ_ONLY_EVIDENCE_SOURCE_ORIGINAL_ROM_144_GENUINE_IMAGES_144_FULL_GUI_48_TRAPS_12_X_CONTRASTS")
print("F9_ONE_F6_ROM_SHA256",sha(rom))
print("F9_INDEXED_HASH_COUNT",len(index))
