# LET ME OUT! – MAIN IV: three runtime-switching six-original-Android layouts (R1at)

**Research evidence 2026-11-16. LOCAL RESEARCH PASS. NOT complete R1 or independent VERIFICATION.**

## Exact observed result

[GitHub Actions run #43868138075](https://github.com/Odourman/let-me-out/actions/runs/43868138075) = **SUCCESS**, with **600/600 consecutive authentic Stella 6.7.1 screenshots** showing exactly six original canonical nine-row white android masks on the same raster Y:

- 2 large males (M), 2 large females (F), 1 small male (SM), 1 small female (SF), source-exact full 8×9 pixel masks.
- Original full yellow player P0 and exactly one static yellow M0 test projectile in all frames.
- Every frame NTSC 262 scanlines; **zero missing or extra white source-mask pixels**.
- **ONE runtime-changing standard 16,384-byte F6/NTSC ROM**, actual SHA256 `486dca4b574d9a394075788bc974232d3b7452282f282e46c7dd3fca454d2c0a`.
- **Three distinct six-Android scene layouts** confirmed in 600 actual framebuffer screenshots; the `FRAMELO & $18` runtime selector changes kernels before entering the nine-scanline critical section.

| Runtime layout | Observed full mask X values in 900px Stella GUI crop, M;M;F;F;SM;SF | Frames |
|---|---|---:|
| A | `75;107;147;179;243;303` | 297 |
| B | `75;107;159;191;243;303` | 151 |
| C | `87;119;159;191;243;303` | 152 |
| Total | Three source-exact six-instance layouts, all with one original P0 player & M0 test shot | **600** |

**Technical consequence:** From A to B the doubled female group moves, while both male copies remain at their same positions. From B to C the doubled male group moves, while both female copies remain at their same positions. Both small original silhouettes remain fixed.

This proves **separable, limited group-level X motion under runtime conditions**; unlike multiple static proof ROMs, all three layouts are in one executable. It does **not** prove that the six NPC individuals can each move to any 160-CC X, swap relative order, overlap/cross or move along Y. NUSIZ duplicates still share a fixed separation within each large-male/large-female pair.

## Reproduction and traceability

- Test code path: `rom/v018/experiments/main_iv_r1at_runtime_three/` on this isolated branch.
- Three source-pinned assembler kernel inputs:
  - A: R1aq batch 0, SHA256 `09e262958e9452ec3f61c3d93f2eea19ad03cda7ac52767ae72608e2f7b3a94b`, reset cycles 28/40/56/66.
  - B: R1ar batch 0, SHA256 `55b5c8b0a85d657a23b00eacc3ce0738ce0defff725e3e630c96c5f0eb59852d`, cycles 28/42/56/66.
  - C: R1ar batch 1, SHA256 `b6d454e53769f1ad17c4441f4784c4f2a8936712e61faf500d51f666dae77080`, cycles 30/42/56/66.
- [Full raw artifact](https://github.com/Odourman/let-me-out/actions/runs/43868138075/artifacts/14225019729): executable ROM, source, DASM listing/symbols, raw 600 PNG, per-frame audit CSV and JSON.
- The **previous run #43868023282 FAIL** was preliminary research, not the final successful proof.

## Scope and acceptance warning

R1 in the authorized v0.18 diagnostic also requires brown PF walls and representative same-Y worst-case positioning; R2 requires gold key and O1, R3 right-hand orange door with black keyhole, R4 movement/overlay stress. This proof does **not** contain these. The shot is a static visible M0 symbol, not a verified real shooting mechanic. The 16KB F6 file currently consists of four copies of one 4KB bank, so **actual F6 bank switching has not been exercised**.

The independent six-X constraint remains unresolved. A distinct experiment also called "R1at" on branch `research/main-iv-r1at-male-independent-x-20261116` tested moving ONLY male earlier while holding female fixed and failed source-perfect pixel checks. Do not conflate that failure with the successful *runtime-three* R1at branch. Follow-up `R1au` explores advancing the GRP1 deadline and must be judged separately.

**Decision:** retain R1 = BLOCKED pending integrated R1 scene, independent VERIFICATION and explicit project authority. No merge to `main`, no production PR #7 modifications, no game rules change, no PAL/map cutover.
