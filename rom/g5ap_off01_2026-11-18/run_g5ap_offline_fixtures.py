#!/usr/bin/env python3
"""Reproducible G5AP OFF-01 synthetic regression runner. NEVER starts emulators.
Each specimen uses artificial Stella-like text and generated RGB PNGs.
No original G5AO user ZIP was available; recreate documented baseline from
GitHub G5AO report and extend with negative/positive edge cases.
"""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from PIL import Image

HERE=Path(__file__).resolve().parent
SRC=HERE/'audit_g5ap_offline.py'
spec=importlib.util.spec_from_file_location('g5ap_auditor',SRC)
aud=importlib.util.module_from_spec(spec)
spec.loader.exec_module(aud)

STAGES=aud.STAGES
A=STAGES[:5];B=STAGES[5:13]
ORIGINAL_G5AL_BLOB='f159c1f8668c1f504fd9538a8d1ef17b2ddefafa'
BASELINE_G5AO_ZIP_EXPECTED='c519555a974199a2c19e07583c179a2af32819af69d2b42ccdb00c4ba1aad633'


def git_blob_sha1(p):
    b=p.read_bytes();return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()


def record_entry(stage):
    return 'A_ENTRY_INITIAL' if stage in ('A_HANDSHAKE','A_FRAME','A_TRAP_ACK') else (
        'A_ENTRY_REENTRY' if stage in ('A_REENTRY_HANDSHAKE','A_TRAP') else (
        'B_ENTRY_INITIAL' if stage in ('B_HANDSHAKE','B_FRAME','B_SET_0','B_SET_1','B_SET_2','B_SET_3')
        else 'B_ENTRY_REENTRY'))


def print_cmd(name,value):
    return '> print '+name+'\nregister-value: $'+format(value,'x')+' #'+str(value)+'\n'


def make_session(root,stage,archive_id,entry,seq):
    text='Stella 6.7.1: OFFLINE_SYNTHETIC_FICTION_NOT_REAL_STELLA\n'
    text+=f'G5AP_SYNTHETIC_CAPTURE archive={archive_id} stage={stage} entry={entry} seq={seq}\n'
    if stage.endswith('HANDSHAKE'):
        text+=print_cmd('pc', 0xF1F0 if stage=='A_REENTRY_HANDSHAKE' else
                              0xF1EE if stage=='B_REENTRY_HANDSHAKE' else 0xF000)
        if stage in ('A_HANDSHAKE','B_HANDSHAKE'):text+=print_cmd('_bank',0)
    elif stage in ('A_FRAME','B_FRAME'):
        text+=print_cmd('pc',0xF063)+print_cmd('_fCount',136)+print_cmd('_bank',0)
    elif stage=='A_TRAP_ACK':
        text+='> trapWriteIf {_scan == #123 && _sCycles > #19 && _sCycles < #23} RESP1\nadded trap 0\n'
    elif stage.startswith('B_SET_'):
        n=int(stage[-1]);text+=f'> break $f1ee #{n}\nset breakpoint at $f1ee + mirrors in bank #{n}\n'
    elif stage in ('A_TRAP','B_PRE','C_POST'):
        if stage=='C_POST':text+='> step\nexecuted 3 cycles\n'
        pc=0xF1EE if stage=='B_PRE' else 0xF1F0
        cycles=18 if stage=='B_PRE' else 21
        text+=print_cmd('pc',pc)+print_cmd('_fCount',136)+print_cmd('_scan',123)
        text+=print_cmd('_sCycles',cycles)+print_cmd('_bank',0)
        text+='> tia\nCOLUxx: synthetic\nP0: synthetic\nP1: synthetic\nM0: synthetic\n'
        text+=print_cmd('pc',pc)+print_cmd('_scan',123)
    else:raise ValueError(stage)
    text+='> saveSes '+aud.session_path(root,stage).name+'\n'
    text+='G5AP_OFFLINE_ONLY_NOT_AN_EMULATOR_MEASUREMENT\n'*7
    return text


def create_fixture(root, stages=STAGES, archive_id='G5AP_SYNTHETIC_CASE', archive_sha_pass=True):
    root=Path(root)
    idx={'source_kind':aud.SOURCE_KIND,'archive_id':archive_id,'archive_sha_pass':archive_sha_pass,
         'stages':{},'native':{},'reference_sha256':''}
    for stage in stages:
        seq=(STAGES.index(stage)+1)*10
        p=aud.session_path(root,stage);p.parent.mkdir(parents=True,exist_ok=True)
        entry=record_entry(stage)
        s=make_session(root,stage,archive_id,entry,seq)
        p.write_text(s,encoding='utf-8')
        idx['stages'][stage]={'path':p.relative_to(root).as_posix(),'source_kind':aud.SOURCE_KIND,
                              'sha256':aud.sha256(p.read_bytes()),'entry_id':entry,
                              'command_seq':seq,
                              'event':'AFTER_RUN_REENTRY' if stage.endswith('REENTRY_HANDSHAKE') else 'SNAPSHOT'}
    ref=root/'ref_g5af/native_TIA_original.png';ref.parent.mkdir(exist_ok=True)
    Image.new('RGB',(320,228),(23,73,19)).save(ref)
    idx['reference_sha256']=aud.sha256(ref.read_bytes())
    for st in ('A_TRAP','B_PRE','C_POST'):
        if st in stages:
            p=aud.native_path(root,st)
            Image.new('RGB',(320,228),(23,73,19)).save(p)
            idx['native'][st]={'sha256':aud.sha256(p.read_bytes()),'source_kind':aud.SOURCE_KIND}
    save_index(root,idx)
    return idx


def save_index(root,idx):
    (Path(root)/aud.REGISTRY_NAME).write_text(json.dumps(idx,indent=2,sort_keys=True)+'\n')


def edit_session(root,stage,old,new,update_sha=True):
    p=aud.session_path(root,stage);text=p.read_text()
    assert old in text,(stage,old)
    p.write_text(text.replace(old,new,1))
    if update_sha:
        idx=aud.load_index(root)
        idx['stages'][stage]['sha256']=aud.sha256(p.read_bytes())
        save_index(root,idx)


def mutate_index(root,func):
    idx=aud.load_index(root);func(idx);save_index(root,idx)


def cli_gate(root,stage):
    """Same core validation as CLI, batchable without importing Pillow in 70 subprocesses."""
    from types import SimpleNamespace
    try:
        index=aud.load_index(root)
        r=aud.validate_stage(root,stage,index)
        if aud.validate_index_coherence(index,{}):r['pass']=False
        return SimpleNamespace(returncode=0 if r['pass'] else 7)
    except ValueError:
        return SimpleNamespace(returncode=7)


def cli_full(root):
    from types import SimpleNamespace
    try:r=aud.audit(root)
    except ValueError:r={'status':'OFFLINE_SYNTHETIC_METHOD_FAIL'}
    return SimpleNamespace(stdout=json.dumps(r),returncode=0 if r['status']=='OFFLINE_SYNTHETIC_A_B_C_CONTRACT_PASS' else 8)


class Registry:
    def __init__(self):self.results=[]
    def check(self,name,actual,expected,detail=None):
        passed=(actual==expected)
        result={'case':name,'expected':expected,'observed':actual,'assertion_pass':passed,
                'classification':'OFFLINE_SYNTHETIC','details':detail or ''}
        self.results.append(result)
        print(('PASS' if passed else 'FAIL')+' '+name+': expected='+repr(expected)+' actual='+repr(actual))
        if not passed:raise AssertionError(name+' EXPECTED '+repr(expected)+' ACTUAL '+repr(actual))


def full_status(r):
    try:return json.loads(r.stdout)['status']
    except Exception:return 'CRASH_RC_'+str(r.returncode)


def run_suite(tests:Registry, root):
    def temporary(case,stages=STAGES):
        p=root/case;create_fixture(p,stages,archive_id='CASE_'+case)
        return p
    p=temporary('positive_all')
    provenance=json.loads((HERE/'FROZEN_G5AL_SOURCE_VERIFICATION.json').read_text())
    tests.check('frozen G5AL original blob from checked GitHub connector metadata',
                provenance['github_verified_blob_sha1'],ORIGINAL_G5AL_BLOB)
    tests.check('frozen original 8426 byte length verified in connector',provenance['github_verified_size_bytes'],8426)
    if (HERE/'audit_g5al_frozen_original_reference.py').exists():
        tests.check('frozen original local copy git blob byteexact',
                    git_blob_sha1(HERE/'audit_g5al_frozen_original_reference.py'),ORIGINAL_G5AL_BLOB)
    tests.check('canonical stage path writer includes debugger_session',
                aud.session_path(p,'A_TRAP').name,'A_TRAP_debugger_session.txt')
    tests.check('all fourteen positive stage --gate calls',
                sum(cli_gate(p,s).returncode==0 for s in STAGES),len(STAGES))
    tests.check('all fourteen positive final stage checks',
                sum(aud.audit(p)['stage_checks'][s]['pass'] for s in STAGES),len(STAGES))
    tests.check('positive full ABC synthetic status',full_status(cli_full(p)),'OFFLINE_SYNTHETIC_A_B_C_CONTRACT_PASS')
    tests.check('positive full ABC actual synthetic flags',(aud.audit(p)['A_pass'],aud.audit(p)['B_pass'],aud.audit(p)['C_pass']),(True,True,True))
    tests.check('positive image reference pixels equal',aud.audit(p)['reference']['pass'],True)
    tests.check('positive C step from pre 18 to post21',aud.audit(p)['stage_checks']['C_POST']['values']['_sCycles'][-1]-aud.audit(p)['stage_checks']['B_PRE']['values']['_sCycles'][-1],3)
    tests.check('reported provenance always OFFLINE_SYNTHETIC',aud.audit(p)['source_kind'],'OFFLINE_SYNTHETIC')
    tests.check('report historical G5AL remains FAIL',aud.audit(p)['historic_G5AL'],'G5AL_F9_TRAP_CONTROL_FAIL_UNCHANGED')

    # G5AO-baseline bug reproductions are represented by the frozen original source as
    # read-only text; new parser must REJECT wrong reentry PC and ACCEPT correct.
    for stage in ('A_REENTRY_HANDSHAKE','B_REENTRY_HANDSHAKE'):
        q=temporary('wrong_pc_'+stage)
        old='#61936' if stage.startswith('A_') else '#61934'
        edit_session(q,stage,old,'#61440')
        tests.check('reject wrong PC '+stage,cli_gate(q,stage).returncode!=0,True)
        tests.check('full audit rejects wrong PC '+stage,aud.audit(q)['A_pass' if stage.startswith('A_') else 'B_pass'],False)
    tests.check('correct A reentry PC gate',cli_gate(p,'A_REENTRY_HANDSHAKE').returncode,0)
    tests.check('correct B reentry PC gate',cli_gate(p,'B_REENTRY_HANDSHAKE').returncode,0)

    q=temporary('A_only',A)
    tests.check('A-only full status PARTIAL_NOT_DETERMINABLE',full_status(cli_full(q)),'OFFLINE_SYNTHETIC_PARTIAL_NOT_DETERMINABLE')
    tests.check('A-only B/C false',(aud.audit(q)['B_pass'],aud.audit(q)['C_pass']),(False,False))
    tests.check('A-only full A true',aud.audit(q)['A_pass'],True)
    tests.check('A-only full read same canonical filenames',all(aud.audit(q)['stage_checks'][s]['pass'] for s in A),True)

    negative=[
        ('bank_4','A_TRAP','#0\n',' #4\n',None),
        ('A_frame_135','A_FRAME','#136\n','#135\n',None),
        ('B_frame_135','B_FRAME','#136\n','#135\n',None),
        ('A_scan_122','A_TRAP','#123\n','#122\n',None),
        ('A_cycles_22','A_TRAP','#21\n','#22\n',None),
        ('B_pre_scan_122','B_PRE','#123\n','#122\n',None),
        ('B_pre_bank_4','B_PRE','#0\n','#4\n',None),
        ('C_post_scan_122','C_POST','#123\n','#122\n',None),
        ('C_post_bank_4','C_POST','#0\n','#4\n',None),
        ('missing_pc','A_TRAP','> print pc\nregister-value: $f1f0 #61936\n','',None),
        ('duplicated_pc','A_TRAP','> saveSes ','> print pc\nregister-value: $f1f0 #61936\n> saveSes ',None),
        ('merged_print','A_TRAP','> print pc\nregister-value: $f1f0 #61936\n','> print pcprint _fCount\ntoo many arguments\n',None),
        ('missing_saveses','A_TRAP','> saveSes A_TRAP_debugger_session.txt\n','',None),
        ('missing_tia_text','A_TRAP','COLUxx: synthetic','MISSING_COLOR',None),
        ('wrong_break_ack','B_SET_2','set breakpoint at $f1ee + mirrors in bank #2','set breakpoint at $f1ee + mirrors in bank #1',None),
        ('cleared_break','B_SET_2','set breakpoint at $f1ee + mirrors in bank #2','cleared breakpoint at $f1ee + mirrors in bank #2',None),
        ('removed_trap','A_TRAP_ACK','added trap 0','removed trap 0',None),
        ('no_step_ack','C_POST','executed 3 cycles','executed 2 cycles',None),
        ('wrong_saveses_filename','A_TRAP','> saveSes A_TRAP_debugger_session.txt','> saveSes A_TRAP_session.txt',None),
    ]
    for name,stage,old,new,_ in negative:
        q=temporary(name)
        edit_session(q,stage,old,new)
        tests.check('negative --gate rejects '+name,cli_gate(q,stage).returncode!=0,True)
        tests.check('negative final stage rejects '+name,aud.audit(q)['stage_checks'][stage]['pass'],False)
    q=temporary('missing_bank_initial');edit_session(q,'A_HANDSHAKE',print_cmd('_bank',0),'')
    tests.check('missing bank initial rejected',cli_gate(q,'A_HANDSHAKE').returncode!=0,True)

    q=temporary('stale_hash');p2=aud.session_path(q,'A_TRAP');p2.write_text(p2.read_text()+'TAMPERED\n')
    tests.check('stale session SHA rejected',cli_gate(q,'A_TRAP').returncode!=0,True)
    tests.check('stale session detects SHA error','SESSION_HASH_STALE_OR_MISMATCH' in aud.validate_stage(q,'A_TRAP')['errors'],True)
    q=temporary('old_archive_id');edit_session(q,'A_TRAP','archive=CASE_old_archive_id','archive=ANCIENT_CASE')
    tests.check('old source archive marker rejected',cli_gate(q,'A_TRAP').returncode!=0,True)
    q=temporary('old_entry_id');edit_session(q,'A_REENTRY_HANDSHAKE','entry=A_ENTRY_REENTRY','entry=A_ENTRY_INITIAL')
    tests.check('old entry marker rejected',cli_gate(q,'A_REENTRY_HANDSHAKE').returncode!=0,True)
    q=temporary('reused_entry_id')
    mutate_index(q,lambda ix: ix['stages']['A_REENTRY_HANDSHAKE'].update(entry_id='A_ENTRY_INITIAL'))
    # Keep session marker and SHA up to date so cross-entry error is genuine.
    edit_session(q,'A_REENTRY_HANDSHAKE','entry=A_ENTRY_REENTRY','entry=A_ENTRY_INITIAL')
    tests.check('same initial entry reused for reentry rejected',cli_gate(q,'A_REENTRY_HANDSHAKE').returncode!=0,True)
    tests.check('reused entry coherence flagged',any('STALE_OR_REUSED_ENTRY' in e for e in aud.audit(q)['coherence_errors']),True)
    q=temporary('duplicate_sequence')
    mutate_index(q,lambda ix: ix['stages']['B_FRAME'].update(command_seq=ix['stages']['A_FRAME']['command_seq']))
    edit_session(q,'B_FRAME','seq=70','seq=20')
    tests.check('duplicated command sequence rejected',cli_gate(q,'B_FRAME').returncode!=0,True)
    q=temporary('bad_stage_name')
    mutate_index(q,lambda ix: ix['stages']['A_TRAP'].update(path='A_TRAP/A_TRAP_session.txt'))
    tests.check('noncanonical registered name rejected',cli_gate(q,'A_TRAP').returncode!=0,True)
    q=temporary('missing_file');aud.session_path(q,'A_TRAP').unlink()
    tests.check('missing session rejected',cli_gate(q,'A_TRAP').returncode!=0,True)
    tests.check('missing session final flagged',not aud.audit(q)['A_pass'],True)
    q=temporary('missing_index');(q/aud.REGISTRY_NAME).unlink()
    tests.check('missing capture registry rejected',cli_gate(q,'A_TRAP').returncode!=0,True)
    tests.check('missing capture registry full fail',full_status(cli_full(q)),'OFFLINE_SYNTHETIC_METHOD_FAIL')
    q=temporary('different_source_kind');mutate_index(q,lambda ix: ix.update(source_kind='STELLA_OBSERVED'))
    tests.check('STELLA_OBSERVED metadata rejected as offlinesynthetic',cli_gate(q,'A_TRAP').returncode!=0,True)
    q=temporary('missing_native');aud.native_path(q,'A_TRAP').unlink()
    tests.check('missing A native makes A FAIL',aud.audit(q)['A_pass'],False)
    q=temporary('tampered_native')
    Image.new('RGB',(320,228),(2,2,2)).save(aud.native_path(q,'A_TRAP'))
    tests.check('tampered native SHA rejected',aud.audit(q)['native_checks']['A_TRAP']['pass'],False)
    q=temporary('wrong_native_dimensions')
    pp=aud.native_path(q,'A_TRAP');Image.new('RGB',(160,228),(23,73,19)).save(pp)
    mutate_index(q,lambda ix: ix['native']['A_TRAP'].update(sha256=aud.sha256(pp.read_bytes())))
    tests.check('wrong native 160x228 rejected',aud.audit(q)['native_checks']['A_TRAP']['pass'],False)
    q=temporary('native_diff_reference')
    pp=q/'ref_g5af/native_TIA_original.png';Image.new('RGB',(320,228),(40,40,40)).save(pp)
    mutate_index(q,lambda ix: ix.update(reference_sha256=aud.sha256(pp.read_bytes())))
    tests.check('different native reference pixels rejected',aud.audit(q)['reference']['pass'],False)
    q=temporary('archive_pass_while_method_fail')
    edit_session(q,'A_TRAP','#21\n','#22\n')
    tests.check('archive SHA true does not elevate method fail',aud.audit(q)['status'],'OFFLINE_SYNTHETIC_METHOD_FAIL')
    tests.check('archive metadata pass retained separately',aud.audit(q)['archive_sha_claim'],True)
    q=temporary('B_only',B)
    tests.check('B without A full FAIL',aud.audit(q)['status'],'OFFLINE_SYNTHETIC_METHOD_FAIL')
    tests.check('B without A coherence error','B_REGISTERED_WITHOUT_A' in aud.audit(q)['coherence_errors'],True)
    q=temporary('C_only',('C_POST',))
    tests.check('C without B full FAIL',aud.audit(q)['status'],'OFFLINE_SYNTHETIC_METHOD_FAIL')
    tests.check('C without B coherence error','C_REGISTERED_WITHOUT_B' in aud.audit(q)['coherence_errors'],True)
    q=temporary('A_B_only',A+B)
    tests.check('A+B but missing C stays PARTIAL_NOT_DETERMINABLE',aud.audit(q)['status'],'OFFLINE_SYNTHETIC_PARTIAL_NOT_DETERMINABLE')
    tests.check('A+B actual C flag false',aud.audit(q)['C_pass'],False)
    q=temporary('C_cycles_delta_2')
    edit_session(q,'C_POST','#21\n','#20\n')
    tests.check('C +2 cycles not +3 rejected in fullaudit',aud.audit(q)['C_pass'],False)
    tests.check('C +2 fails full simulated readiness',aud.audit(q)['status'],'OFFLINE_SYNTHETIC_PARTIAL_NOT_DETERMINABLE')
    q=temporary('C_changed_entry')
    mutate_index(q,lambda ix: ix['stages']['C_POST'].update(entry_id='ANOTHER_ENTRY'))
    edit_session(q,'C_POST','entry=B_ENTRY_REENTRY','entry=ANOTHER_ENTRY')
    tests.check('C changed entry despite step without run rejected',cli_gate(q,'C_POST').returncode!=0,True)
    q=temporary('B_break_without_A')
    # Direct --gate rejection when staged B controls exist but A provenance missing.
    for s in A:
        if s in aud.load_index(q)['stages']:
            mutate_index(q,lambda ix,ss=s:ix['stages'].pop(ss,None))
    tests.check('B --gate rejects missing prior A registry',cli_gate(q,'B_SET_0').returncode!=0,True)
    q=temporary('duplicate_capture_marker')
    pp=aud.session_path(q,'A_TRAP');lines=pp.read_text().splitlines()
    marker=[z for z in lines if z.startswith('G5AP_SYNTHETIC_CAPTURE')][0]
    pp.write_text(pp.read_text()+marker+'\n')
    mutate_index(q,lambda ix:ix['stages']['A_TRAP'].update(sha256=aud.sha256(pp.read_bytes())))
    tests.check('duplicate capture provenance marker rejected',cli_gate(q,'A_TRAP').returncode!=0,True)
    q=temporary('missing_step_cmd')
    edit_session(q,'C_POST','> step\n','')
    tests.check('C step textual ACK without command rejected',cli_gate(q,'C_POST').returncode!=0,True)
    q=temporary('missing_break_cmd')
    edit_session(q,'B_SET_3','> break $f1ee #3\n','')
    tests.check('B set textual ACK without actual command rejected',cli_gate(q,'B_SET_3').returncode!=0,True)
    q=temporary('missing_trap_cmd')
    edit_session(q,'A_TRAP_ACK','> trapWriteIf {_scan == #123 && _sCycles > #19 && _sCycles < #23} RESP1\n','')
    tests.check('A trap textual ACK without actual trap command rejected',cli_gate(q,'A_TRAP_ACK').returncode!=0,True)

    # Also invoke actual separate-process CLI, not only Python function calls.
    sub=subprocess.run([sys.executable,str(SRC),'--gate','A_REENTRY_HANDSHAKE',
                        str(aud.session_path(p,'A_REENTRY_HANDSHAKE'))],text=True,capture_output=True,timeout=8)
    tests.check('real --gate CLI entry correctly accepted',sub.returncode,0)
    sub=subprocess.run([sys.executable,str(SRC),'--fullaudit',str(p)],text=True,capture_output=True,timeout=8)
    tests.check('real --fullaudit CLI full positive accepted',sub.returncode,0)
    sub=subprocess.run([sys.executable,str(SRC),'--fullaudit',str(q)],text=True,capture_output=True,timeout=8)
    tests.check('real --fullaudit CLI failed fixture rejected',sub.returncode!=0,True)
    tests.check('no unknown value type promoted to actual STELLA_OBSERVED',
                'STELLA_OBSERVED' not in json.dumps(aud.audit(p)),True)
    tests.check('historical G5AL failure never reclassified by synthetic success',
                aud.audit(p)['historic_G5AL']=='G5AL_F9_TRAP_CONTROL_FAIL_UNCHANGED',True)


def main():
    output=HERE/'G5AP_OFFLINE_TEST_RESULTS.json'
    with tempfile.TemporaryDirectory(prefix='g5ap_offline_') as temporary:
        tests=Registry()
        try:
            run_suite(tests,Path(temporary))
            all_pass=True
            exception=None
        except BaseException as ex:
            all_pass=False
            exception=repr(ex)
            print('OFFLINE_FIXTURE_SUITE_EXCEPTION '+exception,file=sys.stderr)
        payload={'project':'LET_ME_OUT','task':'G5AP_OFF-01','classification':'OFFLINE_SYNTHETIC',
                 'not_emulator_measurement':True,'historical_G5AL':'G5AL_F9_TRAP_CONTROL_FAIL_UNCHANGED',
                 'g5':'G5_FORMAL_OPEN','g5ao_zip_original_available':False,
                 'g5ao_expected_original_zip_sha256_unverified':BASELINE_G5AO_ZIP_EXPECTED,
                 'g5ao_baseline_source':'GitHub G5AO report 18/18, not original unattached ZIP',
                 'frozen_original_git_blob_expected':ORIGINAL_G5AL_BLOB,
                 'assertions':tests.results,'total_assertions':len(tests.results),
                 'passed_assertions':sum(t['assertion_pass'] for t in tests.results),
                 'failed_assertions':sum(not t['assertion_pass'] for t in tests.results),
                 'exception':exception,'result':'OFFLINE_ONLY_PASS' if all_pass else 'OFFLINE_ONLY_FAIL',
                 'no_stella_gopher_actions_rom_dasm':True}
        output.write_text(json.dumps(payload,ensure_ascii=False,indent=2,sort_keys=True)+'\n')
        print('G5AP_FINAL '+json.dumps({k:payload[k] for k in ('result','total_assertions','passed_assertions','failed_assertions','g5ao_zip_original_available')},sort_keys=True))
        return 0 if all_pass else 1

if __name__=='__main__':raise SystemExit(main())
