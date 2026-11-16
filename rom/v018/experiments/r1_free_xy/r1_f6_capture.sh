#!/usr/bin/env bash
# R1-F6 per-ROM 16 uninterrupted real Stella frame debugger captures.
# The only positive images are imported directly from Stella GUI/Xvfb root.
set -euo pipefail
phase="$1"
[[ "$phase" == 21 || "$phase" == 23 ]] || exit 2
cd "$(dirname "$0")"
export SDL_AUDIODRIVER=dummy SDL_VIDEODRIVER=x11 DISPLAY=:122
home="$(getent passwd "$(id -un)" | cut -d: -f6)"
romfile="$(printf 'r1_f6_two_correct_masks_C%02d_C32_F6.bin' "$phase")"
out="evidence/r1_f6_c$(printf '%02d' "$phase")"
mkdir -p "$home/.config/stella" "$out/raw" "$out/raw_full"
Xvfb :122 -screen 0 1366x900x24 -ac > "$out/xvfb.log" 2>&1 &
xp=$!
pid=""
trap '[[ -z "$pid" ]] || kill "$pid" 2>/dev/null || true; kill "$xp" 2>/dev/null || true' EXIT
sleep 2
printf 'base #10\nframe #10\nprint _fCount\nprint _scanEnd\n' > "$home/.config/stella/autoexec.script"
cp "$home/.config/stella/autoexec.script" "$out/autoexec.script"
rom="$PWD/dist/$romfile"
test "$(stat -c%s "$rom")" -eq 16384
stella -debug -bs F6 -format NTSC -video software -vsync 0 -audio.enabled 0 "$rom" > "$out/stella.log" 2>&1 &
pid=$!
wid=""
for t in $(seq 1 20);do
  if ! kill -0 "$pid" 2>/dev/null;then echo "F6_STELLA_DIED";cat "$out/stella.log";exit 4;fi
  wid="$(xdotool search --onlyvisible --name Stella 2>/dev/null | head -n1 || true)"
  if [[ -n "$wid" ]];then echo "F6_STELLA_GUI_READY $wid at $t";break;fi
  sleep 1
done
if [[ -z "$wid" ]];then echo "F6_INFRA_GUI_NO_WINDOW";cat "$out/stella.log";exit 5;fi
xdotool windowfocus --sync "$wid"
import -window root "$out/initial_uncropped.png"
for ((i=1;i<=16;i++));do
  xdotool key --window "$wid" --clearmodifiers ctrl+f
  sleep 0.06
  num="$(printf '%03d' "$i")"
  import -window root "$out/raw_full/frame_$num.png"
  import -window root -crop 900x300+103+65 "$out/raw/frame_$num.png"
done
import -window root "$out/final_uncropped.png"
kill "$pid" 2>/dev/null || true;wait "$pid" 2>/dev/null || true;pid=""
sha256sum "$out/raw"/frame_*.png > "$out/REAL_CROP_SHA256SUMS.txt"
sha256sum "$out/raw_full"/frame_*.png > "$out/REAL_UNCROPPED_SHA256SUMS.txt"
sha256sum -c "$out/REAL_CROP_SHA256SUMS.txt"
sha256sum -c "$out/REAL_UNCROPPED_SHA256SUMS.txt"
/usr/bin/python3 r1_f6_audit.py --first "$phase" --raw "$out/raw" \
 --out "$out/STRICT_TRUE_16_TOP_DOWN_PIXEL_AUDIT.json" \
 --mutants "$out/SYNTHETIC_NEGATIVES_NOT_STELLA"
echo "F6_16_GENUINE_STELLA_FRAMES_COMPLETE $phase"
