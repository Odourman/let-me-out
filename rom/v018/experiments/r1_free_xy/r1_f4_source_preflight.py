#!/usr/bin/env python3
"""R1-F4 G0: SOURCE-ONLY nine-row timing proof. NEVER invokes DASM/Stella.
Derived from frozen 6B unrolled generator and frozen F2/F3 transformations.
Not pixel proof, not permission to start a runtime / R2 / R4 experiment.
"""
from pathlib import Path
import hashlib,json,argparse
R=Path(__file__).resolve().parent
BASE='e268cf68c19543083e59b63b65087699ef281ec04c170a3cf624eab90c579012'
MASK_GIT_BLOB='058800a4c1904d1ff289e7e61b3902aa111ba16d'
def sha(b):return hashlib.sha256(b).hexdigest()
a=argparse.ArgumentParser();a.add_argument('--out',type=Path,default=R/'r1_f4_source_preflight.json');args=a.parse_args()
src=(R/'build_six_sweep.py').read_text()
f2=(R/'r1_f2_build_runtime.py').read_text()
f3=(R/'r1_f3_build.py').read_text()
assert "'6B':(types,[19,28,37,46,56,66])" in src
assert "clk=10" in src and "instructions.append(' STA RESP1');clk+=3" in src
assert "if tp!=prev:" in src and "' STA GRP1'" in src
assert "assert src.count(' STA RESP1\\n')" in src
assert "e268cf68c19543083e59b63b65087699ef281ec04c170a3cf624eab90c579012" in f2
assert " CPX #0\\n BNE *+2\\n STA RESP1\\n STA GRP1\\n BEQ *+2\\n STA RESP1\\n" in f2
assert " CPY #0\\n BNE *+2\\n STA RESP1\\n STA GRP1\\n BEQ *+2\\n STA RESP1\\n" in f3
canon=(R/'canon_masks.json').read_bytes()
assert hashlib.sha1(b'blob '+str(len(canon)).encode()+b'\\0'+canon).hexdigest()==MASK_GIT_BLOB
ref=json.loads(canon)
assert list(ref['sprites'])==['large_male','large_female','small_male','small_female']
for t,bits in ref['sprites'].items():assert len(bits)==9 and all(len(b)==8 and set(b)<={'0','1'} for b in bits)
def timing(phase):
    # WSYNC c0; LDA P0 2; STA GRP0 3; LDA M0 2; STA ENAM0 3;
    # LDA index0 bitmap 2; x=0 for pre-kernel F2 fixed index2.
    initial=12
    if phase==18:
        pre=[('BIT FRAMELO',3)]
        post=[('NOP',2),('NOP',2),('STA RESP1',3)]
    elif phase==19:
        pre=[('NOP',2),('NOP',2)]
        post=[('BIT FRAMELO',3),('STA RESP1',3)]
    elif phase==20:
        pre=[('CPY #0',2),('BNE *+2 TAKEN',3)]
        post=[('BEQ *+2 NOTTAKEN',2),('STA RESP1',3)]
    elif phase==21:
        pre=[('NOP',2),('NOP',2),('NOP',2)]
        post=[('STA RESP1,X (zeropage indexed X=0)',4)]
    else:raise ValueError(phase)
    r0=initial+sum(c for _,c in pre)+3
    grp0=r0+3
    r1=grp0+sum(c for _,c in post)
    assert r0==phase and r1==28,(r0,r1,phase)
    assert all(c>=2 for op,c in pre+post)
    # Later F2 fixed index2: LDA sprite2 2; CPX#0 2; BNE NOTTAKEN2;
    # STA RESP1 3 at 37; STA GRP1 at 40; BEQ TAKEN3; STA RESP1 at 46.
    return dict(first_resp=r0,first_grp=grp0,second_resp=r1,
       third_resp=37,third_grp=40,fourth_resp=46,fifth_resp=56,
       sixth_resp=66,last_grp=69,WSYNC_write=72,
       early_instructions=pre+[('STA RESP1 (zero page)',3),('STA GRP1 (zero page)',3)]+post,
       X_fixed=0,NUSIZ1=1,bank=0)
rows=[]
for y in range(9):
    row={'source_mask_row':y,'P0_GRP0_cycle':5,'M0_ENAM0_cycle':10,
         '6B':timing(19),'F3_c20':timing(20),'F4_c18':timing(18),
         'F4_c21':timing(21)}
    for k in ('6B','F3_c20','F4_c18','F4_c21'):
        t=row[k];assert t['second_resp']==28 and t['third_resp']==37
        assert [t[n] for n in ('fourth_resp','fifth_resp','sixth_resp')]==[46,56,66]
        assert t['last_grp']==69 and t['WSYNC_write']==72 and 72<76
    rows.append(row)
res={'F4_G0':'SOURCE_ONLY_FEASIBLE_C18_AND_C21_NOT_STELLA',
     'derived_from_6B_ROM_sha256':'36e588b7211be9dfe6afc534117823f6540aa6d3b753c2816a22c5828d0b60b4',
     'frozen_F2_runtime_ROM_sha256':'941c943e9000ca062cc5430cf28bcd34ca92beb70257f4dd84109c487b7c3e2b',
     'frozen_F3_g0_ROM_sha256':'1ed9cd9f735dcbf4cd2dc731da607d84a9c4f85f3c894a4dbd48d2d3fc50c286',
     'canon_git_blob':MASK_GIT_BLOB,'source_sha256':{p:sha((R/p).read_bytes()) for p in ['build_six_sweep.py','r1_f2_build_runtime.py','r1_f3_build.py','canon_masks.json']},
     'linear_requested_crop_X_prior_to_stella':{'c18':[37,75,129,183,243,303],'c21':[55,75,129,183,243,303]},
     'linear_model_is_HYPOTHESIS_not_fixed_acceptance_target':True,
     'physical_success_condition':'observed x0 differs from 43, every original 8x9 row source exact at newly observed x0 on 16 real frames, five others exactly unchanged, P0/M0/PF/NTSC retained',
     'cpu_source_only_not_real_traps':True,'source_rows':rows}
args.out.write_text(json.dumps(res,indent=2)+'\n')
print('F4_G0_SOURCE_ONLY_PASS c18=c18/c21 first-resp, index1=28 index2=37 last GRP1=69 WSYNC=72')
print('F4_G0_SOURCE_TIMING_NINE_ROWS',len(rows),'not DASM or Stella evidence')
