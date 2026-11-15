#!/usr/bin/env bash
# Raw Stella 6.7.1 GUI proof captures; scenes "near" and "far" are different RESP1 delays.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
mkdir -p evidence
export SDL_AUDIODRIVER=dummy SDL_VIDEODRIVER=x11
export HOME="$ROOT/evidence/home"
mkdir -p "$HOME/.config/stella"
ACTUAL_HOME="$(getent passwd "$(id -un)" | cut -d: -f6)"
mkdir -p "$ACTUAL_HOME/.config/stella"
printf "base #10\n" > "$ACTUAL_HOME/.config/stella/autoexec.script"
Xvfb :97 -screen 0 1366x900x24 -ac > evidence/xvfb.log 2>&1 &
XVFBPID=$!
trap 'kill "$XVFBPID" 2>/dev/null || true' EXIT
export DISPLAY=:97
sleep 1
for point in near:20 far:100; do
  name="${point%%:*}"
  frames="${point#*:}"
  mkdir -p "evidence/$name"
  cp dist/LetMeOut_v018_two_silhouette_F6.bin "evidence/$name/proof.bin"
  cp dist/proof.sym "evidence/$name/proof.sym"
  cp dist/proof.lst "evidence/$name/proof.lst"
  {
    echo "base #10"
    echo "frame #$frames"
    echo "print _fCount"
    echo "print _scanEnd"
    echo "print _scan"
    echo "print _sCycles"
    echo "print _bank"
    echo 'print *$80'
    echo 'print *$81'
  } >"evidence/$name/proof.script"
  # ROM-specific script is loaded from same folder as ROM, including DASM symbols/list.
  stella -debug -bs F6 -format NTSC -video software -vsync 0 -audio.enabled 0 "$ROOT/evidence/$name/proof.bin" >"evidence/$name/stella_stdout.txt" 2>&1 &
  pid=$!
  sleep 7
  if ! kill -0 "$pid" 2>/dev/null; then
    echo "ERROR Stella exited before capture for $name" >&2
    cat "evidence/$name/stella_stdout.txt" >&2
    exit 1
  fi
  xdotool search --onlyvisible --name Stella getwindowname >"evidence/$name/window_names.txt" 2>&1 || true
  import -window root "evidence/$name/stella_debugger_full.png"
  test -s "evidence/$name/stella_debugger_full.png"
  kill "$pid" || true
  wait "$pid" 2>/dev/null || true
done
python3 - <<'PY'
import subprocess
from pathlib import Path
import hashlib,json
root=Path("evidence")
out=[]
for p in sorted(root.glob("*/stella_debugger_full.png")):
 resolution=subprocess.check_output(["identify","-format","%wx%h",str(p)],text=True)
 out.append({"path":str(p),"resolution":resolution,"sha256":hashlib.sha256(p.read_bytes()).hexdigest()})
assert len(out)==2,out
(root/"capture_manifest.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps(out,indent=2))
PY
