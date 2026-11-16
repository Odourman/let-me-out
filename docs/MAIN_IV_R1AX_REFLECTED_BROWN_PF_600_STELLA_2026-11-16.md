# LET ME OUT! – MAIN IV R1ax: brown reflected PF sidewalls with six source-exact original NPCs

**Date:** 2026-11-16. **Scope:** strictly isolated v0.18 R1/R4 research; not full R1, not asymmetric door R3, not independent VERIFICATION.

## Definitive evidence, after correcting the pixel *auditor* (not ROM code)

[GitHub Actions run 43883269341](https://github.com/Odourman/let-me-out/actions/runs/43883269341), commit `7e66b2ac721eec009a39753adbee267c80cd3c37`.

The tester was initially invalid because it counted dark brown PF pixels as yellow player/projectile pixels, leading to false shot failures. The new `analyze_600.py` excludes pixels matching the separately audited brown PF color from the yellow P0/M0 set. **All three ROM executables are identical before and after that auditor-only repair**.

| Mode | `PF0` | `CTRLPF` | All six source masks | Full P0+M0 | Both brown sidewalls | NTSC 262 | Outcome |
|---|---|---|---:|---:|---:|---:|---|
| **0 – reflected brown PF** | `$F0` | `$01` | **600/600** | **600/600** | **600/600** | **600/600** | **LOCAL PASS** |
| 1 – PF disabled, negative control | `$00` | `$01` | **600/600** | **600/600** | **0/600** | **600/600** | Intended wall **FAIL** |
| 2 – nonreflected, negative control | `$F0` | `$00` | **600/600** | **600/600** | **0/600** | **600/600** | Intended wall **FAIL** |

Every tested frame retained all four source-distinct types in the required counts: 2 large men, 2 large women, small man, small woman. **Zero missing and zero extra white mask pixels**. The three moving-X screen-crop signatures from R1at were retained in the single positive ROM:

- `75;107;147;179;243;303` – 297 frames.
- `75;107;159;191;243;303` – 151 frames.
- `87;119;159;191;243;303` – 152 frames.

**Mode 0 ROM:** 16,384-byte standard F6 with 4 identical 4KiB banks. SHA256: `64ba6cd5152a395737b2c41607b0a9e54c7836319bbed2bfee9bfdc6af1f81d1`.

Evidence:
- [Mode 0 complete 600 real Stella images, ROM, listing/symbols, JSON/CSV](https://github.com/Odourman/let-me-out/actions/runs/43883269341/artifacts/14233223745)
- [Mode 1 no-PF control artifact](https://github.com/Odourman/let-me-out/actions/runs/43883269341/artifacts/14233672066)
- [Mode 2 nonreflected control artifact](https://github.com/Odourman/let-me-out/actions/runs/43883269341/artifacts/14233726672)

**CI note:** Overall Actions run is marked `failure` because both deliberately negative wall-control jobs terminate with nonzero status; the mode-0 positive job itself concludes `success`. This is *not* a three-mode passing test or full R1 PASS.

## What it does and does not prove

A mirrored brown PF0 side band can coexist with six pixel-perfect P1 originals, full yellow P0 player and one static yellow M0 test shot at same Y, for 600 Stella frames with three constrained runtime-X layouts. The PF init was installed once outside the critical nine-raster-row kernel, so no extra per-line P1 code was added.

**Not yet demonstrated:** per-NPC independent free X, combined runtime X and Y, C04 staggered Y with walls in the *same ROM*, full R2 with gold key/O1, asymmetrical locked/open right door with black keyhole (D01-D03), independent cycle-write trace T07, independent VERIFICATION and full R1-R4 acceptance. In particular, `CTRLPF=$01` explicitly mirrors PF; it cannot itself satisfy a right-only door opening.

MAIN IV next research proof: [R1ba integrated X/Y/PF](https://github.com/Odourman/let-me-out/tree/research/main-iv-r1ba-integrated-xyz-pf-20261116) only inside authorized NTSC R1/R4 diagnostic scope.

No production changes, no draft PR #7 merge, no new game rules, no PAL or mapper expansion.
