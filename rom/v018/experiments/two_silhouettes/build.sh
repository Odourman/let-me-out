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
(cd dist && sha256sum proof_bank.bin LetMeOut_v018_two_silhouette_F6.bin > SHA256SUMS.txt)
cat dist/SHA256SUMS.txt

# Second, independent ROM candidate: NUSIZ1 copy modes 2/4, same original masks.
dasm proof_nusiz.asm -f3 -odist/proof_nusiz_bank.bin -sdist/proof_nusiz.sym -ldist/proof_nusiz.lst >dist/dasm_nusiz.stdout.txt 2>&1
test "$(stat -c %s dist/proof_nusiz_bank.bin)" = 4096
python3 - <<'PY'
from pathlib import Path
p=Path("dist/proof_nusiz_bank.bin").read_bytes()
assert len(p)==4096
Path("dist/LetMeOut_v018_two_silhouette_NUSIZ_F6.bin").write_bytes(p*4)
PY
(cd dist && sha256sum proof_bank.bin LetMeOut_v018_two_silhouette_F6.bin proof_nusiz_bank.bin LetMeOut_v018_two_silhouette_NUSIZ_F6.bin >SHA256SUMS.txt)
cat dist/SHA256SUMS.txt

# Third candidate: timed mid-raster P1 retrigger with independent right-hand X.
dasm proof_retrigger_visible.asm -f3 -odist/proof_retrigger_bank.bin -sdist/proof_retrigger.sym -ldist/proof_retrigger.lst > dist/dasm_retrigger.stdout.txt 2>&1
test "$(stat -c %s dist/proof_retrigger_bank.bin)" = 4096
python3 - <<'PY'
from pathlib import Path
p=Path("dist/proof_retrigger_bank.bin").read_bytes()
assert len(p)==4096
Path("dist/LetMeOut_v018_two_silhouette_RETRIGGER_F6.bin").write_bytes(p*4)
PY
(cd dist && sha256sum proof_bank.bin LetMeOut_v018_two_silhouette_F6.bin proof_nusiz_bank.bin LetMeOut_v018_two_silhouette_NUSIZ_F6.bin proof_retrigger_bank.bin LetMeOut_v018_two_silhouette_RETRIGGER_F6.bin >SHA256SUMS.txt)
cat dist/SHA256SUMS.txt
