#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export SDL_AUDIODRIVER=dummy SDL_VIDEODRIVER=x11
REAL_HOME="$(getent passwd "$(id -un)" | cut -d: -f6)"
mkdir -p "$REAL_HOME/.config/stella" evidence/six_sweep
Xvfb :119 -screen 0 1366x900x24 -ac >evidence/six_sweep/xvfb.log 2>&1 &
XPID=$!
trap 'kill "$XPID" 2>/dev/null || true' EXIT
export DISPLAY=:119
sleep 1
for n in 6B 6C 6D 6E; do
  OUT="evidence/six_sweep/n$n";mkdir -p "$OUT/raw"
  printf 'base #10\nframe #10\nprint _fCount\nprint _scanEnd\n' > "$REAL_HOME/.config/stella/autoexec.script"
  stella -debug -bs F6 -format NTSC -video software -vsync 0 -audio.enabled 0 "$PWD/dist/r1_individual_${n}_F6.bin" > "$OUT/stella.log" 2>&1 &
  pid=$!; sleep 4
  if ! kill -0 "$pid" 2>/dev/null; then cat "$OUT/stella.log"; exit 1; fi
  wid="$(xdotool search --onlyvisible --name Stella | head -n 1)";
  xdotool windowfocus --sync "$wid"
  import -window root "$OUT/initial_full.png"
  for ((i=1;i<=16;i++)); do
    xdotool key --window "$wid" --clearmodifiers ctrl+f
    sleep 0.025
    import -window root -crop 900x300+103+65 "$OUT/raw/frame_$(printf '%03d' "$i").png"
  done
  import -window root "$OUT/final_full.png"
  kill "$pid" 2>/dev/null || true
  wait "$pid" 2>/dev/null || true
  test "$(find "$OUT/raw" -name 'frame_*.png' | wc -l)" -eq 16
  echo "SIX_SWEEP_REAL_STELLA N=$n frames=16"
done
