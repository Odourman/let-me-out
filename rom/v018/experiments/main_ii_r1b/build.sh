#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
dasm r1b_two_masks.asm -f3 -or1b_4k.bin -lr1b.lst -sr1b.sym
test "$(stat -c %s r1b_4k.bin)" -eq 4096
cat r1b_4k.bin r1b_4k.bin r1b_4k.bin r1b_4k.bin > r1b_F6.bin
test "$(stat -c %s r1b_F6.bin)" -eq 16384
cp r1b.sym r1b_F6.sym
cp r1b.lst r1b_F6.lst
sha256sum r1b_4k.bin r1b_F6.bin | tee SHA256SUMS.txt
grep -i -E 'R1bFirstRESP1|R1bFemaleWrite|R1bSecondRESP1' r1b.sym | tee TIMING_SYMBOLS.txt
