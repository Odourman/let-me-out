#!/usr/bin/env bash
# Experimental real Stella 6.7 trace; does NOT assert success without log.
set -euo pipefail
cd "$(dirname "$0")"
ROOT="$PWD"
OUT="$ROOT/evidence/trace_probe"
mkdir -p "$OUT"
export SDL_AUDIODRIVER=dummy SDL_VIDEODRIVER=x11
ACTUAL_HOME="$(getent passwd "$(id -un)" | cut -d: -f6)"
mkdir -p "$ACTUAL_HOME/.config/stella"
cat >"$ACTUAL_HOME/.config/stella/autoexec.script" <<'EOF'
base #10
frame #12
logTrace
frame #1
logTrace
print _fCount
print _scanEnd
EOF
cp dist/vb_9_interleave.F6.bin "$OUT/proof.bin"
cp dist/vb_9_interleave.lst "$OUT/proof.lst"
cp dist/vb_9_interleave.sym "$OUT/proof.sym"
Xvfb :107 -screen 0 1366x900x24 -ac > "$OUT/xvfb.log" 2>&1 &
XVPID=$!
trap 'kill "$XVPID" 2>/dev/null || true' EXIT
export DISPLAY=:107
sleep 1
stella -debug -bs F6 -format NTSC -video software -vsync 0 -audio.enabled 0 "$OUT/proof.bin" >"$OUT/stella_stdout.txt" 2>&1 &
PID=$!
sleep 6
if ! kill -0 "$PID" 2>/dev/null; then cat "$OUT/stella_stdout.txt"; exit 1; fi
import -window root "$OUT/stella_trace_window.png"
kill "$PID" 2>/dev/null || true
wait "$PID" 2>/dev/null || true
find "$ACTUAL_HOME/.config/stella" "$OUT" -maxdepth 5 -type f \( -name '*trace*' -o -name '*.log' -o -name '*.txt' \) -printf '%p %s\n' >"$OUT/trace_file_index.txt" || true
cat "$OUT/trace_file_index.txt"
echo "TRACE_STATUS=INCONCLUSIVE_UNTIL_LOG_PARSED"
