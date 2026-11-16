#!/usr/bin/env bash
# Calibrate physical 4CC ball left-wall X in eight real Stella emulator screens.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p evidence
export SDL_AUDIODRIVER=dummy SDL_VIDEODRIVER=x11
REAL_HOME="$(getent passwd "$(id -un)"|cut -d: -f6)"
mkdir -p "$REAL_HOME/.config/stella"
Xvfb :185 -screen 0 1366x900x24 -ac >evidence/xvfb.log 2>&1 &
xpid=$!
trap 'kill "$xpid" 2>/dev/null || true' EXIT
export DISPLAY=:185
sleep 2
printf 'base #10\nframe #2\n' >"$REAL_HOME/.config/stella/autoexec.script"
stella -debug -bs F6 -format NTSC -video software -vsync 0 -audio.enabled 0 "$PWD/delay_0/probe_F6.bin" >evidence/init.log 2>&1 &
pid=$!
sleep 5
kill "$pid" 2>/dev/null || true
wait "$pid" 2>/dev/null || true
for delay in 0 1 2 3 4 5 6 7; do
  dir="$PWD/delay_$delay/evidence/open"
  mkdir -p "$dir"
  cp "$PWD/delay_$delay/probe_F6.bin" "$dir/proof.bin"
  cp "$PWD/delay_$delay/probe.lst" "$dir/proof.lst"
  cp "$PWD/delay_$delay/probe.sym" "$dir/proof.sym"
  printf 'base #10\nframe #77\nprint _fCount\nprint _scanEnd\nprint _bank\n' >"$dir/commands.txt"
  cp "$dir/commands.txt" "$REAL_HOME/.config/stella/autoexec.script"
  stella -debug -bs F6 -format NTSC -video software -vsync 0 -audio.enabled 0 "$dir/proof.bin" >"$dir/stella_stdout.txt" 2>&1 &
  pid=$!
  sleep 6
  kill -0 "$pid"
  for attempt in 1 2 3 4; do
    import -window root "$dir/stella_full.png"
    colors="$(identify -format '%k' "$dir/stella_full.png")"
    [ "$colors" -gt 5 ] && break
    sleep 3
  done
  [ "$colors" -gt 5 ] || { echo "Invalid Stella capture $delay" >&2;exit 1; }
  kill "$pid" 2>/dev/null || true
  wait "$pid" 2>/dev/null || true
  sha256sum "$dir/stella_full.png" >"$dir/image.sha256"
done
