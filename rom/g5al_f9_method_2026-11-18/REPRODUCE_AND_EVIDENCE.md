# G5AL LM-D25 — reproducibility and readback

The only real measurement is the GitHub Actions workflow `.github/workflows/g5al_f9_stable_bank_neutral.yml` on the dedicated specialist branch. **Never rerun historical G5AF/G5AH/G5AJ**, and never invoke more than two new G5AL measurement runs. The workflow downloads original artifacts; no DASM/compiler or new ROM is used.

Original frozen F9: Actions run `44050126727`, artifact `LET_ME_OUT_R1_F9_ONE_ROM_AND_ACTUAL_STELLA_PARTIAL_OR_COMPLETE_G1`, ROM `r1_f9_three_masks_three_binary_ram_x_ONE_ROM_F6.bin` 16384 bytes SHA256 `6c2585148eb082fb8bc794d664edc4869b18849fcfabb9cada23373d1dc1318b`, four identical banks. Frozen G5AF reference: Actions run `44178247577`, artifact `G5AF_F9_ORIGINAL_READONLY_NATIVE_TIA_AND_DEBUGGER_EVIDENCE`, file `F9_000_M_RESP1/native_TIA_original.png` native 320x228.

Run calls `bash run_g5al_f9.sh` from `rom/g5al_f9_method_2026-11-18`. Python `check_f9_frozen.py` asserts historical source/list/sym/original 8x9 M and all F6 banks. `audit_g5al.py` validates native actual `saveSes` prompt text (actual `#decimal` response, not register-address hexadecimal) and compares the actual A PNG pixel for pixel against historical G5AF. All gate failures stop later stages. A has a bank-neutral 0–3 criterion **for this separate NEW G5AL only**.

A and B each use their own new HOME and Stella process; first autoexec contains only `base #10`. `frame`, `trapWriteIf`, `break` and `run` are typed only after verified live command/session responses. B uses exactly four bank-specific one-time `set`-confirmed breakpoints. One `step` occurs only after B's new pre-STA stop.

The teardown stops and waits for Stella/Xvfb before recomputing frozen ROM SHA256, building `G5AL_AUDIT.json`, `G5AL_EVIDENCE.csv`, `G5AL_PRE_ARCHIVE_VERDICT.txt`, and final `SHA256SUMS.txt`. The capture always uploads original evidence, even on FAIL. The separate same-run archive-readback job independently downloads the exact original artifact and runs `sha256sum -c SHA256SUMS.txt`.

Do not infer C0/RESP0, numeric START/CC, H4, G6, five-NPC, G5 PASS, original-hardware success or independent Verification II from these data. `G5_FORMAL_OPEN`.
