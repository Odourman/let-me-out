#!/usr/bin/env bash
set -euo pipefail
rom=$(realpath "$1")
work=$(realpath -m "$2")
display=":$3"
bin=$(realpath "$4")
mkdir -p "$work"
band=$(awk '$1=="BandEntry"{print $2}' "${rom%.bin}.sym")
test -n "$band"
cp "$rom" "$work/probe.bin"
cat > "$work/measure.script" <<SCRIPT
breakIf { pc == \$$band && _bank == #0 }
trapWrite \$11
SCRIPT
cd "$work"
export HOME="$work" XDG_CONFIG_HOME="$work" SDL_AUDIODRIVER=dummy SDL_VIDEODRIVER=x11 DISPLAY="$display"
p=/workspace/.g5ar-env01/bin
"$p/Xvfb" "$DISPLAY" -screen 0 1280x900x24 -nolisten tcp > xvfb.log 2>&1 &
xpid=$!
trap 'kill "$xpid" 2>/dev/null || :; wait "$xpid" 2>/dev/null || :' EXIT
for _ in {1..20}; do
    if xdpyinfo -display "$DISPLAY" > /dev/null 2>&1; then break; fi
    sleep .1
done
timeout 12s "$bin" -debug -video software -audio.enabled 0 -type F6 -format NTSC "$work/probe.bin" > stdout 2> stderr &
spid=$!
trap 'kill "$spid" "$xpid" 2>/dev/null || :; wait "$spid" "$xpid" 2>/dev/null || :' EXIT
for _ in {1..25}; do
    wid=$("$p/xdotool" search --onlyvisible --name 'Stella' 2>/dev/null | head -1 || :)
    if [[ -n "$wid" ]]; then break; fi
    sleep .15
done
test -n "$wid"
"$p/xdotool" windowfocus --sync "$wid"
sleep 1
for cmd in 'exec measure.script' listBreaks listTraps 'help timer' clearTraps clearBreaks \
           "runToPc \$$band" 'print _scan' 'print _bank' 'timer $ba $b8' 'scanLine #4' listTimers resetTimers 'trapWrite $11' run 'print pc' 'print _scan' saveSes; do
    "$p/xdotool" type "$cmd"
    "$p/xdotool" key Return
    sleep .15
done
import -window root debugger.png || :
find "$work" -name 'session*.txt' -print
