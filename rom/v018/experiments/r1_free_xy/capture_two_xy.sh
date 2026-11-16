#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p evidence/two_xy/raw
REAL_HOME="$(getent passwd "$(id -un)" | cut -d: -f6)"
mkdir -p "$REAL_HOME/.config/stella"
printf 'base #10\nframe #10\nprint _fCount\nprint _scanEnd\n' >"$REAL_HOME/.config/stella/autoexec.script"
export SDL_AUDIODRIVER=dummy SDL_VIDEODRIVER=x11
Xvfb :119 -screen 0 1366x900x24 -ac >evidence/two_xy/xvfb.log 2>&1 &
XVPID=$!
trap 'kill "$XVPID" 2>/dev/null || true' EXIT
export DISPLAY=:119
sleep 1
stella -debug -bs F6 -format NTSC -video software -vsync 0 -audio.enabled 0 "$PWD/dist/LetMeOut_R1_TWO_INDEPENDENT_XY_F6.bin" >evidence/two_xy/stella.log 2>&1 &
PID=$!
sleep 5
kill -0 "$PID" || { cat evidence/two_xy/stella.log; exit 1; }
WID="$(xdotool search --onlyvisible --name Stella | head -1)"
xdotool windowfocus --sync "$WID"
import -window root evidence/two_xy/full_initial.png
for ((i=1;i<=48;i++)); do
 xdotool key --window "$WID" --clearmodifiers ctrl+f
 sleep .035
 import -window root -crop 900x300+103+65 "evidence/two_xy/raw/frame_$(printf '%03d' "$i").png"
done
import -window root evidence/two_xy/full_final.png
kill "$PID" 2>/dev/null || true
wait "$PID" 2>/dev/null || true
test "$(find evidence/two_xy/raw -name 'frame_*.png' | wc -l)" -eq 48
echo "TWO_XY captured 48 original Stella frames"
