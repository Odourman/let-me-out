#!/usr/bin/env bash
# Four genuine Stella TIA trap probes per selected 9-line raster: RESP1/GRP1
# early + late, plus NUSIZ1/HMOVE in VBLANK. Captures actual debugger HUD.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p evidence/traps
REAL_HOME="$(getent passwd "$(id -un)" | cut -d: -f6)"
mkdir -p "$REAL_HOME/.config/stella"
export SDL_AUDIODRIVER=dummy SDL_VIDEODRIVER=x11
Xvfb :118 -screen 0 1366x900x24 -ac >evidence/traps/xvfb.log 2>&1 &
XVFBPID=$!
trap 'kill "$XVFBPID" 2>/dev/null || true' EXIT
export DISPLAY=:118
sleep 1
for test_case in first_resp:RESP1:early first_grp:GRP1:early second_resp:RESP1:late second_grp:GRP1:late nusiz:NUSIZ1:any hmove:HMOVE:any; do
 IFS=: read -r name reg which <<< "$test_case"
 dir="evidence/traps/$name"
 mkdir -p "$dir"
 cp dist/r1_two.sym "$dir/trace.sym"
 cp dist/r1_two.lst "$dir/trace.lst"
 if test "$which" = early; then
   condition='{_scan == #124 && _sCycles < #40}'
 elif test "$which" = late; then
   condition='{_scan == #124 && _sCycles > #40}'
 else
   condition='{_scan < #40}'
 fi
 cat >"$REAL_HOME/.config/stella/autoexec.script" <<ESCRIPT
base #10
frame #12
trapWriteIf $condition $reg
run
ESCRIPT
 stella -debug -bs F6 -format NTSC -video software -vsync 0 -audio.enabled 0 "$PWD/dist/LetMeOut_R1_TWO_2x2_F6.bin" >"$dir/stdout.txt" 2>&1 &
 pid=$!
 sleep 4
 if ! kill -0 "$pid" 2>/dev/null; then cat "$dir/stdout.txt"; exit 1; fi
 import -window root "$dir/stella_full.png"
 test -s "$dir/stella_full.png"
 kill "$pid" 2>/dev/null || true
 wait "$pid" 2>/dev/null || true
 echo "REAL_STELLA_TRAP_CAPTURE $name"
done
