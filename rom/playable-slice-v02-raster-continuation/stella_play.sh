#!/usr/bin/env bash
set -euo pipefail
rom=$(realpath "$1")
out=$(realpath -m "$2")
mkdir -p "$out"/profile "$out"/shots
p=/workspace/.g5ar-env01/bin
export DISPLAY=":$3"
"$p/Xvfb" "$DISPLAY" -screen 0 960x720x24 -nolisten tcp > "$out/xvfb.log" 2>&1 &
xpid=$!
spid=
trap 'if [[ -n $spid ]]; then kill "$spid" 2>/dev/null || true; wait "$spid" 2>/dev/null || true; fi; kill "$xpid" 2>/dev/null || true; wait "$xpid" 2>/dev/null || true' EXIT
for _ in {1..50}; do
    if xdpyinfo -display "$DISPLAY" >/dev/null 2>&1; then break; fi
    sleep .1
done
HOME="$out/profile" XDG_CONFIG_HOME="$out/profile" SDL_VIDEODRIVER=x11 \
    "${STELLA_BIN:-$p/stella}" -video software -audio.enabled 0 -format NTSC -type F6 \
    -ss1x 1 -sssingle 0 -snapname rom -snapsavedir "$out/shots" "$rom" \
    > "$out/stella.stdout" 2> "$out/stella.stderr" &
spid=$!
for _ in {1..80}; do
    window=$("$p/xdotool" search --onlyvisible --pid "$spid" 2>/dev/null | head -1 || true)
    if [[ -n $window ]]; then break; fi
    sleep .1
done
if [[ -z ${window:-} ]]; then exit 1; fi
"$p/xdotool" windowfocus --sync "$window"
"$p/xdotool" getwindowname "$window"
sleep 1.5
if [[ ${4:-} == record ]]; then
    ffmpeg -hide_banner -loglevel warning -f x11grab -draw_mouse 0 -framerate 30 \
        -window_id "$window" -i "$DISPLAY" -t 8 -c:v libx264 -preset fast -crf 18 \
        -vf 'pad=ceil(iw/2)*2:ceil(ih/2)*2' -pix_fmt yuv420p -movflags +faststart \
        "$out/play.mp4" > "$out/ffmpeg.log" 2>&1 &
    rec=$!
fi
printf 'boot\n'
"$p/xdotool" key F12
sleep .5
printf 'right\n'
"$p/xdotool" keydown Right
sleep .55
"$p/xdotool" key F12
printf 'right+up\n'
"$p/xdotool" keydown Up
sleep .28
"$p/xdotool" keyup Up
"$p/xdotool" keyup Right
"$p/xdotool" key F12
sleep .2
printf 'right+fire\n'
"$p/xdotool" keydown Right
"$p/xdotool" keydown space
sleep .3
"$p/xdotool" key F12
sleep .4
"$p/xdotool" keyup space
"$p/xdotool" keyup Right
printf 'left+down\n'
"$p/xdotool" keydown Left
"$p/xdotool" keydown Down
sleep .65
"$p/xdotool" keyup Left
"$p/xdotool" keyup Down
"$p/xdotool" key F12
sleep .4
printf 'up\n'
"$p/xdotool" keydown Up
sleep .6
"$p/xdotool" keyup Up
"$p/xdotool" key F12
if [[ ${4:-} == record ]]; then wait "$rec"; fi
