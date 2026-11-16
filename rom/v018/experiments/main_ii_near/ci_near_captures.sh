#!/usr/bin/env bash
# Real Stella X11 captures for near 60/51 color-clock RESP1 spacing.
set -euo pipefail
cd "$(dirname "$0")"
ROOT="$PWD"
mkdir -p evidence
export SDL_AUDIODRIVER=dummy SDL_VIDEODRIVER=x11
ACTUAL_HOME="$(getent passwd "$(id -un)" | cut -d: -f6)"
mkdir -p "$ACTUAL_HOME/.config/stella"
Xvfb :126 -screen 0 1366x900x24 -ac >evidence/xvfb.log 2>&1 &
XVPID=$!
trap 'kill "$XVPID" 2>/dev/null || true' EXIT
export DISPLAY=:126
sleep 2
# Prime the actual ROM in the actual mode, discard first GUI initialization.
echo 'base #10' >"$ACTUAL_HOME/.config/stella/autoexec.script"
echo 'frame #13' >>"$ACTUAL_HOME/.config/stella/autoexec.script"
stella -debug -bs F6 -format NTSC -video software -vsync 0 -audio.enabled 0 "$ROOT/near57/proof_F6.bin" > evidence/warmup.log 2>&1 &
warm=$!
sleep 7
kill "$warm" 2>/dev/null || true
wait "$warm" 2>/dev/null || true
for variant in near57; do
  folder="$ROOT/$variant"
  for pair in 0:13 1:29 2:45 3:61; do
    name="${pair%%:*}"; frame="${pair##*:}"
    dest="$folder/evidence/phase_$name"; mkdir -p "$dest"
    cp "$folder/proof_F6.bin" "$dest/proof.bin"
    cp "$folder/proof.sym" "$dest/proof.sym"
    cp "$folder/proof.lst" "$dest/proof.lst"
    {
      echo 'base #10'
      echo "frame #$frame"
      echo 'print _fCount'
      echo 'print _scanEnd'
      echo 'print _bank'
    } > "$dest/commands.txt"
    cp "$dest/commands.txt" "$ACTUAL_HOME/.config/stella/autoexec.script"
    stella -debug -bs F6 -format NTSC -video software -vsync 0 -audio.enabled 0 "$dest/proof.bin" > "$dest/stdout.txt" 2>&1 &
    pid=$!
    sleep 7
    kill -0 "$pid"
    for retry in 1 2 3; do
      import -window root "$dest/stella_full.png"
      colors="$(identify -format '%k' "$dest/stella_full.png")"
      test "$colors" -gt 5 && break
      sleep 3
    done
    test "$colors" -gt 5 || { echo "No valid Stella screenshot for $variant phase $name" >&2; exit 1; }
    kill "$pid" || true
    wait "$pid" 2>/dev/null || true
    sha256sum "$dest/stella_full.png" > "$dest/image.sha256"
  done
  for symbol in R1bFirstRESP1 R1bFemaleWrite R1bSecondRESP1; do
    dest="$folder/evidence/pc_$symbol"; mkdir -p "$dest"
    cp "$folder/proof_F6.bin" "$dest/proof.bin"
    cp "$folder/proof.sym" "$dest/proof.sym"
    cp "$folder/proof.lst" "$dest/proof.lst"
    addr=$(awk -v sym="$symbol" 'tolower($1)==tolower(sym) {print $2;exit}' "$folder/proof.sym")
    test -n "$addr"
    {
      echo 'base #10'
      echo 'frame #13'
      printf 'runToPc $%s\n' "$addr"
      echo 'print _scan'
      echo 'print _sCycles'
      echo 'print _bank'
    } > "$dest/commands.txt"
    cp "$dest/commands.txt" "$ACTUAL_HOME/.config/stella/autoexec.script"
    stella -debug -bs F6 -format NTSC -video software -vsync 0 -audio.enabled 0 "$dest/proof.bin" >"$dest/stdout.txt" 2>&1 &
    pid=$!
    sleep 7
    kill -0 "$pid"
    import -window root "$dest/stella_full.png"
    test "$(identify -format '%k' "$dest/stella_full.png")" -gt 5
    kill "$pid" || true
    wait "$pid" 2>/dev/null || true
    sha256sum "$dest/stella_full.png" >"$dest/image.sha256"
  done
  cp ../main_ii_r1b/pixel_audit.py "$folder/pixel_audit.py"
  echo "$variant finished 4 phase frames and 3 PC captures"
done
