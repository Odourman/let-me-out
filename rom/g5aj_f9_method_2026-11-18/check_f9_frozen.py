#!/usr/bin/env python3
"""G5AJ frozen historical F9/source/list/sym and original TOP-DOWN mask gate."""
import hashlib,json,re,sys
from pathlib import Path
src=Path(sys.argv[1]);mask=json.loads(Path(sys.argv[2]).read_text())['sprites'];out=Path(sys.argv[3]);
base=src/'rom/v018/experiments/r1_free_xy'
stem='r1_f9_three_masks_three_binary_ram_x_ONE_ROM'
source=(base/(stem+'.asm')).read_bytes();lst=(base/'dist'/(stem+'.lst')).read_bytes();sym=(base/'dist'/(stem+'.sym')).read_bytes()
rom=(base/'dist'/(stem+'_F6.bin')).read_bytes();old=(base/'dist'/(stem+'.4k.bin')).read_bytes()
hash='6c2585148eb082fb8bc794d664edc4869b18849fcfabb9cada23373d1dc1318b'
assert len(rom)==16384 and hashlib.sha256(rom).hexdigest()==hash
assert len(old)==4096 and rom==old*4
L=lst.decode();S=source.decode();symbols=sym.decode()
for addr,op,name in [(0xF1EE,b'\x85\x11','RESP1'),(0xF1F0,b'\x85\x1c','GRP1'),(0xF1F6,b'\x85\x11','RESP1'),(0xF1F8,b'\x85\x1c','GRP1')]:
 assert old[(addr&0xfff):((addr&0xfff)+2)]==op
 matches=[line for line in L.splitlines() if re.search(r'\b'+f'{addr:04x}'+r'\b',line)]
 assert any('STA' in x.upper() and name in x.upper() for x in matches),(hex(addr),matches)
assert re.search(r'(?m)^X0_SELECT\s+00a0\b',symbols)
M=[int(v,2) for v in mask['large_male']]
assert M==[0x3c,0x3c,0x18,0xff,0x18,0x24,0x24,0x42,0x42]
for y,m in enumerate(M):
 label=f'F9_000_Row{y:02d}:'
 start=S.index(label)
 stop=S.find('\nF9_000_Row',start+len(label))
 if stop<0:stop=S.find('\nF9_001_Row',start+len(label))
 if stop<0:stop=S.find('\nF9AfterRows:',start+len(label))
 v=re.findall(r'\bLDA\s+#\$([0-9a-fA-F]{2})\b',S[start:stop])
 assert len(v)>=3 and int(v[2],16)==m,(label,v)
d={'F9_ROM_16KiB_SHA256':hash,'F6_bank_repetition':4,
   'original_source_SHA256':hashlib.sha256(source).hexdigest(),
   'original_lst_SHA256':hashlib.sha256(lst).hexdigest(),
   'original_sym_SHA256':hashlib.sha256(sym).hexdigest(),
   'original_TOPDOWN_mask_M_hex':['%02X'%i for i in M],
   'original_pre_STA_pc':'F1EE','original_pre_opcode':'85 11 STA RESP1',
   'original_post_STA_pc':'F1F0','source_CPU_cycle_count':3}
(out/'F9_FROZEN_STATIC_ORIGINAL_AUDIT.json').write_text(json.dumps(d,indent=2)+'\n')
print('G5AJ_F9_ORIGINAL_SOURCE_LIST_SYM_AND_MASK_STATIC_PASS',json.dumps(d),flush=True)
