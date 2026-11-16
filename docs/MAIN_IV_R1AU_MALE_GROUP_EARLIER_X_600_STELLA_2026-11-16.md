# LET ME OUT! – MAIN IV: male-group independent earlier X under six-source-exact same-Y P1 kernel (R1au)

**Date:** 2026-11-16. **Status:** LOCAL RESEARCH PARTIAL PASS (1/3 variants). Full R1 still BLOCKED. Independent VERIFICATION not performed.

## Key A/B experiment

Starting from the fully exact R1aq batch-0 six-NPC proof, research R1at male-only advanced first large-male `RESP1` to c26 while holding first `GRP1` and female `RESP1` unchanged. The first male original 8x9 mask lost **2 white pixels per frame** (600/600 frames). Advancing to c24 was worse (38 source-mask pixel errors per frame).

Research **R1au** instead advances the first P1 bitmap `GRP1` deadline *as well as* its early `RESP1`, while **female, small male and small female `RESP1` cycles remain identical** to the successful R1aq baseline. It does not change any original mask bytes, yellow P0 player code or M0 test shot.

[GitHub Actions run #43868835411](https://github.com/Odourman/let-me-out/actions/runs/43868835411): three isolated variants, each with 600 authentic consecutive Stella 6.7.1 X11 screenshots, per-frame strict source-mask audit and NTSC 262-line inspection.

| Variant | Male RESP1 | First male GRP1 advance | Female RESP1 | Six-mask strict 600-frame audit | ROM SHA256 |
|---:|---:|---:|---:|---|---|
| **0** | **c26** | **2 CPU cycles earlier** | **c40 unchanged** | **600/600 PASS; zero original white pixels missing or extra, P0 and M0 intact, 262 NTSC** | `80cec9aebe0c6a4754a48ac2e041e97253a9accb22dc493a866654e213362df0` |
| 1 | c24 | 2 CPU cycles earlier | c40 unchanged | FAIL: first large male incompletely drawn | `c3ea261789d56262c69ac754e84bcef3cc392d2f79f2854e67959469f789574f` |
| 2 | c24 | 4 CPU cycles earlier | c40 unchanged | FAIL: first large male incompletely drawn, additional ghost pixels | `73150230f48ee8581c71e9b529b4726ae828c38f0d02818b7043ca9b7bce49a6` |

**R1au variant 0 establishes another fixed, valid position of the duplicated male group, earlier than the R1aq baseline, with the female group still held at its original `RESP1` time.** It is a *new source-pixel-exact fixed X feasibility case*. This is not arbitrary independent per-Android X: the duplicated male pair remains at NUSIZ-defined fixed separation, and only three other NPC source-mask types are supplied.

Evidence: [variant 0 strict PASS](https://github.com/Odourman/let-me-out/actions/runs/43868835411/artifacts/14227435564), [variant 1 FAIL](https://github.com/Odourman/let-me-out/actions/runs/43868835411/artifacts/14226198881), [variant 2 FAIL](https://github.com/Odourman/let-me-out/actions/runs/43868835411/artifacts/14227335109).

## Combined group-level timing options

- D: male first `RESP1` c26, female c40: R1au variant 0 PASS (this research).
- A: male c28, female c40: R1aq batch 0 PASS 600.
- B: male c28, female c42: R1ar batch 0 PASS 600.
- C: male c30, female c42: R1ar batch 1 PASS 600.

**D → A → B → C** provides a monotone sequence where only one of the two duplicated large-Android groups needs to move at each step. The 3-state A/B/C runtime in [R1at separate runtime-three branch](https://github.com/Odourman/let-me-out/actions/runs/43868138075) already passes 600/600 in one ROM. **The D state has NOT yet been integrated into that runtime selector**, so do not describe D/A/B/C as one finished ROM.

## Design and authority

R1 requirement remains blocked by full playfield brown walls, different Y offsets, six fully independent arbitrary NPC X, real overlap/crossing stress, and independent verification. The static M0 test symbol is not a proved active hand-fired bullet. The 16KiB ROM is standard F6 four identical 4KiB banks; actual bank switching not yet exercised. Source research is isolated; `main` and draft PR #7 untouched.
