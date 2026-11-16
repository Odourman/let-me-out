#!/usr/bin/env bash
# Read-only 6502/TIA write traps for ONE critical source Row05 (Stella _scan=123).
# Separate authentic debugger screenshots: PC, bank, frame, cycle, address, value.
set -euo pipefail
cd "$(dirname "$0")"
export SDL_AUDIODRIVER=dummy SDL_VIDEODRIVER=x11 DISPLAY=:118
h="$(getent passwd "$(id -un)" | cut -d: -f6)"
mkdir -p "$h/.config/stella" evidence/r1_f2_traps
Xvfb :118 -screen 0 1366x900x24 -ac > evidence/r1_f2_traps/xvfb.log 2>&1 &
xpid=$!
trap 'kill "$xpid" 2>/dev/null || true' EXIT
sleep 2
cases=(
  'M2 RESP1 35 12'
  'M2 GRP1 38 12'
  'M2 RESP1 46 12'
  'P1 RESP1 38 12'
  'P1 GRP1 41 12'
  'P1 RESP1 46 12'
  'RUNTIME RESP1 37 10'
  'RUNTIME GRP1 40 10'
  'RUNTIME RESP1 38 14'
  'RUNTIME GRP1 41 14'
  'RUNTIME RESP1 46 14'
)
n=0
for case_string in "${cases[@]}";do
 read -r v reg cyc startframe <<< "$case_string"
 case "$v" in
  M2|P1) rom="dist/r1_f2_6B_I2_${v}_F6.bin";;
  RUNTIME)rom="dist/r1_f2_6B_I2_RUNTIME_F6.bin";;
 esac
 n=$((n+1))
 printf -v name '%02d_%s_%s_c%s_afterframe%s' "$n" "$v" "$reg" "$cyc" "$startframe"
 out="evidence/r1_f2_traps/$name"
 mkdir -p "$out"
 if [ "$v" = RUNTIME ];then
   # Both legal runtime positions, c37 or c38 (GRP c40/c41).
   if [ "$reg" = RESP1 ] && [ "$cyc" != 46 ];then lo=35;hi=40
   elif [ "$reg" = GRP1 ];then lo=38;hi=43
   else lo=44;hi=48;fi
 else
   lo=$((cyc-2));hi=$((cyc+2))
 fi
 printf 'base #10\nframe #%s\ntrapWriteIf {_scan == #123 && _sCycles > #%s && _sCycles < #%s} %s\nrun\n' "$startframe" "$lo" "$hi" "$reg" > "$h/.config/stella/autoexec.script"
 cp "$h/.config/stella/autoexec.script" "$out/autoexec.script"
 stella -debug -bs F6 -format NTSC -video software -vsync 0 -audio.enabled 0 "$PWD/$rom" >"$out/stella.log" 2>&1 &
 pid=$!;sleep 4
 if ! kill -0 "$pid" 2>/dev/null;then echo "STELLA_DIED case=$case_string";cat "$out/stella.log";exit 1;fi
 import -window root "$out/stella_full.png"
 test -s "$out/stella_full.png"
 kill "$pid" 2>/dev/null || true;wait "$pid" 2>/dev/null || true
 echo "F2_REAL_TIA_TRAP_ATTEMPT $case_string $out"
done
sha256sum evidence/r1_f2_traps/*/stella_full.png > evidence/r1_f2_traps/RAW_TRAP_PNG_SHA256.txt
