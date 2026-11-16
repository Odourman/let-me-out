#!/usr/bin/env bash
# Strict R1-F2 G0+G1. 16 real sequential Stella frames PER isolated ROM probe.
set -euo pipefail
cd "$(dirname "$0")"
export SDL_AUDIODRIVER=dummy SDL_VIDEODRIVER=x11 DISPLAY=:119
h="$(getent passwd "$(id -un)" | cut -d: -f6)"
mkdir -p "$h/.config/stella" evidence/r1_f2_g1
Xvfb :119 -screen 0 1366x900x24 -ac > evidence/r1_f2_g1/xvfb.log 2>&1 &
xpid=$!
trap 'kill "$xpid" 2>/dev/null || true' EXIT
sleep 2
for v in BASE M2 P1; do
  case "$v" in
    BASE) rom=dist/r1_individual_6B_F6.bin ;;
    M2) rom=dist/r1_f2_6B_I2_M2_F6.bin ;;
    P1) rom=dist/r1_f2_6B_I2_P1_F6.bin ;;
  esac
  out="evidence/r1_f2_g1/$v";mkdir -p "$out/raw"
  printf 'base #10\nframe #10\nprint _fCount\nprint _scanEnd\n' > "$h/.config/stella/autoexec.script"
  cp "$h/.config/stella/autoexec.script" "$out/autoexec.script"
  stella -debug -bs F6 -format NTSC -video software -vsync 0 -audio.enabled 0 "$PWD/$rom" > "$out/stella.log" 2>&1 &
  pid=$!;sleep 4
  if ! kill -0 "$pid" 2>/dev/null; then cat "$out/stella.log"; exit 1; fi
  wid="$(xdotool search --onlyvisible --name Stella | head -n1)"
  xdotool windowfocus --sync "$wid"
  import -window root "$out/initial_full.png"
  for ((i=1;i<=16;i++)); do
    xdotool key --window "$wid" --clearmodifiers ctrl+f
    sleep 0.025
    import -window root -crop 900x300+103+65 "$out/raw/frame_$(printf '%03d' "$i").png"
  done
  import -window root "$out/final_full.png"
  kill "$pid" 2>/dev/null || true;wait "$pid" 2>/dev/null || true
  test "$(find "$out/raw" -name 'frame_*.png' | wc -l)" -eq 16
  sha256sum "$out"/raw/*.png > "$out/RAW_PNG_SHA256SUMS.txt"
  echo "F2_G1_AUTHENTIC_STELLA $v frames=16 ROM=$rom"
  if [ "$v" = BASE ]; then
    /usr/bin/python3 r1_f2_checker.py --mode "$v" --raw "$out/raw" --output "$out/STRICT_AUDIT.json" --mutants "evidence/r1_f2_g1/MUTANT_NEGATIVE_ONLY"
  else
    /usr/bin/python3 r1_f2_checker.py --mode "$v" --raw "$out/raw" --output "$out/STRICT_AUDIT.json"
  fi
done
echo 'F2_G1_CONTROL_AND_TWO_SINGLE_INDEX_OFFSET_PROBES_COMPLETED'
