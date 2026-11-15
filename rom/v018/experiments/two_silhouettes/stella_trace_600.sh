#!/usr/bin/env bash
# 600 individual debugger frame-advances with a print of _scanEnd after EACH.
# This tests isolated two-silhouette PROOF only; NOT full R1/R2/R4.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
mkdir -p evidence_600
export SDL_AUDIODRIVER=dummy SDL_VIDEODRIVER=x11
export HOME="$ROOT/evidence_600/home"
mkdir -p "$HOME/.config/stella"
ACTUAL_HOME="$(getent passwd "$(id -un)" | cut -d: -f6)"
mkdir -p "$ACTUAL_HOME/.config/stella"
python3 - <<'PY'
from pathlib import Path
p=Path("evidence_600/autoexec_600.script")
cmd=["base #10","frame #10","print _fCount","print _scanEnd"]
for i in range(600):
 cmd.extend(("frame #1", "print _fCount", "print _scanEnd"))
cmd += ["saveSes"]
p.write_text("\n".join(cmd)+"\n")
print("Scripted frame advancements:",sum(line=="frame #1" for line in cmd))
PY
cp evidence_600/autoexec_600.script "$ACTUAL_HOME/.config/stella/autoexec.script"
cp dist/LetMeOut_v018_two_silhouette_NUSIZ_F6.bin evidence_600/proof.bin
cp dist/proof_nusiz.lst evidence_600/proof.lst
cp dist/proof_nusiz.sym evidence_600/proof.sym
# Optional rom.script in the user homedir prevents a misleading missing-file message.
: > "$ACTUAL_HOME/proof.script"
: > "$HOME/proof.script"
Xvfb :99 -screen 0 1366x900x24 -ac >evidence_600/xvfb.log 2>&1 &
XVPID=$!
trap 'kill "$XVPID" 2>/dev/null || true' EXIT
export DISPLAY=:99
sleep 1
stella -debug -bs F6 -format NTSC -video software -vsync 0 -audio.enabled 0 "$ROOT/evidence_600/proof.bin" >evidence_600/stella_stdout.txt 2>&1 &
PID=$!
sleep 25
if ! kill -0 "$PID" 2>/dev/null; then cat evidence_600/stella_stdout.txt; echo "Stella exited"; exit 1; fi
xdotool search --onlyvisible --name Stella getwindowname >evidence_600/window_names.txt 2>&1 || true
import -window root evidence_600/after_600_frames.png
kill "$PID" || true
wait "$PID" 2>/dev/null || true
find "$ACTUAL_HOME" "$ROOT/evidence_600" -maxdepth 5 -type f -name "20??-??-??_??-??-??.txt" -print > evidence_600/sessions_found.txt || true
cat evidence_600/sessions_found.txt
while IFS= read -r f; do cp "$f" "evidence_600/$(basename "$f")"; done < evidence_600/sessions_found.txt
echo "Raw debugger script executed. Inspect Stella frame counter and saveSes to determine pass/fail."
