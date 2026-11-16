#!/usr/bin/env bash
# R1-F7 exactly ONE compiled ROM, 160 consecutive TRUE Stella 6.7.1 frames:
# mode 00 -> 10 -> 00 -> 01 -> 11 -> 01 -> 00, 16 frames/step.
set -euo pipefail
cd "$(dirname "$0")"
export SDL_AUDIODRIVER=dummy SDL_VIDEODRIVER=x11 DISPLAY=:124
home="$(getent passwd "$(id -un)" | cut -d: -f6)"
stem="r1_f7_2x2_independent_RAM_X_ONE_ROM"
out="evidence/r1_f7_one_rom"
mkdir -p "$home/.config/stella" "$out/raw" "$out/raw_full"
rom="$PWD/dist/$stem"_F6.bin
test "$(stat -c %s "$rom")" -eq 16384
Xvfb :124 -screen 0 1366x900x24 -ac > "$out/xvfb.log" 2>&1 &
xp=$!
pid=""
trap '[[ -z "$pid" ]] || kill "$pid" 2>/dev/null || true; kill "$xp" 2>/dev/null || true' EXIT
sleep 2
printf 'base #10\nframe #10\nprint _fCount\nprint _scanEnd\n' > "$home/.config/stella/autoexec.script"
cp "$home/.config/stella/autoexec.script" "$out/autoexec.script"
stella -debug -bs F6 -format NTSC -video software -vsync 0 -audio.enabled 0 "$rom" > "$out/stella.log" 2>&1 &
pid=$!
wid=""
for t in $(seq 1 18);do
 if ! kill -0 "$pid";then echo "F7_STELLA_PROCESS_DIED";cat "$out/stella.log";exit 4;fi
 wid="$(xdotool search --onlyvisible --name Stella 2>/dev/null | head -n1 || true)"
 if [[ -n "$wid" ]];then echo "F7_GUI_READY $wid";break;fi
 sleep 1
done
if [[ -z "$wid" ]];then echo "F7_INFRA_STELLA_WINDOW_MISSING";cat "$out/stella.log";exit 5;fi
xdotool windowfocus --sync "$wid"
import -window root "$out/initial_uncropped_GUI.png"
for ((i=1;i<=160;i++));do
 xdotool key --window "$wid" --clearmodifiers ctrl+f
 sleep 0.055
 index="$(printf '%03d' "$i")"
 import -window root "$out/raw_full/frame_$index.png"
 import -window root -crop 900x300+103+65 "$out/raw/frame_$index.png"
done
import -window root "$out/final_uncropped_GUI.png"
kill "$pid" 2>/dev/null || true
wait "$pid" 2>/dev/null || true
pid=""
sha256sum "$out/raw"/frame_*.png > "$out/TRUE_160_CROP_SHA256SUMS.txt"
sha256sum "$out/raw_full"/frame_*.png > "$out/TRUE_160_FULL_SHA256SUMS.txt"
sha256sum -c "$out/TRUE_160_CROP_SHA256SUMS.txt"
sha256sum -c "$out/TRUE_160_FULL_SHA256SUMS.txt"
/usr/bin/python3 r1_f7_audit.py --raw "$out/raw" \
 --out "$out/TRUE_160_FRAMES_2x2_SOURCE_CANON_PIXEL_AUDIT.json" \
 --mutants "$out/SYNTHETIC_MUTANTS_NOT_REAL_STELLA"
echo "F7_SINGLE_ROM_160_CONSECUTIVE_ACTUAL_STELLA_FRAMES_DONE"
