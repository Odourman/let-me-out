# Let Me Out! - ROM DEVELOPMENT v0.18: sprite feasibility delta, 2026-11-15

## Scope and provenance

This is **only an internal technical investigation inside authorized v0.18 NTSC R1-R4**, not a new release, not full R1 or a complete game. MAIN authority in `docs/MAIN_SPRITE_FEASIBILITY_V018_2026-11-15.md`, `docs/MAIN_RASTER_DELTA_V018_2026-11-15.md` and `docs/MAIN_PLAYER_SCALE_V018_2026-11-15.md` (all from `main`) plus Issue #6. Frozen independent verification baseline: `561d3baf00c6c4c4bd9bc46599a91dc693abdeba`. Parent baseline ROM SHA256: `d31380be676752bd517c18d3c8bb64b30854d3d84175cf9c1163af76689f8620`. Original R1-R4 ROM bytes are **not changed** in this delta. New work only in `rom/v018/experiments/two_silhouettes` and CI.

## Implemented and tested in genuine tools

DASM `2.20.15~20201109+really2.20.14.1-2` (upstream practical version 2.20.14.1) assembled **three independent real 6502 source files**, each to a 4,096-byte bank repeated four times to create a valid 16,384-byte F6-cartridge. The repetition is a packaging convenience; it neither multiplies TIA sprites nor claims four complete scenes. SHA256 files in `dist/SHA256SUMS.txt` are reproducible.

Stella **6.7.1** ran on Ubuntu 24.04 + Xvfb in [GitHub Actions 43752235843](https://github.com/Odourman/let-me-out/actions/runs/43752235843). Raw full debugger screenshots, DASM listings/symbols and script inputs are present in this archive. There are two test positions for each candidate; they are emulated, not schematic. The debugger scripts executed correctly and `proof.lst` / `proof.sym` loaded; Stella still emitted a benign missing optional `~/proof.script` and `.cfg` warning. Frame 20 and 100 were actually observed with prior frame scanline count 262.

### Candidate A1: naïve P1 reset/retrigger on a scanline

- Source: `src/proof.asm`.
- TIA: P0 yellow 8x9 *candidate* player; P1 white male/female with two mid-scanline RESP1 strobes; M0 yellow test projectile; PF off.
- **FAIL:** both white androids absent in real Stella screenshot despite player and shot. Does NOT prove independent-position sprite multiplexing impossible in general, only that this instruction schedule fails.
- SHA256 of 16KB experiment `.bin`: `ff721cfeb2a425845f9be0e558c56a69bdf1cfdc42879d5fe1caeff14e312990`.

### Candidate A2: P1 NUSIZ 2-copy with mid-scanline bitmap update

- Source: `src/proof_nusiz.asm`.
- TIA: P0 yellow player, P1 white original two large NPC silhouettes, M0 test shot. NUSIZ1=2 or 4 gives **32/64 color-clock fixed X-offset**. First copy displays `MaleRows`, second `FemaleRows`, original 8x9 mask data preserved exactly. Both share nine vertical lines. PF unused.
- **Local technical PASS for two fixed-spacing distinct silhouettes:** both original masks were identified pixel-by-pixel in the raw Stella screenshots in BOTH modes. All four matrices (two characters x two modes) match **exactly all 72 pixels**; see `analysis/original_8x9_mask_comparison.json` and full raw screenshots.
- Yellow player is an *unapproved* developer mask candidate (9 rows, roughly equal height, hat/gun intent), not final pixel-art approval. Shot is a diagnostic missile, not validated gameplay projectile.
- **Not an independent X position solution and NOT R1 PASS.** NUSIZ copies have fixed spacing; this does not establish six simultaneous freely placed hazards or R2 key interaction.
- SHA256 of 16KB experiment: `a945ab5a0b91df9c6583d46aeebc717a3b5b13232b3fa606fc15412727b26fe5`.

### Candidate A3: P1 later, more visible interval retrigger

- Source: `src/proof_retrigger_visible.asm`.
- TIA: P0 player, P1 two mid-line RESP1 resets at later CPU-cycle positions, M0 shot; different second delay values.
- **FAIL:** both white androids missing in Stella near/far test screenshots. Distinct implementation from A1, same hardware limitation unresolved.
- SHA256 of 16KB experiment: `1a636e7aa8815e57e605e03327bf5bb59edda5667c1f8c7849babb306d8ec301`.

## CPU cycles and TIA schedule: exact source-derived, not measured write trace

For A2 `SpriteLine` after the `STA WSYNC` reset:

| Step | Near (CPU cycle) | Far (CPU cycle) | TIA target |
|---|---:|---:|---|
| `LDA MaleRows,Y / STA GRP1` | 7 | 7 | GRP1 first P1 copy white male |
| `LDA PlayerRows,Y / STA GRP0` | 14 | 14 | GRP0 yellow full-height player |
| `LDX DELAY` and 4/6 `DEX/BNE` iterations | ends 36 | ends 46 | no TIA write |
| `LDA FemaleRows,Y / STA GRP1` | 43 | 53 | GRP1 second P1 copy white female |
| `LDA ShotRows,Y / STA ENAM0` | 50 | 60 | ENAM0 missile enable |
| `DEY / BPL` taken | 55 | 65 | loop housekeeping |
| Next `STA WSYNC` | 58 | 68 | finishes scanline, 76-cycle maximum |

The 76-cycles constraint is met by the **statically calculated** loop instruction counts (without page-crossing because masks located on one page). This is **not** a measured per-register Stella TIA-write trace; B02 remains unproven. P0 x approx middle screen, P1 near left, M0 right. The real rendered bitmaps and prior-frame 262-line counter support functional timings at sampled frames. `GRP1` second write affects second NUSIZ copy before beam reaches it. No NES hardware or external code is used.

## Actual 600-frame observation and remaining instrumentation gap

`src/stella_trace_600.sh` generated 600 `frame #1` commands, **each followed by** `print _fCount` and `print _scanEnd`; Stella reported `Executed 1805 commands` from `autoexec.script` (three per frame plus bootstrap/final commands). A raw screenshot shows **Frame 610, prior frame scanlines 262**. The attempted `saveSes` emitted a **zero-byte session file**, so values for the other 599 frames have **not been captured and inspected as continuous evidence**. Thus 600 successive emulator frame advances happened but **600-per-frame NTSC stability is INCONCLUSIVE**. This evidence is for A2 only, not full R1/R2/R4. See `evidence/stella_600/after_600_frames.png`.

Stella's [`saveSes` documentation](https://stella-emu.github.io/docs/debugger.html) describes dumping the prompt session but does not guarantee autoexec's command output is retained, which was not the case here.

## Scale-up constraints (no unauthorized compromises)

- The Atari 2600 TIA has only P0/P1 player bitmaps, M0/M1 and BALL 1-bit primitives and a coarse PF with four color-clocks per bit. A 16KB F6 cartridge expands **ROM, not sprite count or per-scanline CPU cycles**.
- P0 is provisionally occupied by equally tall yellow player and M0 by shot. P1 NUSIZ can clone up to three *fixed-spaced* copies of the same sprite; updating GRP1 can make a second copy show a different 8x9 silhouette as proven. But 6 independently positioned NPCs plus player and shot at identical Y still **not proven**. In R2 P1 also needs a key unless a separate viable hybrid plan is established.
- Neither A1 nor A3 succeeded for freely delayed second positions. No arbitrary placement or scalable 6-NPC kernel is demonstrated. Alternative B (reworked PF/TIA kernel) would also face PF bit pitch and cycle limits. No reduction of six androids, replacement of original NPC masks, hidden flicker, or design-waiver has been applied.

## Status relative to 16 acceptance tests

**New isolated feasibility tests:** A1 FAIL, A2 PARTIAL technical success at fixed spacing, A3 FAIL, 600-frame per-frame log INCONCLUSIVE. No new complete R1–R4 test matrix has been passed. The frozen baseline's **5 PASS / 5 FAIL / 5 INCONCLUSIVE / 1 NOT_RUN** remains **historical**; the new experiment MUST NOT inherit them as a new ROM's PASS status. Full R1 graphics remains **BLOCKED**, R2/R3/R4 retained as previously diagnosed in the baseline, with independent VERIFICATION Issue #8 strictly separate. The two-NPC proof is not R1 PASS. A new verification round will be necessary for any future revised ROM.

## Delivery pointers

- Source/build: `rom/v018/experiments/two_silhouettes/` in draft PR #7.
- CI run: https://github.com/Odourman/let-me-out/actions/runs/43752235843
- Current branch: `rom-dev/v018-ntsc-diagnostic`. Frozen baseline untouched and PR **draft**.
- All bundled local file SHA-256 values: `SHA256_MANIFEST.txt` at ZIP root. Exact current commit can be read from GitHub; this report is a delta against original baseline `561d3baf...`.

**Developer conclusion to MAIN:** we have real visual proof that the *unmodified* approved male/female masks can coexist on the same raster band, with yellow full-height player and shot, **under fixed NUSIZ copy spacing**. We DO NOT have a reliable technique for six distinct, freely placed white androids + player + shot on exactly the same raster height. R1 remains unsatisfied. Stop before full gameplay or design compromises; MAIN must decide whether a further within-scope PF/TIA investigation is worthwhile. Independent VERIFICATION is not performed.
