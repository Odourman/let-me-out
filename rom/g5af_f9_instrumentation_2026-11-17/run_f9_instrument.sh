#!/usr/bin/env bash
# G5AF LM-D22, one harness family, two explicitly pre-registered stops on ONE
# pre-existing read-only F9 ROM. NO DASM, NO new .asm/.bin.
set -euo pipefail
cd "$(dirname "$0")"
out="$PWD/evidence"
mkdir -p "$out"
home="$(getent passwd "$(id -un)" | cut -d: -f6)"
mkdir -p "$home/.config/stella"
export SDL_AUDIODRIVER=dummy SDL_VIDEODRIVER=x11 DISPLAY=:154
src="$PWD/../../seed_readonly"
rom="$(find "$src" -type f -name 'r1_f9_three_masks_three_binary_ram_x_ONE_ROM_F6.bin' | head -n1)"
test -n "$rom"
test "$(stat -c %s "$rom")" -eq 16384
expected="6c2585148eb082fb8bc794d664edc4869b18849fcfabb9cada23373d1dc1318b"
printf '%s  %s\n' "$expected" "$rom" | sha256sum -c | tee "$out/ROM_SHA_PRE.txt"
dpkg-query -W -f='${binary:Package} ${Version}\n' stella xvfb xdotool python3-pil > "$out/versions.txt"
echo "G5AF_ROM_FROZEN_SHA256=$expected"

Xvfb :154 -screen 0 1366x900x24 -ac > "$out/xvfb.log" 2>&1 &
xpid=$!
spid=""
cleanup(){ [[ -z "$spid" ]] || kill "$spid" 2>/dev/null || true; kill "$xpid" 2>/dev/null || true; }
trap cleanup EXIT
sleep 2
xdpyinfo -display :154 | grep dimensions: > "$out/x11_dimensions.txt"
fail=0

# Each autoexec contains ONLY pre-registered trap configuration and execution.
# There is deliberately NO saveSes or saveSnap during autoexec first-time load.
# Mode 000, original F9 r1_f9_trace.sh: frame 136, scan123,
# M_RESP1 cycle band 19..23 and F_RESP1 cycle band 30..34.
while read -r ident reg low high; do
  dest="$out/$ident"
  mkdir -p "$dest"
  cat > "$home/.config/stella/autoexec.script" <<EOF
base #10
frame #136
trapWriteIf {_scan == #123 && _sCycles > #$low && _sCycles < #$high} $reg
run
EOF
  cp "$home/.config/stella/autoexec.script" "$dest/autoexec.script"
  echo "G5AF_CASE_BEGIN $ident $reg pre_reg_scan123 low=$low high=$high"
  # Unique pre-test marker ensures snapshots/sessions originate in this case.
  touch "$dest/run_marker"
  stella -debug -bs F6 -format NTSC -video software -vsync 0 -audio.enabled 0 "$rom" > "$dest/stella_stdout.log" 2>&1 &
  spid=$!
  # Source F9's original CI allowed 16s of GUI initialization.
  # Old 6s blind delay failed on first (cold) Stella startup. Wait for
  # actual window visibility, at most 24s, without changing any test data.
  wid=""
  for attempt in $(seq 1 24); do
    if ! kill -0 "$spid" 2>/dev/null; then break; fi
    wid="$(xdotool search --onlyvisible --name Stella 2>/dev/null | head -n1 || true)"
    if [[ -n "$wid" ]]; then
      echo "G5AF_STELLA_GUI_VISIBLE_AFTER_POLL $ident poll=$attempt" | tee "$dest/gui_ready_poll.txt"
      break
    fi
    sleep 1
  done
  if ! kill -0 "$spid" 2>/dev/null; then
    echo "G5AF_STELLA_PROCESS_EXITED $ident" | tee "$dest/FAIL.txt"
    cat "$dest/stella_stdout.log"
    fail=1; spid=""; continue
  fi
  if [[ -z "$wid" ]]; then
    echo "G5AF_NO_VISIBLE_STELLA_PROMPT $ident" | tee "$dest/FAIL.txt"
    fail=1
    kill "$spid" 2>/dev/null || true; wait "$spid" 2>/dev/null || true; spid=""
    continue
  fi
  xdotool windowfocus --sync "$wid" || true
  echo "G5AF_PROMPT_AFTER_GUI_READY window=$wid title=$(xdotool getwindowname "$wid" 2>/dev/null || true)" | tee "$dest/prompt_ready.txt"
  : > "$dest/keyboard_commands.txt"
  send(){
    local cmd="$1"
    printf '%s\n' "$cmd" >> "$dest/keyboard_commands.txt"
    xdotool type --window "$wid" --clearmodifiers --delay 35 "$cmd"
    xdotool key --window "$wid" --clearmodifiers Return
    sleep 0.35
  }
  # All of the following are typed after prompt first-time load / trap.
  # Print the CPU location and numeric scan/cycle/frame/bank, then real TIA
  # register state; repeat CPU/scan to check no emulation occurred meantime.
  send 'print pc'
  send 'print _fCount'
  send 'print _scan'
  send 'print _sCycles'
  send 'print _bank'
  send 'tia'
  send 'print pc'
  send 'print _scan'
  touch "$dest/after_numeric_marker"
  send 'saveSnap'
  send 'saveSes'
  sleep 1
  import -window root "$dest/debugger_GUI_1366x900.png" || true

  # Preserve exact native original Stella TIA image, not the Xvfb GUI crop.
  mapfile -t snaps < <(find "$home" -maxdepth 1 -type f -name '*_dbg_*.png' -newer "$dest/after_numeric_marker" | sort)
  mapfile -t sessions < <(find "$home" -maxdepth 1 -type f -name 'session_*.txt' -newer "$dest/after_numeric_marker" | sort)
  printf '%s\n' "${snaps[@]}" > "$dest/native_source_files.txt"
  printf '%s\n' "${sessions[@]}" > "$dest/session_source_files.txt"
  if [[ "${#snaps[@]}" -ge 1 ]]; then cp "${snaps[-1]}" "$dest/native_TIA_original.png"; fi
  if [[ "${#sessions[@]}" -ge 1 ]]; then cp "${sessions[-1]}" "$dest/debugger_session.txt"; fi
  if [[ -s "$dest/debugger_session.txt" ]]; then
    echo "G5AF_SESSION_BYTES $ident $(stat -c %s "$dest/debugger_session.txt")"
    grep -i -E 'print pc|print _scan|print _sCycles|print _fCount|print _bank|COLUxx|scanline|P0:|P1:|M0:|M1:' "$dest/debugger_session.txt" | head -45 || true
  else
    echo "G5AF_EMPTY_OR_MISSING_SESSION $ident" | tee "$dest/FAIL.txt"
    fail=1
  fi
  if [[ -f "$dest/native_TIA_original.png" ]]; then
    identify -format "G5AF_NATIVE_IMAGE $ident %wx%h %m\n" "$dest/native_TIA_original.png" || true
  else
    echo "G5AF_NATIVE_SNAPSHOT_MISSING $ident" | tee -a "$dest/FAIL.txt"
    fail=1
  fi
  kill "$spid" 2>/dev/null || true
  wait "$spid" 2>/dev/null || true
  spid=""
done <<'EOF_CASES'
F9_000_M_RESP1 RESP1 19 23
F9_000_F_RESP1 RESP1 30 34
EOF_CASES
printf '%s  %s\n' "$expected" "$rom" | sha256sum -c | tee "$out/ROM_SHA_POST.txt"
/usr/bin/python3 "$PWD/audit_evidence.py" "$out" || fail=1
exit "$fail"
