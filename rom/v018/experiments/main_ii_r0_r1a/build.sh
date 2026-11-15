#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
dasm r1a_close_retrigger.asm -f3 -or1a_4k.bin -lr1a.lst -sr1a.sym
test "$(stat -c %s r1a_4k.bin)" -eq 4096
cat r1a_4k.bin r1a_4k.bin r1a_4k.bin r1a_4k.bin > r1a_F6.bin
test "$(stat -c %s r1a_F6.bin)" -eq 16384
cp r1a.sym r1a_F6.sym
cp r1a.lst r1a_F6.lst
sha256sum r1a_4k.bin r1a_F6.bin | tee SHA256SUMS.txt
grep -i -E 'R1aFirstRESP1|R1aSecondRESP1' r1a.sym | tee RESP1_SYMBOLS.txt
grep -i -E 'R1aFirstRESP1|R1aSecondRESP1' r1a.lst > RESP1_LISTING.txt || true
