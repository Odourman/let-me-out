#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
dasm asymmetric_door.asm -f3 -odoor_4k.bin -ldoor.lst -sdoor.sym
test "$(stat -c %s door_4k.bin)" -eq 4096
cat door_4k.bin door_4k.bin door_4k.bin door_4k.bin > door_F6.bin
test "$(stat -c %s door_F6.bin)" -eq 16384
sha256sum door_4k.bin door_F6.bin > SHA256SUMS.txt
