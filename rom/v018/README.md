# LET ME OUT! – ROM DEVELOPMENT NTSC diagnostic v0.18

**2026-11-15 | Scope: R1–R4 ONLY | NOT an approved game or independently verified ROM**

A standalone, genuine Atari 2600 MOS 6502 program with an NTSC-style frame kernel,
16 KiB F6 mapper (4 × 4096 B), and deterministic diagnostic stages.
The binary was produced with a self-contained deterministic assembler subset. No
commercial Berzerk code, ROM, or graphics is included.

## Run

1. Open `dist/LetMeOut_Diagnostic_NTSC_F6_v018.bin` in Stella, select/confirm
   **16 KiB F6** and **NTSC**, and turn on Stella Debugger for raster inspection.
2. The diagnostic changes scenes **automatically** after 600 frames each:
   R1 → R2 → R3 → R4 → repeat. No gameplay, title menu, AI, scoring or sound.
3. Within R2 and R4, raster phase changes at `(FRAMELO >> 6) & 3`:
   every 64 diagnostic frames. The key is hidden by an android only in phases 1/2;
   logical RAM at `$84` (X cell=27), `$85` (Y scanline=80), `$86` (exists=1)
   never changes.
4. In R3, `FRAMELO 0..84`: brown technical baseline; `85..169`: orange
   locked door; `170..255`: visually open right-side door (P1 blank).
   These are diagnostic state cycles, not game rules.
5. In Stella Debugger, measure `_scan`, `_sCycles`, VSYNC/VBLANK, `PF0/PF1/PF2`,
   `GRP0/GRP1`, `COLUP0/COLUP1/COLUPF`, `RESP0/RESP1` for each scene.

**Important**: A Stella emulator and DASM were not available in the build environment.
The enclosed TIA trace and screenshots are **NOT** Stella output. They are
independent original *offline* Python CPU cycle-model traces and explicitly marked
*schematic* image previews. Never use them as Stella-based or physical-hardware proof.

## Rebuild (offline, reproducible)

Python 3.13.5 was used. The project includes its complete minimal assembler source
`tools/as6502.py` v0.18a and requires only Python 3 stdlib for building.

```sh
python3 tools/build.py
sha256sum dist/LetMeOut_Diagnostic_NTSC_F6_v018.bin
python3 tools/verify_preflight.py
python3 tools/render_schematic.py  # needs Pillow, only for unverified schematic PNGs
```

Or `bash build_rom.sh` for assembly plus the non-Stella preflight.

`src/bank0.asm` through `src/bank3.asm` are generated complete 6502 assembler
listings, fully stand-alone for the included assembler. Each has the same kernel
at `$F000..$F3FF`, bank-specific 2048 B of tables at `$F400..$FBFF`, and
identical reset vectors at `$FFFC..$FFFF`. The four concatenated 4096 B banks
form the `.bin`. The binary contains a real 6502 instruction stream rather
than a data-only mock-up.

## Architecture and limitations

| F6 bank | Scene | Pixel strategy |
| --- | --- | --- |
| 0 ($FFF6) | R1 six androider + player + shot | Six coarse 4×9 PF-cell masks; P0 player; PF short shot symbol |
| 1 ($FFF7) | R2 five androider + key + player + shot | PF masks + P1 gold key/K11 vs K09; P0 player; key occlusion via P1 mask zero |
| 2 ($FFF8) | R3 planned C02 room, right-only door | Asymmetric PF0/1/2 rewrites; P1 brown/orange/black door-keyhole target |
| 3 ($FFF9) | R4 moving scanline stress | Four 11-line PF mask profiles; P0 player + P1 key; deterministic movement |

Each PF cell spans four horizontal color clocks; Androids are only 4 PF cells
(16 clocks) wide, so visual gender/size distinction is a **major unresolved
quality risk**, not an approved change to game sprites. No TIA missile/ball
is allocated: the **PF shot symbol** is an allowed temporary visible test
symbol, *not* verified bullet movement or shot physics. TIA's actual sprite
horizontal placement and PF latch effects remain unverified.

Visible NTSC model: 3 VSYNC + 37 VBLANK + 192 visible + 30 overscan =
262 scanlines. A 6502 instruction-level CPU model ran more than 600 frames
for every scene at exactly 262 scanlines once past startup; it does not
simulate Stella's pixel output or provide independent verdicts.

RIOT RAM: 8 bytes `$80..$87` for scene, counters, phase and logical key/color;
no dynamic allocations and no 128 B expansion. F6 adds ROM only.

## Reports / evidence

- `docs/TO_MAIN.md`: engineering deliverable, blockers and handoff.
- `docs/TEST_RESULTS_16.csv`: all 16 original gate test IDs with honest status.
- `evidence/cpu_preflight_summary.json`: offline CPU simulation parameters.
- `evidence/frame_scanline_preflight.csv`: per-frame arithmetic cycles/scanlines.
- `evidence/tia_writes_preflight_samples.csv`: reconstructed 6502 register writes
  with PC, raster line and cycle, **not Stella debugger data**.
- `evidence/*schematic.png`: source-based schematic images, NOT Stella captures.
- `SHA256SUMS.txt`: SHA-256 for every archive file, except itself.

For independent VERIFICATION: rebuild the binary, compare SHA-256, then perform
actual Stella run, cycle audits, screenshot/video capture, and legibility review.
**All design gates remain open until independent VERIFICATION.**
