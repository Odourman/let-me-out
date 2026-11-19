from pathlib import Path
from time import monotonic
import sys
from capture import BIN,Session,record
from pixels import WHITE,expected_mask,masks_for_project,colored,picture,BROWN
out=Path(sys.argv[1])
with Session([str(BIN),"HEADLESS",str(Path('let-me-out-v02-raster-repair.bin').resolve())],"cap-motion") as s:
 s.receive(monotonic()+30)
 for _ in range(24):s.command("STEP FRAME")
 for a,v in {0xb3:1,0x80:4,0x81:100,0x91:64,0x92:67,0x93:72,0x94:52,0x95:74,0x96:150,0x97:47,0x98:60,0x99:82,0x9a:86}.items():
  s.command(f"POKE 0x{a:04x} 0x{v:02x}")
 for x in (72,73,74,75,76,77):
  s.command(f'POKE 0x0095 0x{x:02x}')
  for _ in range(3):s.command("STEP FRAME")
  f=out/f"cap-{x}.png";s.command(f"SCREENSHOT {f}")
  p=picture(f);w=colored(p,WHITE)
  rows=sorted((a,b-15) for a,b in w if 105<=b<=108)
  record("motion",l=x,rows=rows,left=p[105*160:105*160+4],setup_left=p[104*160:104*160+4],tv=s.command("TV FRAME").decode().strip())
