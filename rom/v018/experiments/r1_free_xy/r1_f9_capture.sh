#!/usr/bin/env bash
# F9 ONE immutable ROM. 144 genuine Stella frames from frame #128:
# CPU frame#129..272, RAM FRAMELO128..271, nine 16-frame Gray stages
# 000 ->001 ->011 ->010 ->110 ->111 ->101 ->100 ->000.
set -euo pipefail
cd "$(dirname "$0")"
export SDL_AUDIODRIVER=dummy SDL_VIDEODRIVER=x11 DISPLAY=:124
home="$(getent passwd "$(id -un)" | cut -d: -f6)"
stem="r1_f9_three_masks_three_binary_ram_x_ONE_ROM"
out="evidence/r1_f9_one_rom"
mkdir -p "$home/.config/stella" "$out/raw" "$out/raw_full" "$out/guard"
rom="$PWD/dist/$stem""_F6.bin"
test "$(stat -c %s "$rom")" -eq 16384
echo "F9_ONE_IMMUTABLE_ROM_SHA $(sha256sum "$rom" | cut -d' ' -f1)"
Xvfb :124 -screen 0 1366x900x24 -ac > "$out/xvfb.log" 2>&1 &
xp=$!
pid=""
trap '[[ -z "$pid" ]] || kill "$pid" 2>/dev/null || true; kill "$xp" 2>/dev/null || true' EXIT
sleep 2
printf 'base #10\nframe #128\nprint _fCount\nprint _scanEnd\n' > "$home/.config/stella/autoexec.script"
cp "$home/.config/stella/autoexec.script" "$out/autoexec.script"
stella -debug -bs F6 -format NTSC -video software -vsync 0 -audio.enabled 0 "$rom" > "$out/stella.log" 2>&1 &
pid=$!
wid=""
for t in $(seq 1 22);do
 if ! kill -0 "$pid";then echo "F9_STELLA_PROCESS_DIED";cat "$out/stella.log";exit 4;fi
 wid="$(xdotool search --onlyvisible --name Stella 2>/dev/null | head -n1 || true)"
 if [[ -n "$wid" ]];then break;fi
 sleep 1
done
if [[ -z "$wid" ]];then echo "F9_NO_VISIBLE_STELLA_WINDOW";exit 5;fi
ready=0
for t in $(seq 1 22);do
 import -window root "$out/GUI_READINESS_PROBE.png"
 if /usr/bin/python3 - "$out/GUI_READINESS_PROBE.png" <<'PY'
from PIL import Image
import sys
im=Image.open(sys.argv[1]).convert("RGB")
assert im.size==(1366,900)
r,g,b=im.getpixel((250,450))
assert r>200 and g>200 and b>160 and abs(r-g)<30,(r,g,b)
PY
 then ready=1;echo "F9_REAL_DEBUGGER_GUI_READY $t";break;fi
 sleep 1
done
if [[ "$ready" != 1 ]];then echo "F9_INFRA_GUI_UNMEASURABLE_NO_GEOMETRY_CLAIM";exit 5;fi
wid="$(xdotool search --onlyvisible --name Stella 2>/dev/null | head -n1 || true)"
test -n "$wid"
xdotool windowfocus --sync "$wid"
sleep 0.3
import -window root "$out/initial_uncropped_GUI.png"
for ((i=1;i<=144;i++));do
 xdotool key --window "$wid" --clearmodifiers ctrl+f
 sleep 0.055
 index="$(printf '%03d' "$i")"
 import -window root "$out/raw_full/frame_$index.png"
 import -window root -crop 900x300+103+65 "$out/raw/frame_$index.png"
 if [[ "$i" -eq 1 || $((i%16)) -eq 0 ]];then
  /usr/bin/python3 - "$out/raw/frame_$index.png" "$i" "$out/guard" <<'PY'
import json,sys,hashlib
from pathlib import Path
from PIL import Image
import r1_f9_audit as A
png=Path(sys.argv[1]);i=int(sys.argv[2]);folder=Path(sys.argv[3])
gray=["000","001","011","010","110","111","101","100","000"]
mode=gray[(i-1)//16]
requested=A.g["all_72_rows_SOURCE_ONLY"][mode]["preregistered_cropped_X"]
with Image.open(png) as im:r=A.inspect(im)
ok=bool(r["strict"] and r["rendered_X"]==requested)
record={"true_UNMODIFIED_Stella_image":png.name,"real_png_sha256":hashlib.sha256(png.read_bytes()).hexdigest(),
 "frame_sample_index":i,"Stella_frame_expected":128+i,"FRAMELO_expected":127+i,
 "RAM_mode_source_expected":mode,"preregistered_X":requested,"actual_X":r["rendered_X"],
 "actual_mask_and_controls":r,"PASS":ok}
(folder/("guard_"+format(i,"03d")+".json")).write_text(json.dumps(record,indent=2)+"\n")
print("F9_REAL_STELLA_PIXEL_HARD_GATE",i,mode,requested,r["rendered_X"],ok,flush=True)
if not ok:raise SystemExit(3)
PY
 fi
done
import -window root "$out/final_uncropped_GUI.png"
kill "$pid" 2>/dev/null || true
wait "$pid" 2>/dev/null || true
pid=""
sha256sum "$out/raw"/frame_*.png > "$out/TRUE_144_CROP_SHA256SUMS.txt"
sha256sum "$out/raw_full"/frame_*.png > "$out/TRUE_144_FULL_SHA256SUMS.txt"
sha256sum -c "$out/TRUE_144_CROP_SHA256SUMS.txt" >/dev/null
sha256sum -c "$out/TRUE_144_FULL_SHA256SUMS.txt" >/dev/null
/usr/bin/python3 r1_f9_audit.py --raw "$out/raw" \
  --out "$out/TRUE_144_ALL_THREE_MASK_8_STATE_12_CONTRAST_AUDIT.json" \
  --mutants "$out/SYNTHETIC_NEGATIVE_NOT_REAL_STELLA"
echo "F9_144_REAL_STELLA_FRAMES_ALL_NINE_GRAY_STEPS"
