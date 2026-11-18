"""Native NTSC frames and screenshots, including every scene transition."""
import argparse,json,re,time
from pathlib import Path
from capture import BIN,Session,expect,record

VERSION=rb"v0\.57\.2\n2af86eb725739adbf3d9d45cea2ed69eea57da2a\n"
FRAME=rb"top: (\d+), bottom: (\d+), total: (\d+)\n"
TV=rb"FR=(\d+) SL=(\d+) CL=(-?\d+)\n"

SCENES=(
    ("historic", [127,19,73,100,46], [73,72,73,71,72], True),
    ("shift-left-order", [19,127,73,46,97], [72,73,71,72,73], True),
    ("shift-right-order", [103,73,46,127,19], [71,73,72,71,72], True),
    ("close3-rejected", [73,76,79,82,85], [72]*5, False),
    ("close1-rejected", [73,74,75,76,77], [72]*5, False),
    ("mixed-samex-rejected", [73,73,19,100,46], [75,74,73,72,71], False),
    ("separated", [19,46,73,100,127], [72]*5, True),
    ("seed-wide-outside", [19,52,85,118,151], [72]*5, False),
    ("seed-close-pair-outside", [55,91,130,24,26], [72]*5, False),
)

def replay(rom, out, count, dynamic=False, stress=False, legacy=False):
    if legacy:
        from legacy_stimuli import soak, seeded
        old=tuple((n,x,y) for n,x,y,_ in [*soak(),*seeded()][:20])
        count=len(old)*3
    out.mkdir(parents=True,exist_ok=False)
    with Session([str(BIN),"HEADLESS",str(rom.resolve())],"g5be2") as s:
        s.receive(time.monotonic()+15)
        expect(s,"VERSION REVISION",VERSION)
        expect(s,"CARTRIDGE MAPPER",rb"F6\n")
        for _ in range(4):
            s.command("STEP FRAME")
        previous=None
        for i in range(count):
            if legacy:
                scene=i//3
                label,x,y=old[scene]
                ordered=sorted(x)
                admitted=(ordered[:3]==[19,46,73] and ordered[3] in (97,100,103)
                          and ordered[4]==127 and all(71<=v<=73 for v in y))
            elif dynamic:
                order=(0,1,2,1,0,6) if not stress else (0,3,1,4,2,5,6,7,0,8,1,2)
                scene=order[(i//(100 if count==600 else 4))%len(order)]
                label,x,y,admitted=SCENES[scene]
            else:
                scene=(i//4)%3 if count<50 else [0,1,2,1,0,2][i//100]
                label,x,y,admitted=SCENES[0]
            if not i or scene!=last:
                addresses=range(0x81,0x8b) if dynamic else (0xa8,)
                values=x+y if dynamic else (scene,)
                for address,value in zip(addresses,values):
                    s.command(f"POKE 0x{address:04x} 0x{value:02x}")
                reply=s.command("PEEK "+" ".join(f"0x{a:04x}" for a in addresses))
                assert [int(v,16) for v in re.findall(rb" = 0x([0-9a-f]+)",reply)]==list(values)
                record("switch",i=i,mode=scene,label=label,x=x,y=y,admitted=admitted)
            transition=not i or scene!=last
            last=scene
            s.command("STEP FRAME")
            frame=int(expect(s,"TV",TV)[1])
            assert previous is None or frame==previous+1
            previous=frame
            top,bottom,total=map(int,expect(s,"TV FRAME",FRAME).groups())
            path=out/f"frame_{frame:04d}.png"
            expect(s,f"SCREENSHOT {path}",rb"saving screenshot\n")
            record("raster",mode=scene, label=label,x=x,y=y,admitted=admitted, dynamic=dynamic,transition=transition,frame=frame,
                   top=top,bottom=bottom,scanlines=total,path=path.name)

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("rom",type=Path)
    p.add_argument("images",type=Path)
    p.add_argument("--frames",type=int,default=16)
    p.add_argument("--dynamic",action="store_true")
    p.add_argument("--stress",action="store_true")
    p.add_argument("--legacy",action="store_true")
    a=p.parse_args()
    replay(a.rom,a.images.resolve(),a.frames,a.dynamic,a.stress,a.legacy)
