# Let Me Out! MAIN IV R1ai – isolate P0 occlusion of third complete P1 original mask

**2026-11-16. LOCAL RESEARCH PASS 1200/1200 real Stella frames. NOT independent VERIFICATION, NOT full R1.**

## Provenance and A/B experiment

- [GitHub Actions #43862530097](https://github.com/Odourman/let-me-out/actions/runs/43862530097): both 600-frame experiments SUCCESS, tested commit `50a8e29433aa253db9eebe1f39e2f20ec112e06d`.
- Original [R1ah](https://github.com/Odourman/let-me-out/actions/runs/43862062578) batches 0/3 each yielded only **150/600 strict PASS**; 5,700 / 4,200 lost white original-mask pixels. Their P0 player and single M0 shot remained intact, no white ghosts.
- R1ai built exactly each failed R1ah ROM from pinned original SHA, then changed ONLY initial player placement `LDX #12` to `LDX #9` before the P0 `RESP0` delay loop. No P1 reset timing, GRP1 table, original mask, M0, F6 bank, display row count or player mask bits changed.

| R1ai job | Pinned failed R1ah group | Before strict PASS | After strict PASS | Missing white pixels before → after | R1ai ROM SHA256 |
|---:|---:|---:|---:|---:|---|
| 0 | R1ah batch 0 | 150/600 | **600/600** | 5700 → **0** | `305ad7d36b7098ea2ffda80e972783f466f604e9bfd6078234fe9d77271e1880` |
| 1 | R1ah batch 3 | 150/600 | **600/600** | 4200 → **0** | `d2f18d509073c14d2a0bcdaa0c66780b1ac5762469d6af62cb6740acb3082249` |

All frames have 262 NTSC rasterlines, all three separate original 8×9 white NPC mask instances intact, zero ghost pixels, full yellow original P0 player, one yellow M0 test shot, and four measured three-mask X states per job.

## Causal finding and limits

Moving ONLY the player prevented the white NPC pixel loss. The matched comparison strongly supports **overlap/priority masking of white P1 pixels by yellow P0**, not a generalized 76-cycle timing overload. This is an observed emulator result under controlled positions, not a universal specification of TIA priority in every mode. The third original NPC remains white and visually readable in separated arrangements.

**Caveat:** The static yellow M0 testsymbolskott is NOT reattached to the moved player's hand. This comparison is deliberately a resource/isolation experiment, NOT a complete hand-fired bullet system.

Only **three** white original NPCs are proven on these exact positions, not all six, not full independent X/Y movement, not overlapped player/enemy behavior, no PF/key/door, no collision identity, no PAL. No changes to main or draft ROM DEVELOPMENT PR #7. Independent organizational VERIFICATION is still pending.

Evidence: [batch 0 artifact](https://github.com/Odourman/let-me-out/actions/runs/43862530097/artifacts/14224621507) and [batch 1 artifact](https://github.com/Odourman/let-me-out/actions/runs/43862530097/artifacts/14224102270).
