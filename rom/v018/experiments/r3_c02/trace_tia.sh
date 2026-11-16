#!/usr/bin/env bash
# Actual Stella 6.7 debugger TIA write trap snapshots, NOT static cycle guesses.
set -euo pipefail
cd "$(dirname "$0")"
ROOT="$PWD"
OUT="$ROOT/evidence/register_traps"
mkdir -p "$OUT" "$OUT/home"
export HOME="$OUT/home" SDL_AUDIODRIVER=dummy SDL_VIDEODRIVER=x11
REAL_HOME="$(getent passwd "$(id -un)" | cut -d: -f6)"
mkdir -p "$REAL_HOME/.config/stella"
Xvfb :111 -screen 0 1366x900x24 -ac >"$OUT/xvfb.log" 2>&1 &
VPID=$!
trap 'kill "$VPID" 2>/dev/null || true' EXIT
export DISPLAY=:111
sleep 1
for item in left_pf0:PF0:small left_pf1:PF1:small left_pf2:PF2:small right_pf0:PF0:large right_pf1:PF1:large right_pf2:PF2:large keyhole_grp1:GRP1:large; do
  IFS=: read -r name reg pos <<<"$item"
  d="$OUT/$name"
  mkdir -p "$d"
  cp dist/LetMeOut_v018_R3_C02_F6_NTSC.bin "$d/test.bin"
  cp dist/r3_c02.sym "$d/test.sym"
  cp dist/r3_c02.lst "$d/test.lst"
  if test "$pos" = large; then
    cond="{ _scan == #134 && _sCycles > #30 }"
  else
    cond="{ _scan == #134 && _sCycles < #30 }"
  fi
  cat >"$REAL_HOME/.config/stella/autoexec.script" <<EOF
base #10
frame #90
trapWriteIf $cond $reg
run
EOF
  stella -debug -bs F6 -format NTSC -video software -vsync 0 -audio.enabled 0 "$d/test.bin" > "$d/stella.log" 2>&1 &
  pid=$!
  sleep 6
  if ! kill -0 "$pid" 2>/dev/null; then cat "$d/stella.log"; exit 1; fi
  import -window root "$d/trace_full.png"
  test -s "$d/trace_full.png"
  kill "$pid" 2>/dev/null || true
  wait "$pid" 2>/dev/null || true
  echo "Captured $name real GUI: $d/trace_full.png"
done
