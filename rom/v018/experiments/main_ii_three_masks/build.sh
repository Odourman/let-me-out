#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
dasm r1c_three_toggle.asm -f3 -or1c_4k.bin -lr1c.lst -sr1c.sym
test "$(stat -c %s r1c_4k.bin)" -eq 4096
cat r1c_4k.bin r1c_4k.bin r1c_4k.bin r1c_4k.bin > r1c_F6.bin
test "$(stat -c %s r1c_F6.bin)" -eq 16384
cp r1c.sym r1c_F6.sym
cp r1c.lst r1c_F6.lst
sha256sum r1c_4k.bin r1c_F6.bin | tee SHA256SUMS.txt
grep -i -E 'R1c(Early|Late)(FirstRESP1|SecondRESP1|ThirdRESP1|FemaleWrite|SmallMaleWrite)' r1c.sym | tee TIMING_SYMBOLS.txt
