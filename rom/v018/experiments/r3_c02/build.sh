#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p dist evidence
python3 tools/generate_tables.py
dasm r3_door.asm -f3 -odist/r3_c02.bank.bin -ldist/r3_c02.lst -sdist/r3_c02.sym >dist/dasm.log 2>&1
test "$(stat -c %s dist/r3_c02.bank.bin)" = 4096
python3 - <<'PY'
from pathlib import Path
p=Path("dist/r3_c02.bank.bin").read_bytes()
assert len(p)==4096
Path("dist/LetMeOut_v018_R3_C02_F6_NTSC.bin").write_bytes(p*4)
PY
test "$(stat -c %s dist/LetMeOut_v018_R3_C02_F6_NTSC.bin)" = 16384
(cd dist && sha256sum r3_c02.bank.bin LetMeOut_v018_R3_C02_F6_NTSC.bin r3_tables.inc source_geometry.json > SHA256SUMS.txt && sha256sum -c SHA256SUMS.txt)
