#!/usr/bin/env python3
"""R1-F2 G2: ONE 6B derived kernel; frame-state-controlled single P1 third X.
Not a second precompiled formation. No branch changes PC, masked ROM is immutable.
Timing trick: CPX #0 + BNE *+2 (2/3 cycles), then complementary BEQ *+2
(3/2 cycles) before FOURTH RESP1. Fifth other X writes remain unchanged.
"""
from pathlib import Path
import hashlib,subprocess
R=Path(__file__).resolve().parent
orig=(R/'r1_individual_6B.asm').read_text()
assert hashlib.sha256(orig.encode()).hexdigest()=='e268cf68c19543083e59b63b65087699ef281ec04c170a3cf624eab90c579012'
s=orig
# FRAMELO is existing RIOT RAM address $80. Capture bit2 once after TopBlank.
# Both X=0 and X=4 execute same nine scanline instruction stream.
needle=' BNE TopBlank\n ; Preload sprite and player bitmaps; 9/18 visible scanlines below.\n'
assert s.count(needle)==1
s=s.replace(needle,
''' BNE TopBlank
 ; F2 runtime source: FRAMELO bit 2; X=0 or X=4 over ALL nine scanlines.
 LDA FRAMELO
 AND #$04
 TAX
 ; Preload sprite and player bitmaps; 9/18 visible scanlines below.
''',1)
# After SECOND RESP1, the first large_female bitmap is preloaded.
# Replace its four NOP cycles with CPX (2) and BNE *+2 (2/3).
# Complementary BEQ *+2 (3/2) before FOURTH RESP1 fixes it at c46.
old=' NOP\n NOP\n STA RESP1\n STA GRP1\n BIT FRAMELO\n STA RESP1\n'
new=' CPX #0\n BNE *+2\n STA RESP1\n STA GRP1\n BEQ *+2\n STA RESP1\n'
for row in reversed(range(9)):
    a=s.index(f'R1N6BRow{row:02d}:')
    b=s.index(f'R1N6BRow{row+1:02d}:') if row<8 else s.index('BottomBlank:')
    chunk=s[a:b]
    positions=[i for i in range(len(chunk)) if chunk.startswith(' STA RESP1\n',i)]
    assert len(positions)==6
    j=chunk.index(old,positions[1])
    assert positions[1]<j<positions[2]
    chunk=chunk[:j]+new+chunk[j+len(old):]
    s=s[:a]+chunk+s[b:]
assert s.count(' STA RESP1\n')==54
assert s.count(' STA GRP1\n')==orig.count(' STA GRP1\n')
assert s.count(' CPX #0\n')==9
assert s.count(' BNE *+2\n')==9 and s.count(' BEQ *+2\n')==9
assert s.count(' STA ENAM0\n')==orig.count(' STA ENAM0\n')
assert s.count(' STA GRP0\n')==orig.count(' STA GRP0\n')
assert s.count(' STA PF0\n')==orig.count(' STA PF0\n')
stem='r1_f2_6B_I2_RUNTIME'
(R/f'{stem}.asm').write_text(s)
(R/'dist').mkdir(exist_ok=True)
subprocess.run(['dasm',f'{stem}.asm','-f3',f'-odist/{stem}.bank.bin',f'-ldist/{stem}.lst',f'-sdist/{stem}.sym'],cwd=R,check=True)
bank=(R/'dist'/f'{stem}.bank.bin').read_bytes()
assert len(bank)==4096
rom=bank*4
(R/'dist'/f'{stem}_F6.bin').write_bytes(rom)
print('F2_RUNTIME_SAME_KERNEL one executable 16384 bytes, mode=FRAMELO_and_4,')
print('mode_0: third RESP1 c37 GRP1 c40 fourth RESP1 c46')
print('mode_4: third RESP1 c38 GRP1 c41 fourth RESP1 c46')
print('F2_RUNTIME_SHA256',hashlib.sha256(rom).hexdigest())
