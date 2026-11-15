#!/usr/bin/env bash
# Capture unedited frames from Stella 6.7.1 and raw debugger data, not schematic.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
ROM="$ROOT/rom/v018/dist/LetMeOut_Diagnostic_NTSC_F6_v018.bin"
OUT="$ROOT/rom/v018/evidence/stella_live"
mkdir -p "$OUT"
export HOME="$OUT/home" SDL_AUDIODRIVER=dummy SDL_VIDEODRIVER=x11
mkdir -p "$HOME" "$OUT/snaps"
Xvfb :97 -screen 0 1366x900x24 -ac >"$OUT/xvfb.log" 2>&1 &
XVPID=$!
trap 'kill "$XVPID" 2>/dev/null || true' EXIT
export DISPLAY=:97
sleep 1
for entry in "R1:100" "R2:710" "R3_locked_brown:1230" "R3_locked_orange:1330" "R3_open:1450" "R4:1925"; do
  name="${entry%%:*}"; frames="${entry#*:}"
  mkdir -p "$OUT/$name"
  cp "$ROM" "$OUT/$name/letmeout.bin"
  echo "frame #$frames" > "$OUT/$name/letmeout.script"
  for label in _fCount _scanEnd _scan _sCycles _bank; do echo "print $label" >> "$OUT/$name/letmeout.script"; done
  for addr in 80 81 82 84 85 86; do echo 'print *$'"$addr" >> "$OUT/$name/letmeout.script"; done
  echo "saveSes" >> "$OUT/$name/letmeout.script"
  mkdir -p "$HOME/.config/stella"
  cp "$OUT/$name/letmeout.script" "$HOME/.config/stella/letmeout.script"
  echo "$name frames=$frames" >> "$OUT/scene_plan.txt"
  echo "START $name frames=$frames"
  stella -debug -bs F6 -format NTSC -video software -vsync 0 -audio.enabled 0 -snapsavedir "$OUT/snaps" -snapname rom -ss1x 1 "$OUT/$name/letmeout.bin" >"$OUT/$name/stella_stdout.txt" 2>&1 &
  PID=$!
  sleep 4
  if ! kill -0 "$PID" 2>/dev/null; then echo "Stella exited early for $name"; cat "$OUT/$name/stella_stdout.txt"; continue; fi
  xdotool search --onlyvisible --name "Stella" getwindowname > "$OUT/$name/window_name.txt" 2>&1 || true
  import -window root "$OUT/$name/debugger_screen.png" 2>"$OUT/$name/import.log" || true
  xdotool key --clearmodifiers grave || true
  sleep 0.6
  xdotool key --clearmodifiers F12 || true
  sleep 0.3
  import -window root "$OUT/$name/emulator_window.png" 2>>"$OUT/$name/import.log" || true
  xdotool key --clearmodifiers grave || true
  sleep 0.3
  kill "$PID" 2>/dev/null || true
  wait "$PID" 2>/dev/null || true
  find "$HOME" -type f -name "*.txt" -print >> "$OUT/$name/home_files_list.txt" || true
done
find "$OUT" -type f -print > "$OUT/files_index.txt"
echo "Stella X11 screenshots are real GUI captures; F12 snapshots in snaps are emulator-native."
