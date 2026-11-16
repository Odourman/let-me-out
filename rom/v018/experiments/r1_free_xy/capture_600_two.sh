#!/usr/bin/env bash
# R1 first primitive: 600 unaltered Stella 6.7.1 debugger GUI frames (4 X-pair modes x6).
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p evidence/pilot600/raw
REAL_HOME="$(getent passwd "$(id -un)" | cut -d: -f6)"
mkdir -p "$REAL_HOME/.config/stella"
printf 'base #10\nframe #10\nprint _fCount\nprint _scanEnd\n' > "$REAL_HOME/.config/stella/autoexec.script"
export SDL_AUDIODRIVER=dummy SDL_VIDEODRIVER=x11
Xvfb :120 -screen 0 1366x900x24 -ac >evidence/pilot600/xvfb.log 2>&1 &
XVFBPID=$!
trap 'kill "$XVFBPID" 2>/dev/null || true' EXIT
export DISPLAY=:120
sleep 1
stella -debug -bs F6 -format NTSC -video software -vsync 0 -audio.enabled 0 "$PWD/dist/LetMeOut_R1_TWO_2x2_F6.bin" >evidence/pilot600/stella.log 2>&1 &
PID=$!
sleep 4
if ! kill -0 "$PID" 2>/dev/null; then cat evidence/pilot600/stella.log; exit 1; fi
WID="$(xdotool search --onlyvisible --name Stella | head -n 1)"
xdotool windowfocus --sync "$WID"
import -window root evidence/pilot600/frame_initial_full.png
for ((i=1;i<=600;i++)); do
 xdotool key --window "$WID" --clearmodifiers ctrl+f
 sleep 0.035
 import -window root -crop 900x300+103+65 "evidence/pilot600/raw/frame_$(printf '%04d' "$i").png"
done
import -window root evidence/pilot600/frame_final_full.png
kill "$PID" 2>/dev/null || true
wait "$PID" 2>/dev/null || true
test "$(find evidence/pilot600/raw -name 'frame_*.png' | wc -l)" -eq 600
