The first implementation did phase selection and restoration within the
already crowded VBLANK planner. The active-shot fixture missed the VBLANK
deadline, giving a malformed frame sequence.

A subsequent version moved preparation before the planner but incurred a
six-cycle shift in the timer write and did clock work after the overscan
timer. The no-floor-key standard sequence failed at the first real shot
transition near frame 101. Both versions are rejected.

To reproduce either historical build, replace game.asm and blink.inc in a
scratch copy of the delivered sources with the corresponding archived
files (remove the failed-first- prefix for the earliest one), then use
build.py --edge top --blink 8 or 6. These bins are diagnostics.
