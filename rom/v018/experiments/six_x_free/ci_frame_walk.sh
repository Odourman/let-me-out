#!/usr/bin/env bash
# External X11 screenshot per actual Stella debugger frame, no saveSnap (black).
set -euo pipefail
cd "$(dirname "$0")"
ROOT="$PWD"
CAPTURE_VARIANT="${CAPTURE_VARIANT:-a}"
NFRAMES="${NFRAMES:-12}"
if test "$CAPTURE_VARIANT" = a; then ROM=dist/six_x_free_a_f6.bin; SYM=dist/six_x_free_a.sym; LST=dist/six_x_free_a.lst; else ROM=dist/six_x_free_b_f6.bin; SYM=dist/six_x_free_b.sym; LST=dist/six_x_free_b.lst; fi
OUT="$ROOT/evidence_walk_$CAPTURE_VARIANT"
mkdir -p "$OUT/raw" "$OUT/home"
export HOME="$OUT/home" SDL_AUDIODRIVER=dummy SDL_VIDEODRIVER=x11
ACTUAL_HOME="$(getent passwd "$(id -un)" | cut -d: -f6)"
mkdir -p "$ACTUAL_HOME/.config/stella"
printf 'base #10\nframe #10\n' > "$ACTUAL_HOME/.config/stella/autoexec.script"
cp "$ROM" "$OUT/sexwalk.bin"
cp "$SYM" "$OUT/sexwalk.sym"
cp "$LST" "$OUT/sexwalk.lst"
Xvfb :104 -screen 0 1366x900x24 -ac >"$OUT/xvfb.log" 2>&1 &
XVPID=$!
trap 'kill "$XVPID" 2>/dev/null || true' EXIT
export DISPLAY=:104
sleep 1
stella -debug -bs F6 -format NTSC -video software -vsync 0 -audio.enabled 0 "$OUT/sexwalk.bin" >"$OUT/stella_stdout.txt" 2>&1 &
PID=$!
sleep 4
kill -0 "$PID"
WINDOW_ID="$(xdotool search --onlyvisible --name Stella | head -n1 || true)"
if test -z "$WINDOW_ID"; then echo "No Stella window" >&2; exit 2; fi
xdotool windowfocus --sync "$WINDOW_ID"
import -window root "$OUT/initial_debugger.png"
for ((i=1;i<=NFRAMES;i++)); do
  xdotool key --window "$WINDOW_ID" --clearmodifiers ctrl+f
  sleep 0.03
  import -window root -crop 900x300+103+65 "$OUT/raw/frame_$(printf '%04d' "$i").png"
done
import -window root "$OUT/final_debugger.png"
kill "$PID" 2>/dev/null || true
wait "$PID" 2>/dev/null || true
FOUND="$(find "$OUT/raw" -type f -name 'frame_*.png' | wc -l)"
echo "Frame+1 keypresses: $NFRAMES; original X11 debugger screenshots: $FOUND"
test "$FOUND" -eq "$NFRAMES"
python3 - "$OUT" "$NFRAMES" <<'PY'
import json,sys
from pathlib import Path
out=Path(sys.argv[1]); n=int(sys.argv[2]); files=sorted((out/"raw").glob("frame_*.png"))
assert len(files)==n
assert all(p.stat().st_size>500 for p in files)
(out/"capture_summary.json").write_text(json.dumps({"keypresses":n,"saved_unmodified_debugger_crops":len(files),"continuous_600_frame_stability_proven":False,"per_frame_cpu_scanline_measurement":"not yet decoded from actual HUD screenshot; no PASS without classification"},indent=2)+"\n")
PY
