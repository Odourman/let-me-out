#!/usr/bin/env bash
# Real Stella 6.7.1 conditional TIA write trap diagnostic, NOT a full trace.
set -euo pipefail
cd "$(dirname "$0")"
ROOT="$PWD"
OUT="$ROOT/evidence/resp1_traps"
mkdir -p "$OUT"
export SDL_AUDIODRIVER=dummy SDL_VIDEODRIVER=x11
ACTUAL_HOME="$(getent passwd "$(id -un)" | cut -d: -f6)"
mkdir -p "$ACTUAL_HOME/.config/stella"
Xvfb :108 -screen 0 1366x900x24 -ac >"$OUT/xvfb.log" 2>&1 &
XVFBPID=$!
trap 'kill "$XVFBPID" 2>/dev/null || true' EXIT
export DISPLAY=:108
sleep 1
for line in 120 121; do
  caseDir="$OUT/line$line"
  mkdir -p "$caseDir"
  cp dist/vb_9_interleave.F6.bin "$caseDir/proof.bin"
  cp dist/vb_9_interleave.lst "$caseDir/proof.lst"
  cp dist/vb_9_interleave.sym "$caseDir/proof.sym"
  cat >"$ACTUAL_HOME/.config/stella/autoexec.script" <<EOF
base #10
frame #12
trapWriteIf {_scan==#$line} \$11
frame #1
print _fCount
print _scan
print _sCycles
print _scanEnd
EOF
  stella -debug -bs F6 -format NTSC -video software -vsync 0 -audio.enabled 0 "$caseDir/proof.bin" >"$caseDir/stdout.log" 2>&1 &
  pid=$!
  sleep 5
  if ! kill -0 "$pid" 2>/dev/null; then cat "$caseDir/stdout.log"; exit 1; fi
  import -window root "$caseDir/debugger_tia_write.png"
  kill "$pid" 2>/dev/null || true
  wait "$pid" 2>/dev/null || true
  echo "Conditional RESP1 TIA trap image saved for scanline $line. Judge validity by HUD PC, _scan and prompt."
done
