#!/usr/bin/env bash
# Real X11 GUI evidence in Stella 6.7.1, 262 scanlines must be READ, not assumed.
set -euo pipefail
cd "$(dirname "$0")"
ROOT="$PWD"
OUT="$ROOT/evidence"
mkdir -p "$OUT" "$OUT/home"
export HOME="$OUT/home" SDL_AUDIODRIVER=dummy SDL_VIDEODRIVER=x11
ACTUAL_HOME="$(getent passwd "$(id -un)" | cut -d: -f6)"
mkdir -p "$ACTUAL_HOME/.config/stella"
Xvfb :110 -screen 0 1366x900x24 -ac > "$OUT/xvfb.log" 2>&1 &
XVPID=$!
trap 'kill "$XVPID" 2>/dev/null || true' EXIT
export DISPLAY=:110
sleep 1
for sample in old_brown:historical_v018_F6.bin:1225 old_orange:historical_v018_F6.bin:1335 old_open:historical_v018_F6.bin:1420 new_brown:LetMeOut_v018_R3_C02_F6_NTSC.bin:30 new_orange:LetMeOut_v018_R3_C02_F6_NTSC.bin:90 new_open:LetMeOut_v018_R3_C02_F6_NTSC.bin:150; do
  IFS=: read -r name rom frame <<<"$sample"
  d="$OUT/$name"
  mkdir -p "$d"
  cp "dist/$rom" "$d/test.bin"
  cp "dist/r3_c02.sym" "$d/test.sym"  # old symbols irrelevant to HUD; do not infer scene.
  cp "dist/r3_c02.lst" "$d/test.lst"
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
print *\$83
print *\$84
print *\$85
print *\$86
print *\$87
print *\$89
EOF
  stella -debug -bs F6 -format NTSC -video software -vsync 0 -audio.enabled 0 "$d/test.bin" >"$d/stella.log" 2>&1 &
  pid=$!
  sleep 6
  if ! kill -0 "$pid" 2>/dev/null; then cat "$d/stella.log"; exit 1; fi
  import -window root "$d/stella_full.png"
  test -s "$d/stella_full.png"
  echo "$name frame $frame $(stat -c %s "$d/stella_full.png") bytes"
  kill "$pid" 2>/dev/null || true
  wait "$pid" 2>/dev/null || true
done
