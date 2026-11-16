#!/usr/bin/env bash
# One F4 geometry probe only; 16 consecutive true Stella 6.7.1 frames.
# Capture unmodified 1366x900 debugger screenshot AND 900x300 original crop
# at each frame; synthetic negatives are generated ONLY AFTER real captures.
set -euo pipefail
phase="${1:?phase 18 or 21}"
[[ "$phase" == 18 || "$phase" == 21 ]] || exit 2
cd "$(dirname "$0")"
export SDL_AUDIODRIVER=dummy SDL_VIDEODRIVER=x11 DISPLAY=:120
home="$(getent passwd "$(id -un)" | cut -d: -f6)"
stem="r1_f4_6B_I0_C$(printf '%02d' "$phase")_I2_FIXED"
out="evidence/r1_f4_c$(printf '%02d' "$phase")"
mkdir -p "$home/.config/stella" "$out/raw" "$out/raw_full"
Xvfb :120 -screen 0 1366x900x24 -ac > "$out/xvfb.log" 2>&1 &
xpid=$!
trap 'kill "$xpid" 2>/dev/null || true' EXIT
sleep 2
printf 'base #10\nframe #10\nprint _fCount\nprint _scanEnd\n' > "$home/.config/stella/autoexec.script"
cp "$home/.config/stella/autoexec.script" "$out/autoexec.script"
rom="$PWD/dist/${stem}_F6.bin"
stella -debug -bs F6 -format NTSC -video software -vsync 0 -audio.enabled 0 "$rom" > "$out/stella.log" 2>&1 &
pid=$!
sleep 4
if ! kill -0 "$pid";then cat "$out/stella.log";exit 1;fi
wid="$(xdotool search --onlyvisible --name Stella | head -n1)"
xdotool windowfocus --sync "$wid"
import -window root "$out/initial_full.png"
for ((i=1;i<=16;i++));do
  xdotool key --window "$wid" --clearmodifiers ctrl+f
  sleep 0.05
  stamp="$(printf '%03d' "$i")"
  import -window root "$out/raw_full/frame_${stamp}.png"
  import -window root -crop 900x300+103+65 "$out/raw/frame_${stamp}.png"
done
import -window root "$out/final_full.png"
kill "$pid" 2>/dev/null || true
wait "$pid" 2>/dev/null || true
sha256sum "$out/raw"/frame_*.png > "$out/RAW_CROP_SHA256SUMS.txt"
sha256sum "$out/raw_full"/frame_*.png > "$out/RAW_FULL_SHA256SUMS.txt"
sha256sum -c "$out/RAW_CROP_SHA256SUMS.txt"
sha256sum -c "$out/RAW_FULL_SHA256SUMS.txt"
/usr/bin/python3 r1_f4_audit.py --phase "$phase" --raw "$out/raw" \
  --out "$out/STRICT_16_FRAME_PIXEL_AUDIT.json" \
  --mutants "$out/MUTANT_NEGATIVE_SYNTHETIC_NOT_STELLA"
echo "F4_REAL_STELLA_16_COMPLETE phase=$phase (read classification JSON; CI success does NOT imply geometry PASS)"
