# Let Me Out! MAIN IV R1ah – third different canonical 8x9 P1 NPC on same Y

**2026-11-16. PARTIAL research result: 2/4 STRICT Stella jobs PASS; full R1 remains BLOCKED.**

## Provenance

- [Run 43862062578](https://github.com/Odourman/let-me-out/actions/runs/43862062578), tested commit `99c58ffe3b777ba8648b0f84a2fd8548521a2e11`, four parallel real Stella 6.7.1 jobs.
- Experimental base: exact R1ag original-male/original-female close-X ROM SHA256 `4188d0c22a2c9b908de37af1f257e8a4c25799038c938976323204cedd46dbcd`.
- Third bitmap: exact approved `design/NPC_REFERENCE_8x9_masks.json` small_male from main, Git blob `058800a4c1904d1ff289e7e61b3902aa111ba16d` copied unchanged to research branch (no main edit). Top-down bytes: 00,00,3C,3C,18,7E,18,24,00.
- All four ROMs: 16,384 B standard F6/NTSC, with player P0 and a single static shot M0 maintained. Every job captures 600 consecutive real Stella GUI frames; independent organizational VERIFICATION NOT performed.

## Exact outcomes

| Job | Third P1 RESP1 gap after second | Frame PASS | White missing pixels | Ghost pixels | ROM SHA256 |
|---:|---:|---:|---:|---:|---|
| 0 | 18 CPU cycles (+first-X offset) | **150/600 FAIL** | 5,700 | 0 | `c2a5b53a5573107ed3c96aa355d88c1183a3f1ce5a90b358e373eb794d0d744a` |
| 1 | 14 CPU cycles (+first-X offset) | **600/600 PASS** | 0 | 0 | `d23f6ff594046fe1ecac4b0dfce154e50d43f9323483622e4c31c68489262a19` |
| 2 | 10 CPU cycles (+first-X offset) | **600/600 PASS** | 0 | 0 | `6915711bb5d44a8603b3857853f7c688a49f32fb4b1f5ba9ccc0461868ce6a2f` |
| 3 | 20 CPU cycles (+first-X offset) | **150/600 FAIL** | 4,200 | 0 | `3d15b41f73e51359f0f0e4c915c188beb3be8115ee25309a55f3e7ac8abdcad0` |

## What we learned

Two valid isolated ROM variants now show **three DIFFERENT, individually identifiable, FULL original 8x9 android masks** (large male, large female, small male), all on the identical nine physical raster rows through P1, **plus one complete yellow original player P0 and a single yellow M0 test shot**. Each PASS variant has 600 consecutive valid frame IDs, 262 NTSC scanlines and ZERO missing/ghost pixels. The third NPC is not merely a white dot or duplicated mask.

The failed variants lose ONLY white pixels, with yellow P0 and M0 intact and no ghosts. Their failed frame records place third P1 near the fixed player crop X259: e.g. P1 x255/267 versus player x259. In modes where the third P1 lies outside that range, the strict pixel test PASSes. This indicates **possible white P1 masking by yellow P0 at object overlap**, NOT proven as a general timing ceiling. It is being isolated in separate R1ai by modifying ONLY the player RESP0 preload delay while preserving all other sprite bytes and register timing.

**No full six NPC R1 PASS:** only three NPC at limited X ranges, no dynamic crossing, no overlap policy, no full 14-row R1s integrated kernel, no left/right PF wall, key, door, score, shot gameplay, sound, PAL or independent VERIFICATION. Never merge to production PR #7 or main based on this research.

## Evidence

- [Batch 0 FAIL artifact](https://github.com/Odourman/let-me-out/actions/runs/43862062578/artifacts/14224261421)
- [Batch 1 PASS artifact](https://github.com/Odourman/let-me-out/actions/runs/43862062578/artifacts/14223424125)
- [Batch 2 PASS artifact](https://github.com/Odourman/let-me-out/actions/runs/43862062578/artifacts/14223388361)
- [Batch 3 FAIL artifact](https://github.com/Odourman/let-me-out/actions/runs/43862062578/artifacts/14223831935)
