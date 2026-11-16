#!/usr/bin/env bash
# R1-F2 G2: exactly 32 sequential authenticated frames from ONE F6 ROM.
# No alternate executable, no reassemble between positions, no screen synthesis.
set -euo pipefail
cd "$(dirname "$0")"
export SDL_AUDIODRIVER=dummy SDL_VIDEODRIVER=x11 DISPLAY=:119
h="$(getent passwd "$(id -un)" | cut -d: -f6)"
mkdir -p "$h/.config/stella" evidence/r1_f2_runtime/raw
Xvfb :119 -screen 0 1366x900x24 -ac > evidence/r1_f2_runtime/xvfb.log 2>&1 &
xpid=$!
trap 'kill "$xpid" 2>/dev/null || true' EXIT
sleep 2
printf 'base #10\nframe #10\nprint _fCount\nprint _scanEnd\n' > "$h/.config/stella/autoexec.script"
cp "$h/.config/stella/autoexec.script" evidence/r1_f2_runtime/autoexec.script
stella -debug -bs F6 -format NTSC -video software -vsync 0 -audio.enabled 0 "$PWD/dist/r1_f2_6B_I2_RUNTIME_F6.bin" > evidence/r1_f2_runtime/stella.log 2>&1 &
pid=$!;sleep 4
if ! kill -0 "$pid" 2>/dev/null;then cat evidence/r1_f2_runtime/stella.log;exit 1;fi
wid="$(xdotool search --onlyvisible --name Stella | head -n1)"
xdotool windowfocus --sync "$wid"
import -window root evidence/r1_f2_runtime/initial_full.png
for ((i=1;i<=32;i++));do
 xdotool key --window "$wid" --clearmodifiers ctrl+f
 sleep 0.025
 import -window root -crop 900x300+103+65 "evidence/r1_f2_runtime/raw/frame_$(printf '%03d' "$i").png"
done
import -window root evidence/r1_f2_runtime/final_full.png
kill "$pid" 2>/dev/null || true
wait "$pid" 2>/dev/null || true
test "$(find evidence/r1_f2_runtime/raw -name 'frame_*.png'|wc -l)" -eq 32
sha256sum evidence/r1_f2_runtime/raw/*.png > evidence/r1_f2_runtime/RAW_PNG_SHA256SUMS.txt
echo 'F2_G2_EXACTLY_32_SEQUENTIAL_REAL_STELLA_FRAMES from one ROM'
/usr/bin/python3 r1_f2_checker.py --mode RUNTIME --raw evidence/r1_f2_runtime/raw --output evidence/r1_f2_runtime/STRICT_32_FRAME_AUDIT.json
