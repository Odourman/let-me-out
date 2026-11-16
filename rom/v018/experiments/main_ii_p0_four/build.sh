#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
dasm r1e_four_originals.asm -f3 -or1e_4k.bin -lr1e.lst -sr1e.sym
test "$(stat -c %s r1e_4k.bin)" -eq 4096
cat r1e_4k.bin r1e_4k.bin r1e_4k.bin r1e_4k.bin > r1e_F6.bin
test "$(stat -c %s r1e_F6.bin)" -eq 16384
cp r1e.sym r1e_F6.sym
cp r1e.lst r1e_F6.lst
sha256sum r1e_4k.bin r1e_F6.bin | tee SHA256SUMS.txt
grep -i -E 'R1c(FirstRESP1|SecondRESP1|ThirdRESP1)|R1eFourth(P0Write|ColorWrite)' r1e.sym > TIMING_SYMBOLS.txt
