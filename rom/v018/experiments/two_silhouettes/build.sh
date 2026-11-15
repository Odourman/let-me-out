#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p dist evidence
dasm proof.asm -f3 -odist/proof_bank.bin -sdist/proof.sym -ldist/proof.lst > dist/dasm.stdout.txt 2>&1
test "$(stat -c %s dist/proof_bank.bin)" = 4096
python3 - <<'PY'
from pathlib import Path
p=Path("dist/proof_bank.bin").read_bytes()
assert len(p)==4096
# 4 identical code banks in 16KiB F6 diagnostic cartridge, no false sprite benefit.
Path("dist/LetMeOut_v018_two_silhouette_F6.bin").write_bytes(p*4)
print("bank size",len(p),"F6 ROM size",len(p)*4)
PY
sha256sum dist/proof_bank.bin dist/LetMeOut_v018_two_silhouette_F6.bin > dist/SHA256SUMS.txt
cat dist/SHA256SUMS.txt
