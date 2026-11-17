#!/usr/bin/env bash
# G5AL / LM-D24: only already-built F9, run A then B and one step C.
# Do not compile anything. Pre-registered mode 000; two separately launched
# Stella 6.7.1 debugger processes. All outcomes fail-closed.
set -Eeuo pipefail
cd "$(dirname "$0")"
root="$PWD"
out="$root/evidence"
mkdir -p "$out/A_TRAP" "$out/B_BREAK_STEP"
spid=""; xpid=""; finalized=0
expected='6c2585148eb082fb8bc794d664edc4869b18849fcfabb9cada23373d1dc1318b'
seed="$root/../../seed_f9"
stem='r1_f9_three_masks_three_binary_ram_x_ONE_ROM'
dist="$seed/rom/v018/experiments/r1_free_xy/dist"
rom="$dist/${stem}_F6.bin"
export SDL_AUDIODRIVER=dummy SDL_VIDEODRIVER=x11 DISPLAY=:159 PYTHONUNBUFFERED=1
home="$(getent passwd "$(id -un)" | cut -d: -f6)"
mkdir -p "$home/.config/stella"
printf 'run_f9_method.sh invoked at %s\n' "$(date -u --iso-8601=seconds)" > "$out/runner_metadata.txt"

teardown() {
  local code="$?"
  if [[ "$finalized" == "1" ]]; then return; fi
  finalized=1
  trap - EXIT
  set +e
  if [[ -n "$spid" ]]; then kill "$spid" 2>/dev/null; wait "$spid" 2>/dev/null; echo "stella_final_exit_status=$?" >> "$out/runner_metadata.txt"; spid=""; fi
  if [[ -n "$xpid" ]]; then kill "$xpid" 2>/dev/null; wait "$xpid" 2>/dev/null; echo "Xvfb_final_exit_status=$?" >> "$out/runner_metadata.txt"; xpid=""; fi
  printf '%s\n' "$code" > "$out/script_exit_code.txt"
  python3 "$root/audit_g5al.py" "$out"
  local auditcode="$?"
  # Files may ONLY be hashed after both emulator and X server are dead/waited.
  python3 - "$out" <<'PY'
import hashlib,sys
from pathlib import Path
root=Path(sys.argv[1]); f=root/'SHA256SUMS.txt'
with f.open('w') as o:
 for p in sorted(root.rglob('*')):
  if p.is_file() and p!=f:
   o.write(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(root).as_posix()+'\n')
print('G5AL_FINAL_SHA256SUMS_AFTER_STELLA_XVFB_WAIT',len(f.read_text().splitlines()))
PY
  if [[ "$code" != "0" || "$auditcode" != "0" ]]; then
    echo "G5AL_FAILURE script=$code audit=$auditcode"; exit 8
  fi
  echo 'G5AL_F9_METHOD_READY_BOUNDED'
  exit 0
}
trap teardown EXIT
stop() {
  local stage="$1" reason="$2"
  printf '%s\n' "$stage|$reason" > "$out/FAILURE_STAGE.txt"
  echo "G5AL_HARD_STOP $stage $reason"
  exit 11
}
kill_stella() {
  if [[ -n "$spid" ]]; then kill "$spid" 2>/dev/null || :; wait "$spid" 2>/dev/null || :; spid=""; fi
}
check_rom() {
  [[ -f "$rom" ]] || stop 'STATIC' 'historical ROM missing'
  [[ "$(stat -c %s "$rom")" -eq 16384 ]] || stop 'STATIC' 'F9 is not 16KiB'
  printf '%s  %s\n' "$expected" "$rom" | sha256sum -c | tee "$out/F9_ROM_SHA_PRE.txt" || stop 'STATIC' 'original ROM SHA mismatch'
  python3 "$root/check_f9_frozen.py" "$seed" "$root/../../design/NPC_REFERENCE_8x9_masks.json" "$out" || stop 'STATIC' 'F9 source/list/sym/mask mismatch'
  cp "$dist/$stem.lst" "$dist/${stem}_F6.lst"
  cp "$dist/$stem.sym" "$dist/${stem}_F6.sym"
  cp "$dist/$stem.lst" "$out/original_f9.lst"
  cp "$dist/$stem.sym" "$out/original_f9.sym"
  cp "$seed/rom/v018/experiments/r1_free_xy/$stem.asm" "$out/original_f9_source.txt"
}
# Every poll records ALL Stella window IDs AND titles (including game view).
# Accept ONLY semantic Debugger mode title, not an arbitrary early game window.
wait_debugger() {
  local dest="$1" stage="$2" limit="${3:-36}"
  local poll id title selected="" now
  : > "$dest/window_poll_${stage}.tsv"
  for ((poll=1;poll<=limit;poll++)); do
    now="$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)"
    if ! kill -0 "$spid" 2>/dev/null; then
      printf '%s\t%d\tprocess_exited\t-\t-\n' "$now" "$poll" >> "$dest/window_poll_${stage}.tsv"
      break
    fi
    local ids
    ids="$(xdotool search --onlyvisible --name Stella 2>/dev/null || true)"
    if [[ -z "$ids" ]]; then
      printf '%s\t%d\tno_window\t-\t-\n' "$now" "$poll" >> "$dest/window_poll_${stage}.tsv"
    else
      while IFS= read -r id; do
        title="$(xdotool getwindowname "$id" 2>/dev/null || true)"
        printf '%s\t%d\twindow\t%s\t%s\n' "$now" "$poll" "$id" "$title" >> "$dest/window_poll_${stage}.tsv"
        if [[ "$title" == 'Stella 6.7.1: Debugger mode' ]];then selected="$id";fi
      done <<< "$ids"
    fi
    if [[ -n "$selected" ]]; then
      printf '%s\n' "$selected" > "$dest/verified_debugger_window_${stage}.txt"
      echo "G5AL_VERIFIED_DEBUGGER_MODE stage=$stage poll=$poll wid=$selected title=Stella_6.7.1_Debugger_mode" | tee "$dest/debugger_${stage}_found.txt"
      xdotool windowfocus --sync "$selected" || stop "$stage" 'could not focus debugger'
      printf '%s' "$selected"
      return 0
    fi
    sleep 1
  done
  stop "$stage" 'GUI_GAME_VIEW_ONLY_OR_NO_DEBUGGER_PROMPT'
}
# Important: use result variable for window without command substitution to
# avoid subshell error/exit bypass and logging to stdout.
wid=""
find_debugger() {
  local dest="$1" stage="$2" limit="${3:-36}" i id title ids now
  : > "$dest/window_poll_${stage}.tsv"; wid=""
  for ((i=1;i<=limit;i++)); do
    now="$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)"
    if ! kill -0 "$spid" 2>/dev/null; then
      printf '%s\t%d\tprocess_exited\t-\t-\n' "$now" "$i" >> "$dest/window_poll_${stage}.tsv";break
    fi
    ids="$(xdotool search --onlyvisible --name Stella 2>/dev/null || true)"
    if [[ -z "$ids" ]];then printf '%s\t%d\tno_window\t-\t-\n' "$now" "$i" >> "$dest/window_poll_${stage}.tsv";fi
    while IFS= read -r id;do
      [[ -n "$id" ]] || continue
      title="$(xdotool getwindowname "$id" 2>/dev/null || true)"
      printf '%s\t%d\twindow\t%s\t%s\n' "$now" "$i" "$id" "$title" >> "$dest/window_poll_${stage}.tsv"
      if [[ "$title" == 'Stella 6.7.1: Debugger mode' ]];then wid="$id";fi
    done <<< "$ids"
    if [[ -n "$wid" ]];then
      printf '%s\n' "$wid" > "$dest/verified_debugger_window_${stage}.txt"
      printf 'stage=%s poll=%d window=%s title=%s\n' "$stage" "$i" "$wid" 'Stella 6.7.1: Debugger mode' > "$dest/verified_debugger_${stage}.txt"
      echo "G5AL_VERIFIED_DEBUGGER_MODE stage=$stage poll=$i window=$wid"
      xdotool windowfocus --sync "$wid" || stop "$stage" 'failed to focus verified debugger'
      return 0
    fi
    sleep 1
  done
  stop "$stage" 'GUI_GAME_VIEW_ONLY_OR_NO_DEBUGGER_PROMPT'
}
case_dir=""
send() {
  local cmd="$1"
  [[ -n "$wid" ]] || stop 'INPUT' 'no verified debugger window'
  [[ "$(xdotool getwindowname "$wid" 2>/dev/null)" == 'Stella 6.7.1: Debugger mode' ]] || stop 'INPUT' 'target is not debugger mode'
  printf '%s\n' "$cmd" >> "$case_dir/commands_sent.txt"
  xdotool type --window "$wid" --clearmodifiers --delay 30 "$cmd"
  xdotool key --window "$wid" --clearmodifiers Return
  sleep 0.40
}
copy_session() {
  local name="$1" dir="$case_dir" marker="$case_dir/session_marker_${1}"
  touch "$marker"
  send "saveSes $dir/${name}_debugger_session.txt"
  sleep 0.75
  local newest="$dir/${name}_debugger_session.txt"
  [[ -s "$newest" ]] || stop "$name" "saveSes did not create a live prompt session"
  printf "%s\n" "$newest" > "$dir/${name}_session_original_path.txt"
  [[ "$(stat -c %s "$dir/${name}_debugger_session.txt")" -gt 100 ]] || stop "$name" 'session is zero/small'
}
copy_native() {
  local name="$1" dir="$case_dir" marker="$case_dir/snapshot_marker_${1}"
  touch "$marker"
  send 'saveSnap'
  sleep 1.15
  local newest
  newest="$(find "$home" -maxdepth 1 -type f -name '*_dbg_*.png' -newer "$marker" -printf '%T@ %p\n' | sort -nr | head -n1 | cut -d' ' -f2- || true)"
  [[ -n "$newest" && -s "$newest" ]] || stop "$name" 'no actual native TIA snapshot'
  cp "$newest" "$dir/${name}_native_TIA.png"
  printf '%s\n' "$newest" > "$dir/${name}_native_original_path.txt"
}
verify_session() {
  local name="$1";shift
  python3 "$root/audit_g5al.py" --gate "$name" "$case_dir/${name}_debugger_session.txt" "$@" || stop "$name" 'RESPONSE_OR_NUMERIC_NOT_PROVEN'
}
record_cpu() {
  for cmd in 'print pc' 'print _fCount' 'print _scan' 'print _sCycles' 'print _bank' 'tia' 'print pc' 'print _scan';do send "$cmd";done
}

check_rom
dpkg-query -W -f='${binary:Package} ${Version}\n' stella xvfb xdotool python3-pil > "$out/versions.txt"
# A. Fresh Stella debugger: initial autoexec ONLY base #10.
# Four-break strategy was frozen in PREREGISTERED_F9_METHOD.md BEFORE first run.
Xvfb :159 -screen 0 1366x900x24 -ac > "$out/Xvfb_stdout.txt" 2>&1 & xpid=$!
sleep 2
xdpyinfo -display :159 | grep 'dimensions:' > "$out/x11_dimensions.txt"
case_dir="$out/A_TRAP"
home="$root/runtime_home_A"
mkdir -p "$home/.config/stella"
export HOME="$home" XDG_CONFIG_HOME="$home/.config"
printf 'base #10\n' > "$home/.config/stella/autoexec.script"
cp "$home/.config/stella/autoexec.script" "$case_dir/autoexec.script"
printf '%s\n' 'stella -debug -dbg.logbreaks 0 -dev.settings 0 -dev.bankrandom 0 -plr.bankrandom 0 -bs F6 -format NTSC -video software -vsync 0 -audio.enabled 0 ORIGINAL_F9; startbank=NOT_SET; bank always from print _bank' > "$case_dir/invocation.txt"
stella -debug -dbg.logbreaks 0 -dev.settings 0 -dev.bankrandom 0 -plr.bankrandom 0 -bs F6 -format NTSC -video software -vsync 0 -audio.enabled 0 "$rom" > "$case_dir/stella_stdout.txt" 2>&1 & spid=$!
find_debugger "$case_dir" A_INITIAL 40
send 'print pc';send 'print _bank'
copy_session A_HANDSHAKE
verify_session A_HANDSHAKE

# Interactive frame advancement: NEVER during first autoexec.
send 'frame #136'
find_debugger "$case_dir" A_AFTER_FRAME 40
send 'print _fCount';send 'print _bank';send 'print pc'
copy_session A_FRAME
verify_session A_FRAME

# Interactive trap; check REAL parser response before one run.
send 'trapWriteIf {_scan == #123 && _sCycles > #19 && _sCycles < #23} RESP1'
copy_session A_TRAP_ACK
verify_session A_TRAP_ACK
send run
wid=""
find_debugger "$case_dir" A_NEW_TRAP_REENTRY 40
record_cpu
copy_native A_TRAP
copy_session A_TRAP
verify_session A_TRAP

# Exact RGB-pixel equality with historical frozen G5AF M; log any difference.
python3 - "$case_dir/A_TRAP_native_TIA.png" "$root/../../ref_g5af/F9_000_M_RESP1/native_TIA_original.png" "$case_dir/A_G5AF_PIXEL_COMPARISON_PRECHECK.json" "$root" <<'PY'
import sys,json
from pathlib import Path
sys.path.insert(0,sys.argv[4])
from audit_g5al import compare_png
r=compare_png(Path(sys.argv[1]),Path(sys.argv[2]))
Path(sys.argv[3]).write_text(json.dumps(r,indent=2)+'\n')
print('G5AL_F9_PIXEL_COMPARE',json.dumps(r),flush=True)
assert r['pixel_equal'], "NATIVE_TIA_REF_MISMATCH"
PY
printf 'G5AL_A_STRICT_PASS_BANK_NEUTRAL_RESP1_TRAP\n' > "$case_dir/STAGE_A_PASS.txt"
kill_stella

# B: New CLEAN instance; frozen four separate one-time bank-bound breakpoints.
case_dir="$out/B_BREAK_STEP"
home="$root/runtime_home_B"
mkdir -p "$home/.config/stella"
export HOME="$home" XDG_CONFIG_HOME="$home/.config"
printf 'base #10\n' > "$home/.config/stella/autoexec.script"
cp "$home/.config/stella/autoexec.script" "$case_dir/autoexec.script"
printf '%s\n' 'stella -debug -dbg.logbreaks 0 -dev.settings 0 -dev.bankrandom 0 -plr.bankrandom 0 -bs F6 -format NTSC -video software -vsync 0 -audio.enabled 0 ORIGINAL_F9; startbank=NOT_SET; bank always measured' > "$case_dir/invocation.txt"
stella -debug -dbg.logbreaks 0 -dev.settings 0 -dev.bankrandom 0 -plr.bankrandom 0 -bs F6 -format NTSC -video software -vsync 0 -audio.enabled 0 "$rom" > "$case_dir/stella_stdout.txt" 2>&1 & spid=$!
find_debugger "$case_dir" B_INITIAL 40
send 'print pc';send 'print _bank'
copy_session B_HANDSHAKE
verify_session B_HANDSHAKE
send 'frame #136'
find_debugger "$case_dir" B_AFTER_FRAME 40
send 'print _fCount';send 'print _bank';send 'print pc'
copy_session B_FRAME
verify_session B_FRAME
for n in 0 1 2 3;do
  send "break \$f1ee #$n"
  copy_session "B_SET_$n"
  verify_session "B_SET_$n"
done
send run
wid=""
find_debugger "$case_dir" B_NEW_BREAK_REENTRY 40
record_cpu
copy_native B_PRE
copy_session B_PRE
verify_session B_PRE
printf 'G5AL_B_STRICT_PASS_PC_F1EE_FOUR_SET_RECEIPTS\n' > "$case_dir/STAGE_B_PASS.txt"

# C: Exactly one CPU instruction with two numerical source-TIA snapshots.
send step
record_cpu
copy_native C_POST
copy_session C_POST
verify_session C_POST
printf 'G5AL_C_STRICT_PASS_ONE_STELLA_STEP\n' > "$case_dir/STAGE_C_PASS.txt"
kill_stella
# Teardown waits for Xvfb, records post-ROM hash and performs final integrity checks.
