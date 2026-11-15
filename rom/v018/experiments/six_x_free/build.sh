#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p dist
dasm six_x_free_a.asm -f3 -odist/six_x_free_a_bank.bin -sdist/six_x_free_a.sym -ldist/six_x_free_a.lst >dist/dasm.stdout.txt 2>&1
test "$(stat -c %s dist/six_x_free_a_bank.bin)" -eq 4096
python3 - <<'PY'
from pathlib import Path
b=Path("dist/six_x_free_a_bank.bin").read_bytes()
assert len(b)==4096
Path("dist/six_x_free_a_f6.bin").write_bytes(b*4)
PY
(cd dist && sha256sum six_x_free_a_bank.bin six_x_free_a_f6.bin >SHA256SUMS.txt && sha256sum -c SHA256SUMS.txt)

# Candidate B: 4-color-clock PF six bodies + 1 original P1 silhouette.
dasm six_x_free_b_hybrid.asm -f3 -odist/six_x_free_b_bank.bin -sdist/six_x_free_b.sym -ldist/six_x_free_b.lst >dist/dasm_b.stdout.txt 2>&1
test "$(stat -c %s dist/six_x_free_b_bank.bin)" -eq 4096
python3 - <<'PY'
from pathlib import Path
b=Path("dist/six_x_free_b_bank.bin").read_bytes()
assert len(b)==4096
Path("dist/six_x_free_b_f6.bin").write_bytes(b*4)
PY
(cd dist && sha256sum six_x_free_a_bank.bin six_x_free_a_f6.bin six_x_free_b_bank.bin six_x_free_b_f6.bin >SHA256SUMS.txt && sha256sum -c SHA256SUMS.txt)
