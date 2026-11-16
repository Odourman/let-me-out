#!/usr/bin/env python3
"""Authorized R1: two original 8x9 silhouettes in 16 factorized X0/X1/Y0/Y1
combinations, exactly same nine-line raster masks, no sprite scaling or turn-taking.
TIA P1 close copies; each Y profile is a source-exact ROM table selected
with independent pre-raster zero-page pointers (no per-row branches). 6502 P1 raster cycles remain same as source-exact
2x2 pilot; no third party ROM code.
"""
from pathlib import Path
import hashlib,json,subprocess
HERE=Path(__file__).resolve().parent
REPO=HERE.parents[3]
BASE=REPO/'rom/v018/experiments/venetian_blinds/vb_9_interleave.asm'
CANON=HERE/'canon_masks.json'
old=BASE.read_text(); raw=BASE.read_bytes()
assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\x00'+raw).hexdigest()=='a25c92adb4ca5087eeace674e371be98b273ae5b'
ref=json.loads(CANON.read_text())['sprites']
assert ref['large_male']==['00111100','00111100','00011000','11111111','00011000','00100100','00100100','01000010','01000010']
assert ref['large_female']==['00111100','00111100','00011000','11111111','00111100','01111110','01111110','00100100','00100100']
# The exact original masks remain in source. RAM copies shift Y by 0 or 1.
for name,shape in [('MaleRows','large_male'),('FemaleRows','large_female')]:
    assert '\n'+name+':\n BYTE '+','.join('$%02X'%int(x,2) for x in ref[shape])+'\n' in old
s=old.replace('COLUBK=$09\n','COLUBK=$09\nCOLUPF=$08\nCTRLPF=$0A\n')
s=s.replace(' STA COLUBK\n LDA #145\n',''' STA COLUBK
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
s=s.replace(' STA VBLANK\n ; Vblank scanline3:', ' STA VBLANK\n LDA #1\n STA NUSIZ1\n ; Vblank scanline3:',1)
s=s.replace(' ORG $F300\n',' ORG $F800\n',1)
# Two independent ROM table pointers; choose each before raster in two of the
# 80 existing visible blank scanlines (no visible row or VSYNC count added).
# Rather than copying ROM bitmaps into RAM on startup, this arrangement avoids
# CPU-per-frame copy overhead and stays under 76 cycles per setup line.
s=s.replace('FRAMELO=$80\n','FRAMELO=$80\nMALE_PTR_LO=$94\nMALE_PTR_HI=$95\nFEMALE_PTR_LO=$96\nFEMALE_PTR_HI=$97\n',1)
special=''' LDA #0
 STA VBLANK
 STA WSYNC
 LDA FRAMELO
 AND #$04
 BEQ MalePointerZero
 LDA #<MaleDy1Rows
 STA MALE_PTR_LO
 LDA #>MaleDy1Rows
 STA MALE_PTR_HI
 JMP MalePointerDone
MalePointerZero:
 LDA #<MaleDy0Rows
 STA MALE_PTR_LO
 LDA #>MaleDy0Rows
 STA MALE_PTR_HI
MalePointerDone:
 STA WSYNC
 LDA FRAMELO
 AND #$08
 BEQ FemalePointerZero
 LDA #<FemaleDy1Rows
 STA FEMALE_PTR_LO
 LDA #>FemaleDy1Rows
 STA FEMALE_PTR_HI
 JMP FemalePointerDone
FemalePointerZero:
 LDA #<FemaleDy0Rows
 STA FEMALE_PTR_LO
 LDA #>FemaleDy0Rows
 STA FEMALE_PTR_HI
FemalePointerDone:
 LDX #78
TopBlank:
 STA WSYNC
 DEX
 BNE TopBlank
'''
needle=' LDA #0\n STA VBLANK\n LDX #80\nTopBlank:\n STA WSYNC\n DEX\n BNE TopBlank\n'
assert s.count(needle)==1
s=s.replace(needle,special,1)
# 10 row physical band accommodates the two independent 0/1 Y starts.
anchor='Row00:\n';end='\n STA WSYNC\n LDA #0\n STA GRP0\n STA GRP1\n STA ENAM0\n LDX #102\nBottomBlank:'
assert s.count(anchor)==s.count(end)==1
pre,rest=s.split(anchor,1);_,tail=rest.split(end,1)
# Use original X mode 2x2 factorized kernel, independent of Y bits2 and3.
positions={'A':(32,56),'B':(34,56),'C':(32,58),'D':(34,58)}
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
for key,(c1,c2) in positions.items():
    n1=(c1-32)//2;n_between=(c2-c1-8)//2
    body=[' ALIGN 256','R1Kernel'+key+':',' LDY #0','R1Line'+key+':',' STA WSYNC',
          ' LDA (FEMALE_PTR_LO),Y',' TAX',' LDA PlayerDraw10,Y',' STA GRP0',
          ' LDA ShotDraw10,Y',' STA ENAM0',' LDA (MALE_PTR_LO),Y',' BIT FRAMELO']
    body+=[' NOP']*n1
    body+=[' STA RESP1',' NOP',' STA GRP1']
    body+=[' NOP']*n_between
    body+=[' STA RESP1',' STX GRP1',' INY',' CPY #10',' BNE R1Line'+key,' JMP R1ProbeEnd']
    select+='\n'.join(body)+'\n'
# Include 10 scanlines vs old 9, bottom blank shorter 1 to maintain 262.
s=pre+select+'R1ProbeEnd:\n'+end.lstrip('\n').replace(' LDX #102\nBottomBlank:',' LDX #101\nBottomBlank:',1)+tail
assert s.count(' STA RESP1\n')==8
for label in ('MaleRows','FemaleRows','PlayerRows'):
    assert old.split('\n'+label+':\n',1)[1].split('\n',1)[0]==s.split('\n'+label+':\n',1)[1].split('\n',1)[0]
player=[0x3c,0x7e,0x18,0x7e,0x1e,0x3c,0x18,0x24,0x42,0]
shot=[0,0,0,0,2,0,0,0,0,0]
extra=' ORG $F900\nPlayerDraw10:\n BYTE '+','.join('$%02X'%x for x in player)+'\nShotDraw10:\n BYTE '+','.join('$%02X'%x for x in shot)+'\n'
for tag,name,dy in [('MaleDy0Rows','large_male',0),('MaleDy1Rows','large_male',1),('FemaleDy0Rows','large_female',0),('FemaleDy1Rows','large_female',1)]:
    original=[int(z,2) for z in ref[name]]
    rows=original+[0] if dy==0 else [0]+original
    assert len(rows)==10
    extra+=tag+':\n BYTE '+','.join('$%02X'%x for x in rows)+'\n'
s=s.replace(' ORG $FFFA\n',extra+' ORG $FFFA\n',1)
HERE.joinpath('dist').mkdir(exist_ok=True)
(HERE/'r1_two_xy.asm').write_text(s)
subprocess.run(['dasm','r1_two_xy.asm','-f3','-odist/r1_two_xy.bank.bin','-ldist/r1_two_xy.lst','-sdist/r1_two_xy.sym'],cwd=HERE,check=True)
bank=(HERE/'dist/r1_two_xy.bank.bin').read_bytes();assert len(bank)==4096,len(bank)
rom=bank*4
(HERE/'dist/LetMeOut_R1_TWO_INDEPENDENT_XY_F6.bin').write_bytes(rom)
meta={'16_runtime_combinations':16,'two_NPC_X_c1c2':positions,
      'independent_male_dy_bit2':[0,1],'independent_female_dy_bit3':[0,1],
      'ROM_SHA256':hashlib.sha256(rom).hexdigest(),'size':len(rom),
      'original_source_mask_reference_blob':'058800a4c1904d1ff289e7e61b3902aa111ba16d',
      'cpu_row_reset_cycle_STATIC':{'c1':[32,34],'c2':[56,58]},
      'claim':'UNTESTED UNTIL REAL STELLA CANONICAL ALL-PIXEL AUDIT',
      'not_full_R1':True}
(HERE/'dist/xy_metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
print(json.dumps(meta,indent=2))
