#!/usr/bin/env bash
set -euo pipefail
rom=$(realpath "$1")
out=$(realpath -m "$2")
mkdir -p "$out"/{profile,images}
p=/workspace/.g5ar-env01/bin
export DISPLAY=":$3"
"$p/Xvfb" "$DISPLAY" -screen 0 1280x900x24 -nolisten tcp > "$out/xvfb.log" 2>&1 &
xpid=$!
spid=
trap 'if [[ -n $spid ]]; then kill "$spid" 2>/dev/null || :; wait "$spid" 2>/dev/null || :; fi; kill "$xpid" 2>/dev/null || :; wait "$xpid" 2>/dev/null || :' EXIT
for _ in {1..20}; do
    if xdpyinfo -display "$DISPLAY" > /dev/null 2>&1; then break; fi
    sleep .15
done
HOME="$out/profile" XDG_CONFIG_HOME="$out/profile" SDL_VIDEODRIVER=x11 \
    "$p/stella" -video software -audio.enabled 0 -format NTSC -type F6 \
    -ss1x 1 -sssingle 0 -snapname rom -snapsavedir "$out/images" "$rom" \
    > "$out/stella.stdout" 2> "$out/stella.stderr" &
spid=$!
for _ in {1..20}; do
    window=$("$p/xdotool" search --onlyvisible --pid "$spid" 2>/dev/null | head -1 || :)
    if [[ -n $window ]]; then break; fi
    sleep .15
done
if [[ -z ${window:-} ]]; then
    printf 'Could not locate Stella window\n' >&2
    exit 1
fi
"$p/xdotool" windowfocus --sync "$window"
"$p/xdotool" getwindowname "$window"
sleep .4
if [[ ${4:-} == select ]]; then
    "$p/xdotool" keydown F1
    sleep .35
fi
for _ in {1..12}; do
    "$p/xdotool" key F12
    sleep .082
done
if [[ ${4:-} == select ]]; then "$p/xdotool" keyup F1; fi
find "$out/images" -type f -iname '*.png' -printf '%f\n'
