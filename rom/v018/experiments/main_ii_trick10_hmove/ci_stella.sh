#!/usr/bin/env bash
# Four actual Stella 6.7.1 phase captures plus a real HMOVE pre-write PC stop.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p evidence
export SDL_AUDIODRIVER=dummy SDL_VIDEODRIVER=x11
ACTUAL_HOME="$(getent passwd "$(id -un)" | cut -d: -f6)"
mkdir -p "$ACTUAL_HOME/.config/stella"
Xvfb :151 -screen 0 1366x900x24 -ac > evidence/xvfb.log 2>&1 &
XVFB_PID=$!
trap 'kill "$XVFB_PID" 2>/dev/null || true' EXIT
export DISPLAY=:151
sleep 2
# Discard initialization GUI, which can be a black frame on fresh Xvfb.
printf 'base #10\nframe #2\n' > "$ACTUAL_HOME/.config/stella/autoexec.script"
stella -debug -bs F6 -format NTSC -video software -vsync 0 -audio.enabled 0 "$PWD/trick10_F6.bin" > evidence/init.log 2>&1 &
init=$!
sleep 5
kill "$init" 2>/dev/null || true
wait "$init" 2>/dev/null || true
for entry in 0:13 1:29 2:45 3:61; do
    phase="$(echo "$entry"|cut -d: -f1)"
    target="$(echo "$entry"|cut -d: -f2)"
    dst="evidence/phase_$phase";mkdir -p "$dst"
    cp trick10_F6.bin "$dst/proof.bin"
    cp trick10.sym "$dst/proof.sym"
    cp trick10.lst "$dst/proof.lst"
    {
      echo 'base #10'
      echo "frame #$target"
      echo 'print _fCount'
      echo 'print _scanEnd'
      echo 'print _bank'
      echo 'print _scan'
      echo 'print _sCycles'
    } > "$dst/commands.txt"
    cp "$dst/commands.txt" "$ACTUAL_HOME/.config/stella/autoexec.script"
    stella -debug -bs F6 -format NTSC -video software -vsync 0 -audio.enabled 0 "$PWD/$dst/proof.bin" >"$dst/stella_stdout.txt" 2>&1 &
    pid=$!
    sleep 7
    kill -0 "$pid"
    for attempt in 1 2 3 4; do
      import -window root "$dst/stella_full.png"
      colors="$(identify -format '%k' "$dst/stella_full.png")"
      if [ "$colors" -gt 5 ]; then break; fi
      echo "Re-attempt Stella phase $phase shot $attempt" >&2
      sleep 3
    done
    test "$colors" -gt 5 || { echo "Capture black/invalid: phase $phase" >&2;exit 2; }
    kill "$pid" || true
    wait "$pid" 2>/dev/null || true
    sha256sum "$dst/stella_full.png" > "$dst/image.sha256"
done
mkdir -p evidence/hmove_pc
cp trick10_F6.bin evidence/hmove_pc/proof.bin
cp trick10.sym evidence/hmove_pc/proof.sym
cp trick10.lst evidence/hmove_pc/proof.lst
addr="$(awk 'tolower($1)=="hmovestrobe" {print $2;exit}' trick10.sym)"
test -n "$addr"
{
  echo 'base #10'
  echo 'frame #13'
  printf 'runToPc $%s\n' "$addr"
  echo 'print _fCount'
  echo 'print _bank'
  echo 'print _scan'
  echo 'print _sCycles'
  echo 'print *$20'
  echo 'print *$21'
  echo 'print *$22'
} >evidence/hmove_pc/commands.txt
cp evidence/hmove_pc/commands.txt "$ACTUAL_HOME/.config/stella/autoexec.script"
stella -debug -bs F6 -format NTSC -video software -vsync 0 -audio.enabled 0 "$PWD/evidence/hmove_pc/proof.bin" >evidence/hmove_pc/stella_stdout.txt 2>&1 &
pid=$!
sleep 7
kill -0 "$pid"
import -window root evidence/hmove_pc/stella_full.png
test "$(identify -format '%k' evidence/hmove_pc/stella_full.png)" -gt 5
kill "$pid" || true
wait "$pid" 2>/dev/null || true
sha256sum evidence/hmove_pc/stella_full.png >evidence/hmove_pc/image.sha256
