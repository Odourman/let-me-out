#!/usr/bin/env bash
# R1-F3 READ-ONLY source-row05 timing checks for already failed G0 diagnostic.
# Reuse byte-identical 16KiB executable. No new geometry or runtime variant.
set -euo pipefail
cd "$(dirname "$0")"
export SDL_AUDIODRIVER=dummy SDL_VIDEODRIVER=x11 DISPLAY=:118
h="$(getent passwd "$(id -un)" | cut -d: -f6)"
mkdir -p "$h/.config/stella" evidence/r1_f3_g0_traps
Xvfb :118 -screen 0 1366x900x24 -ac > evidence/r1_f3_g0_traps/xvfb.log 2>&1 &
xp=$!;trap 'kill "$xp" 2>/dev/null||true' EXIT
sleep 2
rom="$PWD/dist/r1_f3_6B_I0_P1_I2_FIXED_F6.bin"
for spec in "01_FIRST_RESP1 RESP1 18 22" "02_FIRST_GRP1 GRP1 21 25" "03_SECOND_RESP1 RESP1 26 30" "04_THIRD_RESP1 RESP1 35 39";do
 read -r label reg lo hi <<< "$spec"
 out="evidence/r1_f3_g0_traps/$label";mkdir -p "$out"
 printf 'base #10\nframe #12\ntrapWriteIf {_scan == #123 && _sCycles > #%s && _sCycles < #%s} %s\nrun\n' "$lo" "$hi" "$reg" > "$h/.config/stella/autoexec.script"
 cp "$h/.config/stella/autoexec.script" "$out/autoexec.script"
 stella -debug -bs F6 -format NTSC -video software -vsync 0 -audio.enabled 0 "$rom" > "$out/stella.log" 2>&1 &
 pid=$!;sleep 4
 kill -0 "$pid"
 import -window root "$out/stella_full.png"
 test -s "$out/stella_full.png"
 kill "$pid" 2>/dev/null||true;wait "$pid" 2>/dev/null||true
 echo "R1_F3_G0_ACTUAL_STELLA_TRAP $label $reg CYCLE_IN=$lo..$hi BANK0 SOURCE_ROW05 SCAN123"
done
sha256sum evidence/r1_f3_g0_traps/*/stella_full.png > evidence/r1_f3_g0_traps/REAL_TRAP_SCREENSHOTS_SHA256.txt
