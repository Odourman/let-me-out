#!/usr/bin/env bash
# Full, unmodified X11 Stella 6.7.1 GUI images at deterministic debugger frames.
set -euo pipefail
cd "$(dirname "$0")"
ROOT="$PWD"
OUT="$ROOT/evidence"
mkdir -p "$OUT"
export SDL_AUDIODRIVER=dummy SDL_VIDEODRIVER=x11
ACTUAL_HOME="$(getent passwd "$(id -un)" | cut -d: -f6)"
mkdir -p "$ACTUAL_HOME/.config/stella"
Xvfb :106 -screen 0 1366x900x24 -ac >"$OUT/xvfb.log" 2>&1 &
XVPID=$!
trap 'kill "$XVPID" 2>/dev/null || true' EXIT
export DISPLAY=:106
sleep 1
for variant in vb_9_interleave vb_18_doubled; do
  for frame in 12 17; do
    dir="$OUT/$variant/frame_$frame"
    mkdir -p "$dir"
    cp "dist/$variant.F6.bin" "$dir/proof.bin"
    cp "dist/$variant.sym" "$dir/proof.sym"
    cp "dist/$variant.lst" "$dir/proof.lst"
    cat >"$ACTUAL_HOME/.config/stella/autoexec.script" <<EOF
base #10
frame #$frame
print _fCount
print _scanEnd
print _scan
print _sCycles
print *\$80
print *\$81
print *\$82
print *\$90
print *\$91
EOF
    stella -debug -bs F6 -format NTSC -video software -vsync 0 -audio.enabled 0 "$dir/proof.bin" >"$dir/stella_stdout.txt" 2>&1 &
    pid=$!
    sleep 5
    if ! kill -0 "$pid" 2>/dev/null; then
      cat "$dir/stella_stdout.txt"; exit 1
    fi
    import -window root "$dir/stella_full.png"
    test -s "$dir/stella_full.png"
    kill "$pid" 2>/dev/null || true
    wait "$pid" 2>/dev/null || true
    echo "$variant frame $frame bytes $(stat -c %s "$dir/stella_full.png")"
  done
done
find "$OUT" -type f -print | sort > "$OUT/FILES.txt"
