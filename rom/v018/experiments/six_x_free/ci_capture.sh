#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
ROOT="$PWD"
OUT="$ROOT/evidence"
mkdir -p "$OUT" "$OUT/home" "$OUT/frames"
export SDL_AUDIODRIVER=dummy SDL_VIDEODRIVER=x11
export HOME="$OUT/home"
mkdir -p "$HOME/.config/stella"
ACTUAL_HOME="$(getent passwd "$(id -un)" | cut -d: -f6)"
mkdir -p "$ACTUAL_HOME/.config/stella"
# Stella debugger 6.7 loads real-user autoexec.script; 600 intended snapshots,
# first use 12-frame shakedown to detect saveSnap black images / overwriting.
python3 - <<'PY'
from pathlib import Path
cmd=["base #10","frame #10"]
for n in range(12):
 cmd.extend(("frame #1","saveSnap"))
cmd.extend(("print _fCount","print _scanEnd","print *$90","print *$91","print *$92","print *$93","print *$94","print *$95","print *$83","saveSes"))
Path("evidence/autoexec.script").write_text("\n".join(cmd)+"\n")
PY
cp "$OUT/autoexec.script" "$ACTUAL_HOME/.config/stella/autoexec.script"
cp dist/six_x_free_a_f6.bin "$OUT/sixfree.bin"
cp dist/six_x_free_a.lst "$OUT/sixfree.lst"
cp dist/six_x_free_a.sym "$OUT/sixfree.sym"
Xvfb :99 -screen 0 1366x900x24 -ac > "$OUT/xvfb.log" 2>&1 &
XVFB_PID=$!
trap 'kill "$XVFB_PID" 2>/dev/null || true' EXIT
export DISPLAY=:99
sleep 1
stella -debug -bs F6 -format NTSC -video software -vsync 0 -audio.enabled 0 -snapsavedir "$OUT/frames" "$OUT/sixfree.bin" > "$OUT/stella_stdout.txt" 2>&1 &
PID=$!
sleep 10
if ! kill -0 "$PID" 2>/dev/null; then cat "$OUT/stella_stdout.txt"; exit 1; fi
import -window root "$OUT/debugger_full.png"
kill "$PID" 2>/dev/null || true
wait "$PID" 2>/dev/null || true
python3 - <<'PY'
from pathlib import Path
import json,hashlib
files=list(Path("evidence/frames").glob("*.png"))
sizes=[p.stat().st_size for p in files]
print("Raw Stella saves:",len(files),"bytes",sizes[:20])
Path("evidence/measurement_status.json").write_text(json.dumps({
 "requested_frame_commands":12,
 "raw_snapshot_files":len(files),
 "all_nonempty":all(s>100 for s in sizes),
 "black_or_uninspected_pixels":True,
 "600_frame_claim":False,
 "note":"12-frame saveSnap instrument check ONLY. No 600-PASS claim."
},indent=2)+"\n")
PY
