#!/usr/bin/env python3
"""R1 authorized two-silhouette primitive: independent 2x2 X, all original 8x9.
Uses the previously verified R1af/R1ae delayed-GRP1 opcode pattern, but freshly
rebuilds a standalone source from the pinned original Venetian source and approved
mask JSON. No third-party Atari code is copied.
"""
from pathlib import Path
import hashlib,json,subprocess,re
HERE=Path(__file__).resolve().parent
REPO=HERE.parents[3]
BASE=REPO/'rom/v018/experiments/venetian_blinds/vb_9_interleave.asm'
CANON=REPO/'design/NPC_REFERENCE_8x9_masks.json'
old=BASE.read_text()
assert hashlib.sha1(b'blob '+str(len(BASE.read_bytes())).encode()+b'\x00'+BASE.read_bytes()).hexdigest()=='a25c92adb4ca5087eeace674e371be98b273ae5b'
ref=json.loads(CANON.read_text())
assert ref['width']==8 and ref['height']==9
for name,spec in [('MaleRows','large_male'),('FemaleRows','large_female')]:
    rows=[int(x,2) for x in ref['sprites'][spec]]
    needle='\n'+name+':\n BYTE '+','.join('$%02X'%n for n in rows)+'\n'
    assert needle in old,(name,'source mask differs')
assert ' COLUPF=' not in old and 'CTRLPF=' not in old
assert old.count(' STA COLUBK\n LDA #145\n')==1
s=old.replace('COLUBK=$09\n','COLUBK=$09\nCOLUPF=$08\nCTRLPF=$0A\n')
s=s.replace(' STA COLUBK\n LDA #145\n',
''' STA COLUBK
 LDA #$26
 STA COLUPF
 LDA #1
 STA CTRLPF
 LDA #$F0
 STA PF0
 LDA #1
 STA NUSIZ1
 LDA #145
''',1)
s=s.replace(' ORG $F300\n',' ORG $F800\n',1)
s=s.replace(' ORG $FFFA\n','ShotEnable:\n BYTE $00,$00,$00,$00,$02,$00,$00,$00,$00\n ORG $FFFA\n',1)
anchor='Row00:\n'
end='\n STA WSYNC\n LDA #0\n STA GRP0\n STA GRP1\n STA ENAM0\n LDX #102\nBottomBlank:'
assert s.count(anchor)==1 and s.count(end)==1
pre,rest=s.split(anchor,1)
oldrows,tail=rest.split(end,1)
assert oldrows.count(' STA RESP1')==9
# Every next line first blanks lingering P1? Proven R1af relies on close copy
# following register reset plus staggered GRP write instead of a full reset.
positions={'A':(28,52),'B':(30,52),'C':(28,54),'D':(30,54)}
select='''R1ProbeSelect:
 LDA FRAMELO
 AND #3
 BEQ R1PickA
 CMP #1
 BEQ R1PickB
 CMP #2
 BEQ R1PickC
 JMP R1KernelD
R1PickA:
 JMP R1KernelA
R1PickB:
 JMP R1KernelB
R1PickC:
 JMP R1KernelC
'''
notes={}
for k,(c1,c2) in positions.items():
    n1=(c1-28)//2
    n_between=(c2-c1-8)//2
    assert n1>=0 and n_between>=0
    body=[' ALIGN 256','R1Kernel'+k+':',' LDY #8','R1Line'+k+':',' STA WSYNC',' LDX FemaleRows,Y',' LDA PlayerRows,Y',' STA GRP0',' LDA ShotEnable,Y',' STA ENAM0',' LDA MaleRows,Y',' BIT FRAMELO']
    body+=[' NOP']*n1
    body+=[' STA RESP1',' NOP',' STA GRP1']
    body+=[' NOP']*n_between
    body+=[' STA RESP1',' STX GRP1',' DEY',' BPL R1Line'+k,' JMP R1ProbeEnd']
    select+='\n'.join(body)+'\n'
    notes[k]={'first_RESP1_end_cycle':c1,'second_RESP1_end_cycle':c2,'first_GRP1_end_cycle':c1+5,'second_GRP1_end_cycle':c2+3,'remaining_after_last_RESP1':76-c2}
s=pre+select+'R1ProbeEnd:\n'+end.lstrip('\n')+tail
# Note: end starts STA WSYNC and bottom blank unchanged.
assert s.count(' STA RESP1\n')==8  # two sites per 4 mode loops
for name in ('MaleRows','FemaleRows','PlayerRows'):
    assert old.split('\n'+name+':\n',1)[1].split('\n',1)[0]==s.split('\n'+name+':\n',1)[1].split('\n',1)[0]
HERE.joinpath('r1_two.asm').write_text(s)
subprocess.run(['dasm','r1_two.asm','-f3','-odist/r1_two.bank.bin','-ldist/r1_two.lst','-sdist/r1_two.sym'],cwd=HERE,check=True)
bank=(HERE/'dist/r1_two.bank.bin').read_bytes();assert len(bank)==4096,len(bank)
rom=bank*4;(HERE/'dist/LetMeOut_R1_TWO_2x2_F6.bin').write_bytes(rom)
meta={'kind':'R1 two original 8x9 masks same height with independent 2x2 X runtime combos','NUSIZ1':1,'COLUPF':0x26,'PF0':0xF0,'CTRLPF':1,
      'mask_blob_sha':'058800a4c1904d1ff289e7e61b3902aa111ba16d','original_venetian_blob_sha':'a25c92adb4ca5087eeace674e371be98b273ae5b',
      'cycle_plans_STATIC':notes,'ROM_SHA256':hashlib.sha256(rom).hexdigest(),'bytes':len(rom),'complete_R1':False}
(HERE/'dist/metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
print(json.dumps(meta,indent=2))
