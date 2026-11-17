#!/usr/bin/env python3
"""G5AJ exact Stella 6.7.1 response/GUI/native F9-only audit; fail closed."""
import csv,hashlib,json,re,sys
from pathlib import Path
from PIL import Image
root=Path(sys.argv[1]).resolve() if len(sys.argv)>1 and sys.argv[1]!='--gate' else None
# Do not treat typed commands as observed; only actual Stella saveSes.

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else 'MISSING'
def extracted(s,name):
 lines=s.splitlines();result=[]
 needle=re.compile(r'(?i)\bprint\s+'+re.escape(name)+r'\s*$')
 for i,line in enumerate(lines):
  if not needle.search(line.strip()):continue
  for t in lines[i+1:i+4]:
   v=t.strip()
   if re.search(r'(?i)\b(print|saveSes|saveSnap|tia)\b',v):break
   dec=re.findall(r'#(\d+)\b',v)
   if dec:result.append(int(dec[-1]));break
   m=re.search(r'(?<![\w])(?:\$([0-9a-fA-f]+)|(\d+))(?![\w])',v)
   if m:result.append(int(m.group(1),16) if m.group(1) else int(m.group(2)));break
 return result

def parsed(path):
 s=path.read_text(errors='replace') if path.exists() else ''
 d={'path':path.name,'bytes':path.stat().st_size if path.exists() else 0,
    'sha256':sha(path),'stella_version_printed':'Stella 6.7.1' in s,
    'has_tia':'COLUxx:' in s and 'P0:' in s and 'P1:' in s and 'M0:' in s,
    'step_completed':'executed 3 cycles' in s,
    'break_set':bool(re.search(r'set breakpoint at \$f1ee \+ mirrors in bank #0',s,re.I)),
    'break_cleared':bool(re.search(r'cleared breakpoint',s,re.I))}
 for k in ['pc','_fCount','_scan','_sCycles','_bank']:
  d[k]=extracted(s,k)
 return d

def last(d,k):return d[k][-1] if d[k] else None

def session_gate(g,p):
 d=parsed(p)
 if g=='A_TRAP':
  return d['bytes']>700 and d['has_tia'] and d['pc']==[0xF1F0,0xF1F0] and d['_fCount']==[136] and d['_scan']==[123,123] and d['_sCycles']==[21] and d['_bank']==[0]
 if g=='B_HANDSHAKE':
  return d['bytes']>150 and d['stella_version_printed'] and bool(d['pc']) and bool(d['_bank']) and not d['break_set']
 if g=='B_AFTER_FRAME':
  return d['bytes']>250 and last(d,'_fCount')==136 and last(d,'_bank')==0
 if g=='B_BREAK_ACK':
  return d['bytes']>300 and d['break_set'] and not d['break_cleared'] and last(d,'_bank')==0
 if g=='B_PRE_STEP':
  return d['bytes']>700 and d['has_tia'] and last(d,'pc')==0xF1EE and last(d,'_fCount')==136 and last(d,'_scan')==123 and last(d,'_bank')==0 and len(d['pc'])>=2 and d['pc'][-2:]==[0xF1EE,0xF1EE]
 if g=='C_POST_STEP':
  return d['bytes']>700 and d['has_tia'] and d['step_completed'] and last(d,'pc')==0xF1F0 and last(d,'_fCount')==136 and last(d,'_scan')==123 and last(d,'_bank')==0 and len(d['pc'])>=2 and d['pc'][-2:]==[0xF1F0,0xF1F0]
 return False

def native(p):
 if not p.exists():return {'exists':False,'sha256':'MISSING','size':None,'ok':False}
 try:
  with Image.open(p) as im:
   out={'exists':True,'sha256':sha(p),'size':[im.width,im.height],'mode':im.mode}
   out['ok']=im.size==(320,228) and im.mode=='RGB'
   return out
 except Exception as e:return {'exists':True,'sha256':sha(p),'error':str(e),'ok':False}

if sys.argv[1]=='--gate':
 name,p=sys.argv[2],Path(sys.argv[3]);d=parsed(p);ok=session_gate(name,p)
 print('G5AJ_LIVE_COMMAND_RESPONSE_GATE',json.dumps({'gate':name,'pass':ok,'observed':d}),flush=True)
 sys.exit(0 if ok else 5)

A=root/'A_TRAP';B=root/'B_BREAK_STEP'
files={'A_TRAP':A/'A_TRAP_debugger_session.txt',
       'B_HANDSHAKE':B/'B_HANDSHAKE_debugger_session.txt',
       'B_AFTER_FRAME':B/'B_AFTER_FRAME_debugger_session.txt',
       'B_BREAK_ACK':B/'B_BREAK_ACK_debugger_session.txt',
       'B_PRE_STEP':B/'B_PRE_STEP_debugger_session.txt',
       'C_POST_STEP':B/'C_POST_STEP_debugger_session.txt'}
sessions={k:parsed(v) for k,v in files.items()}
gates={k:session_gate(k,v) for k,v in files.items()}
images={'A_TRAP':native(A/'A_TRAP_native_TIA.png'),
        'B_PRE_STEP':native(B/'B_PRE_STEP_native_TIA.png'),
        'C_POST_STEP':native(B/'C_POST_STEP_native_TIA.png')}
winlogs={k:(folder/f'window_poll_{stage}.tsv').read_text(errors='replace') if (folder/f'window_poll_{stage}.tsv').exists() else '' for k,folder,stage in [('A_TRAP',A,'A_TRAP'),('B_INITIAL_PROMPT',B,'B_INITIAL_PROMPT'),('B_REENTRY',B,'B_REENTRY')]}
windows={k:any('Stella 6.7.1: Debugger mode' in line for line in text.splitlines()) for k,text in winlogs.items()}
Apass=bool(gates['A_TRAP'] and images['A_TRAP']['ok'] and windows['A_TRAP'] and (A/'STAGE_A_PASS.txt').exists())
Bpass=bool(Apass and all(gates[x] for x in ['B_HANDSHAKE','B_AFTER_FRAME','B_BREAK_ACK','B_PRE_STEP'])
            and images['B_PRE_STEP']['ok'] and windows['B_INITIAL_PROMPT'] and windows['B_REENTRY']
            and (B/'STAGE_B_BREAK_SET.txt').exists() and (B/'STAGE_B_REENTRY_PASS.txt').exists())
pre=sessions['B_PRE_STEP'];post=sessions['C_POST_STEP']
Cpass=bool(Bpass and gates['C_POST_STEP'] and images['C_POST_STEP']['ok'] and (B/'STAGE_C_PASS.txt').exists()
           and len(pre['_sCycles'])>=1 and len(post['_sCycles'])>=1
           and post['_sCycles'][-1]-pre['_sCycles'][-1]==3
           and post['_scan'][-1]==pre['_scan'][-1]
           and post['_fCount'][-1]==pre['_fCount'][-1]
           and post['_bank'][-1]==pre['_bank'][-1])
romsha=(root/'F9_ROM_SHA_PRE.txt').read_text(errors='replace') if (root/'F9_ROM_SHA_PRE.txt').exists() else ''
postsha=(root/'F9_ROM_SHA_POST.txt').read_text(errors='replace') if (root/'F9_ROM_SHA_POST.txt').exists() else ''
rom_ok='OK' in romsha and 'OK' in postsha
ready=Apass and Bpass and Cpass and rom_ok and (root/'script_exit_code.txt').read_text().strip()=='0'
status='G5AJ_F9_METHOD_READY_BOUNDED' if ready else ('G5AJ_F9_METHOD_PARTIAL_NOT_DETERMINABLE' if Apass else 'G5AJ_F9_TRAP_CONTROL_FAIL')
if (root/'script_exit_code.txt').read_text().strip()!='0' and not Apass:
 status='G5AJ_F9_TRAP_CONTROL_FAIL'
rows=[]
for case in ['A_TRAP','B_HANDSHAKE','B_AFTER_FRAME','B_BREAK_ACK','B_PRE_STEP','C_POST_STEP']:
 d=sessions[case];pix=images.get(case,{})
 rows.append({'case':case,'measurement':'STELLA_OBSERVED' if gates[case] else 'NOT_DETERMINABLE',
              'passed':gates[case],'PC_observed':last(d,'pc'),'frame_observed':last(d,'_fCount'),
              'scan_observed':last(d,'_scan'),'sCycles_observed':last(d,'_sCycles'),
              'bank_observed':last(d,'_bank'),'break_set_response':d['break_set'],
              'step_three_cycles_response':d['step_completed'],
              'session_bytes':d['bytes'],'session_SHA256':d['sha256'],
              'native_320x228':pix.get('ok','NOT_APPLICABLE'),
              'native_SHA256':pix.get('sha256','NOT_APPLICABLE'),
              'source_inferred_BUS_WRITE_PHASE':'NOT_MEASURED_DIRECTLY',
              'F9_ROM_SHA256':'6c2585148eb082fb8bc794d664edc4869b18849fcfabb9cada23373d1dc1318b'})
with (root/'G5AJ_EVIDENCE.csv').open('w',newline='') as f:
 writer=csv.DictWriter(f,fieldnames=rows[0]);writer.writeheader();writer.writerows(rows)
summary={'verdict_before_archive_readback':status,'A_trap_PASS':Apass,'B_break_PASS':Bpass,'C_step_PASS':Cpass,
 'D_archive_readback_NOT_IN_THIS_JOB':True,'frozen_ROM_PRE_AND_POST_SHA_PASS':rom_ok,
 'session_result_gates':gates,'sessions':sessions,'native_TIA_images':images,'verified_debugger_window_logs':windows,
 'PC_before_STA_F1EE_source_only_if_not_observed':'SOURCE_INFERRED','STA_CPU_write_bus_clock':'SOURCE_INFERRED_NOT_DIRECTLY_MEASURED',
 'C0_X40_X104':'NOT_RUN_NO_ROM','new_ROM_build':False,
 'prior_G5AH_failure_and_hash_mismatch':'HISTORICAL_PRESERVED_UNCHANGED'}
(root/'G5AJ_AUDIT.json').write_text(json.dumps(summary,indent=2)+'\n')
(root/'G5AJ_STATUS.txt').write_text(status+'\n')
print('G5AJ_FINAL_MEASUREMENT_CLASSIFICATION',json.dumps({'status':status,'A':Apass,'B':Bpass,'C':Cpass,'hashes_before_after':rom_ok,'readback':'PENDING'},ensure_ascii=True),flush=True)
sys.exit(0 if ready else 7)
