#!/usr/bin/env bash
# Four different PF-bit positions, real Stella X11 screenshot per variant.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p evidence
export SDL_AUDIODRIVER=dummy SDL_VIDEODRIVER=x11
HOME_DIR="$(getent passwd "$(id -un)"|cut -d: -f6)"
mkdir -p "$HOME_DIR/.config/stella"
Xvfb :157 -screen 0 1366x900x24 -ac >evidence/xvfb.log 2>&1 &
xpid=$!
trap 'kill "$xpid" 2>/dev/null || true' EXIT
export DISPLAY=:157
sleep 2
printf 'base #10\nframe #2\n' >"$HOME_DIR/.config/stella/autoexec.script"
stella -debug -bs F6 -format NTSC -video software -vsync 0 -audio.enabled 0 "$PWD/left2/probe_F6.bin" >evidence/init.log 2>&1 &
pid=$!
sleep 5
kill "$pid" 2>/dev/null || true
wait "$pid" 2>/dev/null || true
for name in left2 left1 right1 right2; do
  dir="$PWD/$name/evidence"
  mkdir -p "$dir"
  cp "$PWD/$name/probe_F6.bin" "$dir/proof.bin"
  cp "$PWD/$name/probe.sym" "$dir/proof.sym"
  cp "$PWD/$name/probe.lst" "$dir/proof.lst"
  printf 'base #10\nframe #13\nprint _fCount\nprint _scanEnd\nprint _bank\n' >"$dir/commands.txt"
  cp "$dir/commands.txt" "$HOME_DIR/.config/stella/autoexec.script"
  stella -debug -bs F6 -format NTSC -video software -vsync 0 -audio.enabled 0 "$dir/proof.bin" >"$dir/stella_stdout.txt" 2>&1 &
  pid=$!
  sleep 7
  kill -0 "$pid"
  for attempt in 1 2 3 4; do
    import -window root "$dir/stella_full.png"
    colors="$(identify -format '%k' "$dir/stella_full.png")"
    test "$colors" -gt 5 && break
    sleep 3
  done
  test "$colors" -gt 5 || { echo "Invalid screenshot for $name" >&2;exit 1; }
  kill "$pid" 2>/dev/null || true
  wait "$pid" 2>/dev/null || true
  sha256sum "$dir/stella_full.png" >"$dir/image_sha256.txt"
done
