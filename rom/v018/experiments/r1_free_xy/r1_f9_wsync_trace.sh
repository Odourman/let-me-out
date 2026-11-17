#!/usr/bin/env bash
# R1-F9 supplementary WSYNC AFTER-WRITE real Stella screenshots, SAME frozen
# one 16KiB ROM, eight actual source RAM modes, NO assembler/no rebuild.
# CPU source c54/c56 vs post-write Stella next scanline/c0 MUST be distinct.
set -euo pipefail
cd "$(dirname "$0")"
export SDL_AUDIODRIVER=dummy SDL_VIDEODRIVER=x11 DISPLAY=:126
home="$(getent passwd "$(id -un)" | cut -d: -f6)"
rom="$PWD/dist/r1_f9_three_masks_three_binary_ram_x_ONE_ROM_F6.bin"
test "$(stat -c%s "$rom")" -eq 16384
printf '%s  %s\n' 6c2585148eb082fb8bc794d664edc4869b18849fcfabb9cada23373d1dc1318b "$rom" | sha256sum -c
out="evidence/r1_f9_same_rom_wsync_after"
mkdir -p "$home/.config/stella" "$out"
Xvfb :126 -screen 0 1366x900x24 -ac > "$out/xvfb.log" 2>&1 &
xp=$!
trap 'kill "$xp" 2>/dev/null || true' EXIT
sleep 2
while read -r bits frame wsync;do
 low=$((wsync-2)); high=$((wsync+2))
 d="$out/mode_$bits";mkdir -p "$d"
 printf 'base #10\nframe #%s\ntrapWriteIf {_scan == #123 && _sCycles > #%s && _sCycles < #%s} WSYNC\nrun\n' \
   "$frame" "$low" "$high" > "$home/.config/stella/autoexec.script"
 cp "$home/.config/stella/autoexec.script" "$d/autoexec.script"
 stella -debug -bs F6 -format NTSC -video software -vsync 0 -audio.enabled 0 "$rom" > "$d/stella.log" 2>&1 &
 pid=$!;ok=0
 for t in $(seq 1 16);do
  sleep 1
  if ! kill -0 "$pid";then cat "$d/stella.log";break;fi
  import -window root "$d/stella_full.png"
  if /usr/bin/python3 - "$d/stella_full.png" <<'PY'
from PIL import Image
import sys
im=Image.open(sys.argv[1]).convert("RGB")
assert im.size==(1366,900)
r,g,b=im.getpixel((800,100))
assert r>100 and g>85 and b>50
PY
  then ok=1;echo "F9_WSYNCACTUAL_NEXT_SCANLINE_GUI_CAPTURED mode=$bits FRAME=$frame WSYNC_SOURCE_CPU=$wsync";break;fi
 done
 kill "$pid" 2>/dev/null || true; wait "$pid" 2>/dev/null || true
 if [[ "$ok" != 1 ]];then echo "F9_WSYNC_TRAP_UNMEASURABLE $bits" > "$d/UNMEASURABLE.txt";exit 5;fi
done <<'EOF'
000 136 54
001 152 56
011 168 56
010 184 54
110 200 54
111 216 56
101 232 56
100 248 54
EOF
test "$(find "$out" -name stella_full.png | wc -l)" -eq 8
test "$(find "$out" -name UNMEASURABLE.txt | wc -l)" -eq 0
find "$out" -name stella_full.png -print0 | sort -z | xargs -0 sha256sum > "$out/REAL_EIGHT_WSYNC_AFTER_WRITE_GUI_SHA256SUMS.txt"
echo "F9_SUPPLEMENTAL_WSYNC_SOURCE_C54_C56_ALL_8_REAL_STELLA_GUI_DONE"
