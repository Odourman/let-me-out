#!/usr/bin/env python3
"""Attempt N=3,4,5,6 original independent software RESP1 starts per scanline.
One P1 reused, NUSIZ1=1 close-copy; no NUSIZ pair-cloning, no flicker.
Four variants are *experimental only*. Six instances are not assumed valid.
Source masks loaded from local exact approved canon_masks.json and never edited.
Assemble original 6502 using DASM; no Python rendering as evidence.
"""
from pathlib import Path
import hashlib,subprocess,json
HERE=Path(__file__).resolve().parent
REPO=HERE.parents[3]
BASE=REPO/'rom/v018/experiments/venetian_blinds/vb_9_interleave.asm'
old=BASE.read_text()
assert hashlib.sha1(b'blob '+str(len(BASE.read_bytes())).encode()+b'\0'+BASE.read_bytes()).hexdigest()=='a25c92adb4ca5087eeace674e371be98b273ae5b'
ref=json.loads((HERE/'canon_masks.json').read_text())
assert ref['width']==8 and ref['height']==9
sprites=ref['sprites']
player=['00111100','01111110','00011000','01111110','00011110','00111100','00011000','00100100','01000010']
types=['large_male','large_male','large_female','large_female','small_male','small_female']
scenarios={
 '6B':(types,[19,28,37,46,56,66]),
 '6C':(types,[20,29,38,47,57,67]),
 '6D':(types,[21,30,39,48,58,68]),
 '6E':(types,[18,27,36,45,56,66]),
}

( HERE/'dist' ).mkdir(exist_ok=True)
anchor='Row00:\n'
end='\n STA WSYNC\n LDA #0\n STA GRP0\n STA GRP1\n STA ENAM0\n LDX #102\nBottomBlank:'
assert old.count(anchor)==old.count(end)==1
head,rest=old.split(anchor,1)
oldrows,tail=rest.split(end,1)
assert oldrows.count(' STA RESP1')==9
for n,(types,cycles) in scenarios.items():
    s=head
    s=s.replace('COLUBK=$09\n','COLUBK=$09\nCOLUPF=$08\nCTRLPF=$0A\n')
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
    # Full unrolled 9 rows, each row starts at WSYNC and schedules each
    # individual bitmap's position on THIS scanline.
    lines=[]
    planned=[]
    for y in range(9):
        instructions=['R1N%sRow%02d:'%(n,y),' STA WSYNC',
          ' LDA #$%02X'%int(player[y],2),' STA GRP0',
          ' LDA #$%02X'%(2 if y==4 else 0),' STA ENAM0']
        clk=10;prev=''
        times=[]
        for index,(tp,target) in enumerate(zip(types,cycles)):
            if tp!=prev:
                instructions+=[' LDA #$%02X'%int(sprites[tp][y],2)];clk+=2
            delta=target-3-clk
            if delta<0 or delta==1:raise RuntimeError((n,y,tp,target,'Impossible padding',delta))
            b=delta%2;a=(delta-3*b)//2
            assert a>=0 and 2*a+3*b==delta
            instructions+=[' NOP']*a
            if b:instructions.append(' BIT FRAMELO')
            clk+=delta
            instructions.append(' STA RESP1');clk+=3
            assert clk==target,(n,y,index,clk,target)
            if tp!=prev:
                instructions.append(' STA GRP1');clk+=3
            times.append({'type':tp,'RESP1_end':target,'GRP1_end':clk if tp!=prev else None})
            prev=tp
        assert clk+3<=76,(n,y,clk)
        planned.append({'row':y,'times':times,'next_WSYNC_end_if_no_other_work':clk+3})
        lines+=instructions
    src=s+'\n'.join(lines)+'\n'+end.lstrip('\n')+tail.replace(' ORG $F300\n',' ORG $F800\n',1)
    # Three stage insertion lengths must not affect baseline VSYNC/NTSC rows.
    assert src.count(' STA RESP1\n')==9*len(types),(n,src.count(' STA RESP1\n'))
    path=HERE/('r1_individual_%s.asm'%n);path.write_text(src)
    stem='r1_individual_%s'%n
    subprocess.run(['dasm',stem+'.asm','-f3','-odist/'+stem+'.bank.bin','-ldist/'+stem+'.lst','-sdist/'+stem+'.sym'],cwd=HERE,check=True)
    bank=(HERE/'dist'/(stem+'.bank.bin')).read_bytes();assert len(bank)==4096,(n,len(bank))
    rom=bank*4
    (HERE/'dist'/(stem+'_F6.bin')).write_bytes(rom)
    meta={'N':n,'type_order':types,'exact_original_canonical_byte_rows':True,'display_rows_top_to_bottom':True,
          'p0':player,'m0_one_testshot':True,'NUSIZ1':1,'PF0':0xF0,'CTRLPF':1,'brown_COLORUPF':0x26,
          'cycles_STATIC_only':planned,'new_ROM_SHA256':hashlib.sha256(rom).hexdigest(),
          'status':'UNTESTED_UNTIL_REAL_STELLA_PIXEL_AUDIT'}
    (HERE/'dist'/(stem+'_meta.json')).write_text(json.dumps(meta,indent=2)+'\n')
    print('BUILD_R1_N',n,'4KiB*4',meta['new_ROM_SHA256'],'worst',max(x['next_WSYNC_end_if_no_other_work'] for x in planned))
