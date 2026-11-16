#!/usr/bin/env bash
# Sole missing R1-F3 G0 actual first P1 reset. READ ONLY (no other ROM variant).
set -euo pipefail
cd "$(dirname "$0")"
export SDL_AUDIODRIVER=dummy SDL_VIDEODRIVER=x11 DISPLAY=:117
h="$(getent passwd "$(id -un)" | cut -d: -f6)"
out="evidence/r1_f3_g0_first_resp_retry"
mkdir -p "$h/.config/stella" "$out"
Xvfb :117 -screen 0 1366x900x24 -ac > "$out/xvfb.log" 2>&1 &
xp=$!;trap 'kill "$xp" 2>/dev/null || true' EXIT
sleep 2
printf 'base #10\nframe #12\ntrapWriteIf {_scan == #123 && _sCycles > #18 && _sCycles < #22} RESP1\nrun\n' > "$h/.config/stella/autoexec.script"
cp "$h/.config/stella/autoexec.script" "$out/autoexec.script"
stella -debug -bs F6 -format NTSC -video software -vsync 0 -audio.enabled 0 "$PWD/dist/r1_f3_6B_I0_P1_I2_FIXED_F6.bin" > "$out/stella.log" 2>&1 &
pid=$!
ok=0
for t in $(seq 1 12);do
 sleep 1
 kill -0 "$pid" || { cat "$out/stella.log";exit 1; }
 import -window root "$out/stella_full.png"
 if python3 - "$out/stella_full.png" <<'PY'
import sys
from PIL import Image
r,g,b=Image.open(sys.argv[1]).convert('RGB').getpixel((800,100))
if not (r>100 and g>85 and b>50):raise SystemExit(1)
PY
 then ok=1;echo "F3_G0_FIRST_RESP1_GUI_CONFIRMED attempt=$t";break;fi
done
kill "$pid" 2>/dev/null||true;wait "$pid" 2>/dev/null||true
sha256sum "$out/stella_full.png" > "$out/RAW_SHA256.txt"
test "$ok" = 1 || { echo 'F3_G0_FIRST_RESP1_STILL_INCONCLUSIVE_TRAP';exit 1; }
