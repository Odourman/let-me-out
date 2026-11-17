#!/usr/bin/env bash
# G5AH LM-D23 PHASE A: read-only historical F9 and Stella 6.7.1; NO ROM BUILD.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p evidence/phase_a
out="$PWD/evidence/phase_a"
src="$PWD/../../seed_original_f9"
stem=r1_f9_three_masks_three_binary_ram_x_ONE_ROM
dist="$src/rom/v018/experiments/r1_free_xy/dist"
rom="$dist/$stem"_F6.bin
test "$(stat -c %s "$rom")" -eq 16384
hash=6c2585148eb082fb8bc794d664edc4869b18849fcfabb9cada23373d1dc1318b
printf '%s  %s\n' "$hash" "$rom" | sha256sum -c | tee "$out/seed_sha_before.txt"
python3 "$PWD/check_prebuild_original.py" "$src" "$PWD/../../design/NPC_REFERENCE_8x9_masks.json" "$out"
# For Stella auto-load, duplicate historical listing and symbols under ROM stem.
cp "$dist/$stem.lst" "$dist/$stem"_F6.lst
cp "$dist/$stem.sym" "$dist/$stem"_F6.sym
cp "$dist/$stem.lst" "$out/original_f9.lst"
cp "$dist/$stem.sym" "$out/original_f9.sym"
export DISPLAY=:157 SDL_VIDEODRIVER=x11 SDL_AUDIODRIVER=dummy
Xvfb :157 -screen 0 1366x900x24 -ac > "$out/xvfb.log" 2>&1 &
xp=$!
sp=""
cleanup(){ [[ -z "$sp" ]] || kill "$sp" 2>/dev/null || true;kill "$xp" 2>/dev/null || true;}
trap cleanup EXIT
sleep 2
xdpyinfo -display :157 | grep dimensions: | tee "$out/x11_dimensions.txt"
mkdir -p "$HOME/.config/stella"
cat > "$HOME/.config/stella/autoexec.script" <<'AUTO'
base #10
frame #136
break $f1ee
run
AUTO
cp "$HOME/.config/stella/autoexec.script" "$out/autoexec.script"
stella -debug -bs F6 -format NTSC -video software -vsync 0 -audio.enabled 0 "$rom" > "$out/stella_stdout.txt" 2>&1 &
sp=$!
wid=""
for t in $(seq 1 24);do
  if ! kill -0 "$sp" 2>/dev/null;then break;fi
  wid="$(xdotool search --onlyvisible --name Stella 2>/dev/null | head -n1 || true)"
  if [[ -n "$wid" ]];then echo "G5AH_GUI_POLL=$t" | tee "$out/gui_initialization.txt";break;fi
  sleep 1
done
test -n "$wid" || { echo "G5AH_FAIL_NO_DEBUGGER_GUI";exit 11;}
xdotool windowfocus --sync "$wid" || true
echo "$(xdotool getwindowname "$wid")" > "$out/gui_title.txt"
: > "$out/commands_sent.txt"
send(){
  local cmd="$1"
  printf '%s\n' "$cmd" >> "$out/commands_sent.txt"
  xdotool type --window "$wid" --clearmodifiers --delay 28 "$cmd"
  xdotool key --window "$wid" --clearmodifiers Return
  sleep 0.24
}
for cmd in \
 'print pc' 'print _fCount' 'print _scan' 'print _sCycles' 'print _bank' \
 'print X0_SELECT' 'disAsm $f1ee #4' 'tia';do send "$cmd";done
touch "$out/pre_snapshot_marker"
send 'saveSnap'
send "saveSes $out/pre_step_debugger_session.txt"
sleep 1
snap="$(find "$HOME" -maxdepth 1 -type f -name '*_dbg_*.png' -newer "$out/pre_snapshot_marker" | sort | tail -n1)"
if [[ -n "$snap" ]];then cp "$snap" "$out/pre_step_native_TIA.png";fi
# Advance exactly one real 6507 instruction at source-listed breakpoint.
send 'step'
for cmd in 'print pc' 'print _fCount' 'print _scan' 'print _sCycles' \
 'print _bank' 'print X0_SELECT' 'tia';do send "$cmd";done
touch "$out/post_snapshot_marker"
send 'saveSnap'
send "saveSes $out/post_step_debugger_session.txt"
sleep 1
snap="$(find "$HOME" -maxdepth 1 -type f -name '*_dbg_*.png' -newer "$out/post_snapshot_marker" | sort | tail -n1)"
if [[ -n "$snap" ]];then cp "$snap" "$out/post_step_native_TIA.png";fi
import -window root "$out/DEBUGGER_GUI_HELP_ONLY.png" || :
printf '%s  %s\n' "$hash" "$rom" | sha256sum -c | tee "$out/seed_sha_after.txt"
python3 "$PWD/audit_phase_a.py" "$out"
