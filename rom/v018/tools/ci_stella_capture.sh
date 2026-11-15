#!/usr/bin/env bash
# Unaltered Stella 6.7.x screenshot evidence, not schematic.
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
  cat >"$OUT/$name/letmeout.bin.script" <<EOF
frame #$frames
print _fCount
print _scanEnd
print _scan
print _sCycles
print _bank
print *$80
print *$81
print *$82
print *$84
print *$85
print *$86
saveSes
EOF
  printf '%s	%s
' "$name" "$frames" >>"$OUT/scene_plan.tsv"
  echo "START $name frames=$frames"
  stella -debug -bs F6 -format NTSC -video software -vsync 0 -audio.enabled 0 -snapsavedir "$OUT/snaps" -snapname rom -ss1x 1 "$OUT/$name/letmeout.bin" >"$OUT/$name/stella_stdout.txt" 2>&1 &
  PID=$!
  sleep 4
  if ! kill -0 "$PID" 2>/dev/null; then echo "Stella process exited early in $name"; cat "$OUT/$name/stella_stdout.txt"; continue; fi
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
  find "$HOME" -type f ( -name '*.txt' -o -name '*.png' ) -printf '%p %s bytes
' >> "$OUT/$name/home_files_list.txt" || true
done
find "$OUT" -type f ( -name '*.png' -o -name '*.txt' ) -printf '%P %s bytes
' | sort >"$OUT/files_index.txt"
echo "Stella X11 screenshots are actual GUI screen captures. F12 snapshots under snaps are raw emulator snapshots."