#!/usr/bin/env bash
# F3-G0: ONE compiled index0 +1 CPU cycle geometry probe; index2 fixed baseline.
# Exactly 16 sequential genuine Stella frames, without any production changes.
set -euo pipefail
cd "$(dirname "$0")"
export SDL_AUDIODRIVER=dummy SDL_VIDEODRIVER=x11 DISPLAY=:119
h="$(getent passwd "$(id -un)" | cut -d: -f6)"
mkdir -p "$h/.config/stella" evidence/r1_f3_g0/raw
Xvfb :119 -screen 0 1366x900x24 -ac > evidence/r1_f3_g0/xvfb.log 2>&1 &
xpid=$!
trap 'kill "$xpid" 2>/dev/null || true' EXIT
sleep 2
printf 'base #10\nframe #10\nprint _fCount\nprint _scanEnd\n' > "$h/.config/stella/autoexec.script"
cp "$h/.config/stella/autoexec.script" evidence/r1_f3_g0/autoexec.script
rom="$PWD/dist/r1_f3_6B_I0_P1_I2_FIXED_F6.bin"
stella -debug -bs F6 -format NTSC -video software -vsync 0 -audio.enabled 0 "$rom" > evidence/r1_f3_g0/stella.log 2>&1 &
pid=$!;sleep 4
if ! kill -0 "$pid" 2>/dev/null; then cat evidence/r1_f3_g0/stella.log;exit 1;fi
wid="$(xdotool search --onlyvisible --name Stella | head -n1)"
xdotool windowfocus --sync "$wid"
import -window root evidence/r1_f3_g0/initial_full.png
for ((i=1;i<=16;i++));do
 xdotool key --window "$wid" --clearmodifiers ctrl+f
 sleep 0.03
 import -window root -crop 900x300+103+65 "evidence/r1_f3_g0/raw/frame_$(printf '%03d' "$i").png"
done
import -window root evidence/r1_f3_g0/final_full.png
kill "$pid" 2>/dev/null || true;wait "$pid" 2>/dev/null || true
sha256sum evidence/r1_f3_g0/raw/frame_*.png > evidence/r1_f3_g0/RAW_PNG_SHA256SUMS.txt
/usr/bin/python3 r1_f3_audit.py --mode G0 --raw evidence/r1_f3_g0/raw --out evidence/r1_f3_g0/STRICT_PIXEL_AUDIT.json --mutants evidence/r1_f3_g0/MUTANT_NEGATIVE_NOT_STELLA
echo 'F3_G0_INDEX0_GEOMETRY_ONE_OFFSET_PASS_ONLY_IF_ABOVE_TESTS_PASSED'
