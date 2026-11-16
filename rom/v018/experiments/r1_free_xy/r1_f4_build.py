#!/usr/bin/env python3
"""R1-F4 authorized ONE fixed geometry probe per invocation: c18 OR c21.
c21 MAY ONLY be built if MAIN F4 gate allows after failed non-destructive c18.
No runtime selector, no new kernel family; 9 original mask rows byte-exact.
"""
from pathlib import Path
import argparse,subprocess,hashlib,json
R=Path(__file__).resolve().parent
ap=argparse.ArgumentParser()
ap.add_argument('--phase',type=int,choices=[18,21],required=True)
args=ap.parse_args()
phase=args.phase
source_preflight=json.loads((R/'r1_f4_source_preflight.json').read_text())
assert source_preflight['F4_G0']=='SOURCE_ONLY_FEASIBLE_C18_AND_C21_NOT_STELLA'
source=(R/'r1_f2_6B_I2_RUNTIME.asm').read_text()
baseline=(R/'r1_individual_6B.asm').read_text()
sha=lambda s:hashlib.sha256(s.encode()).hexdigest()
assert sha(baseline)=='e268cf68c19543083e59b63b65087699ef281ec04c170a3cf624eab90c579012'
assert 'FRAMELO=$80' in source
assert source.count(' LDA FRAMELO\n AND #$04\n TAX\n')==1
# Keep F2's third (index2) CPX/BNE/BEQ compensating branch pair,
# but permanently select X=0 so third RESP1 remains at c37.
s=source.replace(' LDA FRAMELO\n AND #$04\n TAX\n',
''' ; F4 GEOMETRY ONLY: index2 remains frozen F2 X=0 -> RESP1 c37.
 LDX #0
''',1)
old=' NOP\n NOP\n STA RESP1\n STA GRP1\n BIT FRAMELO\n STA RESP1\n'
assert source.count(old)==9,('unexpected F2 early copy template',source.count(old))
if phase==18:
    # First RESP1 c18: use 3-cycle BIT instead of old 4-cycle two NOP;
    # add 4-cycle two NOP after GRP1 to preserve second RESP1 c28.
    new=' BIT FRAMELO\n STA RESP1\n STA GRP1\n NOP\n NOP\n STA RESP1\n'
    first_grp=21
else:
    # First RESP1 c21: pre-pad =6, then STA 3 then GRP1 3,
    # second RESP1 c28 via 4-cycle 6502 ZERO PAGE INDEXED STORE X=0.
    # X=0 is fixed OUTSIDE nine-line kernel and never updated inside.
    new=' NOP\n NOP\n NOP\n STA RESP1\n STA GRP1\n STA RESP1,X\n'
    first_grp=24
for y in range(8,-1,-1):
    a=s.index(f'R1N6BRow{y:02d}:')
    b=s.index(f'R1N6BRow{y+1:02d}:') if y<8 else s.index('BottomBlank:')
    row=s[a:b]
    assert row.count(old)==1,(y,'early first P1 copy not unique')
    assert row.count(' STA GRP0\n')==1 and row.count(' STA ENAM0\n')==1
    assert row.count(' STA RESP1\n')==6
    # The only bitmap source change is NONE: no LDA immediate/GRP0/M0/PF alterations.
    row=row.replace(old,new,1)
    s=s[:a]+row+s[b:]
assert s.count(old)==0 and s.count(new)==9
assert s.count(' STA GRP1\n')==source.count(' STA GRP1\n')
assert s.count(' STA GRP0\n')==source.count(' STA GRP0\n')
assert s.count(' STA ENAM0\n')==source.count(' STA ENAM0\n')
assert s.count(' STA PF0\n')==source.count(' STA PF0\n')
assert s.count(' STA COLUPF\n')==source.count(' STA COLUPF\n')
assert s.count(' STA HMOVE\n')==source.count(' STA HMOVE\n')
assert s.count(' STA NUSIZ1\n')==source.count(' STA NUSIZ1\n')
assert s.count(' LDX #0\n')>=1
assert s.count(' TAX\n')==source.count(' TAX\n')-1
assert s.count(' CPX #0\n')==9
assert s.count(' BNE *+2\n')==9 and s.count(' BEQ *+2\n')==9
assert s.count(' STA RESP1\n')+s.count(' STA RESP1,X\n')==54
assert s.count(' STA RESP1,X\n')==(9 if phase==21 else 0)
# Check no X write or new branch inside any of nine rows.
for y in range(9):
    a=s.index(f'R1N6BRow{y:02d}:')
    b=s.index(f'R1N6BRow{y+1:02d}:') if y<8 else s.index('BottomBlank:')
    row=s[a:b]
    assert not any(f' {op} ' in row for op in ['LDX','TAX','INX','DEX','TXA'])
    assert row.count(' STA RESP1\n')+row.count(' STA RESP1,X\n')==6
    assert row.count(' STA GRP1\n')==4
stem=f'r1_f4_6B_I0_C{phase:02d}_I2_FIXED'
src=R/f'{stem}.asm';src.write_text(s)
(R/'dist').mkdir(exist_ok=True)
subprocess.run(['dasm',src.name,'-f3',
                f'-odist/{stem}.bank.bin',f'-ldist/{stem}.lst',f'-sdist/{stem}.sym'],cwd=R,check=True)
bank=(R/'dist'/f'{stem}.bank.bin').read_bytes();assert len(bank)==4096
rom=bank*4
f=R/'dist'/f'{stem}_F6.bin';f.write_bytes(rom)
assert len(rom)==16384 and all(rom[i*4096:(i+1)*4096]==bank for i in range(4))
listing=(R/'dist'/f'{stem}.lst').read_text()
if phase==21:
    # zero-page indexed assembler emits 95 [RESP1] (four cycles),
    # instead of 85 [RESP1] (three cycles); X fixed $00.
    assert len([x for x in listing.splitlines() if 'STA RESP1,X' in x])==9
meta={'phase':phase,'F4_one_compiled_probe':True,
    'base_F2_fixed_index2_first_resp':37,
    'first_RESP1_CPU_cycle_SOURCE_ONLY':phase,
    'first_GRP1_CPU_cycle_SOURCE_ONLY':first_grp,
    'second_RESP1_CPU_cycle_SOURCE_ONLY':28,
    'remaining_RESP1_CPU_cycle_SOURCE_ONLY':[37,46,56,66],
    'last_GRP1_CPU_cycle_SOURCE_ONLY':69,'WSYNC_CPU_cycle_SOURCE_ONLY':72,
    'linear_requested_crop_X_before_real_Stella':[37 if phase==18 else 55,75,129,183,243,303],
    'physical_X_response_is_unknown_until_real_Stella':True,
    'canonical_bitmap_changed':False,'P0_M0_PF_changed':False,
    'index2_fixed_X_register':0,
    'source_sha256':sha(s),'ROM_SHA256':hashlib.sha256(rom).hexdigest(),
    'ROM_bytes':16384,'bank_bytes':4096,'bank_0_equals_1_2_3':True}
(R/'dist'/f'{stem}_meta.json').write_text(json.dumps(meta,indent=2)+'\n')
print('F4_COMPILED_ONE_GEOMETRY',stem,'phase',phase,'ROM_SHA256',meta['ROM_SHA256'])
print('F4_STATIC_ONLY_ROW09_TIMING c0',phase,'GRP1',first_grp,'index1 28 index2 37 index3 46 index4 56 index5 66 last_GRP1 69 WSYNC 72')
