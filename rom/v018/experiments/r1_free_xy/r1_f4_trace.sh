#!/usr/bin/env bash
# Genuine F4 Stella read-only register/cycle traces, one unchanged ROM.
# Each trap is a fresh emulator session; GUI startup screenshots that are black
# MUST NOT be counted as a valid CPU measurement.
set -euo pipefail
phase="${1:?phase 18 or 21}"
[[ "$phase" == 18 || "$phase" == 21 ]] || exit 2
cd "$(dirname "$0")"
export SDL_AUDIODRIVER=dummy SDL_VIDEODRIVER=x11 DISPLAY=:121
home="$(getent passwd "$(id -un)" | cut -d: -f6)"
stem="r1_f4_6B_I0_C$(printf '%02d' "$phase")_I2_FIXED"
out="evidence/r1_f4_c$(printf '%02d' "$phase")/traps"
mkdir -p "$home/.config/stella" "$out"
Xvfb :121 -screen 0 1366x900x24 -ac > "$out/xvfb.log" 2>&1 &
xp=$!
trap 'kill "$xp" 2>/dev/null || true' EXIT
sleep 2
grp=$(( phase+3 ))
specs=(
  "01_INDEX0_RESP1 RESP1 $((phase-2)) $((phase+2))"
  "02_INDEX0_GRP1 GRP1 $((grp-2)) $((grp+2))"
  "03_INDEX1_RESP1 RESP1 26 30"
  "04_INDEX2_RESP1 RESP1 35 39"
  "05_LAST_GRP1 GRP1 67 71"
  "06_WSYNC WSYNC 70 74"
)
rom="$PWD/dist/${stem}_F6.bin"
for spec in "${specs[@]}";do
 read -r label reg low high <<< "$spec"
 dir="$out/$label";mkdir -p "$dir"
 printf 'base #10\nframe #12\ntrapWriteIf {_scan == #123 && _sCycles > #%s && _sCycles < #%s} %s\nrun\n' \
   "$low" "$high" "$reg" > "$home/.config/stella/autoexec.script"
 cp "$home/.config/stella/autoexec.script" "$dir/autoexec.script"
 stella -debug -bs F6 -format NTSC -video software -vsync 0 -audio.enabled 0 "$rom" > "$dir/stella.log" 2>&1 &
 pid=$!
 ok=0
 for t in $(seq 1 14);do
   sleep 1
   if ! kill -0 "$pid" 2>/dev/null;then cat "$dir/stella.log";break;fi
   import -window root "$dir/stella_full.png"
   if /usr/bin/python3 - "$dir/stella_full.png" <<'PY'
from PIL import Image
import sys
im=Image.open(sys.argv[1]).convert('RGB')
if im.size!=(1366,900):raise SystemExit(1)
r,g,b=im.getpixel((800,100))
if not (r>100 and g>85 and b>50):raise SystemExit(1)
PY
   then ok=1;echo "F4_REAL_GUI_VISIBLE $label $reg phase=$phase screenshot_attempt=$t";break;fi
 done
 kill "$pid" 2>/dev/null || true;wait "$pid" 2>/dev/null || true
 if [[ "$ok" != 1 ]];then
    echo "F4_MISSING_USABLE_REGISTER_TRAP $label; screenshot incomplete, not claimed as actual"
    printf '%s\n' "INCONCLUSIVE no valid GUI screenshot" > "$dir/UNMEASURABLE.txt"
 fi
done
find "$out" -name stella_full.png -print0 | sort -z | xargs -0 sha256sum > "$out/REAL_TIA_TRAP_PNG_SHA256.txt"
echo "F4_REAL_STELLA_TRAP_RUN_COMPLETE phase=$phase (inspect PC and actual cycles in each screen)"
