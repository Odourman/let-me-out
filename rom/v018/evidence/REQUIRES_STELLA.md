# Unperformed emulator verification evidence

No Stella executable/debugger was available in this environment. The 11
`*_schematic.png` files are drawn from source data and are **NOT Stella
screenshots**. `frame_scanline_preflight.csv` and `tia_writes_preflight_samples.csv`
are data from the project's standalone 6502 timing model, **NOT Stella traces**.

Before closing T01-T13, VERIFICATION must rerun 600 actual continuous Stella
frames for each critical scene (R1/R2/R4 at minimum), save real video/frame
captures, inspect TIA PF/GRP register timing and 262 scanlines, and make a
manual legibility assessment. T15 explicitly requires a separate actor.
