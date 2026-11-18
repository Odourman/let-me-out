"""Real debugger RAM writes, readbacks and unmodified screenshots."""
import argparse
import re
from pathlib import Path
import time
from capture import BIN, Session, expect, Rejected, record
from stimuli import cases, soak, seeded, reorders, stress_soak

VERSION = rb"v0\.57\.2\n2af86eb725739adbf3d9d45cea2ed69eea57da2a\n"
TV = rb"FR=(\d+) SL=(\d+) CL=(-?\d+)\n"
TV_FRAME = rb"top: (\d+), bottom: (\d+), total: (\d+)\n"


def peek(session, addresses):
    reply = session.command("PEEK " + " ".join(f"0x{a:04x}" for a in addresses))
    lines = reply.splitlines()
    if len(lines) != len(addresses):
        raise Rejected(f"wrong PEEK count {reply!r}")
    result = []
    for address, line in zip(addresses, lines):
        match = re.fullmatch(rb"0x([0-9a-f]+)(?: \([^)]*\))+ = 0x([0-9a-f]+)", line)
        if not match or int(match[1],16)!=address:
            raise Rejected(f"unexpected PEEK {line!r}")
        result.append(int(match[2],16))
    return result


def run(mode, output, long_run, seeded_run=False, fixture=None, reordered=False, stress=False):
    output.mkdir(parents=True,exist_ok=False)
    rom = Path("roms",mode+".bin").resolve()
    if seeded_run:
        order = seeded()
        if long_run:
            order = [(label,x,y,50) for label,x,y,_ in order if label[:5]=="seed-" and label[5:].isdigit()]
    else:
        order = soak() if long_run else cases(mode)
    if reordered:
        order = reorders(long_run)
    if stress:
        order = stress_soak()
    if fixture is not None:
        order = [entry for entry in order if entry[0] == fixture]
        if len(order) != 1:
            raise ValueError(f"unknown fixture {fixture!r}")
    addresses = list(range(0x81,0x8b))
    previous_frame = None
    with Session([str(BIN),"HEADLESS",str(rom)],"gopher-runtime") as session:
        session.receive(time.monotonic()+15)
        expect(session,"VERSION REVISION",VERSION)
        expect(session,"CARTRIDGE MAPPER",rb"F6\n")
        for _ in range(3):
            session.command("STEP FRAME")
        for name,x,y,frames in order:
            expected = x+y
            old = peek(session,addresses)
            changed = []
            for address,before,after in zip(addresses,old,expected):
                if before != after:
                    reply = session.command(f"POKE 0x{address:04x} 0x{after:02x}")
                    if b"poked to" not in reply:
                        raise Rejected(f"no POKE ACK {reply!r}")
                    changed.append(address)
            if peek(session,addresses)!=expected:
                raise Rejected("coordinate write/readback mismatch")
            record("fixture",label=name,x=x,y=y,changed=changed,before=old)
            for step in range(frames+1):
                session.command("STEP FRAME")
                fr = int(expect(session,"TV",TV)[1])
                if previous_frame is not None and fr!=previous_frame+1:
                    raise Rejected("nonconsecutive emulator frames")
                previous_frame = fr
                top,bottom,total = map(int,expect(session,"TV FRAME",TV_FRAME).groups())
                # First completed raster may predate the write at frame entry.
                if step == 0:
                    record("transition",label=name,frame=fr,scanlines=total)
                    continue
                states = dict(frame=fr,label=name,x=x,y=y,top=top,bottom=bottom,scanlines=total)
                if not long_run or step in (1,2,frames):
                    states["planner_misses_previous"],states["compact_slot_previous"] = peek(session,[0x9c,0x9d])
                path = output/f"frame_{fr:04d}.png"
                expect(session,f"SCREENSHOT {path}",rb"saving screenshot\n")
                if not path.is_file() or path.read_bytes()[:8]!=b"\x89PNG\r\n\x1a\n":
                    raise Rejected("missing screenshot")
                record("raster",**states,path=path.name)
            if peek(session,addresses)!=expected:
                raise Rejected("renderer mutated coordinates")


if __name__=="__main__":
    p = argparse.ArgumentParser()
    p.add_argument("mode",choices=("latch4","sharep0","shareclean","sharefour","shareearly","baseline"))
    p.add_argument("images",type=Path)
    p.add_argument("--soak",action="store_true")
    p.add_argument("--seeded",action="store_true")
    p.add_argument("--fixture")
    p.add_argument("--reorders",action="store_true")
    p.add_argument("--stress",action="store_true")
    args=p.parse_args()
    run(args.mode,args.images.resolve(),args.soak,args.seeded,args.fixture,args.reorders,args.stress)
