#!/usr/bin/env bash
# R1-F1 ONE and ONLY A/B microprobe: 6C last RESP1 c67 -> c65 (remove last NOP per row).
# No other P1 resets, GRP bytes, P0/M0/PF, timing families or mask changes.
set -euo pipefail
cd "$(dirname "$0")"
python3 - <<'PY'
from pathlib import Path
import hashlib
base=Path('r1_individual_6C.asm').read_text()
assert hashlib.sha256(base.encode()).hexdigest()=='781fd41bb2da64739827b0debf90de2af98d023a4b0d9b0bbbb4edda38c8d2a0'
ids=[f'R1N6CRow{i:02d}:' for i in range(9)]
s=base
for i in reversed(range(9)):
 a=s.index(ids[i]);b=s.index(ids[i+1]) if i<8 else s.index('BottomBlank:')
 seg=s[a:b];needle=' NOP\n STA RESP1\n STA GRP1\n';j=seg.rfind(needle)
 assert j>=0,(i,j)
 seg=seg[:j]+' STA RESP1\n STA GRP1\n'+seg[j+len(needle):]
 s=s[:a]+seg+s[b:]
assert s.count(' STA RESP1\n')==base.count(' STA RESP1\n')
Path('r1_individual_6C_F1AB.asm').write_text(s)
print('ONE 2-cycle NOP removed immediately before SIXTH RESP1 in each of 9 rows')
PY
dasm r1_individual_6C_F1AB.asm -f3 -odist/r1_individual_6C_F1AB.bank.bin -ldist/r1_individual_6C_F1AB.lst -sdist/r1_individual_6C_F1AB.sym
python3 - <<'PY'
from pathlib import Path
import hashlib
bank=Path('dist/r1_individual_6C_F1AB.bank.bin').read_bytes();assert len(bank)==4096
rom=bank*4;Path('dist/r1_individual_6C_F1AB_F6.bin').write_bytes(rom)
print('F1_AB_ROM_SHA256',hashlib.sha256(rom).hexdigest())
PY
export SDL_AUDIODRIVER=dummy SDL_VIDEODRIVER=x11 DISPLAY=:119
h="$(getent passwd "$(id -un)" | cut -d: -f6)"
mkdir -p "$h/.config/stella" evidence/r1_f1_ab/raw
Xvfb :119 -screen 0 1366x900x24 -ac > evidence/r1_f1_ab/xvfb.log 2>&1 &
xpid=$!
trap 'kill "$xpid" 2>/dev/null || true' EXIT
sleep 1
printf 'base #10\nframe #10\nprint _fCount\nprint _scanEnd\n' > "$h/.config/stella/autoexec.script"
stella -debug -bs F6 -format NTSC -video software -vsync 0 -audio.enabled 0 "$PWD/dist/r1_individual_6C_F1AB_F6.bin" > evidence/r1_f1_ab/stella.log 2>&1 &
pid=$!
sleep 4
kill -0 "$pid"
wid="$(xdotool search --onlyvisible --name Stella | head -n 1)"
xdotool windowfocus --sync "$wid"
import -window root evidence/r1_f1_ab/initial_full.png
for ((i=1;i<=16;i++)); do
 xdotool key --window "$wid" --clearmodifiers ctrl+f
 sleep 0.025
 import -window root -crop 900x300+103+65 "evidence/r1_f1_ab/raw/frame_$(printf '%03d' "$i").png"
done
import -window root evidence/r1_f1_ab/final_full.png
kill "$pid" 2>/dev/null || true
wait "$pid" 2>/dev/null || true
python3 - <<'PY'
import json,hashlib
from PIL import Image
from pathlib import Path
from collections import Counter
sprites=json.loads(Path('canon_masks.json').read_text())['sprites']
M={k:{(2*j+d,i) for i,row in enumerate(rows) for j,ch in enumerate(row) for d in (0,1) if ch=='1'} for k,rows in sprites.items()}
required=Counter(['large_male','large_male','large_female','large_female','small_male','small_female'])
records=[]
for path in sorted(Path('evidence/r1_f1_ab/raw').glob('frame_*.png')):
 pix=Image.open(path).convert('RGB').load()
 whites={(x,y) for y in range(50,195) for x in range(336) if min(pix[x,y])>180 and max(pix[x,y])-min(pix[x,y])<40}
 y0=min(y for x,y in whites);groups=[]
 for x in sorted({x for x,y in whites}):
  if not groups or x-groups[-1][-1]>16:groups.append([])
  groups[-1].append(x)
 matches=[]
 for g in groups:
  blob={(x,y) for x,y in whites if g[0]<=x<=g[-1]}
  matches.append(min((len({(x+start,y+y0) for x,y in mask}^blob),typ,start)
   for typ,mask in M.items() for start in range(max(0,g[0]-16),g[0]+1)))
 ok=len(groups)==6 and Counter(t for c,t,x in matches if c==0)==required and all(c==0 for c,t,x in matches)
 records.append(dict(raw=str(path),png_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
  pixel_exact=ok,group_count=len(groups),costs=[c for c,t,x in matches],starts=[x for c,t,x in matches]))
assert len(records)==16
Path('evidence/r1_f1_ab/AB_16_FRAME_PIXEL_AUDIT.json').write_text(json.dumps(records,indent=2)+'\n')
print('REAL_STELLA_AB_FRAME_COUNT',len(records),'EXACT',sum(r['pixel_exact'] for r in records))
print('FIRST_FRAME',records[0])
PY
sha256sum evidence/r1_f1_ab/raw/*.png > evidence/r1_f1_ab/RAW_SCREENSHOT_SHA256.txt
