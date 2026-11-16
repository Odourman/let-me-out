# Let Me Out! MAIN IV – R1at: one 16 KB ROM, three runtime X layouts, six exact Android masks

**2026-11-16. Research-only LOCAL PASS, NOT integrated v0.18 R1 PASS or independent VERIFICATION.**

## Reproducible evidence

- [GitHub Actions 43868138075](https://github.com/Odourman/let-me-out/actions/runs/43868138075): full CI **SUCCESS** on code commit `124d3df324a35e71eeeeeb7ce62373e2093f2eca`.
- Full [artifact 14225019729](https://github.com/Odourman/let-me-out/actions/runs/43868138075/artifacts/14225019729) has 600 authentic consecutive Stella 6.7.1 X11 screenshots, complete assembler source, list/sym, ROM, Python generator, frame-level CSV and summary JSON.
- Exact experiment F6 16,384-byte NTSC ROM SHA256: `486dca4b574d9a394075788bc974232d3b7452282f282e46c7dd3fca454d2c0a`.
- The ROM combines three **previously each 600/600 pixel-PASS** original 8x9 six-Android masks kernel variants built from exact pinned parent ROM SHA:
  - A R1aq batch0 `09e262958e9452ec3f61c3d93f2eea19ad03cda7ac52767ae72608e2f7b3a94b` (P1 RESP1 cycles `28,40,56,66`).
  - B R1ar batch0 `55b5c8b0a85d657a23b00eacc3ce0738ce0defff725e3e630c96c5f0eb59852d` (cycles `28,42,56,66`).
  - C R1ar batch1 `b6d454e53769f1ad17c4441f4784c4f2a8936712e61faf500d51f666dae77080` (cycles `30,42,56,66`).

## Confirmed single-ROM runtime changes

One dispatcher **before the critical first `WSYNC`** uses `FRAMELO & $18`, selecting A, B, C, A in successive 8-frame slots. Three different cycle-perfect nine-row unrolled kernels remain unchanged while drawing.

| Layout | Actual 900x300 Stella-crop X positions of six original masks, left to right | Measured frames |
|---|---|---:|
| A baseline | `75;107;147;179;243;303` | 297 |
| B large female group +12 GUI pixels | `75;107;159;191;243;303` | 151 |
| C large male group +12 more GUI pixels | `87;119;159;191;243;303` | 152 |

- **600/600** source-exact, physically separate six full 8x9 original Android shapes: 2 large males, 2 large females, 1 small male, 1 small female on same nine scanlines. Every frame has zero missing/extra white pixels.
- **600/600** complete yellow original P0 player and exactly one M0 test bullet, 262 scanlines NTSC and valid consecutive debugger frame IDs. Precisely 3 genuine measured X signatures in one running ROM, each >100 frames.
- Initial CI attempt [43868023282](https://github.com/Odourman/let-me-out/actions/runs/43868023282) failed **only assembler short-branch range**; fixed by adding near jump trampolines before visible WSYNC. **No P1 timing or approved source mask changed.**

## Important limitations

1. These are **three predefined runtime layouts**, not general independent 160-color-clock movement and not six independently movable NPC. Each NUSIZ male/female pair has fixed copy spacing. Disallowed closer state `(30,40,56,66)` failed static feasibility because second male copy disappears.
2. A->B and B->C move a single large pair independently, but C->A in this baseline changes both large groups at once. A future test should use cycle A->B->C->B->A so only one group changes per transition.
3. No multi-Y staggering, crossing/overlap, PF wall, key/O1, orange door, active moving gameplay projectile, AI, sound, PAL, data bank switching between unique banks or full R1–R4 scene integration. M0 is a diagnostic stationary symbol, not confirmed in-hand shot.
4. Research may inform authorized ROM DEVELOPMENT v0.18; do not merge research, alter game canon, grant design waivers or self-issue independent Verification. `main` and draft PR #7 are unchanged.

## Next research

R1au: one-ROM A->B->C->B->A sequence that enforces exactly one large group changed per transition and passes 600 true Stella images with correct 3-layout phase map. Then assess whether a data-driven runtime X scheduler is possible under 76 cycles/scanline and how C04 staggered Y and PF overlap fit.
