from capture import BIN, Session, record
from pathlib import Path
from time import monotonic
from pixels import WHITE, colored, picture
rom=Path('let-me-out-v02-continuation.bin').resolve()
out=Path('/workspace/work/slice2cont-run/hole')
with Session([str(BIN),"HEADLESS",str(rom)],"door-hole-m1") as s:
    s.receive(monotonic()+30)
    for _ in range(25): s.command("STEP FRAME")
    for addr,v in {0xb3:1,0x91:150,0x96:85,0xa0:255,0xa1:0,0xa2:0,0xa3:0,0xa4:0}.items():
        s.command(f'POKE 0x{addr:04x} 0x{v:02x}')
    for label in ('locked','unlocked'):
        if label=='unlocked': s.command('POKE 0x00b2 0x01')
        for _ in range(4): s.command("STEP FRAME")
        f=out/(label+'.png')
        s.command(f'SCREENSHOT {f}')
        data=picture(f)
        record('m1-hole',label=label,frame=s.command('TV FRAME').decode().strip(),
               white=len(colored(data,WHITE)),rows=[data[y*160+156:(y+1)*160] for y in range(100,109)])
