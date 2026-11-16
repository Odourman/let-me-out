#!/usr/bin/env bash
# R1-F1: read-only register timing for frozen 6B, 6C and N5.
set -euo pipefail
cd "$(dirname "$0")"
export SDL_AUDIODRIVER=dummy SDL_VIDEODRIVER=x11 DISPLAY=:118
h="$(getent passwd "$(id -un)" | cut -d: -f6)"
mkdir -p "$h/.config/stella" evidence/r1_f1_row05_traps
Xvfb :118 -screen 0 1366x900x24 -ac > evidence/r1_f1_row05_traps/xvfb.log 2>&1 &
xpid=$!
trap 'kill "$xpid" 2>/dev/null || true' EXIT
sleep 1
for v in 6B 6C N5; do
  case "$v" in
    6B) rom=dist/r1_individual_6B_F6.bin
       evs="RESP1:19 RESP1:28 RESP1:37 RESP1:46 RESP1:56 RESP1:66 GRP1:22 GRP1:40 GRP1:59 GRP1:69" ;;
    6C) rom=dist/r1_individual_6C_F6.bin
       evs="RESP1:20 RESP1:29 RESP1:38 RESP1:47 RESP1:57 RESP1:67 GRP1:23 GRP1:41 GRP1:60 GRP1:70" ;;
    N5) rom=dist/r1_individual_5_F6.bin
       evs="RESP1:21 RESP1:31 RESP1:42 RESP1:53 RESP1:65 GRP1:24 GRP1:45 GRP1:56 GRP1:68" ;;
  esac
  evs="$evs GRP0:5 ENAM0:10"
  # NUSIZ1 / HMOVE already attempted in first trap run; only row05 P1 and P0/M0 here.
  n=0
  for ev in $evs; do
    n=$((n+1))
    reg="${ev%:*}"; cyc="${ev#*:}"
    printf -v name '%02d_%s_static_%s' "$n" "$reg" "$cyc"
    out="evidence/r1_f1_row05_traps/$v/$name"
    mkdir -p "$out"
    if [ "$cyc" = -1 ]; then
      if [ "$reg" = NUSIZ1 ]; then cond='{_scan < #40 && a == #1}'
      else cond='{_scan < #40}'; fi
    else
      lo=$((cyc-2)); hi=$((cyc+2))
      cond="{_scan == #122 && _sCycles > #$lo && _sCycles < #$hi}"
    fi
    printf 'base #10\nframe #12\ntrapWriteIf %s %s\nrun\n' "$cond" "$reg" > "$h/.config/stella/autoexec.script"
    cp "$h/.config/stella/autoexec.script" "$out/autoexec.script"
    stella -debug -bs F6 -format NTSC -video software -vsync 0 -audio.enabled 0 "$PWD/$rom" >"$out/stella.log" 2>&1 &
    pid=$!
    sleep 2.6
    if ! kill -0 "$pid" 2>/dev/null; then echo "STELLA_DIED $v $reg $cyc"; cat "$out/stella.log"; exit 1; fi
    import -window root "$out/stella_full.png"
    test -s "$out/stella_full.png"
    kill "$pid" 2>/dev/null || true
    wait "$pid" 2>/dev/null || true
    echo "STELLA_TRAP_ATTEMPT $v $reg static_end_cycle=$cyc $out"
  done
done
sha256sum evidence/r1_f1_row05_traps/*/*/stella_full.png > evidence/r1_f1_row05_traps/REAL_SCREENSHOTS_SHA256.txt
