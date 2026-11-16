# R3/C02 – leveranspekare 2026-11-16

**ONLY authorized Atari 2600 v0.18 NTSC / R3**, isolated development result. Full R1–R4 v0.18 remains BLOCKED/NOT ACCEPTED; no independent VERIFICATION, no draft PR #7 merge, no gameplay or v0.19 map cutover.

- **GitHub branch:** `rom-dev/v018-r3-c02-20261116`. Original branch parent `82667dae033f70570dce903f8e1d4866528be02a`, separate from unmerged PR #7.
- **Real Stella CI, final source commit:** [GitHub Actions run 43904337337](https://github.com/Odourman/let-me-out/actions/runs/43904337337), code/head `98e8ca1ed4c5bb406627bcf093c62d6f95434372`. Result: success; real DASM, baseline reproduction, 10 full Stella screenshots, 600 debugger frame captures 11–610, seven actual TIA register-write traps at scanline134, negative logical passage tests.
- **Compiled actual ROM SHA256:** `991cea24f67accb2128743bba5722a87ee8cec08c00f6e39e4df1e07c3826e9c`. Exactly 16 384 bytes standard F6, four identical 4 KB banks.
- **Historical source ROM recompiled byte-identically:** `d31380be676752bd517c18d3c8bb64b30854d3d84175cf9c1163af76689f8620`.
- **Actual source map hash** `design/PLANERADE_RUMSKARTOR_V011.json`: `760d77bbb71bfdd0b3020d827ca7874abdcde4e399979289f75719572ee22d4a`. Exact C02 user-selected layout.
- **Full final evidence package** [LetMeOut_v018_R3_C02_DEVELOPER_HANDOFF_2026-11-16.zip on Google Drive](https://drive.google.com/file/d/1AXuFOA1yRm6KwVGVrz8VfkaIgO5_yqK8/view?usp=drivesdk), project parent folder ID `1HJwAJlT0TZpvR93g8MtmpCtg0iZVjw7u`, **3 420 134 bytes**, SHA256 `4b4c7325f0ea17b2f48c936164bbefae0ceac5bd6e32dfaad510b54558307113`; ZIP-integrity and 729/729 individual SHA256-manifest entries verified. Contains 600 raw debugger crops, 10 full-state screenshots, 7 full TIA trap screenshots, ROMs, ASM, DASM listings, build scripts, per-frame CSV, test matrix and analysis code.
- **Local R3 result:** D01/D02/D03 DEVELOPER_LOCAL_PASS, minimal passage allowed only after unlock at right (39,10); locked right and 3 invalid open requests denied. **600/600 frames** 262 scanline-HUD and source-matched closed left boundary. **7/7 TIA write traps** measured at a representative critical scanline 134 (PF0/1/2 left, PF0/1/2 right, GRP1). Worst-case code-derived 74/76 cycles, not a comprehensive measured all-scanline trace.
- **16 test cases:** 6 DEVELOPER_LOCAL_PASS, 2 INCONCLUSIVE (full-scene T01 and T07), 8 NOT_RUN. T15 independent verification not activated.
- **Report:** [TO_MAIN_R3.md](TO_MAIN_R3.md). [Detailed matrix](TEST_MATRIX_R3_DELTA.csv); [real TIA register cycle table](R3_REAL_TIA_REGISTER_TIMING.csv); [600 frame summary](R3_FRAMES_600_SUMMARY.json); [pixel audit](R3_PIXEL_AUDIT.json).

MAIN V decides acceptance of the limited developer result and next task. This branch does not merge or modify `main`, historical independent VERIFICATION baseline `561d3baf00c6c4c4bd9bc46599a91dc693abdeba`, or other projects.
