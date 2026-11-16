#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p evidence
export SDL_AUDIODRIVER=dummy SDL_VIDEODRIVER=x11
ACTUAL_HOME="$(getent passwd "$(id -un)" | cut -d: -f6)"
mkdir -p "$ACTUAL_HOME/.config/stella"
Xvfb :134 -screen 0 1366x900x24 -ac >evidence/xvfb.log 2>&1 &
xpid=$!
trap 'kill "$xpid" 2>/dev/null || true' EXIT
export DISPLAY=:134
sleep 2
for variant in nusiz3_only four_mask_probe; do
  root="$PWD/$variant"
  for mode in frame R1cFirstRESP1 R1cSecondRESP1 R1cThirdRESP1; do
    dst="$root/evidence/$mode"
    mkdir -p "$dst"
    cp "$root/probe_F6.bin" "$dst/proof.bin"
    cp "$root/probe.sym" "$dst/proof.sym"
    cp "$root/probe.lst" "$dst/proof.lst"
    {
      echo 'base #10'
      echo 'frame #13'
      if [ "$mode" != frame ]; then
        addr="$(awk -v sym="$mode" 'tolower($1)==tolower(sym) {print $2;exit}' "$root/probe.sym")"
        test -n "$addr"
        printf 'runToPc $%s\n' "$addr"
      fi
      echo 'print _fCount'
      echo 'print _scanEnd'
      echo 'print _scan'
      echo 'print _sCycles'
      echo 'print _bank'
    } > "$dst/commands.txt"
    cp "$dst/commands.txt" "$ACTUAL_HOME/.config/stella/autoexec.script"
    stella -debug -bs F6 -format NTSC -video software -vsync 0 -audio.enabled 0 "$dst/proof.bin" > "$dst/stella_stdout.txt" 2>&1 &
    pid=$!
    sleep 7
    if ! kill -0 "$pid" 2>/dev/null; then cat "$dst/stella_stdout.txt" >&2;exit 2;fi
    for attempt in 1 2 3; do
      import -window root "$dst/stella_full.png"
      colors="$(identify -format '%k' "$dst/stella_full.png")"
      if [ "$colors" -gt 5 ]; then break; fi
      sleep 3
    done
    test "$colors" -gt 5 || { echo "Invalid capture $variant $mode" >&2; exit 2; }
    kill "$pid" 2>/dev/null || true
    wait "$pid" 2>/dev/null || true
    sha256sum "$dst/stella_full.png" > "$dst/image.sha256"
  done
done
