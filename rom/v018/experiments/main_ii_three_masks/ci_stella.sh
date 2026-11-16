#!/usr/bin/env bash
# Capture raw Stella 6.7.1 images and real debugger opcode stops, never synthesize pixels.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p evidence
export SDL_AUDIODRIVER=dummy SDL_VIDEODRIVER=x11
ACTUAL_HOME="$(getent passwd "$(id -un)" | cut -d: -f6)"
mkdir -p "$ACTUAL_HOME/.config/stella"
Xvfb :130 -screen 0 1366x900x24 -ac >evidence/xvfb.log 2>&1 &
xpid=$!
trap 'kill "$xpid" 2>/dev/null || true' EXIT
export DISPLAY=:130
sleep 2
# Initialize Stella's debugger window once; discard the first session.
printf 'base #10\nframe #13\n' >"$ACTUAL_HOME/.config/stella/autoexec.script"
stella -debug -bs F6 -format NTSC -video software -vsync 0 -audio.enabled 0 "$PWD/r1c_F6.bin" > evidence/initialization_stdout.txt 2>&1 &
p=$!
sleep 6
kill "$p" 2>/dev/null || true
wait "$p" 2>/dev/null || true
for mode in frame R1cFirstRESP1 R1cFemaleWrite R1cSecondRESP1 R1cSmallMaleWrite R1cThirdRESP1; do
  dst="evidence/$mode"
  mkdir -p "$dst"
  cp r1c_F6.bin "$dst/proof.bin"
  cp r1c_F6.sym "$dst/proof.sym"
  cp r1c_F6.lst "$dst/proof.lst"
  {
    echo 'base #10'
    echo 'frame #13'
    if [ "$mode" != frame ]; then
      addr=$(awk -v sym="$mode" 'tolower($1)==tolower(sym) {print $2;exit}' r1c.sym)
      test -n "$addr"
      printf 'runToPc $%s\n' "$addr"
    fi
    echo 'print _fCount'
    echo 'print _scanEnd'
    echo 'print _scan'
    echo 'print _sCycles'
    echo 'print _bank'
  } >"$dst/commands.txt"
  cp "$dst/commands.txt" "$ACTUAL_HOME/.config/stella/autoexec.script"
  stella -debug -bs F6 -format NTSC -video software -vsync 0 -audio.enabled 0 "$PWD/$dst/proof.bin" > "$dst/stella_stdout.txt" 2>&1 &
  pid=$!
  sleep 7
  kill -0 "$pid"
  for attempt in 1 2 3; do
    import -window root "$dst/stella_full.png"
    count=$(identify -format '%k' "$dst/stella_full.png")
    if [ "$count" -gt 5 ]; then break; fi
    sleep 3
  done
  test "$count" -gt 5 || { echo "Stella screenshot invalid for $mode" >&2; exit 2; }
  kill "$pid" || true
  wait "$pid" 2>/dev/null || true
  sha256sum "$dst/stella_full.png" > "$dst/image_sha256.txt"
done
