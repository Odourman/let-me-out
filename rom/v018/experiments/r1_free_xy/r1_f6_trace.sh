#!/usr/bin/env bash
# R1-F6 genuine Stella debugger register traps on actual scanline123.
# One fresh instance of the SAME pinned probe ROM for each target write.
set -euo pipefail
phase="$1"
[[ "$phase" == 21 || "$phase" == 23 ]] || exit 2
cd "$(dirname "$0")"
export SDL_AUDIODRIVER=dummy SDL_VIDEODRIVER=x11 DISPLAY=:123
home="$(getent passwd "$(id -un)" | cut -d: -f6)"
romfile="$(printf 'r1_f6_two_correct_masks_C%02d_C32_F6.bin' "$phase")"
rom="$PWD/dist/$romfile"
out="evidence/r1_f6_c$(printf '%02d' "$phase")/traps"
mkdir -p "$home/.config/stella" "$out"
Xvfb :123 -screen 0 1366x900x24 -ac > "$out/xvfb.log" 2>&1 &
xp=$!
trap 'kill "$xp" 2>/dev/null || true' EXIT
sleep 2
grp=$((phase+3))
set -- \
 "01_FIRST_RESP1 RESP1 $((phase-2)) $((phase+2))" \
 "02_FIRST_GRP1 GRP1 $((grp-2)) $((grp+2))" \
 "03_SECOND_RESP1 RESP1 30 34" \
 "04_SECOND_GRP1 GRP1 33 37" \
 "05_LAST_VISIBLE_WSYNC WSYNC 36 42"
for spec in "$@";do
 read -r label reg low high <<< "$spec"
 d="$out/$label";mkdir -p "$d"
 printf 'base #10\nframe #12\ntrapWriteIf {_scan == #123 && _sCycles > #%s && _sCycles < #%s} %s\nrun\n' \
    "$low" "$high" "$reg" > "$home/.config/stella/autoexec.script"
 cp "$home/.config/stella/autoexec.script" "$d/autoexec.script"
 stella -debug -bs F6 -format NTSC -video software -vsync 0 -audio.enabled 0 "$rom" > "$d/stella.log" 2>&1 &
 pid=$!
 ready=0
 for t in $(seq 1 18);do
   sleep 1
   if ! kill -0 "$pid" 2>/dev/null;then cat "$d/stella.log";break;fi
   import -window root "$d/stella_full.png"
   if /usr/bin/python3 - "$d/stella_full.png" <<'PY'
from PIL import Image
import sys
im=Image.open(sys.argv[1]).convert('RGB')
assert im.size==(1366,900)
r,g,b=im.getpixel((800,100))
assert r>100 and g>85 and b>50, (r,g,b)
PY
   then ready=1;echo "F6_GUI_TRAP_SCREENSHOT_READY $phase $label $reg attempt=$t";break;fi
 done
 kill "$pid" 2>/dev/null || true; wait "$pid" 2>/dev/null || true
 if [[ "$ready" != 1 ]];then
   printf '%s\n' "INCONCLUSIVE GUI never showed a valid trap screenshot" > "$d/UNMEASURABLE.txt"
   echo "F6_MISSING_VALID_TRAP $phase $label"
 fi
done
find "$out" -name stella_full.png -print0 | sort -z | xargs -0 sha256sum > "$out/REAL_GUI_TRAP_PNG_SHA256.txt"
echo "F6_REAL_TIA_REGISTER_TRAP_EXECUTION_COMPLETED $phase"
