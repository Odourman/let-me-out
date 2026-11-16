#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p evidence
export SDL_AUDIODRIVER=dummy SDL_VIDEODRIVER=x11
ACTUAL_HOME="$(getent passwd "$(id -un)" | cut -d: -f6)"
mkdir -p "$ACTUAL_HOME/.config/stella"
Xvfb :138 -screen 0 1366x900x24 -ac > evidence/xvfb.log 2>&1 &
xpid=$!
trap 'kill "$xpid" 2>/dev/null || true' EXIT
export DISPLAY=:138
sleep 2
for variant in p0wide_control p0wide_recolor; do
  folder="$PWD/$variant"
  for mode in frame R1cFirstRESP1 R1cSecondRESP1 R1cThirdRESP1; do
    dest="$folder/evidence/$mode"
    mkdir -p "$dest"
    cp "$folder/probe_F6.bin" "$dest/proof.bin"
    cp "$folder/probe.sym" "$dest/proof.sym"
    cp "$folder/probe.lst" "$dest/proof.lst"
    {
      echo 'base #10'
      echo 'frame #13'
      if [ "$mode" != frame ]; then
        addr="$(awk -v sym="$mode" 'tolower($1)==tolower(sym) {print $2;exit}' "$folder/probe.sym")"
        test -n "$addr"
        printf 'runToPc $%s\n' "$addr"
      fi
      echo 'print _fCount'
      echo 'print _scanEnd'
      echo 'print _scan'
      echo 'print _sCycles'
      echo 'print _bank'
    } > "$dest/commands.txt"
    cp "$dest/commands.txt" "$ACTUAL_HOME/.config/stella/autoexec.script"
    stella -debug -bs F6 -format NTSC -video software -vsync 0 -audio.enabled 0 "$dest/proof.bin" >"$dest/stella_stdout.txt" 2>&1 &
    pid=$!
    sleep 7
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
  done
done
