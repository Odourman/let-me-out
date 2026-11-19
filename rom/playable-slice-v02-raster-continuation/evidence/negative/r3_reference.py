from pathlib import Path
import sys
from time import monotonic
from capture import BIN, Session, record

out=Path(sys.argv[1]).resolve()
with Session([str(BIN),"HEADLESS",str(out/"r3.bin")],"r3-original") as session:
    session.receive(monotonic()+15)
    for i in range(1380):
        session.command("STEP FRAME")
        if i in (1286,1312,1376):
            record("r3_frame",n=i,tv=session.command("TV FRAME").decode().strip())
            session.command(f"SCREENSHOT {out}/frame-{i}.png")
