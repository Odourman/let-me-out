#!/usr/bin/env python3
"""R1-F2 G1: exactly two precompiled X-offset probes on 6B instance index 2.
Index 2 is the FIRST large_female, physically between the two large_males and
the SECOND large_female. Five others retain byte-exact RESP1 deadlines.
Source P0/M0/PF, mask bytes, NUSIZ1=$01, and F6 mapper stay untouched.
"""
from pathlib import Path
import hashlib,subprocess,json
R=Path(__file__).resolve().parent
base=(R/'r1_individual_6B.asm').read_text()
assert hashlib.sha256(base.encode()).hexdigest()=='e268cf68c19543083e59b63b65087699ef281ec04c170a3cf624eab90c579012'
cycles={
  'M2':([19,28,35,46,56,66],
        ' NOP\n STA RESP1\n STA GRP1\n NOP\n BIT FRAMELO\n STA RESP1\n'),
  'P1':([19,28,38,46,56,66],
        ' NOP\n BIT FRAMELO\n STA RESP1\n STA GRP1\n NOP\n STA RESP1\n')
}
orig=' NOP\n NOP\n STA RESP1\n STA GRP1\n BIT FRAMELO\n STA RESP1\n'
dist=R/'dist';dist.mkdir(exist_ok=True)
for label,(times,replacement) in cycles.items():
    source=base
    for row in reversed(range(9)):
        a=source.index(f'R1N6BRow{row:02d}:')
        b=source.index(f'R1N6BRow{row+1:02d}:') if row<8 else source.index('BottomBlank:')
        chunk=source[a:b]
        # Pin the ONLY allowed edited locus after SECOND RESP1.
        stamps=[p for p in range(len(chunk)) if chunk.startswith(' STA RESP1\n',p)]
        assert len(stamps)==6,(row,len(stamps))
        j=chunk.index(orig,stamps[1],stamps[3])
        assert j+len(orig)<=stamps[3]+len(' STA RESP1\n')
        chunk=chunk[:j]+replacement+chunk[j+len(orig):]
        source=source[:a]+chunk+source[b:]
    assert source.count(' STA RESP1\n')==54
    assert source.count(' STA GRP1\n')==9*4+1  # final clear
    stem=f'r1_f2_6B_I2_{label}'
    (R/f'{stem}.asm').write_text(source)
    subprocess.run(['dasm',f'{stem}.asm','-f3',f'-odist/{stem}.bank.bin',f'-ldist/{stem}.lst',f'-sdist/{stem}.sym'],cwd=R,check=True)
    bank=(dist/f'{stem}.bank.bin').read_bytes()
    assert len(bank)==4096
    rom=bank*4
    (dist/f'{stem}_F6.bin').write_bytes(rom)
    print('F2_G1',label,'type=large_female','index=2','cycles=',times,
          'rom_sha256=',hashlib.sha256(rom).hexdigest(),'bank_size=',len(bank))
    assert times[:2]==[19,28] and times[3:]==[46,56,66]
