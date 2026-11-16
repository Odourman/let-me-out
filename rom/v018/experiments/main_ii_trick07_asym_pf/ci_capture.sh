#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p evidence
export SDL_AUDIODRIVER=dummy SDL_VIDEODRIVER=x11
HOME_DIR="$(getent passwd "$(id -un)"|cut -d: -f6)"
mkdir -p "$HOME_DIR/.config/stella"
Xvfb :168 -screen 0 1366x900x24 -ac >evidence/xvfb.log 2>&1 &
xpid=$!
trap 'kill "$xpid" 2>/dev/null || true' EXIT
export DISPLAY=:168
sleep 2
printf 'base #10\nframe #2\n' >"$HOME_DIR/.config/stella/autoexec.script"
stella -debug -bs F6 -format NTSC -video software -vsync 0 -audio.enabled 0 "$PWD/door_F6.bin" >evidence/init.log 2>&1 &
pid=$!
sleep 5
kill "$pid" 2>/dev/null || true
wait "$pid" 2>/dev/null || true
for config in locked:13 open:29; do
  name="$(echo "$config"|cut -d: -f1)"
  frame="$(echo "$config"|cut -d: -f2)"
  dir="$PWD/evidence/$name"
  mkdir -p "$dir"
  cp door_F6.bin "$dir/proof.bin"
  cp door.lst "$dir/proof.lst"
  cp door.sym "$dir/proof.sym"
  printf 'base #10\nframe #%s\nprint _fCount\nprint _scanEnd\nprint _bank\n' "$frame" > "$dir/commands.txt"
  cp "$dir/commands.txt" "$HOME_DIR/.config/stella/autoexec.script"
  stella -debug -bs F6 -format NTSC -video software -vsync 0 -audio.enabled 0 "$dir/proof.bin" >"$dir/stdout.txt" 2>&1 &
  pid=$!
  sleep 7
  kill -0 "$pid"
  for i in 1 2 3 4;do
    import -window root "$dir/stella_full.png"
    colors="$(identify -format '%k' "$dir/stella_full.png")"
    [ "$colors" -gt 5 ] && break
    sleep 3
  done
  [ "$colors" -gt 5 ] || { echo "bad screenshot $name" >&2;exit 1; }
  kill "$pid" 2>/dev/null || true
  wait "$pid" 2>/dev/null || true
  sha256sum "$dir/stella_full.png" >"$dir/image.sha256"
done
