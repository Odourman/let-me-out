#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p dist
for variant in vb_9_interleave vb_18_doubled vb_9_vdel; do
  dasm "$variant.asm" -f3 -o"dist/$variant.bank.bin" -l"dist/$variant.lst" -s"dist/$variant.sym" >"dist/$variant.dasm.log" 2>&1
  test "$(stat -c %s "dist/$variant.bank.bin")" -eq 4096
  python3 - "$variant" <<'PY'
import sys
from pathlib import Path
variant=sys.argv[1]
p=Path("dist")/(variant+".bank.bin")
assert p.stat().st_size==4096
(Path("dist")/(variant+".F6.bin")).write_bytes(p.read_bytes()*4)
PY
  test "$(stat -c %s "dist/$variant.F6.bin")" -eq 16384
done
(cd dist && sha256sum *bank.bin *F6.bin >SHA256SUMS.txt && sha256sum -c SHA256SUMS.txt)
