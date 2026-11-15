#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
dasm xmatrix_two_masks.asm -f3 -oxmatrix_4k.bin -lxmatrix.lst -sxmatrix.sym
test "$(stat -c %s xmatrix_4k.bin)" -eq 4096
cat xmatrix_4k.bin xmatrix_4k.bin xmatrix_4k.bin xmatrix_4k.bin > xmatrix_F6.bin
test "$(stat -c %s xmatrix_F6.bin)" -eq 16384
cp xmatrix.sym xmatrix_F6.sym
cp xmatrix.lst xmatrix_F6.lst
sha256sum xmatrix_4k.bin xmatrix_F6.bin | tee SHA256SUMS.txt
grep -i -E 'R1bFirstRESP1|R1bFemaleWrite|R1bSecondRESP1|PhaseReady' xmatrix.sym > TIMING_SYMBOLS.txt
