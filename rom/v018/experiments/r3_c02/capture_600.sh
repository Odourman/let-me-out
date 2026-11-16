#!/usr/bin/env bash
# 600 genuine Stella 6.7.1 debugger Ctrl+F steps and external X11 screenshots.
# Source is the current R3 C02 test ROM ONLY. These are cropped GUI images
# (900x300) for deterministic HUD pixel template matching; six full originals
# are supplied separately by capture.sh.
set -euo pipefail
cd "$(dirname "$0")"
ROOT="$PWD"
OUT="$ROOT/evidence/sequence_600"
mkdir -p "$OUT/raw" "$OUT/home"
export HOME="$OUT/home" SDL_AUDIODRIVER=dummy SDL_VIDEODRIVER=x11
REAL_HOME="$(getent passwd "$(id -un)" | cut -d: -f6)"
mkdir -p "$REAL_HOME/.config/stella"
printf 'base #10\nframe #10\n' >"$REAL_HOME/.config/stella/autoexec.script"
cp dist/LetMeOut_v018_R3_C02_F6_NTSC.bin "$OUT/sequence.bin"
cp dist/r3_c02.sym "$OUT/sequence.sym"
cp dist/r3_c02.lst "$OUT/sequence.lst"
Xvfb :112 -screen 0 1366x900x24 -ac > "$OUT/xvfb.log" 2>&1 &
VPID=$!
trap 'kill "$VPID" 2>/dev/null || true' EXIT
export DISPLAY=:112
sleep 1
stella -debug -bs F6 -format NTSC -video software -vsync 0 -audio.enabled 0 "$OUT/sequence.bin" >"$OUT/stella.log" 2>&1 &
PID=$!
sleep 5
kill -0 "$PID"
WINDOW="$(xdotool search --onlyvisible --name Stella | head -n 1 || true)"
test -n "$WINDOW"
xdotool windowfocus --sync "$WINDOW"
import -window root "$OUT/initial_full.png"
for ((frame=1;frame<=600;frame++)); do
  xdotool key --window "$WINDOW" --clearmodifiers ctrl+f
  sleep 0.025
  import -window root -crop 900x300+103+65 "$OUT/raw/frame_$(printf '%04d' "$frame").png"
  if (( frame % 100 == 0 )); then echo "Captured $frame consecutive Stella debugger frames"; fi
done
import -window root "$OUT/final_full.png"
kill "$PID" || true
wait "$PID" 2>/dev/null || true
test "$(find "$OUT/raw" -name 'frame_*.png' | wc -l)" -eq 600
python3 - "$OUT" <<'PY'
from pathlib import Path
import hashlib,json,sys
p=Path(sys.argv[1]); files=sorted((p/"raw").glob("frame_*.png"))
assert len(files)==600
assert all(f.stat().st_size>800 for f in files)
unique=len(set(hashlib.sha256(f.read_bytes()).digest() for f in files))
assert unique>=20, "Stella frames apparently did not advance"
(p/"capture_metadata.json").write_text(json.dumps({
 "actual_stella_debugger_F6": True,
 "requested_step_count":600,"saved_stella_gui_crops":len(files),
 "unique_png_file_hashes":unique,"cropped_to":"900x300+103+65 from 1366x900 Xvfb",
 "source":"Stella 6.7.1 X11 debugger, Ctrl+F one frame per capture",
 "scanline_result":"Must be independently extracted from actual image HUD"
},indent=2)+"\n")
print("STELLA_600_CAPTURE_COMPLETE",len(files),"unique",unique)
PY
