#!/usr/bin/env bash
# Capture each of 600 actual consecutive Stella debugger frames in GitHub Actions.
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
cp xmatrix_F6.bin "$OUT/proof.bin"
cp xmatrix_F6.lst "$OUT/proof.lst"
cp xmatrix_F6.sym "$OUT/proof.sym"
Xvfb :122 -screen 0 1366x900x24 -ac >"$OUT/xvfb.log" 2>&1 &
XPID=$!
trap 'kill "$XPID" 2>/dev/null || true' EXIT
export DISPLAY=:122
sleep 2
stella -debug -bs F6 -format NTSC -video software -vsync 0 -audio.enabled 0 "$OUT/proof.bin" >"$OUT/stella_stdout.txt" 2>&1 &
PID=$!
sleep 7
kill -0 "$PID"
# Some fresh Xvfb/Stella sessions expose only unmapped debugger windows.
# Diagnose actual X11 windows and retry by name without --onlyvisible.
xwininfo -root -tree >"$OUT/windows.txt" 2>&1 || true
xdotool search --name Stella >"$OUT/window_ids.txt" 2>&1 || true
WINDOW_ID="$(head -n1 "$OUT/window_ids.txt" 2>/dev/null || true)"
if [ -z "$WINDOW_ID" ]; then
  echo "Stella window absent. Window-tree:" >&2
  cat "$OUT/windows.txt" >&2
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
sha256sum xmatrix_F6.bin >"$OUT/ROM_SHA256.txt"
