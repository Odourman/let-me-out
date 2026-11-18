#!/usr/bin/env python3
"""G5AP OFF-01: offline-only repair of frozen G5AL session audit.

NO emulator input is trusted or executed. Every accepted fixture requires the
OFFLINE_SYNTHETIC marker, a separate capture registry, exact recorded file SHA,
matching archive/stage/entry/sequence IDs, and a real command/result pairing.
This is NOT a drop-in runtime adapter for stock Stella saveSes and is NOT
independent verification of the Atari ROM/TIA.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from PIL import Image, ImageChops

SOURCE_KIND = 'OFFLINE_SYNTHETIC'
REGISTRY_NAME = 'G5AP_CAPTURE_INDEX.json'
STAGES = ('A_HANDSHAKE','A_FRAME','A_TRAP_ACK','A_REENTRY_HANDSHAKE','A_TRAP',
          'B_HANDSHAKE','B_FRAME','B_SET_0','B_SET_1','B_SET_2','B_SET_3',
          'B_REENTRY_HANDSHAKE','B_PRE','C_POST')
A_REQUIRED = STAGES[:5]
B_REQUIRED = STAGES[5:13]
KEYS = ('pc','_fCount','_scan','_sCycles','_bank')
CMD_RE = re.compile(r'^\s*>\s*(.*?)\s*$')
PRINT_RE = re.compile(r'^print\s+(pc|_fCount|_scan|_sCycles|_bank)$',re.I)
VALUE_RE = re.compile(r'(?<!\w)#(\d+)\b')
MARK_RE = re.compile(r'^G5AP_SYNTHETIC_CAPTURE\s+(.+)$')


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def session_path(root: Path, stage: str) -> Path:
    """One canonical filename used by writer, --gate and complete audit."""
    if stage not in STAGES:
        raise ValueError('UNKNOWN_STAGE')
    directory = 'A_TRAP' if stage.startswith('A_') else 'B_BREAK_STEP'
    return Path(root) / directory / (stage + '_debugger_session.txt')


def native_path(root: Path, stage: str) -> Path:
    if stage not in ('A_TRAP','B_PRE','C_POST'):
        raise ValueError('NO_NATIVE_FOR_STAGE')
    return Path(root) / ('A_TRAP' if stage.startswith('A_') else 'B_BREAK_STEP') / (stage + '_native_TIA.png')


def load_index(root: Path) -> dict:
    p = Path(root) / REGISTRY_NAME
    try:
        index = json.loads(p.read_text(encoding='utf-8'))
    except (OSError, ValueError) as ex:
        raise ValueError('REGISTRY_MISSING_OR_INVALID') from ex
    if index.get('source_kind') != SOURCE_KIND:
        raise ValueError('REGISTRY_NOT_OFFLINE_SYNTHETIC')
    if not isinstance(index.get('archive_id'),str) or not index['archive_id']:
        raise ValueError('REGISTRY_ARCHIVE_ID_MISSING')
    if not isinstance(index.get('stages'),dict):
        raise ValueError('REGISTRY_STAGES_INVALID')
    return index


def parse_commands(session: str) -> tuple[dict,list[str],dict]:
    """Pair exact `> print foo` command with a #decimal on its OWN response line.

    Commands fused together, duplicated or missing responses and parser errors
    are rejected.  A text fragment with `print` is never a real command ACK.
    """
    lines = session.splitlines()
    commands = []
    for i,line in enumerate(lines):
        m = CMD_RE.fullmatch(line)
        if m: commands.append((i,m.group(1)))
    vals = {k:[] for k in KEYS}
    issues = []
    for position,(i,cmd) in enumerate(commands):
        next_index = commands[position+1][0] if position+1 < len(commands) else len(lines)
        region = '\n'.join(lines[i+1:next_index])
        if re.search(r'(?i)\b(too many arguments|invalid expression|unknown command|error:)\b',region):
            issues.append('PROMPT_COMMAND_ERROR')
        if 'print' in cmd.lower() and not PRINT_RE.fullmatch(cmd):
            issues.append('MALFORMED_OR_JOINED_PRINT')
        pr = PRINT_RE.fullmatch(cmd)
        if pr:
            key = next(k for k in KEYS if k.lower()==pr.group(1).lower())
            response = [int(m.group(1)) for line in lines[i+1:next_index]
                        for m in VALUE_RE.finditer(line)]
            if len(response)!=1:
                issues.append('PRINT_RESPONSE_NOT_EXACTLY_ONE:'+key)
            else: vals[key].append(response[0])
    if any('too many arguments' in line.lower() for line in lines):
        issues.append('PROMPT_COMMAND_ERROR')
    if any('print pcprint' in line.lower() for line in lines):
        issues.append('JOINED_PRINT_PC')
    command_strs = [cmd for _,cmd in commands]
    return vals,sorted(set(issues)),{'commands':command_strs,'text':session}


def validate_stage(root: Path, stage: str, index: dict|None=None) -> dict:
    path = session_path(root,stage)
    out = {'stage':stage,'path':str(path.relative_to(root)),
           'source_kind':SOURCE_KIND,'pass':False,'errors':[]}
    def err(s):out['errors'].append(s)
    if index is None:
        try:index=load_index(root)
        except ValueError as ex:err(str(ex));return out
    record=index['stages'].get(stage)
    if record is None:
        err('STAGE_NOT_REGISTERED');return out
    if not path.is_file():
        err('SESSION_FILE_MISSING');return out
    if record.get('path')!=path.relative_to(root).as_posix():
        err('NONCANONICAL_REGISTRY_PATH')
    raw=path.read_bytes()
    out['bytes']=len(raw)
    out['sha256']=sha256(raw)
    if out['sha256']!=record.get('sha256'):
        err('SESSION_HASH_STALE_OR_MISMATCH')
    if len(raw)<180:err('SESSION_TOO_SHORT')
    try:s=raw.decode('utf-8')
    except UnicodeDecodeError:err('SESSION_NOT_UTF8');return out
    markers = [x for x in s.splitlines() if MARK_RE.fullmatch(x)]
    if len(markers)!=1:
        err('CAPTURE_MARKER_MISSING_OR_DUPLICATED');marker={}
    else:
        marker={}
        for token in markers[0].split()[1:]:
            if '=' in token:
                a,b=token.split('=',1);marker[a]=b
        expected={'archive':index['archive_id'],'stage':stage,
                  'entry':str(record.get('entry_id','')),'seq':str(record.get('command_seq',''))}
        if any(marker.get(k)!=v for k,v in expected.items()):
            err('MARKER_INDEX_PROVENANCE_MISMATCH')
    if record.get('source_kind')!=SOURCE_KIND:
        err('STAGE_NOT_OFFLINE_SYNTHETIC')
    if not isinstance(record.get('command_seq'),int) or record['command_seq']<=0:
        err('COMMAND_SEQUENCE_INVALID')
    if not isinstance(record.get('entry_id'),str) or not record.get('entry_id'):
        err('ENTRY_ID_MISSING')
    if 'Stella 6.7.1' not in s:err('VERSION_HEADER_MISSING')
    vals,problems,d=parse_commands(s)
    out['values']=vals
    for e in problems:err(e)
    commands=d['commands']
    if not any(c.startswith('saveSes ') and c.endswith(path.name) for c in commands):
        err('SAVESES_CANONICAL_COMMAND_MISSING')
    if len([c for c in commands if c.startswith('saveSes ')])!=1:
        err('SAVESES_COUNT_INVALID')
    if not commands or not commands[-1].startswith('saveSes '):
        err('SAVESES_NOT_LAST_COMMAND')

    def exact(k,n,expect=None):
        found=vals[k]
        if len(found)!=n:err('PRINT_COUNT_'+k)
        if expect is not None and (len(found)!=n or any(x!=expect for x in found)):
            err('WRONG_'+k)
    def bank(n=1):
        exact('_bank',n)
        if vals['_bank'] and any(x not in (0,1,2,3) for x in vals['_bank']):
            err('BANK_OUTSIDE_F6_RANGE')
    def frame():exact('_fCount',1,136)
    if stage in ('A_HANDSHAKE','B_HANDSHAKE'):
        exact('pc',1);bank()
    elif stage in ('A_REENTRY_HANDSHAKE','B_REENTRY_HANDSHAKE'):
        exact('pc',1,0xF1F0 if stage.startswith('A_') else 0xF1EE)
        if record.get('event')!='AFTER_RUN_REENTRY':err('NO_NEW_REENTRY_EVENT')
    elif stage in ('A_FRAME','B_FRAME'):
        frame();exact('pc',1);bank()
    elif stage=='A_TRAP_ACK':
        if not any(c.startswith('trapWriteIf ') for c in commands):err('TRAP_COMMAND_MISSING')
        if not re.search(r'(?im)^\s*added trap\s+\$?[0-9a-f]+\s*$',s):
            err('TRAP_SET_ACK_MISSING')
        if re.search(r'(?i)removed trap',s):err('TRAP_REMOVED')
    elif stage=='A_TRAP':
        exact('pc',2,0xF1F0);exact('_scan',2,123);exact('_sCycles',1,21);frame();bank()
        if not all(x in s for x in ('COLUxx:','P0:','P1:','M0:')):
            err('TIA_REGISTER_TEXT_MISSING')
    elif stage.startswith('B_SET_'):
        n=int(stage[-1]);reg=re.escape('set breakpoint at $f1ee + mirrors in bank #'+str(n))
        if not any(c.lower()==('break $f1ee #'+str(n)) for c in commands):err('BREAK_COMMAND_MISSING_OR_WRONG_BANK')
        if not re.search(reg,s,re.I):err('BREAK_SET_ACK_MISSING_OR_WRONG_BANK')
        if re.search(r'(?i)cleared breakpoint',s):err('BREAK_WAS_CLEARED')
    elif stage=='B_PRE':
        exact('pc',2,0xF1EE);exact('_scan',2,123);frame();bank();exact('_sCycles',1)
        if not all(x in s for x in ('COLUxx:','P0:','P1:','M0:')):
            err('TIA_REGISTER_TEXT_MISSING')
    elif stage=='C_POST':
        if 'step' not in commands:err('STEP_COMMAND_MISSING')
        exact('pc',2,0xF1F0);exact('_scan',2,123);frame();bank();exact('_sCycles',1)
        if len(re.findall('executed 3 cycles',s,re.I))!=1:err('STEP_THREE_CYCLES_ACK_MISSING_OR_DUPLICATED')
        if not all(x in s for x in ('COLUxx:','P0:','P1:','M0:')):
            err('TIA_REGISTER_TEXT_MISSING')
    out['entry_id']=record.get('entry_id')
    out['command_seq']=record.get('command_seq')
    out['pass']=not out['errors']
    return out


def validate_index_coherence(index:dict, details:dict) -> list[str]:
    errors=[];records=index.get('stages',{})
    order=[records[s].get('command_seq') for s in STAGES if s in records]
    if any(not isinstance(x,int) or x<1 for x in order) or len(order)!=len(set(order)):
        errors.append('COMMAND_SEQUENCE_DUPLICATED_OR_INVALID')
    # Monotone order in canonical A->B->C capture progression.
    if any(a>=b for a,b in zip(order,order[1:])):
        errors.append('COMMAND_SEQUENCE_NOT_MONOTONE')
    for newer,prior in (('A_REENTRY_HANDSHAKE','A_FRAME'),('B_REENTRY_HANDSHAKE','B_FRAME')):
        if newer in records and prior in records:
            if records[newer].get('entry_id')==records[prior].get('entry_id'):
                errors.append('STALE_OR_REUSED_ENTRY:'+newer)
    for newer,prior in (('A_TRAP','A_REENTRY_HANDSHAKE'),('B_PRE','B_REENTRY_HANDSHAKE'),('C_POST','B_PRE')):
        if newer in records and prior in records:
            if records[newer].get('entry_id')!=records[prior].get('entry_id'):
                errors.append('ENTRY_CHANGED_WITHOUT_RUN:'+newer)
    if any(s.startswith('B_') for s in records) and not all(s in records for s in A_REQUIRED):
        errors.append('B_REGISTERED_WITHOUT_A')
    if 'C_POST' in records and not all(s in records for s in B_REQUIRED):
        errors.append('C_REGISTERED_WITHOUT_B')
    return errors


def native_info(root:Path,stage:str,index:dict)->dict:
    p=native_path(root,stage);rec=index.get('native',{}).get(stage)
    out={'pass':False,'sha256':'MISSING','errors':[]}
    if not rec:
        out['errors'].append('NATIVE_NOT_REGISTERED');return out
    if not p.is_file():
        out['errors'].append('NATIVE_MISSING');return out
    out['sha256']=sha256(p.read_bytes())
    if out['sha256']!=rec.get('sha256'):out['errors'].append('NATIVE_SHA_MISMATCH')
    try:
        with Image.open(p) as im:
            out['size']=list(im.size);out['mode']=im.mode
            if im.size!=(320,228) or im.mode!='RGB':out['errors'].append('NATIVE_FORMAT_WRONG')
    except Exception:
        out['errors'].append('NATIVE_UNREADABLE')
    out['pass']=not out['errors'];return out


def compare_reference(root:Path,index:dict)->dict:
    ref=Path(root)/'ref_g5af'/'native_TIA_original.png'
    new=native_path(root,'A_TRAP')
    out={'pass':False,'errors':[]}
    if not ref.is_file() or not new.is_file():
        out['errors'].append('REFERENCE_OR_NEW_NATIVE_MISSING');return out
    out['reference_sha256']=sha256(ref.read_bytes())
    if out['reference_sha256']!=index.get('reference_sha256'):
        out['errors'].append('REFERENCE_SHA_MISMATCH')
    try:
        with Image.open(ref) as a,Image.open(new) as b:
            out['pixel_equal']=a.size==b.size and a.mode==b.mode and ImageChops.difference(a,b).getbbox() is None
            if not out['pixel_equal']:out['errors'].append('REFERENCE_PIXELS_DIFFER')
    except Exception:
        out['errors'].append('REFERENCE_OR_NEW_NATIVE_UNREADABLE')
    out['pass']=not out['errors'];return out


def audit(root:Path)->dict:
    index=load_index(root)
    stages={s:validate_stage(root,s,index) for s in STAGES}
    coherency=validate_index_coherence(index,stages)
    natives={s:native_info(root,s,index) for s in ('A_TRAP','B_PRE','C_POST')}
    ref=compare_reference(root,index)
    a=all(stages[s]['pass'] for s in A_REQUIRED) and natives['A_TRAP']['pass'] and ref['pass']
    b=a and not coherency and all(stages[s]['pass'] for s in B_REQUIRED) and natives['B_PRE']['pass']
    c=b and stages['C_POST']['pass'] and natives['C_POST']['pass']
    step_errors=[]
    if c:
        pre=stages['B_PRE']['values'];post=stages['C_POST']['values']
        if (post['_sCycles'][-1]-pre['_sCycles'][-1]!=3 or
            any(pre[k][-1]!=post[k][-1] for k in ('_fCount','_scan','_bank'))):
            step_errors.append('C_PRE_POST_CYCLE_FRAME_SCAN_OR_BANK_MISMATCH');c=False
    if coherency:
        a=False;b=False;c=False
    status=('OFFLINE_SYNTHETIC_A_B_C_CONTRACT_PASS' if a and b and c else
            'OFFLINE_SYNTHETIC_PARTIAL_NOT_DETERMINABLE' if a else
            'OFFLINE_SYNTHETIC_METHOD_FAIL')
    # Archive SHA can have PASS while method FAIL: never elevate method status.
    out={'source_kind':SOURCE_KIND,'archive_id':index['archive_id'],'stage_checks':stages,
         'native_checks':natives,'reference':ref,'coherence_errors':coherency,
         'step_errors':step_errors,
         'A_pass':bool(a),'B_pass':bool(b),'C_pass':bool(c),
         'archive_sha_claim':index.get('archive_sha_pass',False),
         'status':status,'historic_G5AL':'G5AL_F9_TRAP_CONTROL_FAIL_UNCHANGED',
         'historic_G5AJ':'G5AJ_F9_TRAP_CONTROL_FAIL_UNCHANGED',
         'G5':'G5_FORMAL_OPEN','rom_or_emulator_ran':False}
    return out


def main()->int:
    parser=argparse.ArgumentParser()
    parser.add_argument('--gate',nargs=2,metavar=('STAGE','SESSION'))
    parser.add_argument('--fullaudit',metavar='EVIDENCE_ROOT')
    args=parser.parse_args()
    if bool(args.gate)==bool(args.fullaudit):parser.error('choose --gate or --fullaudit')
    if args.gate:
        stage,path=args.gate
        try:
            path=Path(path).resolve()
            root=path.parent.parent
            if stage not in STAGES or path!=session_path(root,stage).resolve():
                raise ValueError('NONCANONICAL_STAGE_SESSION_PATH')
            index=load_index(root)
            result=validate_stage(root,stage,index)
            coherence=validate_index_coherence(index,{})
            if coherence:
                result['errors'].extend(coherence)
                result['pass']=False
        except ValueError as ex:
            result={'stage':stage,'pass':False,'errors':[str(ex)],'source_kind':SOURCE_KIND}
        print(json.dumps(result,sort_keys=True))
        return 0 if result['pass'] else 7
    try:result=audit(Path(args.fullaudit).resolve())
    except ValueError as ex:
        result={'status':'OFFLINE_SYNTHETIC_METHOD_FAIL','errors':[str(ex)],'source_kind':SOURCE_KIND,
                'A_pass':False,'B_pass':False,'C_pass':False}
    print(json.dumps(result,sort_keys=True))
    return 0 if result['status']=='OFFLINE_SYNTHETIC_A_B_C_CONTRACT_PASS' else 8

if __name__=='__main__':raise SystemExit(main())
