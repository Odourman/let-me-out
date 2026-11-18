#!/usr/bin/env bash
# Exact opcode PC breakpoint (DASM listing) to measure actual _scan/_sCycles.
set -euo pipefail
cd "$(dirname "$0")"
ROOT="$PWD"
OUT="$ROOT/evidence/pc_cycle_breakpoints"
mkdir -p "$OUT"
export SDL_AUDIODRIVER=dummy SDL_VIDEODRIVER=x11
ACTUAL_HOME="$(getent passwd "$(id -un)" | cut -d: -f6)"
mkdir -p "$ACTUAL_HOME/.config/stella"
Xvfb :109 -screen 0 1366x900x24 -ac >"$OUT/xvfb.log" 2>&1 &
XVPID=$!
trap 'kill "$XVPID" 2>/dev/null || true' EXIT
export DISPLAY=:109
sleep 1
for pc in f0a8 f0bd; do
  d="$OUT/$pc"
  mkdir -p "$d"
  cp dist/vb_9_interleave.F6.bin "$d/proof.bin"
  cp dist/vb_9_interleave.lst "$d/proof.lst"
  cp dist/vb_9_interleave.sym "$d/proof.sym"
  cat > "$ACTUAL_HOME/.config/stella/autoexec.script" <<EOF
base #10
frame #12
break \$$pc
frame #1
step
print _fCount
print _scan
print _sCycles
EOF
  stella -debug -bs F6 -format NTSC -video software -vsync 0 -audio.enabled 0 "$d/proof.bin" >"$d/stdout.log" 2>&1 &
  pid=$!
  sleep 5
  if ! kill -0 "$pid" 2>/dev/null; then cat "$d/stdout.log"; exit 1; fi
  import -window root "$d/pc_break_image.png"
  kill "$pid" 2>/dev/null || true
  wait "$pid" 2>/dev/null || true
done
