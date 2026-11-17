#!/usr/bin/env bash
# F9 original unchanged ONE ROM; 8 actual RAM modes, each 6 separate
# real Stella GUI traps: RESP1/GRP1 for M,F,SM = 48 genuine screenshots.
# CPU/TIA register write traps are not internal START latch measurements.
set -euo pipefail
cd "$(dirname "$0")"
export SDL_AUDIODRIVER=dummy SDL_VIDEODRIVER=x11 DISPLAY=:125
home="$(getent passwd "$(id -un)" | cut -d: -f6)"
out="evidence/r1_f9_one_rom/traps"
mkdir -p "$home/.config/stella" "$out"
rom="$PWD/dist/r1_f9_three_masks_three_binary_ram_x_ONE_ROM_F6.bin"
test "$(stat -c %s "$rom")" -eq 16384
Xvfb :125 -screen 0 1366x900x24 -ac > "$out/xvfb.log" 2>&1 &
xp=$!
trap 'kill "$xp" 2>/dev/null || true' EXIT
sleep 2
# Source-frame 135,151,... in each of the 8 Gray 16-frame states.
while read -r bits frame first second third;do
 case "$bits" in
   000|001|011|010|110|111|101|100) ;;
   *)echo "F9_UNAUTHORIZED_RAM_MODE";exit 3;;
 esac
 for k in 1 2 3 4 5 6;do
  case "$k" in
    1)label=M_RESP1;reg=RESP1;center="$first";;
    2)label=M_GRP1;reg=GRP1;center=$((first+3));;
    3)label=F_RESP1;reg=RESP1;center="$second";;
    4)label=F_GRP1;reg=GRP1;center=$((second+3));;
    5)label=SM_RESP1;reg=RESP1;center="$third";;
    6)label=SM_GRP1;reg=GRP1;center=$((third+3));;
  esac
  low=$((center-2)); high=$((center+2))
  dir="$out/mode_$bits/$label";mkdir -p "$dir"
  printf 'base #10\nframe #%s\ntrapWriteIf {_scan == #123 && _sCycles > #%s && _sCycles < #%s} %s\nrun\n' \
    "$frame" "$low" "$high" "$reg" > "$home/.config/stella/autoexec.script"
  cp "$home/.config/stella/autoexec.script" "$dir/autoexec.script"
  stella -debug -bs F6 -format NTSC -video software -vsync 0 -audio.enabled 0 "$rom" > "$dir/stella.log" 2>&1 &
  pid=$!
  ok=0
  for t in $(seq 1 16);do
    sleep 1
    if ! kill -0 "$pid";then echo "F9_STELLA_TRAP_PROCESS_DIED $bits $label";cat "$dir/stella.log";break;fi
    import -window root "$dir/stella_full.png"
    if /usr/bin/python3 - "$dir/stella_full.png" <<'PY'
from PIL import Image
import sys
im=Image.open(sys.argv[1]).convert("RGB")
assert im.size==(1366,900)
r,g,b=im.getpixel((800,100))
assert r>100 and g>85 and b>50,(r,g,b)
PY
    then ok=1;echo "F9_REAL_STELLA_REGISTER_GUI_TRAP $bits frame=$frame $label $reg CPU_expected=$center";break;fi
  done
  kill "$pid" 2>/dev/null || true;wait "$pid" 2>/dev/null || true
  if [[ "$ok" != 1 ]];then
    printf 'F9_UNMEASURABLE_NO_CLAIM\n' > "$dir/UNMEASURABLE.txt"
    echo "F9_FAIL_NO_VALID_TIA_TRAP $bits $label"
    exit 5
  fi
 done
done <<'EOF'
000 136 21 32 48
001 152 21 32 50
011 168 21 33 50
010 184 21 33 48
110 200 23 33 48
111 216 23 33 50
101 232 23 32 50
100 248 23 32 48
EOF
find "$out" -name stella_full.png -print0 | sort -z | xargs -0 sha256sum > "$out/REAL_F9_48_TIA_PC_BANK_CYCLE_TRAPS_SHA256SUMS.txt"
test "$(find "$out" -name stella_full.png | wc -l)" -eq 48
test "$(find "$out" -name UNMEASURABLE.txt | wc -l)" -eq 0
echo "F9_48_GENUINE_TIA_PC_BANK_CYCLE_GUI_TRAPS_EIGHT_RAM_MODES"
