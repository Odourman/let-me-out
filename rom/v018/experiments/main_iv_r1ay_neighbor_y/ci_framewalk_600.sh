#!/usr/bin/env bash
# Capture 600 consecutive real Stella frames for two different full original 8x9 P1 masks using same-row RESP1 re-trigger plus diagnostic P0/M0.
# Actual X11 pixels, not offline renders or static CPU estimates.
set -euo pipefail
cd "$(dirname "$0")"
ROOT="$PWD"
OUT="$ROOT/evidence_600"
mkdir -p "$OUT/raw"
export SDL_AUDIODRIVER=dummy SDL_VIDEODRIVER=x11
ACTUAL_HOME="$(getent passwd "$(id -un)" | cut -d: -f6)"
mkdir -p "$ACTUAL_HOME/.config/stella"
printf 'base #10\nframe #10\n' > "$ACTUAL_HOME/.config/stella/autoexec.script"
cp r1ay_F6.bin "$OUT/proof.bin"
cp r1ay.lst "$OUT/proof.lst"
cp r1ay.sym "$OUT/proof.sym"
Xvfb :189 -screen 0 1366x900x24 -ac >"$OUT/xvfb.log" 2>&1 &
XPID=$!
trap 'kill "$XPID" 2>/dev/null || true' EXIT
export DISPLAY=:189
sleep 2
# Stella may not create an X11 window on its first fresh-runner launch.
# Retry cleanly rather than recording black images or declaring a ROM failure.
WINDOW_ID=""
for attempt in 1 2 3 4; do
  stella -debug -bs F6 -format NTSC -video software -vsync 0 -audio.enabled 0 "$OUT/proof.bin" >"$OUT/stella_stdout_attempt_$attempt.txt" 2>&1 &
  PID=$!
  sleep 7
  if kill -0 "$PID" 2>/dev/null; then
    WINDOW_ID="$(xdotool search --name Stella 2>/dev/null | head -n1 || true)"
  fi
  if [ -n "$WINDOW_ID" ]; then
    echo "Mapped Stella on attempt $attempt window $WINDOW_ID"
    break
  fi
  echo "No Stella GUI on attempt $attempt; restarting" >&2
  kill "$PID" 2>/dev/null || true
  wait "$PID" 2>/dev/null || true
done
if [ -z "$WINDOW_ID" ]; then
  echo "ERROR: no Stella debugger X11 window after 4 attempts" >&2
  exit 2
fi
xdotool getwindowname "$WINDOW_ID" >"$OUT/window_name.txt" 2>&1 || true
xdotool windowmap "$WINDOW_ID" || true
xdotool windowfocus --sync "$WINDOW_ID" || true
import -window root "$OUT/initial_debugger.png"
echo "Stella window ID: $WINDOW_ID"
for ((i=1;i<=600;i++)); do
  xdotool key --window "$WINDOW_ID" --clearmodifiers ctrl+f
  sleep 0.035
  import -window root -crop 900x300+103+65 "$OUT/raw/frame_$(printf '%04d' "$i").png"
  if ((i%100==0)); then echo "Captured consecutive debugger frames: $i/600"; fi
done
import -window root "$OUT/final_debugger.png"
kill "$PID" || true
wait "$PID" 2>/dev/null || true
count="$(find "$OUT/raw" -name 'frame_*.png' -type f | wc -l)"
echo "Saved raw frame crops: $count"
test "$count" -eq 600
sha256sum r1ay_F6.bin >"$OUT/ROM_SHA256.txt"
