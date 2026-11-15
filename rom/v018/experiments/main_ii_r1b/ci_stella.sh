#!/usr/bin/env bash
# R1b real Stella 6.7.1 screenshots; exact source symbols via runToPc.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p evidence
export SDL_AUDIODRIVER=dummy SDL_VIDEODRIVER=x11
ACTUAL_HOME="$(getent passwd "$(id -un)" | cut -d: -f6)"
mkdir -p "$ACTUAL_HOME/.config/stella"
Xvfb :119 -screen 0 1366x900x24 -ac > evidence/xvfb.log 2>&1 &
xpid=$!
trap 'kill "$xpid" 2>/dev/null || true' EXIT
export DISPLAY=:119
sleep 2
for pair in 0:13 1:29 2:45 3:61; do
  phase="${pair%%:*}"; frame="${pair##*:}"
  dst="evidence/phase_${phase}"
  mkdir -p "$dst"
  cp r1b_F6.bin "$dst/proof.bin"
  cp r1b_F6.lst "$dst/proof.lst"
  cp r1b_F6.sym "$dst/proof.sym"
  {
    echo 'base #10'
    echo "frame #$frame"
    echo 'print _fCount'
    echo 'print _scanEnd'
    echo 'print _scan'
    echo 'print _sCycles'
    echo 'print _bank'
    echo 'print *$81'
    echo 'print *$82'
  } >"$dst/commands.txt"
  cp "$dst/commands.txt" "$ACTUAL_HOME/.config/stella/autoexec.script"
  stella -debug -bs F6 -format NTSC -video software -vsync 0 -audio.enabled 0 "$PWD/$dst/proof.bin" > "$dst/stella_stdout.txt" 2>&1 &
  pid=$!
  sleep 8
  if kill -0 "$pid" 2>/dev/null; then
    for attempt in 1 2 3 4; do
      import -window root "$dst/stella_full.png"
      colors=$(identify -format '%k' "$dst/stella_full.png")
      if [ "$colors" -gt 20 ]; then break; fi
      echo "Black/unmapped screenshot for $dst, retry $attempt" >&2
      sleep 4
    done
    test "$(identify -format '%k' "$dst/stella_full.png")" -gt 20
    kill "$pid" || true; wait "$pid" 2>/dev/null || true
  else
    cat "$dst/stella_stdout.txt" >&2; exit 1
  fi
  test -s "$dst/stella_full.png"
  sha256sum "$dst/stella_full.png" >"$dst/image_sha256.txt"
done
for label in R1bFirstRESP1 R1bFemaleWrite R1bSecondRESP1; do
  dst="evidence/pc_$label"
  mkdir -p "$dst"
  cp r1b_F6.bin "$dst/proof.bin"
  cp r1b_F6.lst "$dst/proof.lst"
  cp r1b_F6.sym "$dst/proof.sym"
  addr=$(awk -v sym="$label" 'tolower($1)==tolower(sym) {print $2; exit}' r1b.sym)
  test -n "$addr"
  {
    echo 'base #10'
    echo 'frame #13'
    printf 'runToPc $%s\n' "$addr"
    echo 'print _fCount'
    echo 'print _scan'
    echo 'print _sCycles'
    echo 'print _bank'
    echo 'print *$81'
    echo 'print *$82'
  } >"$dst/commands.txt"
  cp "$dst/commands.txt" "$ACTUAL_HOME/.config/stella/autoexec.script"
  stella -debug -bs F6 -format NTSC -video software -vsync 0 -audio.enabled 0 "$PWD/$dst/proof.bin" > "$dst/stella_stdout.txt" 2>&1 &
  pid=$!
  sleep 8
  if kill -0 "$pid" 2>/dev/null; then
    for attempt in 1 2 3 4; do
      import -window root "$dst/stella_full.png"
      colors=$(identify -format '%k' "$dst/stella_full.png")
      if [ "$colors" -gt 20 ]; then break; fi
      echo "Black/unmapped screenshot for $dst, retry $attempt" >&2
      sleep 4
    done
    test "$(identify -format '%k' "$dst/stella_full.png")" -gt 20
    kill "$pid" || true; wait "$pid" 2>/dev/null || true
  else
    cat "$dst/stella_stdout.txt" >&2; exit 1
  fi
  test -s "$dst/stella_full.png"
  sha256sum "$dst/stella_full.png" >"$dst/image_sha256.txt"
done
