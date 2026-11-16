#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p evidence
export SDL_AUDIODRIVER=dummy SDL_VIDEODRIVER=x11
actual_home="$(getent passwd "$(id -un)"|cut -d: -f6)"
mkdir -p "$actual_home/.config/stella"
Xvfb :174 -screen 0 1366x900x24 -ac > evidence/xvfb.log 2>&1 &
xpid=$!
trap 'kill "$xpid" 2>/dev/null || true' EXIT
export DISPLAY=:174
sleep 2
# Stella debug first session occasionally opens black; discard a warm-up.
printf 'base #10\nframe #2\n' > "$actual_home/.config/stella/autoexec.script"
stella -debug -bs F6 -format NTSC -video software -vsync 0 -audio.enabled 0 "$PWD/pre_mask/probe_F6.bin" > evidence/init.log 2>&1 &
pid=$!
sleep 5
kill "$pid" 2>/dev/null || true
wait "$pid" 2>/dev/null || true
for variant in pre_mask post_mask post_lda post_color; do
  dir="$PWD/$variant"
  for mode in frame R1fWhiteRESP0; do
    dest="$dir/evidence/$mode"
    mkdir -p "$dest"
    cp "$dir/probe_F6.bin" "$dest/proof.bin"
    cp "$dir/probe.sym" "$dest/proof.sym"
    cp "$dir/probe.lst" "$dest/proof.lst"
    {
      echo 'base #10'
      echo 'frame #13'
      if [ "$mode" != frame ]; then
        address="$(awk -v sym="$mode" 'tolower($1)==tolower(sym) {print $2;exit}' "$dir/probe.sym")"
        test -n "$address" || { echo "Missing symbol $mode" >&2;exit 1; }
        printf 'runToPc $%s\n' "$address"
      fi
      echo 'print _fCount'
      echo 'print _scanEnd'
      echo 'print _scan'
      echo 'print _sCycles'
      echo 'print _bank'
    } >"$dest/commands.txt"
    cp "$dest/commands.txt" "$actual_home/.config/stella/autoexec.script"
    stella -debug -bs F6 -format NTSC -video software -vsync 0 -audio.enabled 0 "$dest/proof.bin" >"$dest/stella_stdout.txt" 2>&1 &
    pid=$!
    sleep 7
    kill -0 "$pid" || { cat "$dest/stella_stdout.txt"; exit 1; }
    for i in 1 2 3 4; do
      import -window root "$dest/stella_full.png"
      colors="$(identify -format '%k' "$dest/stella_full.png")"
      [ "$colors" -gt 5 ] && break
      sleep 3
    done
    [ "$colors" -gt 5 ] || { echo "Bad/blank capture: $variant $mode" >&2;exit 1; }
    kill "$pid" 2>/dev/null || true
    wait "$pid" 2>/dev/null || true
    sha256sum "$dest/stella_full.png" >"$dest/screenshot.sha256"
  done
done
