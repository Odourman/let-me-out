#!/usr/bin/env python3
"""F3 G0 static preflight and one compiled early-index geometry probe.
Based on untouched F2-generated runtime source. ONE geometry offset (+1 CPU
cycle) applied identically to source index0 on each of nine 8x9 raster rows;
index2 is held at F2 baseline (X=129), other four unchanged. No new kernel.
"""
from pathlib import Path
import argparse,hashlib,subprocess
R=Path(__file__).resolve().parent
A=argparse.ArgumentParser();A.add_argument('--runtime',action='store_true');args=A.parse_args()
base_path=R/'r1_f2_6B_I2_RUNTIME.asm'
assert base_path.exists(),'FIRST build existing F2 runtime via r1_f2_build_runtime.py'
base=base_path.read_text()
# F2 generated full source is immutable; F3 only writes fresh files
old=' NOP\n NOP\n STA RESP1\n STA GRP1\n BIT FRAMELO\n STA RESP1\n'
new=' CPY #0\n BNE *+2\n STA RESP1\n STA GRP1\n BEQ *+2\n STA RESP1\n'
assert base.count(old)==9,('unexpected first-index timing patterns',base.count(old))
assert base.count(' CPX #0\n BNE *+2\n STA RESP1\n STA GRP1\n BEQ *+2\n STA RESP1\n')==9
mode_setup=' LDA FRAMELO\n AND #$04\n TAX\n'
assert base.count(mode_setup)==1
if args.runtime:
    # Two INDEPENDENT RIOT-RAM bytes, overwritten separately from FRAMELO bit3
    # and bit2. Both logical bytes can be written independently by game logic.
    # Diagnostic FRAMELO gives 00 -> 01 -> 11 -> 10 with single-bit edges.
    s=base.replace('FRAMELO=$80\n','FRAMELO=$80\nF3_X0_MODE=$83\nF3_X2_MODE=$84\n',1)
    setup=''' ; F3 diagnostic Gray order: FRAMELO bits3 and2 are
 ; independent input bits, stored to TWO individually writable RAM cells.
 ; Source input is not inferred from observed sprite pixels.
 LDA FRAMELO
 AND #$08
 STA F3_X0_MODE
 LDA FRAMELO
 AND #$04
 STA F3_X2_MODE
 LDY F3_X0_MODE
 LDX F3_X2_MODE
'''
    stem='r1_f3_6B_I0_I2_RUNTIME'
else:
    s=base
    # Y=1 -> first P1 index0 late by 1 CPU cycle. X=0 -> index2 baseline.
    setup=' LDY #1\n LDX #0\n'
    stem='r1_f3_6B_I0_P1_I2_FIXED'
s=s.replace(mode_setup,setup,1)
for i in range(8,-1,-1):
    a=s.index(f'R1N6BRow{i:02d}:')
    b=s.index(f'R1N6BRow{i+1:02d}:') if i<8 else s.index('BottomBlank:')
    row=s[a:b]
    assert row.count(old)==1,(i,'first index target not unique')
    row=row.replace(old,new,1)
    s=s[:a]+row+s[b:]
assert s.count(old)==0
assert s.count(new)==9
assert s.count(' STA RESP1\n')==base.count(' STA RESP1\n')==54
assert s.count(' STA GRP1\n')==base.count(' STA GRP1\n')
assert s.count(' STA GRP0\n')==base.count(' STA GRP0\n')
assert s.count(' STA ENAM0\n')==base.count(' STA ENAM0\n')
assert s.count(' STA PF0\n')==base.count(' STA PF0\n')
assert s.count(' CPX #0\n')==9 and s.count(' CPY #0\n')==9
assert s.count(' BNE *+2\n')==18 and s.count(' BEQ *+2\n')==18
if args.runtime:
    assert s.count('STA F3_X0_MODE')==1 and s.count('STA F3_X2_MODE')==1
    assert s.count('LDY F3_X0_MODE')==1 and s.count('LDX F3_X2_MODE')==1
    print('F3_INDEPENDENT_RAM: $83=F3_X0_MODE; $84=F3_X2_MODE; bit3/bit2 independently selected')
else:
    print('F3_G0_FIRST_INDEX +1 CPU cycle; second index fixed baseline')
# Early RESP1 c19/c20, next c28; F2 mid index c37/c38, next c46.
# GRP1 early c22/c23, mid c40/c41, final c69; WSYNC late 72 <=76.
print('F3_STATIC_PAIR_BALANCE index0: CPY2+BNE(2/3)+BEQ(3/2)=7 both modes')
print('F3_STATIC_PAIR_BALANCE index2: CPX2+BNE(2/3)+BEQ(3/2)=7 both modes')
print('F3_STATIC_TIMING RESP1 index0=19/20, index1=28, index2=37/38, index3=46, index4=56, index5=66')
print('F3_STATIC_TIMING last GRP1=69 WSYNC=72 margin=4/76 (SOURCE-derived, verify Stella)')
out=R/f'{stem}.asm';out.write_text(s)
(R/'dist').mkdir(exist_ok=True)
subprocess.run(['dasm',out.name,'-f3',f'-odist/{stem}.bank.bin',f'-ldist/{stem}.lst',f'-sdist/{stem}.sym'],cwd=R,check=True)
bank=(R/'dist'/f'{stem}.bank.bin').read_bytes();assert len(bank)==4096
rom=bank*4
(R/'dist'/f'{stem}_F6.bin').write_bytes(rom)
print('F3_ROM',stem,'bytes',len(rom),'sha256',hashlib.sha256(rom).hexdigest())
