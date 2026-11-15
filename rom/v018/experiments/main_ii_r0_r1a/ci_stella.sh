#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p evidence
export SDL_AUDIODRIVER=dummy SDL_VIDEODRIVER=x11
ACTUAL_HOME="$(getent passwd "$(id -un)" | cut -d: -f6)"
mkdir -p "$ACTUAL_HOME/.config/stella"
Xvfb :118 -screen 0 1366x900x24 -ac > evidence/xvfb.log 2>&1 &
xpid=$!
trap 'kill "$xpid" 2>/dev/null || true' EXIT
export DISPLAY=:118
sleep 2
for mode in frame breakpoint_first breakpoint_second; do
  dest="evidence/$mode"; mkdir -p "$dest"
  cp r1a_F6.bin "$dest/proof.bin"
  cp r1a_F6.lst "$dest/proof.lst"
  cp r1a_F6.sym "$dest/proof.sym"
  {
    echo 'base #10'
    echo 'frame #13'
    if [ "$mode" != frame ]; then
      if [ "$mode" = breakpoint_first ]; then symbol=R1aFirstRESP1; else symbol=R1aSecondRESP1; fi
      addr=$(awk -v sym="$symbol" 'tolower($1)==tolower(sym) {print $2;exit}' r1a.sym)
      test -n "$addr" || { echo "missing symbol $symbol" >&2; exit 1; }
      echo "break \$$addr"
      echo 'run'
    fi
    echo 'print _fCount'
    echo 'print _scan'
    echo 'print _sCycles'
    echo 'print _bank'
  } > "$dest/commands.txt"
  cp "$dest/commands.txt" "$ACTUAL_HOME/.config/stella/autoexec.script"
  stella -debug -bs F6 -format NTSC -video software -vsync 0 -audio.enabled 0 "$PWD/$dest/proof.bin" > "$dest/stella_stdout.txt" 2>&1 &
  pid=$!
  sleep 7
  if kill -0 "$pid" 2>/dev/null; then
    import -window root "$dest/stella_full.png"
    kill "$pid" || true
    wait "$pid" 2>/dev/null || true
  else
    echo "Stella exited prematurely for $mode" >&2
    cat "$dest/stella_stdout.txt" >&2
    exit 1
  fi
  test -s "$dest/stella_full.png"
  sha256sum "$dest/stella_full.png" | tee "$dest/screenshot.sha256"
done
