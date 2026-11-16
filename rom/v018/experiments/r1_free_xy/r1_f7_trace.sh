#!/usr/bin/env bash
# F7 genuine TIA traps in 4 RAM-selected modes, unchanged ONE ROM.
set -euo pipefail
cd "$(dirname "$0")"
export SDL_AUDIODRIVER=dummy SDL_VIDEODRIVER=x11 DISPLAY=:125
home="$(getent passwd "$(id -un)" | cut -d: -f6)"
out="evidence/r1_f7_one_rom/traps"
mkdir -p "$home/.config/stella" "$out"
rom="$PWD/dist/r1_f7_2x2_independent_RAM_X_ONE_ROM_F6.bin"
Xvfb :125 -screen 0 1366x900x24 -ac > "$out/xvfb.log" 2>&1 &
xp=$!
trap 'kill "$xp" 2>/dev/null || true' EXIT
sleep 2
while read -r bits frame first second;do
  fgrp=$((first+3));sgrp=$((second+3))
  for k in 1 2 3 4;do
    case "$k" in
      1)label=FIRST_RESP1;reg=RESP1;center="$first";;
      2)label=FIRST_GRP1;reg=GRP1;center="$fgrp";;
      3)label=SECOND_RESP1;reg=RESP1;center="$second";;
      4)label=SECOND_GRP1;reg=GRP1;center="$sgrp";;
    esac
    low=$((center-2));high=$((center+2))
    dir="$out/mode_$bits/$label";mkdir -p "$dir"
    printf 'base #10\nframe #%s\ntrapWriteIf {_scan == #123 && _sCycles > #%s && _sCycles < #%s} %s\nrun\n' \
      "$frame" "$low" "$high" "$reg" > "$home/.config/stella/autoexec.script"
    cp "$home/.config/stella/autoexec.script" "$dir/autoexec.script"
    stella -debug -bs F6 -format NTSC -video software -vsync 0 -audio.enabled 0 "$rom" > "$dir/stella.log" 2>&1 &
    pid=$!
    ok=0
    for t in $(seq 1 16);do
      sleep 1
      if ! kill -0 "$pid";then cat "$dir/stella.log";break;fi
      import -window root "$dir/stella_full.png"
      if /usr/bin/python3 - "$dir/stella_full.png" <<'PY'
from PIL import Image
import sys
im=Image.open(sys.argv[1]).convert("RGB")
assert im.size==(1366,900)
r,g,b=im.getpixel((800,100))
assert r>100 and g>85 and b>50
PY
      then ok=1;echo "F7_REAL_GUI_TRAP $bits $frame $label $reg attempt=$t";break;fi
    done
    kill "$pid" 2>/dev/null || true;wait "$pid" 2>/dev/null || true
    if [[ "$ok" != 1 ]];then
      printf 'INVALID_UNMEASURABLE_TRAP\n' > "$dir/UNMEASURABLE.txt"
      echo "F7_MISSING_VALID_REGISTER_TRAP $bits $label"
    fi
  done
done <<'EOF'
00 12 21 32
10 20 23 32
01 52 21 33
11 68 23 33
EOF
find "$out" -name stella_full.png -print0 | sort -z | xargs -0 sha256sum > "$out/REAL_F7_16_REG_TRAPS_SHA256SUMS.txt"
test "$(find "$out" -name stella_full.png | wc -l)" -eq 16
test "$(find "$out" -name UNMEASURABLE.txt | wc -l)" -eq 0
echo "F7_TIA_16_REAL_REGISTER_TRAP_SCREENS_ACROSS_FOUR_RUNTIME_RAM_MODES"
