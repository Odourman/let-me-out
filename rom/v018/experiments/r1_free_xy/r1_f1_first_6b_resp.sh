#!/usr/bin/env bash
# R1-F1: ONE non-A/B read-only recapture of the first 6B RESP1, source row05.
# Previous first Xvfb shot was black; wait for visible debugger UI before capture.
set -euo pipefail
cd "$(dirname "$0")"
export SDL_AUDIODRIVER=dummy SDL_VIDEODRIVER=x11 DISPLAY=:117
h="$(getent passwd "$(id -un)" | cut -d: -f6)"
mkdir -p "$h/.config/stella" evidence/r1_f1_first_6B_resp
Xvfb :117 -screen 0 1366x900x24 -ac > evidence/r1_f1_first_6B_resp/xvfb.log 2>&1 &
xpid=$!
trap 'kill "$xpid" 2>/dev/null || true' EXIT
sleep 2
printf 'base #10\nframe #12\ntrapWriteIf {_scan == #123 && _sCycles > #17 && _sCycles < #21} RESP1\nrun\n' > "$h/.config/stella/autoexec.script"
cp "$h/.config/stella/autoexec.script" evidence/r1_f1_first_6B_resp/autoexec.script
stella -debug -bs F6 -format NTSC -video software -vsync 0 -audio.enabled 0 "$PWD/dist/r1_individual_6B_F6.bin" > evidence/r1_f1_first_6B_resp/stella.log 2>&1 &
pid=$!
ok=0
for attempt in $(seq 1 12); do
  sleep 1
  kill -0 "$pid"
  xdotool search --onlyvisible --name Stella > evidence/r1_f1_first_6B_resp/windows.txt || true
  import -window root evidence/r1_f1_first_6B_resp/stella_full.png
  if python3 - <<'PY'
from PIL import Image
im=Image.open('evidence/r1_f1_first_6B_resp/stella_full.png').convert('RGB')
p=im.getpixel((800,100))
if not (p[0]>100 and p[1]>85 and p[2]>50):raise SystemExit(1)
PY
  then
    ok=1; echo "STELLA_FIRST_6B_RESP_GUI_READY after_attempt=$attempt"
    break
  fi
done
kill "$pid" 2>/dev/null || true
wait "$pid" 2>/dev/null || true
sha256sum evidence/r1_f1_first_6B_resp/stella_full.png > evidence/r1_f1_first_6B_resp/SHA256SUMS.txt
test "$ok" -eq 1 || { echo "NO_AUTHENTIC_GUI_TRAP: source-only cycle c19"; exit 1; }
