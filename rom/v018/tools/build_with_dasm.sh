#!/usr/bin/env bash
# Independent compiler cross-check; does not replace Stella or independent VERIFICATION.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
command -v dasm >/dev/null || { echo "DASM missing"; exit 2; }
mkdir -p dist/dasm
for bank in 0 1 2 3; do
  printf ' processor 6502\n' > "dist/dasm/bank$bank.dasm.asm"
  # DASM requires indented ORG directives and accumulator shifts without the A operand.
  # These are syntax-only rewrites; binary identity below detects changes in semantics.
  sed -e 's/^ORG / ORG /' -e 's/^ LSR A$/ LSR/' "src/bank$bank.asm" >> "dist/dasm/bank$bank.dasm.asm"
  dasm "dist/dasm/bank$bank.dasm.asm" -f3 -o"dist/dasm/bank$bank.bin" -s"dist/dasm/bank$bank.sym" -l"dist/dasm/bank$bank.lst" >"dist/dasm/bank$bank.stdout.txt" 2>&1
  test "$(stat -c %s "dist/dasm/bank$bank.bin")" = 4096
done
cat dist/dasm/bank{0,1,2,3}.bin > dist/dasm/rebuilt-v018-F6.bin
test "$(stat -c %s dist/dasm/rebuilt-v018-F6.bin)" = 16384
sha256sum dist/dasm/rebuilt-v018-F6.bin dist/LetMeOut_Diagnostic_NTSC_F6_v018.bin
cmp dist/dasm/rebuilt-v018-F6.bin dist/LetMeOut_Diagnostic_NTSC_F6_v018.bin && echo "DASM_BUILD_BYTE_IDENTICAL=YES" || { echo "DASM_BUILD_BYTE_IDENTICAL=NO"; exit 1; }
