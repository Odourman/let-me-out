# LET ME OUT! – MAIN IV R1aq: SIX original 8×9 Android instances on SAME nine rows, P0 player, M0 shot

**2026-11-16. Status: LOCAL_RESEARCH_PASS_R1AQ_SIX_STATIC_P1_1200_FRAMES.** Full v0.18 R1 still **BLOCKED** (no free independent NPC X; no complete integrated scene). NOT ROM DEVELOPMENT integration or independent VERIFICATION.

## Highest-confidence new result

- [GitHub Actions #43866445424](https://github.com/Odourman/let-me-out/actions/runs/43866445424), SUCCESS in **both** parallel 600-consecutive-Stella-6.7.1-X11-image tests, tested source commit `b5a326f07059ef01567fbb53ef74de8f052513ef`.
- In **every** one of the 1,200 genuine captured frames, an exact white source bitmap classifier finds precisely these SIX separately visible complete 8×9 mask instances on the SAME nine physical raster scanlines: `M, M, F, F, SM, SF` (large man ×2; large woman ×2; small man ×1; small woman ×1). No missing or extra white pixels, no ghost/partial group. The six sprites are only FOUR unique approved source bitmap shapes; two pairs are NUSIZ copies.
- The full original yellow P0 player and ONE two-pixel yellow M0 static shot remain visually complete in all 1,200 frames; every frame has the correct Stella frame-ID and NTSC 262 scanlines.
- **Independent source pin:** approved reference `design/NPC_REFERENCE_8x9_masks.json` Git blob `058800a4c1904d1ff289e7e61b3902aa111ba16d`; original working R1aj 4-mask ROM SHA256 `ff0f1c64ffff1915cef934f224b3f3d780bc2de6cc52038d62666904c1f0f263`. All source 8×9 mask data remain byte-for-byte unchanged.

| Batch | P1 RESP1 CPU-end cycles per line | Stella full 6-mask strict pass | 262 NTSC, intact P0, one M0 | White missing / extra | Full ROM SHA256 |
|---:|---|---:|---|---|---|
| 0 | `28,40,56,66` | **600/600** | 600/600 | **0 / 0** | `09e262958e9452ec3f61c3d93f2eea19ad03cda7ac52767ae72608e2f7b3a94b` |
| 1 | `28,40,54,64` | **600/600** | 600/600 | **0 / 0** | `eb91ddcf197c6f16dbea6e54a806b6b41f6c5d642eab74baa22fa6e9de9e4461` |

Both proof ROMs are **16,384-byte NTSC standard F6 cartridge files** with four copies of one 4KiB source image. The test does NOT establish bank switching between different banks.

## The working raster mechanism (why R1aq succeeds after earlier failures)

1. `NUSIZ1=$03` provides THREE close/medium copy opportunities on one P1 position counter. Controlled repeated `RESP1` resets at four precisely timed points show more than the two physically independent TIA players could normally display.
2. The display kernel unrolls all NINE physical scanlines, with immediate precomputed `LDX #bitmap` / `LDA #bitmap` source values for each original row. There is NO 9-row loop branch overhead. Source masks remain intact in the ROM for comparison.
3. It clears stale P1 at the start of each line during blanking with `STX GRP1`, then preloads the four canonical original masks (M,F,SM,SF). A single shared P1 automatically generates second copies of the first two large masks. The two smaller masks are separately written.
4. The yellow P0 player is pre-positioned independently (the VBLANK `PlayerDelay` adjusted from 9 to 5 in this isolated experiment), away from both large F copies, avoiding the partial P1 occlusion observed in previous variants. Note that the static M0 test shot is not guaranteed to remain visually attached to the player's hand after P0 moves.
5. The two confirmed last P1 timing windows `54/64` and `56/66` show the result is not tied to a single exact X pair; they are NOT a free-X positional API.
6. The Stella audit classifies **every white cluster** by entire nine-row pixel geometry and rejects any noncanonical extra cluster. It separately demands original player + one M0 and correct NTSC HUD/IDs. This is a local research self-test, not organizational independent VERIFICATION.

## Earlier failures are preserved, not overwritten

- [R1ak run #43864335638](https://github.com/Odourman/let-me-out/actions/runs/43864335638): six NUSIZ modes from unchanged R1aj fail exact six, although `$03` sometimes creates five or six other complete mask combinations.
- [R1al #43864735163](https://github.com/Odourman/let-me-out/actions/runs/43864735163): reset `28/40/52/62`, lost/extra P1 and edge ghosts, strict full six FAIL.
- [R1am #43865151103](https://github.com/Odourman/let-me-out/actions/runs/43865151103): 3-cycle late `GRP1` clear broke 262 scanlines/shot, FAIL.
- [R1an #43865371281](https://github.com/Odourman/let-me-out/actions/runs/43865371281): `28/40/54/64` in old loop, failed due unaddressed P0 overlap/timing, not contradicting R1aq.
- [R1ao #43865530760](https://github.com/Odourman/let-me-out/actions/runs/43865530760): unrolling loop without precomputed immediate bytes and P0 separation did not preserve all six.
- [R1ap #43866037253](https://github.com/Odourman/let-me-out/actions/runs/43866037253): five required full masks `M M F F SM` were 600/600 exact, but the rightmost SF was not. R1aq shifts only late SM/SF timing and obtains six exact original instances.

## Critical limitations: R1 is STILL blocked

- Six **static**, specially spaced copies are now feasible. BUT duplicate M/M and F/F relative spacing comes from NUSIZ geometry: copies cannot be positioned independently. Only four different original mask tables exist; six simultaneously visible instances is not six freely steerable NPC.
- No independent walking/chasing X changes across 160 color clocks, crossing/overlap while preserving correct per-NPC identity, full game Y movement, flicker limit under stress, integration with brown PF wall/right orange door, gold key/O1 occlusion, real movement/shooting collisions, or R2/R3/R4 gates. The M0 test shot remains static and not necessarily in-hand.
- Nine physical rows here, so no silent 14-row waiver. No new mapper, PAL implementation, canon change, cutover, production merge or self-issued independent VERIFICATION.
- Production `main` independently checked SHA `f6b3fc76c59161e04e583dc8c0787332d2f261c7`; draft PR #7 head still `82667dae033f70570dce903f8e1d4866528be02a`, unmerged.

## Reproducible evidence/downloads

- [R1aq batch 0 PASS, ROM, source, DASM, 600 Stella screenshot PNGs, pixel CSV, SHA](https://github.com/Odourman/let-me-out/actions/runs/43866445424/artifacts/14225747192)
- [R1aq batch 1 PASS, ROM, source, DASM, 600 Stella screenshot PNGs, pixel CSV, SHA](https://github.com/Odourman/let-me-out/actions/runs/43866445424/artifacts/14225557646)
- Research source: `rom/v018/experiments/main_iv_r1aq_timing/` in `research/main-iv-r1aq-last-two-masks-20261116`.

## Proposed NEXT research gate (not implementation)

R1ar: find exact cycle-preserving variants that move the first M/F groups separately while retaining all six exact bitmaps; maintain no-ghost, 262-line, P0 and M0 invariants across 600 real Stella frames per mode. Then map the NUSIZ fixed-copy geometry and determine whether six NPC can actually have enough individual movement freedom. If not, evaluate scoped alternatives, not an assumed design waiver.
