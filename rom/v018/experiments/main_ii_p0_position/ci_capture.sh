#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p evidence
export SDL_AUDIODRIVER=dummy SDL_VIDEODRIVER=x11
ACTUAL_HOME="$(getent passwd "$(id -un)" | cut -d: -f6)"
mkdir -p "$ACTUAL_HOME/.config/stella"
Xvfb :142 -screen 0 1366x900x24 -ac > evidence/xvfb.log 2>&1 &
xpid=$!
trap 'kill "$xpid" 2>/dev/null || true' EXIT
export DISPLAY=:142
sleep 2
for n in 04 06 08 10 12 13 14 15; do
  dest="$PWD/delay_$n/evidence"
  mkdir -p "$dest"
  cp "delay_$n/probe_F6.bin" "$dest/proof.bin"
  printf 'base #10\nframe #13\nprint _scanEnd\nprint _fCount\n' >"$ACTUAL_HOME/.config/stella/autoexec.script"
  stella -debug -bs F6 -format NTSC -video software -vsync 0 -audio.enabled 0 "$dest/proof.bin" > "$dest/stdout.txt" 2>&1 &
  pid=$!
  sleep 6
  kill -0 "$pid"
  for attempt in 1 2 3; do
    import -window root "$dest/stella_full.png"
    colors="$(identify -format '%k' "$dest/stella_full.png")"
    if [ "$colors" -gt 5 ]; then break; fi
    sleep 3
  done
  test "$colors" -gt 5
  kill "$pid" 2>/dev/null || true
  wait "$pid" 2>/dev/null || true
  sha256sum "$dest/stella_full.png" > "$dest/image.sha256"
  echo "Captured P0Delay=$n"
done
