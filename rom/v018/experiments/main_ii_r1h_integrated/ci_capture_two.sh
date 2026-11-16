#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p evidence
export SDL_AUDIODRIVER=dummy SDL_VIDEODRIVER=x11
REAL_HOME="$(getent passwd "$(id -un)"|cut -d: -f6)"
mkdir -p "$REAL_HOME/.config/stella"
Xvfb :186 -screen 0 1366x900x24 -ac > evidence/xvfb.log 2>&1 &
xpid=$!
trap 'kill "$xpid" 2>/dev/null || true' EXIT
export DISPLAY=:186
sleep 2
printf 'base #10\nframe #2\n' >"$REAL_HOME/.config/stella/autoexec.script"
stella -debug -bs F6 -format NTSC -video software -vsync 0 -audio.enabled 0 "$PWD/r1h_F6.bin" >evidence/init.log 2>&1 &
pid=$!
sleep 5
kill "$pid" 2>/dev/null || true
wait "$pid" 2>/dev/null || true
for setting in locked:13 open:77; do
 name="$(echo "$setting"|cut -d: -f1)"
 target="$(echo "$setting"|cut -d: -f2)"
 dir="$PWD/evidence/$name"
 mkdir -p "$dir"
 cp r1h_F6.bin "$dir/proof.bin"
 cp r1h.sym "$dir/proof.sym"
 cp r1h.lst "$dir/proof.lst"
 printf 'base #10\nframe #%s\nprint _fCount\nprint _scanEnd\nprint _bank\n' "$target" >"$dir/commands.txt"
 cp "$dir/commands.txt" "$REAL_HOME/.config/stella/autoexec.script"
 stella -debug -bs F6 -format NTSC -video software -vsync 0 -audio.enabled 0 "$dir/proof.bin" >"$dir/stella_stdout.txt" 2>&1 &
 pid=$!
 sleep 7
 kill -0 "$pid"
 for attempt in 1 2 3 4; do
   import -window root "$dir/stella_full.png"
   colors="$(identify -format '%k' "$dir/stella_full.png")"
   [ "$colors" -gt 5 ] && break
   sleep 3
 done
 [ "$colors" -gt 5 ] || { echo "No real screenshot $name" >&2;exit 2; }
 kill "$pid" 2>/dev/null || true
 wait "$pid" 2>/dev/null || true
 sha256sum "$dir/stella_full.png" >"$dir/image.sha256"
done
