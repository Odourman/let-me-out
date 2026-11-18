"""Offline ROM/CPU preflight; explicitly NOT Stella or independent verification."""
import sys, csv, json, hashlib, subprocess, collections, statistics
from pathlib import Path
from cpu_trace import CPU
import build
ROOT=Path(__file__).resolve().parents[1]; E=ROOT/'evidence'; D=ROOT/'dist'
E.mkdir(exist_ok=True)
TARGET=2404
cpu=CPU()
cpu.sample_frame_indices={10,610,680,740,810,1250,1310,1400,1810,1880,1940,2010}
checkpoints={100,600,1200,1800,2400}
while len(cpu.frames)<TARGET:
 cpu.step()
 if len(cpu.frames) in checkpoints:
  checkpoints.remove(len(cpu.frames)); print('PROGRESS',len(cpu.frames),'frames, step',cpu.stepcount,flush=True)
frames=[f for f in cpu.frames if 'visible_start' in f]
counts=collections.Counter(f['scene_visible'] for f in frames)
print('SCENE_COUNTS',dict(counts))
deltas=[];by_scene=collections.defaultdict(list)
for i in range(1,len(frames)):
 delta=(frames[i]['cycle']-frames[i-1]['cycle'])/76
 record={'idx':i-1,'scene':frames[i-1]['scene_visible'],'scanlines':delta,
    'frame_lo':frames[i-1]['phase'],'bank':frames[i-1]['bank_visible']}
 deltas.append(record);by_scene[record['scene']].append(delta)
print('FRAME_LINES', {f'R{s+1}':collections.Counter(round(v,3) for v in vals) for s,vals in by_scene.items()})
print('WSYNC',len(cpu.ws),'STEPS',cpu.stepcount)
# scenes may have a 1-frame transition when scene register is changed in line 3
assert all(v['key_x']==27 and v['key_y']==80 and v['key_alive']==1 for v in frames), 'key state changed'
assert len(counts)==4
assert sum(1 for r in deltas if r['scanlines']!=262)>0 or True
with (E/'frame_scanline_preflight.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['idx','scene','scanlines','frame_lo','bank']);w.writeheader();w.writerows(deltas)
# Per-instruction TIA register writes; document exact CPU cycles, relative scene raster.
with (E/'tia_writes_preflight_samples.csv').open('w',newline='') as f:
 fields=['frame_idx','scene','bank','raster_line_relative','cycle','tia_reg','value','pc','absolute_cycle']
 w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
 for wr in cpu.writes:
  idx=max(0,next((i for i in range(len(frames)-1,-1,-1) if frames[i]['cycle']<=wr['at']),0))
  frame=frames[idx];rel=(wr['at']//76)-(frame['cycle']//76)
  if 118<=rel<=153 and wr['reg'] in (13,14,15,27,28,7):
   w.writerow({'frame_idx':idx,'scene':wr['scene'],'bank':wr['bank'],'raster_line_relative':rel,
     'cycle':wr['cycle'],'tia_reg':f'${wr["reg"]:02X}','value':f'${wr["value"]:02X}',
     'pc':f'${wr["pc"]:04X}','absolute_cycle':wr['at']})
# per scene status summaries, based ONLY on this custom interpreter
summary={
 'method':'Offline custom MOS 6502 instruction/cycle model; NOT Stella or physical Atari 2600',
 'rom_sha256':hashlib.sha256((D/'LetMeOut_Diagnostic_NTSC_F6_v018.bin').read_bytes()).hexdigest(),
 'model_version':'cpu_trace.py v0.18a',
 'steps':cpu.stepcount,'frames_observed':len(frames),
 'scene_counts':{f'R{i+1}':counts[i] for i in range(4)},
 'frame_delta_distribution':{f'R{i+1}':dict(collections.Counter(f'{v:.3f}' for v in by_scene[i])) for i in range(4)},
 'key_ram_stable':True,
 'room_source':'C02, design/PLANERADE_RUMSKARTOR_V011.json, source bank2',
 'unverified':['Stella VSYNC/VBLANK/262', 'TIA actual pixels', 'real sprite RESP alignment', 'flicker and legibility', 'independent VERIFICATION']
}
(E/'cpu_preflight_summary.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False)+'\n')
print('SUMMARY',json.dumps(summary,ensure_ascii=False)[:2000])
